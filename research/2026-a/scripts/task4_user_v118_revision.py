"""Fill only missing fields in the authoritative user-supplied sixteen-city input."""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_user_city_indicators import SOURCE, build, evaluate
from task4_v5_model import ROOT, NAMES, SPEC, weights

MANIFEST = ROOT/'design/task4_user_v118_admissions.json'
OUT = ROOT/'results/task4_user_v118_revision'

def inputs():
    manifest=json.loads(MANIFEST.read_text())
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==manifest['input_sha256']
    observations=[]
    for path,digest in manifest['source_hashes'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    for path in manifest['observation_files']:
        observations.extend(json.loads((ROOT/path).read_text()))
    return pd.read_csv(SOURCE),observations

def revised_bounds(selected=None):
    frame,observations=inputs();lo,hi,_=build(frame)
    before=np.stack([lo,hi]).copy();seen=set()
    for r in observations:
        key=(r['city'],r['indicator'])
        if selected is not None and key not in selected:continue
        assert key not in seen;seen.add(key)
        i=frame.city.tolist().index(r['city']);j=NAMES.index(r['indicator'])
        # Never replace a nonempty attachment measurement or its Jensen interval.
        np.testing.assert_array_equal([lo[i,j],hi[i,j]],[0,1])
        if r.get('kind')=='teacher_interval':
            low,high=r['teacher_fte_bounds'];students=r['students']
            new=[15/(15+students/low),15/(15+students/high)]
        else:
            assert r['indicator'] in {'public_pool_density','public_transport_density'}
            assert float(frame.iloc[i].population)==r['population']
            x=r['raw_count']*100000/r['population'];a=SPEC[j][2]
            new=[x/(a+x),1]
        np.testing.assert_allclose(new,r['utility_after'],atol=1e-12,rtol=0)
        for path,digest in r.get('source_hashes',{}).items():
            assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
        lo[i,j],hi[i,j]=new
    protected=~((before[0]==0)&(before[1]==1))
    np.testing.assert_array_equal(np.stack([lo,hi])[:,protected],before[:,protected])
    assert np.all(lo>=before[0]) and np.all(hi<=before[1]) and np.all(lo<=hi)
    return frame,lo,hi

def main():
    source,obs=inputs();lo0,hi0,_=build(source);cities=source.city.tolist()
    cases=[('before',lo0,hi0)]
    for r in obs:
        key=(r['city'],r['indicator']);_,l,h=revised_bounds({key});cases.append((':'.join(key),l,h))
    _,l,h=revised_bounds();cases.append(('after',l,h))
    all_keys={(r['city'],r['indicator']) for r in obs}
    for key in sorted(all_keys):
        _,l,h=revised_bounds(all_keys-{key});cases.append(('without:'+':'.join(key),l,h))
    _,l,h=revised_bounds(set());cases.append(('withdrawal',l,h))
    allr=[];allb=[];reports=[]
    for label,lo,hi in cases:
        for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
            old=evaluate(cities,lo0,hi0,w);f=evaluate(cities,lo,hi,w)
            if label=='withdrawal':pd.testing.assert_frame_equal(f,old,check_exact=True)
            f['previous_decision_rank']=old.decision_rank
            f['rank_change_positive_improves']=old.decision_rank-f.decision_rank
            f['score_width_before']=old.score_upper-old.score_lower
            f['score_width']=f.score_upper-f.score_lower
            allr.append(f.assign(scenario=label,weight_reference=ref))
            reports.append(dict(scenario=label,weight_reference=ref,
                changed_cells=int(np.sum((lo!=lo0)|(hi!=hi0))),
                possible_champions=f.loc[f.possible_champion,'city'].tolist(),
                choices=f.loc[f.decision_rank==1,'city'].tolist(),
                kendall_tau_b=float(kendalltau(old.decision_rank,f.decision_rank).statistic),
                mean_score_width=float(f.score_width.mean())))
        allb.extend(dict(scenario=label,city=c,indicator=n,lower=lo[i,j],upper=hi[i,j]) for i,c in enumerate(cities) for j,n in enumerate(NAMES))
    OUT.mkdir(exist_ok=True)
    ranks=pd.concat(allr,ignore_index=True);ranks.to_csv(OUT/'ranks.csv',index=False)
    ranks[(ranks.scenario=='after')&(ranks.weight_reference=='fixed')].to_csv(OUT/'current_ranks.csv',index=False)
    pd.DataFrame(allb).to_csv(OUT/'utility_bounds.csv',index=False)
    result=dict(dataset='user16',version='V118',original_csv_unchanged=True,existing_measurements_unchanged=True,
        weights_and_interval_rules_unchanged=True,scenarios=reports,
        input_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        admissions_sha256=hashlib.sha256(MANIFEST.read_bytes()).hexdigest())
    (OUT/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([r for r in reports if r['scenario']=='after'],indent=2))

if __name__=='__main__':main()
