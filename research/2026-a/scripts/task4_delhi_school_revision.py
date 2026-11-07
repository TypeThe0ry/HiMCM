"""Add directly measured Delhi grade11-12 pupil/participating-teacher ratio."""
import hashlib,json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_school_stage_revision import school_bounds
from task4_continuous_preferences import feasible_preferences
SOURCE=ROOT/'data/task4_v34_education'
def delhi_bounds(shared_allocation=False):
    for m in json.loads((SOURCE/'manifest.json').read_text()):
        assert hashlib.sha256((SOURCE/m['file']).read_bytes()).hexdigest()==m['sha256']
    r=json.loads((SOURCE/'observation.json').read_text());assert r['city']=='Delhi' and r['year']=='2024/25'
    assert r['participating_teacher_headcount']==r['dedicated_high_school_teachers']+r['shared_secondary_high_school_teachers']
    u=15/(15+r['students']/r['participating_teacher_headcount']);a=15/(15+r['students']/r['dedicated_high_school_teachers'])
    np.testing.assert_allclose([a,u],[r['allocation_utility_lower'],r['utility_headcount']],atol=1e-12,rtol=0)
    lo,hi=school_bounds();i=CITIES.index('Delhi');j=NAMES.index('upper_secondary_ptr');assert lo[i,j]==0 and hi[i,j]==1
    lo[i,j],hi[i,j]=(a,u) if shared_allocation else (u,u)
    return lo,hi

def main():
    lo,hi=school_bounds();base,_=summarize(lo,hi,weights());frames=[];rows=[];stats=[]
    for label,(l,h) in [('v32_before',(lo,hi)),('participating_headcount',delhi_bounds()),('shared_allocation_sensitivity',delhi_bounds(True))]:
        keep=np.ones(l.shape,bool);keep[CITIES.index('Delhi'),NAMES.index('upper_secondary_ptr')]=False
        np.testing.assert_array_equal(l[keep],lo[keep]);np.testing.assert_array_equal(h[keep],hi[keep]);assert np.all((lo<=l)&(l<=h)&(h<=hi))
        f,d=summarize(l,h,weights());f['scenario']=label;frames.append(f)
        possible=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(l))!=k])['possible']]
        stats.append(dict(scenario=label,choice=[CITIES[k] for k in d['minimax_choices']],possible_champions=int(f.possible_champion.sum()),continuous_alpha_possible=possible,changed_ranks=int((f.decision_rank!=base.decision_rank).sum()),kendall_tau=float(kendalltau(f.decision_rank,base.decision_rank).statistic),delhi=f.iloc[CITIES.index('Delhi')][['score_lower','score_upper','decision_rank','max_regret']].to_dict(),phoenix_rank=int(f.iloc[CITIES.index('Phoenix')].decision_rank)))
        rows.extend(dict(scenario=label,city=c,indicator=n,lower=float(l[i,j]),upper=float(h[i,j])) for i,c in enumerate(CITIES) for j,n in enumerate(NAMES))
    out=ROOT/'results/task4_v34_delhi_school';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);pd.DataFrame(rows).to_csv(out/'utility_bounds.csv',index=False)
    result=dict(main_admitted=False,new_city_indicator_cells=1,primary_scenario='participating_headcount',scope='Delhi NCT grade11-12 all-management school pupils per participating teacher headcount; shared teachers counted once, not workload FTE. Allocation scenario is conditional sensitivity, not observed teaching hours.',sources=[dict(file=p,sha256=hashlib.sha256((SOURCE/p).read_bytes()).hexdigest()) for p in ['manifest.json','observation.json','extract.py']],scenarios=stats)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps([{k:v for k,v in s.items() if k!='continuous_alpha_possible'} for s in stats],indent=2))
if __name__=='__main__':main()
