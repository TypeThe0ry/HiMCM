"""Staged V204 operational analyses; isolated from active V203 outputs."""
from pathlib import Path
import hashlib, json
import numpy as np
import pandas as pd
from task4_user_v203_revision import revised_bounds as v203
from task4_user_v204_revision import revised_bounds as v204, MANIFEST
from task4_v5_model import ROOT, NAMES, score, weights
from task4_interval_decision import interval_decision, voi_1d
import task4_current_point_withdrawal as withdrawal

OUT=ROOT/'results/task4_v204_operational_rebase'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert not OUT.exists(), 'Output must be absent; preserve existing results'
    f,oldlo,oldhi=v203(); _,lo,hi=v204(); cities=f.city.tolist()
    i=cities.index('Vienna'); j=NAMES.index('public_transport_density')
    diff=lo!=oldlo
    assert diff.sum()==1 and diff[i,j] and np.array_equal(hi,oldhi)
    mask=lo==hi; missing=(lo==0)&(hi==1); uncertain=lo<hi
    assert [int(mask.sum()),int((uncertain&~missing).sum()),int(missing.sum())]==[112,37,11]
    sourcepaths=[MANIFEST,ROOT/'results/task4_v204_transition/verification.json',ROOT/'scripts/task4_current_priority.py',ROOT/'scripts/task4_current_point_withdrawal.py',ROOT/'scripts/task4_current_point_source_ledger.py',ROOT/'results/current_priority/all_uncertain_priority.csv',ROOT/'results/current_point_withdrawal/cases.csv',ROOT/'results/current_point_withdrawal/ranks.csv',ROOT/'results/current_point_source_ledger/ledger.csv',ROOT/'results/current_point_source_ledger/verification.json',Path(__file__)]
    hashes={str(p.relative_to(ROOT)):sha(p) for p in sourcepaths}
    OUT.mkdir(parents=True); ac=OUT/'acquisition'; ac.mkdir()
    rows=[]; ends=[]; lowers=[]; baselines=[]
    for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
        L,U=score(lo,w),score(hi,w); base=interval_decision(L,U)
        baselines.append(dict(weight_reference=ref,mean_score_interval_width=float((U-L).mean()),minimax_regret=float(base['minimax_regret']),conservative_recommendation=';'.join(cities[k] for k in base['minimax_choices']),possible_champions=int(base['possible_champion'].sum())))
        for i,j in zip(*np.where(uncertain)):
            left,right=float(lo[i,j]),float(hi[i,j])
            def callback(x,exact=True):
                a,b=lo.copy(),hi.copy();a[i,j]=x
                if exact:b[i,j]=x
                return score(a,w),score(b,w)
            v=voi_1d(callback,i,left,right,baseline=(L,U)); exclusions=[]
            for label,x in [('lower',left),('upper',right)]:
                l,u=callback(x);d=interval_decision(l,u);exclusions.append(16-int(d['possible_champion'].sum()))
                ends.append(dict(weight_reference=ref,city=cities[i],indicator=NAMES[j],endpoint=label,resolved_utility=x,possible_count=int(d['possible_champion'].sum()),minimax_regret=float(d['minimax_regret'])))
            rows.append(dict(weight_reference=ref,city=cities[i],indicator=NAMES[j],current_lower=left,current_upper=right,current_information='fully_missing' if missing[i,j] else 'partial_interval',guaranteed_exact_resolution_regret_reduction=v['guaranteed_gain'],best_possible_exact_resolution_regret_reduction=v['best_possible_gain'],optimistic_champion_exclusions=max(exclusions),worst_post_regret=v['worst_post_regret'],best_post_regret=v['best_post_regret']))
            for fraction in [0.,.25,.5,.75,1.]:
                x=left+fraction*(right-left);l,u=callback(x,False);d=interval_decision(l,u);np.testing.assert_array_equal(u,U)
                lowers.append(dict(weight_reference=ref,city=cities[i],indicator=NAMES[j],fraction_of_retained_interval=fraction,utility_lower=x,utility_upper=right,minimax_regret=float(d['minimax_regret']),regret_reduction=float(base['minimax_regret']-d['minimax_regret']),possible_count=int(d['possible_champion'].sum()),conservative_recommendation=';'.join(cities[k] for k in d['minimax_choices'])))
    keys=['weight_reference','city','indicator']; order=['weight_reference','guaranteed_exact_resolution_regret_reduction','best_possible_exact_resolution_regret_reduction','city','indicator']
    out=pd.DataFrame(rows).sort_values(order,ascending=[True,False,False,True,True]); old=pd.read_csv(ROOT/'results/current_priority/all_uncertain_priority.csv',float_precision='round_trip')
    out['priority_position']=out.groupby('weight_reference').cumcount()+1;old['priority_position']=old.groupby('weight_reference').cumcount()+1
    cmp=out.merge(old,on=keys,suffixes=('_v204','_v203'),validate='one_to_one')
    for c in ['current_lower','guaranteed_exact_resolution_regret_reduction','best_possible_exact_resolution_regret_reduction','optimistic_champion_exclusions','priority_position']:
        cmp[c+'_change']=cmp[c+'_v204']-cmp[c+'_v203']
    out.to_csv(ac/'all_uncertain_priority.csv',index=False); pd.DataFrame(ends).to_csv(ac/'endpoints.csv',index=False);pd.DataFrame(lowers).to_csv(ac/'lower_only_refinements.csv',index=False);cmp.to_csv(ac/'comparison_v203.csv',index=False)
    assert len(out)==96 and len(ends)==192 and len(lowers)==480
    # Invoke the existing isolated engine with only bounds factory and destination replaced.
    withdrawal.revised_bounds=v204; withdrawal.O=OUT/'point_withdrawal'; withdrawal.main()
    wd=OUT/'point_withdrawal'; s=json.loads((wd/'summary.json').read_text());s.update(primary_model='V204 staged, pending activation',activation_status='staged_not_active',source_sha256={k:v for k,v in hashes.items() if k not in ['results/current_priority/all_uncertain_priority.csv','results/current_point_source_ledger/ledger.csv']});(wd/'summary.json').write_text(json.dumps(s,indent=2)+'\n')
    cases=pd.read_csv(wd/'cases.csv',keep_default_na=False); oldcases=pd.read_csv(ROOT/'results/current_point_withdrawal/cases.csv',keep_default_na=False)
    ck=['weight_reference','withdrawn_city','indicator']; cp=cases.merge(oldcases,on=ck,suffixes=('_v204','_v203'),validate='one_to_one'); assert len(cp)==224
    for c in ['baseline_choice_excess_regret','post_minimax_regret','mean_width','possible_champions']:
        cp[c+'_change']=pd.to_numeric(cp[c+'_v204'])-pd.to_numeric(cp[c+'_v203'])
    cp.to_csv(wd/'comparison_v203.csv',index=False)
    ledger=pd.read_csv(ROOT/'results/current_point_source_ledger/ledger.csv',dtype=str,keep_default_na=False); assert len(ledger)==112
    for ref in ['fixed','equal']:
        x=cases[cases.weight_reference==ref].set_index(['withdrawn_city','indicator']); assert len(x)==112
        for index,row in ledger.iterrows():
            case=x.loc[(row.city,row.indicator)]; assert np.isclose(float(row.retained_utility),float(case.retained_utility),rtol=0,atol=1e-15)
            ledger.loc[index,ref+'_withdrawal_switch']=str(case.recommendation_set_changed)
            ledger.loc[index,ref+'_original_policy_excess_regret']=str(case.baseline_choice_excess_regret)
    ledger['review_priority_excess_regret']=ledger.apply(lambda r:max(float(r.fixed_original_policy_excess_regret),float(r.equal_original_policy_excess_regret)),axis=1)
    le=OUT/'point_source_ledger';le.mkdir();ledger.to_csv(le/'ledger.csv',index=False);ledger.sort_values(['review_priority_excess_regret','city','indicator'],ascending=[False,True,True]).to_csv(le/'review_priority.csv',index=False)
    prior=pd.read_csv(ROOT/'results/current_point_source_ledger/ledger.csv',dtype=str,keep_default_na=False)
    protected=[c for c in prior if c not in ['fixed_withdrawal_switch','equal_withdrawal_switch','fixed_original_policy_excess_regret','equal_original_policy_excess_regret','review_priority_excess_regret']]
    pd.testing.assert_frame_equal(ledger[protected],prior[protected]);counts=ledger.classification.value_counts().to_dict()
    ranks=pd.read_csv(wd/'ranks.csv'); oldr=pd.read_csv(ROOT/'results/current_point_withdrawal/ranks.csv'); rk=ck+['city']; rr=ranks.merge(oldr,on=rk,suffixes=('_v204','_v203'),validate='one_to_one');assert len(rr)==3584
    changed_rank=int((rr.decision_rank_v204!=rr.decision_rank_v203).sum())
    summary=dict(activation_status='staged_not_active',baseline='V203',changed_bound={'city':'Vienna','indicator':'public_transport_density','v203_lower':float(oldlo[cities.index('Vienna'),NAMES.index('public_transport_density')]),'v204_lower':float(lo[cities.index('Vienna'),NAMES.index('public_transport_density')]),'upper_unchanged':True},point_cells=112,partial_cells=37,fully_missing_cells=11,acquisition_rows=96,endpoint_rows=192,lower_only_rows=480,withdrawal_cases=224,withdrawal_rank_rows=3584,ledger_rows=112,classification_counts=counts,baseline_choices=baselines,acquisition_changed_bound_rows=int((abs(cmp.current_lower_change)>1e-12).sum()),acquisition_changed_priority_positions=int((cmp.priority_position_change!=0).sum()),acquisition_changed_information_rows=int(((abs(cmp.guaranteed_exact_resolution_regret_reduction_change)>1e-12)|(abs(cmp.best_possible_exact_resolution_regret_reduction_change)>1e-12)|(cmp.optimistic_champion_exclusions_change!=0)).sum()),withdrawal_choice_changes_v204=s['changed_recommendation_cases'],withdrawal_choice_changes_v203=json.loads((ROOT/'results/current_point_withdrawal/summary.json').read_text())['changed_recommendation_cases'],withdrawal_after_choice_changed_vs_v203=int((cp.after_choices_v204!=cp.after_choices_v203).sum()),withdrawal_rank_rows_changed_vs_v203=changed_rank,source_sha256=hashes,scope='Conditional calculations on staged V204; acquisition assumes exact identification within retained bounds, and point withdrawal is hypothetical ignorance, not source error. Ledger evidence and source classifications remain V203 records. No activation or manuscript change.')
    for p,h in hashes.items(): assert sha(ROOT/p)==h,p
    summary['output_sha256']={str(p.relative_to(OUT)):sha(p) for p in sorted(OUT.rglob('*')) if p.is_file()}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
