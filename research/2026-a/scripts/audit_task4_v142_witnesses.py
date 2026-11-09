"""Independent scalar-score and source checks for deterministic interior witnesses."""
from pathlib import Path
import gzip,hashlib,html,json,math,re
import numpy as np
import pandas as pd
from task4_user_v136_revision import revised_bounds
from task4_v5_model import ROOT,NAMES
OUT=ROOT/'results/task4_v142_witnesses';PAPER=ROOT.parents[2]/'HiMCM-Overleaf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def score_scalar(row,w):
    good=math.sqrt(math.fsum(float(weight)*float(x)**2 for weight,x in zip(w,row)))
    bad=math.sqrt(math.fsum(float(weight)*(1-float(x))**2 for weight,x in zip(w,row)))
    return 100*good/(good+bad)
def main():
    summary=read(OUT/'summary.json');frozen=summary['source_sha256']
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    frame,lo,hi=revised_bounds();cities=frame.city.tolist();mask=lo<hi
    cells=pd.read_csv(OUT/'utility_completions.csv',float_precision='round_trip');scores=pd.read_csv(OUT/'scores.csv',float_precision='round_trip');cases=pd.read_csv(OUT/'cases.csv',float_precision='round_trip')
    assert len(cells)==2560 and len(scores)==512 and len(cases)==32
    assert set(cells.target)==set(cities) and not cells.duplicated(['target','city','indicator']).any()
    keys=pd.MultiIndex.from_product([cities,NAMES],names=['city','indicator']);independent=[]
    for i,target in enumerate(cities):
        g=cells[cells.target.eq(target)].set_index(['city','indicator']).loc[keys]
        u=g.utility.to_numpy().reshape(16,10)
        np.testing.assert_array_equal(g.original_lower.to_numpy().reshape(16,10),lo);np.testing.assert_array_equal(g.original_upper.to_numpy().reshape(16,10),hi)
        expected=lo+.05*(hi-lo);expected[i]=lo[i]+.95*(hi[i]-lo[i]);np.testing.assert_array_equal(u,expected)
        np.testing.assert_array_equal(u[~mask],lo[~mask]);assert np.all(u[mask]>lo[mask]) and np.all(u[mask]<hi[mask])
        for reference,w in [('fixed',[.1125]*6+[.05,.1125,.1125,.05]),('equal',[.1]*10)]:
            s=np.array([score_scalar(row,w) for row in u]);margin=float(s[i]-np.delete(s,i).max());assert margin>0
            saved=scores[scores.target.eq(target)&scores.weight_reference.eq(reference)].set_index('city').loc[cities]
            np.testing.assert_allclose(saved.score,s,atol=2e-12,rtol=0)
            assert s[i]==max(s) and int(saved.loc[target,'rank'])==1
            case=cases[cases.target.eq(target)&cases.weight_reference.eq(reference)];assert len(case)==1 and case.iloc[0].winner==target
            assert abs(case.iloc[0].strict_margin-margin)<2e-12
            order=np.argsort(-s,kind='stable');assert case.iloc[0].runner_up==cities[order[1]]
            independent.append(dict(target=target,weight_reference=reference,strict_margin=margin,all112_points_unchanged=True,all48_uncertain_strictly_interior=True))
    for ref in ['fixed','equal']:
        m=min(x['strict_margin'] for x in independent if x['weight_reference']==ref)
        assert abs(m-summary['minimum_strict_margin_by_weight'][ref])<2e-12
    sources=ROOT/'data/task4_v142_education';meta=read(sources/'retrieval.json');raw=gzip.decompress((sources/'helsinki_metadata_original.html.gz').read_bytes())
    assert len(raw)==meta['raw_bytes'] and hashlib.sha256(raw).hexdigest()==meta['raw_sha256']
    t=html.unescape(re.sub('<[^>]+>',' ',raw.decode('iso-8859-1')));t=' '.join(t.split())
    for quote in read(sources/'helsinki_scope_excerpts.json').values():assert quote in t
    assert read(sources/'observations.json')==[]
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    receipt=dict(status='pass',version='V142',distinct_completions=16,independent_weight_cases=32,independent_scalar_city_scores=512,utility_values_checked=2560,point_values_unchanged_per_completion=112,uncertain_values_strictly_interior_per_completion=48,independent_cases=independent,primary_data_admissions=0,source_metadata_original_verified=True,source_sha256={str(p.relative_to(ROOT)):sha(p) for p in sources.iterdir() if p.is_file()},result_sha256={str(p.relative_to(ROOT)):sha(p) for p in OUT.iterdir() if p.suffix in {'.csv','.json'} and p.name not in {'verification.json','recheck_verification.json'}},verifier_sha256=sha(Path(__file__)),source_hashes_before_after_match=True,interpretation=summary['interpretation'])
    target=OUT/('recheck_verification.json' if (OUT/'verification.json').exists() else 'verification.json');target.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if not isinstance(v,(dict,list))},indent=2))
if __name__=='__main__':main()
