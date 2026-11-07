"""Keep London unknown; diagnose assumptions needed to use a released workforce estimate."""
import gzip,hashlib,json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_delhi_school_revision import delhi_bounds
from task4_continuous_preferences import feasible_preferences

def main():
    src=ROOT/'data/task4_v35_london'
    for m in json.loads((src/'manifest.json').read_text()):
        raw=(src/m['file']).read_bytes();assert len(raw)==m['bytes'] and hashlib.sha256(raw).hexdigest()==m['sha256']
        if m['file'].endswith('.gz'):
            plain=gzip.decompress(raw);assert len(plain)==m['uncompressed_bytes'] and hashlib.sha256(plain).hexdigest()==m['uncompressed_sha256']
    obs=json.loads((src/'observation.json').read_text());assert obs['main_admitted'] is False
    assert obs['students']==obs['year12_pupils']+obs['year13_pupils']
    cap=15/(15+obs['students']/obs['secondary_teacher_headcount_estimate'])
    np.testing.assert_allclose(cap,obs['conditional_utility_upper'],atol=1e-12,rtol=0)
    lo,hi=delhi_bounds();i=CITIES.index('London');j=NAMES.index('upper_secondary_ptr');assert lo[i,j]==0 and hi[i,j]==1
    baseline,_=summarize(lo,hi,weights());frames=[];stats=[]
    prior=pd.read_csv(ROOT/'results/task4_v34_delhi_school/ranks.csv');prior=prior[prior.scenario=='participating_headcount'].reset_index(drop=True)
    assert baseline.city.tolist()==prior.city.tolist()
    for col in ['score_lower','score_upper','decision_rank','max_regret']:np.testing.assert_allclose(baseline[col],prior[col],atol=1e-12,rtol=0)
    for label in ['current_evidence_unchanged','inadmissible_naive_cap']:
        l,h=lo.copy(),hi.copy()
        if label=='inadmissible_naive_cap':h[i,j]=cap
        mask=np.ones(l.shape,bool);mask[i,j]=False
        np.testing.assert_array_equal(l,lo);np.testing.assert_array_equal(h[mask],hi[mask])
        f,d=summarize(l,h,weights());f['scenario']=label;frames.append(f)
        possible=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(l))!=k])['possible']]
        stats.append(dict(scenario=label,choice=[CITIES[k] for k in d['minimax_choices']],possible_champions=int(f.possible_champion.sum()),continuous_alpha_possible=possible,changed_ranks=int((f.decision_rank!=baseline.decision_rank).sum()),london=f.iloc[i][['score_lower','score_upper','decision_rank','max_regret']].to_dict()))
    out=ROOT/'results/task4_v35_admission';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    result=dict(new_admitted_cells=0,main_model_changed=False,canonical_function='task4_delhi_school_revision.delhi_bounds',london_main_bounds=[0,1],inadmissible_naive_cap=cap,source_hashes={p:hashlib.sha256((src/p).read_bytes()).hexdigest() for p in ['manifest.json','observation.json','extract.py']},scenarios=stats)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps([{k:v for k,v in s.items() if k!='continuous_alpha_possible'} for s in stats],indent=2))
if __name__=='__main__':main()
