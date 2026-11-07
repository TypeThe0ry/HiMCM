"""V6: append screened evidence to V5, then derive acquisition certificates.

Every primary admission is explicit. Diagnostic, FTE and mixed-purpose travel
rows cannot silently enter the headcount/school-trip target.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,SPEC,build,score,weights,summarize
from task4_champion_acquisition import certificates,elimination_threshold
OUT=ROOT/'results/task4_v6'

HEADCOUNT_ADMISSIONS = {
 'observed_general_upper_secondary_scope_conditional': 'students_per_teacher_headcount',
 'observed_general_upper_secondary_manual_source_scope_conditional': 'students_per_teacher_including_headmaster_headcount',
}


def admit_observations(lo,hi,frame,scale=1):
    lo=lo.copy();hi=hi.copy();audit=[]
    for row in frame.to_dict('records'):
        r=dict(row);status=str(r.get('status',''))
        admissible=(status in HEADCOUNT_ADMISSIONS and r.get('unit')==HEADCOUNT_ADMISSIONS[status]
                    and r.get('indicator')=='upper_secondary_ptr')
        if not admissible:
            audit.append(dict(r,admitted=False,reason='Status and exact headcount unit have not been admitted together'))
            continue
        i=CITIES.index(r['city']);j=NAMES.index(r['indicator']);x=float(r['value'])
        if not np.isfinite(x) or x<0:raise ValueError('Invalid measurement')
        u=scale*SPEC[j][2]/(scale*SPEC[j][2]+x)
        # Do not silently replace older point evidence or conflicting intervals.
        if not lo[i,j]-1e-12<=u<=hi[i,j]+1e-12:raise ValueError('Evidence conflict requires explicit reconciliation')
        lo[i,j]=hi[i,j]=u
        audit.append(dict(r,admitted=True,reason='Matched students and headcount; stated general-high-school scope',utility_lower=u,utility_upper=u))
    return lo,hi,audit


def inputs():
    frames=[]
    for name in ['education','phoenix','commute']:
        p=ROOT/f'data/task4_v6_{name}/observations.csv'
        if p.exists():frames.append(pd.read_csv(p))
    return pd.concat(frames,ignore_index=True) if frames else pd.DataFrame()


def admit_travel(lo,hi,strict_archived=False,frame=None):
    lo=lo.copy();hi=hi.copy();audit=[]
    p=ROOT/'data/task4_v6_commute/bounds.csv'
    if frame is None:
        if not p.exists():return lo,hi,audit
        frame=pd.read_csv(p)
    for r in frame.to_dict('records'):
        status=str(r.get('status',''))
        admitted=(r.get('indicator')=='travel' and (str(r.get('mapping_robust',False)).strip().lower()=='true')
                  and ('manual_primary_index' in status or status=='observed_upper_secondary_travel_bound'))
        if strict_archived and 'manual' in status:admitted=False
        if not admitted:
            audit.append(dict(r,admitted=False,reason='Source or mapping requires excluded condition'));continue
        i=CITIES.index(r['city']);j=NAMES.index('travel');a=float(r['utility_lower']);b=float(r['utility_upper'])
        if not 0<=a<=b<=1:raise ValueError('Invalid travel bounds')
        if max(lo[i,j],a)>min(hi[i,j],b):raise ValueError('Conflicting travel evidence')
        lo[i,j]=max(lo[i,j],a);hi[i,j]=min(hi[i,j],b)
        audit.append(dict(r,admitted=True,reason='Mapping-robust upper-secondary travel bound with source conditions'))
    return lo,hi,audit


def run():
    OUT.mkdir(parents=True,exist_ok=True); w=weights();l0,h0,_=build()
    l,h,audit=admit_observations(l0,h0,inputs())
    l,h,travel_audit=admit_travel(l,h);audit.extend(travel_audit)
    assert np.all(l>=l0-1e-12) and np.all(h<=h0+1e-12)
    before,d0=summarize(l0,h0,w);after,d1=summarize(l,h,w)
    before.to_csv(OUT/'before_v5.csv',index=False);after.to_csv(OUT/'after_v6.csv',index=False)
    pd.DataFrame(audit).to_csv(OUT/'source_admission.csv',index=False)
    change=before[['city','decision_rank','best_rank','worst_rank']].merge(after,on='city',suffixes=('_before','_after'))
    change['decision_rank_change']=change.decision_rank_before-change.decision_rank_after
    change.to_csv(OUT/'rank_changes.csv',index=False)
    pd.DataFrame([dict(city=c,indicator=n,before_lower=l0[i,j],before_upper=h0[i,j],after_lower=l[i,j],after_upper=h[i,j])
                  for i,c in enumerate(CITIES) for j,n in enumerate(NAMES)]).to_csv(OUT/'utility_bounds.csv',index=False)
    for label,ll,hh in [('before',l0,h0),('after',l,h)]:
        rows,bundles=certificates(ll,hh,w,NAMES,CITIES)
        pd.DataFrame(rows).to_csv(OUT/f'acquisition_certificate_{label}.csv',index=False)
        pd.DataFrame(bundles).to_csv(OUT/f'minimal_bundles_{label}.csv',index=False)
    thresholds=[]
    for i,c in enumerate(CITIES):
        for j,n in enumerate(NAMES):
            if h[i,j]-l[i,j]>1e-10:
                t=elimination_threshold(l,h,w,i,j)
                thresholds.append(dict(city=c,indicator=n,utility_strict_cutoff=t,single_cell_can_eliminate=t is not None))
    pd.DataFrame(thresholds).to_csv(OUT/'single_cell_elimination_thresholds.csv',index=False)
    # Scope sensitivity and normative parameter changes are separate from data updates.
    sens=[]
    for scale in [.5,1,2]:
        for aux in [.05,.1,.2]:
            for mode in ['baseline','all_new_conditional','new_archived_only','new_education_only']:
                ll,hh,_=build(scale=scale)
                frame=inputs()
                if mode=='new_archived_only':frame=frame[~frame.status.str.contains('manual',na=False)]
                if mode!='baseline':ll,hh,_=admit_observations(ll,hh,frame,scale)
                if mode in ('all_new_conditional','new_archived_only'):ll,hh,_=admit_travel(ll,hh,strict_archived=mode=='new_archived_only')
                _,d=summarize(ll,hh,weights(aux))
                sens.append(dict(anchor_scale=scale,auxiliary_weight=aux,evidence_mode=mode,
                                 possible_champions=int(d['possible_champion'].sum()),minimax_regret=d['minimax_regret'],
                                 choices='|'.join(CITIES[k] for k in d['minimax_choices'])))
    pd.DataFrame(sens).to_csv(OUT/'sensitivity.csv',index=False)
    summary=dict(before_possible=int(d0['possible_champion'].sum()),after_possible=int(d1['possible_champion'].sum()),
                 before_mean_width=float((before.score_upper-before.score_lower).mean()),after_mean_width=float((after.score_upper-after.score_lower).mean()),
                 before_minimax=d0['minimax_regret'],after_minimax=d1['minimax_regret'],
                 before_choices=[CITIES[i] for i in d0['minimax_choices']],after_choices=[CITIES[i] for i in d1['minimax_choices']],
                 kendall_decision_rank=float(kendalltau(before.decision_rank,after.decision_rank).statistic),
                 informative_before=int(np.sum(h0-l0<1-1e-12)),informative_after=int(np.sum(h-l<1-1e-12)),
                 new_primary_cells=int(np.sum((l>l0+1e-12)|(h<h0-1e-12))))
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    cert=pd.read_csv(OUT/'acquisition_certificate_after.csv')
    values=cert.minimum_city_local_exact_measurements
    fig,ax=plt.subplots(figsize=(10,8));y=np.arange(len(CITIES));colors=['#c45328' if c=='Phoenix' else '#197d91' for c in CITIES]
    ax.barh(y,values.fillna(0),color=colors);ax.set_yticks(y,CITIES);ax.invert_yaxis()
    for i,v in enumerate(values):
        ax.text(.05 if pd.isna(v) else v+.05,i,'Not possible with own data alone' if pd.isna(v) else str(int(v)),va='center',fontsize=9)
    ax.set_xlim(0,5);ax.set_xticks(range(6));ax.set_xlabel('Minimum exact measurements that COULD exclude this city')
    ax.set_title('Acquisition planning: competitor lower bounds held fixed\nHypothetical outcomes; no changes to observed evidence')
    fig.tight_layout();fig.savefig(OUT/'acquisition_certificates.png',dpi=160);plt.close(fig)
    print(json.dumps(summary,indent=2))
if __name__=='__main__':run()
