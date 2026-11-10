"""V200 conditional information limits for all 48 uncertain cells.

Exact identification and lower-bound-only refinement are distinct experiments.
No new source admission or change to active science/manuscript.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from task4_user_v200_revision import revised_bounds
from task4_interval_decision import interval_decision, voi_1d
from task4_v5_model import ROOT, NAMES, score, weights

OUT = ROOT/'results/current_priority'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    snapshot=ROOT/'design/task4_user_v200_snapshot.json'
    bound=json.loads(snapshot.read_text())['source_sha256']
    for name,h in bound.items(): assert sha(ROOT/name)==h,name
    nav=[ROOT/'design'/('task4_user_current_'+n+'.json') for n in ['model','extensions','review','delivery']]
    protect={str(p.relative_to(ROOT)):sha(p) for p in [*nav,snapshot,Path(__file__),ROOT/'results/task4_v199_priority/all_uncertain_priority.csv']}
    assert json.loads(nav[0].read_text())['version']=='V200'
    f,lo,hi=revised_bounds(); before=np.stack([lo,hi]).copy(); cities=f.city.tolist()
    missing=(lo==0)&(hi==1); uncertain=lo<hi
    assert [int((lo==hi).sum()),int((uncertain&~missing).sum()),int(missing.sum())]==[112,37,11]
    rows=[]; ends=[]; lower_rows=[]; baselines=[]
    for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
        L,U=score(lo,w),score(hi,w); base=interval_decision(L,U)
        baselines.append(dict(weight_reference=ref,mean_score_interval_width=float((U-L).mean()),minimax_regret=float(base['minimax_regret']),conservative_recommendation=';'.join(cities[k] for k in base['minimax_choices']),possible_champions=int(base['possible_champion'].sum())))
        for i,j in zip(*np.where(uncertain)):
            left,right=float(lo[i,j]),float(hi[i,j])
            def callback(x,exact=True):
                a,b=lo.copy(),hi.copy(); a[i,j]=x
                if exact:b[i,j]=x
                return score(a,w),score(b,w)
            v=voi_1d(callback,i,left,right,baseline=(L,U))
            exclusions=[]
            for label,x in [('lower',left),('upper',right)]:
                l,u=callback(x);d=interval_decision(l,u)
                exclusions.append(16-int(d['possible_champion'].sum()))
                ends.append(dict(weight_reference=ref,city=cities[i],indicator=NAMES[j],endpoint=label,resolved_utility=x,possible_count=int(d['possible_champion'].sum()),minimax_regret=float(d['minimax_regret'])))
            rows.append(dict(weight_reference=ref,city=cities[i],indicator=NAMES[j],current_lower=left,current_upper=right,current_information='fully_missing' if missing[i,j] else 'partial_interval',guaranteed_exact_resolution_regret_reduction=v['guaranteed_gain'],best_possible_exact_resolution_regret_reduction=v['best_possible_gain'],optimistic_champion_exclusions=max(exclusions),worst_post_regret=v['worst_post_regret'],best_post_regret=v['best_post_regret']))
            for fraction in [0.,.25,.5,.75,1.]:
                x=left+fraction*(right-left);l,u=callback(x,False);d=interval_decision(l,u)
                np.testing.assert_array_equal(u,U)
                lower_rows.append(dict(weight_reference=ref,city=cities[i],indicator=NAMES[j],fraction_of_retained_interval=fraction,utility_lower=x,utility_upper=right,minimax_regret=float(d['minimax_regret']),regret_reduction=float(base['minimax_regret']-d['minimax_regret']),possible_count=int(d['possible_champion'].sum()),conservative_recommendation=';'.join(cities[k] for k in d['minimax_choices'])))
    out=pd.DataFrame(rows).sort_values(['weight_reference','guaranteed_exact_resolution_regret_reduction','best_possible_exact_resolution_regret_reduction','city','indicator'],ascending=[True,False,False,True,True])
    assert len(out)==96
    old=pd.read_csv(ROOT/'results/task4_v199_priority/all_uncertain_priority.csv',float_precision='round_trip')
    compare=out.merge(old,on=['weight_reference','city','indicator'],suffixes=('_current','_V199'),validate='one_to_one')
    assert len(compare)==96
    for name in ['guaranteed_exact_resolution_regret_reduction','best_possible_exact_resolution_regret_reduction','optimistic_champion_exclusions']:
        compare[name+'_change']=compare[name+'_current']-compare[name+'_V199']
    OUT.mkdir(parents=True,exist_ok=True)
    out.to_csv(OUT/'all_uncertain_priority.csv',index=False)
    pd.DataFrame(ends).to_csv(OUT/'endpoints.csv',index=False)
    pd.DataFrame(lower_rows).to_csv(OUT/'lower_only_refinements.csv',index=False)
    compare.to_csv(OUT/'previous_comparison.csv',index=False)
    _,a,b=revised_bounds();np.testing.assert_array_equal(before,np.stack([a,b]))
    for name,h in {**bound,**protect}.items():assert sha(ROOT/name)==h,name
    report=dict(version='Current V200 acquisition priorities',science='V200 unchanged',paper='current single-main paper unchanged',point_cells=112,partial_cells=37,fully_missing_cells=11,uncertain_cells=48,weight_cell_rows=96,lower_only_rows=len(lower_rows),baseline=baselines,primary_admissions=0,actual_score_width_reduction=0,scope='Conditional complete exact utility identification within retained intervals; not source availability, attainable endpoint observations, future prediction or a guarantee for partial evidence. Lower-only refinements retain each existing upper bound.',source_sha256={**bound,**protect})
    (OUT/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(out.groupby('weight_reference').head(5).to_string(index=False))
if __name__=='__main__':main()
