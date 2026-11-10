"""Independent V204 staged operational rebase audit; no manuscript or registry access."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,math
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_user_v204_revision import revised_bounds
from task4_user_city_indicators import SOURCE,build,FIELDS
from task4_v5_model import ROOT,NAMES,weights
from audit_current_priority import scalar_scores,decision
from task4_audit_output import audit_parser,check_output,emit_report
R=ROOT;G=R.parents[1];O=R/'results/task4_v204_operational_rebase';AC=O/'acquisition';WD=O/'point_withdrawal';LE=O/'point_source_ledger'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def readrows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def close(a,b):np.testing.assert_allclose(a,b,atol=2e-10,rtol=0)
def same(a,b):
    if pd.isna(b):return a==''
    try:return math.isclose(float(a),float(b),rel_tol=0,abs_tol=2e-10)
    except (ValueError,TypeError):return a==str(b)

def main():
    args=audit_parser(__doc__).parse_args();check_output(args,O/'verification.json',G)
    snapshot=read(R/'design/task4_user_v204_snapshot.json');core=snapshot['upstream_source_sha256'];new=snapshot['source_sha256']
    assert len(core)==548 and len(new)==110
    for mapping in (core,new):
        for n,h in mapping.items():assert sha(R/n)==h,n
    summary=read(O/'summary.json');assert summary['activation_status']=='staged_not_active'
    for n,h in summary['source_sha256'].items():assert sha(R/n)==h,n
    for n,h in summary['output_sha256'].items():assert sha(O/n)==h,n
    frozen={n:sha(R/n) for n in summary['source_sha256']}
    f,lo,hi=revised_bounds();original=np.stack([lo,hi]).copy();cities=f.city.tolist()
    assert lo.shape==hi.shape==(16,10)
    uncertain=lo<hi;missing=(lo==0)&(hi==1)
    assert [int((lo==hi).sum()),int((uncertain&~missing).sum()),int(missing.sum())]==[112,37,11]
    references={'fixed':np.array([.1125]*6+[.05,.1125,.1125,.05]),'equal':np.full(10,.1)}
    tables={n:pd.read_csv(AC/(n+'.csv'),float_precision='round_trip') for n in ['all_uncertain_priority','endpoints','lower_only_refinements']}
    priority=tables['all_uncertain_priority'];endpoints=tables['endpoints'];lower=tables['lower_only_refinements']
    expected={(r,cities[i],NAMES[j]) for r in references for i,j in zip(*np.where(uncertain))}
    key=['weight_reference','city','indicator']
    assert len(priority)==96 and not priority.duplicated(key).any()
    assert set(priority[key].itertuples(index=False,name=None))==expected
    assert len(endpoints)==192 and len(lower)==480
    assert not endpoints.duplicated(key+['endpoint']).any()
    assert not lower.duplicated(key+['fraction_of_retained_interval']).any()
    count=0; interior=0
    def case(ref,city,indicator,x,exact=True):
        nonlocal count
        i=cities.index(city);j=NAMES.index(indicator)
        assert uncertain[i,j] and lo[i,j]-1e-14<=x<=hi[i,j]+1e-14
        a,b=lo.copy(),hi.copy();a[i,j]=x
        if exact: b[i,j]=x
        mask=np.ones((16,10),bool);mask[i,j]=False
        np.testing.assert_array_equal(a[mask],lo[mask]);np.testing.assert_array_equal(b[mask],hi[mask])
        l,u=scalar_scores(a,references[ref]),scalar_scores(b,references[ref]);count+=1
        return i,l,u,decision(l,u)
    bases={}
    for ref,w in references.items():
        l,u=scalar_scores(lo,w),scalar_scores(hi,w);d=decision(l,u);bases[ref]=(l,u,d)
        record=next(r for r in summary['baseline_choices'] if r['weight_reference']==ref)
        close(record['minimax_regret'],d[1]);close(record['mean_score_interval_width'],(u-l).mean())
        assert record['conservative_recommendation']==';'.join(cities[k] for k in d[3])==('Oslo' if ref=='fixed' else 'Zurich')
        assert record['possible_champions']==int(d[2].sum())==16
    for row in priority.itertuples():
        ref,city,ind=row.weight_reference,row.city,row.indicator;i=cities.index(city);j=NAMES.index(ind)
        left,right=float(lo[i,j]),float(hi[i,j]);close([row.current_lower,row.current_upper],[left,right])
        assert row.current_information==('fully_missing' if missing[i,j] else 'partial_interval')
        def branches(x):
            _,_,_,d=case(ref,city,ind,x)
            return float(d[0][i]),float(np.delete(d[0],i).min())
        def difference(x):a,b=branches(x);return a-b
        candidates=[left,right]
        if difference(left)*difference(right)<0:candidates.append(brentq(difference,left,right,xtol=1e-14))
        best=min(min(branches(x)) for x in [left,right]);worst=max(min(branches(x)) for x in candidates)
        risk=bases[ref][2][1]
        close([row.best_post_regret,row.worst_post_regret,row.guaranteed_exact_resolution_regret_reduction,row.best_possible_exact_resolution_regret_reduction],[best,worst,risk-worst,risk-best])
        endpoint_cases=[case(ref,city,ind,x)[3] for x in [left,right]]
        ceiling=max(16-int(d[2].sum()) for d in endpoint_cases)
        assert row.optimistic_champion_exclusions==ceiling
        for x in np.linspace(left,right,103)[1:-1]:
            _,_,_,d=case(ref,city,ind,float(x));interior+=1
            assert best-2e-10<=d[1]<=worst+2e-10
            assert 16-int(d[2].sum())<=ceiling
        e=endpoints[(endpoints.weight_reference==ref)&(endpoints.city==city)&(endpoints.indicator==ind)]
        assert set(e.endpoint)=={'lower','upper'}
        for label,x,d in [('lower',left,endpoint_cases[0]),('upper',right,endpoint_cases[1])]:
            saved=e[e.endpoint==label].iloc[0]
            close(saved.resolved_utility,x);close(saved.minimax_regret,d[1]);assert saved.possible_count==int(d[2].sum())
        low=lower[(lower.weight_reference==ref)&(lower.city==city)&(lower.indicator==ind)]
        assert set(low.fraction_of_retained_interval)=={0.,.25,.5,.75,1.}
        for item in low.itertuples():
            x=left+item.fraction_of_retained_interval*(right-left)
            _,l,u,d=case(ref,city,ind,x,False)
            close([item.utility_lower,item.utility_upper,item.minimax_regret,item.regret_reduction],[x,right,d[1],risk-d[1]])
            np.testing.assert_array_equal(u,bases[ref][1])
            assert item.possible_count==int(d[2].sum())
            assert item.conservative_recommendation==';'.join(cities[k] for k in d[3])

    # Reconstruct comparisons from both saved full tables; check every field, not just aggregates.
    old=pd.read_csv(R/'results/current_priority/all_uncertain_priority.csv',float_precision='round_trip');old['priority_position']=old.groupby('weight_reference').cumcount()+1
    expected=priority.merge(old,on=key,suffixes=('_v204','_v203'),validate='one_to_one')
    for col in ['current_lower','guaranteed_exact_resolution_regret_reduction','best_possible_exact_resolution_regret_reduction','optimistic_champion_exclusions','priority_position']:
        expected[col+'_change']=expected[col+'_v204']-expected[col+'_v203']
    comparison=pd.read_csv(AC/'comparison_v203.csv',float_precision='round_trip')
    pd.testing.assert_frame_equal(expected,comparison,check_exact=False,atol=2e-12,rtol=0)
    assert int((expected.priority_position_change!=0).sum())==summary['acquisition_changed_priority_positions']==6
    assert int((abs(expected.current_lower_change)>1e-12).sum())==summary['acquisition_changed_bound_rows']==2
    info=((abs(expected.guaranteed_exact_resolution_regret_reduction_change)>1e-12)|(abs(expected.best_possible_exact_resolution_regret_reduction_change)>1e-12)|(expected.optimistic_champion_exclusions_change!=0))
    assert int(info.sum())==summary['acquisition_changed_information_rows']==1
    # Ranking order and recorded ordinal are independently specified by the declared sort.
    ordered=priority.sort_values(['weight_reference','guaranteed_exact_resolution_regret_reduction','best_possible_exact_resolution_regret_reduction','city','indicator'],ascending=[True,False,False,True,True]).reset_index(drop=True)
    assert priority[key].reset_index(drop=True).equals(ordered[key])
    assert list(priority.priority_position)==list(priority.groupby('weight_reference').cumcount()+1)
    s=read(WD/'summary.json')
    def near(a,b):return math.isclose(float(a),float(b),rel_tol=0,abs_tol=2e-10)
    f,lo,hi=revised_bounds(); raw=pd.read_csv(SOURCE); oldlo,oldhi,_=build(raw); cities=f.city.tolist()
    assert cities==raw.city.tolist() and lo.shape==(16,10)
    mask=lo==hi; assert mask.sum()==112 and (~mask).sum()==48 and np.array_equal(mask,oldlo==oldhi)
    assert np.array_equal(lo[mask],oldlo[mask]) and np.array_equal(hi[mask],oldhi[mask])
    ws={'fixed':[.1125]*6+[.05,.1125,.1125,.05], 'equal':[.1]*10}
    assert np.allclose(weights(.1),ws['fixed'],rtol=0,atol=1e-16)
    def calc(a,b,w):
     def sc(z):
      x=math.sqrt(sum(w[j]*float(z[j])**2 for j in range(10)));y=math.sqrt(sum(w[j]*(1-float(z[j]))**2 for j in range(10)));return 100*x/(x+y)
     L=[sc(row) for row in a]; U=[sc(row) for row in b]
     regret=[max(0.,max(U[k] for k in range(16) if k!=i)-L[i]) for i in range(16)]
     best=[1+sum(L[k]>U[i]+1e-12 for k in range(16) if k!=i) for i in range(16)]
     worst=[1+sum(U[k]>L[i]+1e-12 for k in range(16) if k!=i) for i in range(16)]
     possible=[U[i]>=max(L[k] for k in range(16) if k!=i)-1e-12 for i in range(16)]
     necessary=[L[i]>=max(U[k] for k in range(16) if k!=i)-1e-12 for i in range(16)]
     choices=[cities[i] for i,r in enumerate(regret) if r<=min(regret)+1e-12]
     rank=[1+sum(x<regret[i]-1e-10 for x in regret) for i in range(16)]
     return L,U,regret,best,worst,possible,necessary,choices,rank
    cases=readrows(WD/'cases.csv'); ranks=readrows(WD/'ranks.csv'); assert len(cases)==224 and len(ranks)==3584
    cases_by={(x['weight_reference'],x['withdrawn_city'],x['indicator']):x for x in cases}
    ranks_by={(x['weight_reference'],x['withdrawn_city'],x['indicator'],x['city']):x for x in ranks}
    assert len(cases_by)==224 and len(ranks_by)==3584
    changed={}
    for ref,w in ws.items():
     base=calc(lo,hi,w); bc=base[7]; bmin=min(base[2]); bw=sum(u-l for l,u in zip(base[0],base[1]))/16
     assert s['baseline'][ref]['choices']==bc and near(s['baseline'][ref]['minimax_regret'],bmin) and near(s['baseline'][ref]['mean_width'],bw)
     changed[ref]=0
     for i,j in np.argwhere(mask):
      a=lo.copy();b=hi.copy();a[i,j]=0;b[i,j]=1; assert np.array_equal(a[~mask],lo[~mask]) and np.array_equal(b[~mask],hi[~mask])
      L,U,reg,br,wr,pc,nc,choice,dr=calc(a,b,w); case=cases_by[(ref,cities[i],NAMES[j])]; field=FIELDS[j]; source=raw.iloc[i]
      assert case['input_field']==field and same(case['submitted_value'],source[field]) and same(case['submitted_year'],source.get(field+'_year')) and same(case['submitted_flag'],source.get(field+'_flag'))
      assert near(case['retained_utility'],lo[i,j]) and json.loads(case['baseline_choices'])==bc and json.loads(case['after_choices'])==choice
      ch=choice!=bc;changed[ref]+=ch; assert (case['recommendation_set_changed']=='True')==ch
      mw=sum(u-l for l,u in zip(L,U))/16
      assert near(case['baseline_choice_excess_regret'],min(reg[cities.index(c)] for c in bc)-min(reg)) and near(case['post_minimax_regret'],min(reg)) and near(case['baseline_minimax_regret'],bmin) and near(case['mean_width'],mw) and near(case['mean_width_increase'],mw-bw)
      assert int(case['possible_champions'])==sum(pc) and int(case['necessary_champions'])==sum(nc)
      for k,c in enumerate(cities):
       row=ranks_by[(ref,cities[i],NAMES[j],c)]
       assert near(row['score_lower'],L[k]) and near(row['score_upper'],U[k]) and near(row['max_regret'],reg[k])
       assert int(row['best_rank'])==br[k] and int(row['worst_rank'])==wr[k] and int(row['decision_rank'])==dr[k]
       assert (row['possible_champion']=='True')==pc[k] and (row['necessary_champion']=='True')==nc[k]
    assert changed==s['changed_recommendation_cases']=={'fixed':10,'equal':35}
    assert s['point_cells']==112 and s['existing_interval_cells_held_fixed']==48 and s['weight_references']==2 and s['cases']==224 and s['rank_rows']==3584 and s['primary_admissions']==s['actual_primary_width_reduction']==0
    ledger=readrows(LE/'ledger.csv');priority=readrows(LE/'review_priority.csv');assert len(ledger)==len(priority)==112
    keys={(x['city'],x['indicator']) for x in ledger};assert len(keys)==112
    f,l,h=revised_bounds();expected={(f.city.iloc[i],NAMES[j]) for i in range(16) for j in range(10) if l[i,j]==h[i,j]};assert keys==expected
    raw={x['city']:x for x in readrows(R/'data/task4_v117_team_intake/city_indicators.csv')}
    costs={(x['city'],x['indicator']):x for x in readrows(R/'data/current_all16_cost_editions/comparison.csv')}
    band={x['city']:x for x in readrows(R/'data/current_all16_broadband_fields/comparison.csv')}
    stress={(x['weight_reference'],x['withdrawn_city'],x['indicator']):x for x in readrows(WD/'cases.csv')}
    counts=Counter()
    for x in ledger:
        city=x['city'];indicator=x['indicator'];field=x['input_field'];r=raw[city]
        assert [x['original_value'],x['original_year'],x['original_flag']]==[r[field],r[field+'_year'],r[field+'_flag']]
        i=f.city.tolist().index(city);j=NAMES.index(indicator);assert math.isclose(float(x['retained_utility']),l[i,j],abs_tol=1e-15,rel_tol=0)
        state='not_included_in_bounded_classification'
        if indicator=='fixed_broadband_mbps':state='publisher_match_different_statistic' if city=='Singapore' else 'publisher_value_match_scope_unverified';assert band[city]['exact_match_fields']==('fixedMean' if city=='Singapore' else 'fixedMedian')
        elif field in ('cli','pir'):state='publisher_value_match_scope_unverified' if costs[city,field]['exact_matches'] else 'no_match_checked_cost_editions'
        elif indicator=='upper_secondary_ptr' and city in ('Tokyo','Singapore'):state='documented_value_match_different_stage'
        elif indicator=='upper_secondary_ptr' and city=='Oslo':state='no_match_examined_PTR_series'
        elif indicator=='upper_secondary_ptr' and city in ('Vienna','Berlin'):
            state='reviewed_lineage_unresolved';folder='current_vienna_ptr_point' if city=='Vienna' else 'current_berlin_ptr_point';followup=read(R/'data'/folder/'scope.json')
            assert followup['original_value']==float(r[field]) and followup['original_year']==int(r[field+'_year'])
            assert not followup['exact_value_match'] and not followup['original_lineage_verified'] and not followup['target_scope_verified']
        elif (city,indicator) in [('Oslo','pm25'),('Oslo','research_he_density'),('Zurich','homicide_rate')]:state='reviewed_lineage_unresolved'
        if (city,indicator)==('Oslo','research_he_density'):
            report=read(R/'results/current_oslo_he_identity_completion/verification.json')
            assert report['national_identity_matches']==27 and report['registry_codes_checked']==27
            assert report['identity_matches_among_positive_each_period']==25 and report['inherited_rows_preserved']==25
            assert report['newly_bridged_codes']==['1404','1405'] and not report['original25_lineage_verified']
            assert report['programme_only_new_identities'] and report['address_discrepancy_codes']==['1405']
            assert not report['city_count_corrected']
            for n,h in report['source_sha256'].items():assert sha(R/n)==h,n
            assert x['evidence']=='data/current_oslo_he_identity_completion/README.md'
            assert 'programme-only' in x['scope_detail'] and 'Bærum3201' in x['scope_detail']
        assert x['classification']==state;counts[state]+=1
        assert x['measurement_fully_certified']==x['original_extraction_lineage_verified']=='False'
        if x['evidence']:assert (R/x['evidence']).is_file()
        excess=[]
        for ref in ['fixed','equal']:
            case=stress[ref,city,indicator]
            assert x[ref+'_withdrawal_switch']==case['recommendation_set_changed']
            value=float(case['baseline_choice_excess_regret']);assert math.isclose(float(x[ref+'_original_policy_excess_regret']),value,rel_tol=0,abs_tol=1e-14);excess.append(value)
        assert math.isclose(float(x['review_priority_excess_regret']),max(excess),rel_tol=0,abs_tol=1e-14)
    assert dict(counts)==summary['classification_counts']
    assert sum(x['fixed_withdrawal_switch']=='True' for x in ledger)==10==10
    assert sum(x['equal_withdrawal_switch']=='True' for x in ledger)==35==35
    assert priority==sorted(ledger,key=lambda x:(-float(x['review_priority_excess_regret']),x['city'],x['indicator']))
    teacher=read(R/'data/current_point_source_ledger/teacher_scope.json');assert len(teacher['points'])==5
    source_count=0
    def source_hashes(node):
        nonlocal source_count
        if isinstance(node,dict):
            if 'path' in node and 'sha256' in node:assert sha(G/node['path'])==node['sha256'];source_count+=1
            for v in node.values():source_hashes(v)
        elif isinstance(node,list):
            for v in node:source_hashes(v)
    source_hashes(teacher)
    for item in teacher['points']:
        city=item['city'];r=raw[city];assert item['original_value']==float(r['pupil_teacher_ratio']) and item['original_year']==int(r['pupil_teacher_ratio_year']) and item['original_flag']==r['pupil_teacher_ratio_flag']

    oldcases=pd.read_csv(R/'results/current_point_withdrawal/cases.csv',keep_default_na=False,float_precision='round_trip');newcases=pd.read_csv(WD/'cases.csv',keep_default_na=False,float_precision='round_trip');ck=['weight_reference','withdrawn_city','indicator']
    cp=newcases.merge(oldcases,on=ck,suffixes=('_v204','_v203'),validate='one_to_one')
    for col in ['baseline_choice_excess_regret','post_minimax_regret','mean_width','possible_champions']:cp[col+'_change']=pd.to_numeric(cp[col+'_v204'])-pd.to_numeric(cp[col+'_v203'])
    savedcp=pd.read_csv(WD/'comparison_v203.csv',keep_default_na=False,float_precision='round_trip')
    pd.testing.assert_frame_equal(cp,savedcp,check_exact=False,atol=2e-12,rtol=0)
    oldrank=pd.read_csv(R/'results/current_point_withdrawal/ranks.csv');newrank=pd.read_csv(WD/'ranks.csv');rr=newrank.merge(oldrank,on=ck+['city'],suffixes=('_v204','_v203'),validate='one_to_one');assert len(rr)==3584
    assert int((rr.decision_rank_v204!=rr.decision_rank_v203).sum())==summary['withdrawal_rank_rows_changed_vs_v203']==520
    assert int((cp.after_choices_v204!=cp.after_choices_v203).sum())==summary['withdrawal_after_choice_changed_vs_v203']==0
    assert changed==summary['withdrawal_choice_changes_v204']=={'fixed':10,'equal':35}
    # Every inherited evidence field and source classification is preserved; stress fields updated above.
    original=readrows(R/'results/current_point_source_ledger/ledger.csv')
    dynamic={'fixed_withdrawal_switch','equal_withdrawal_switch','fixed_original_policy_excess_regret','equal_original_policy_excess_regret','review_priority_excess_regret'}
    old_by={(x['city'],x['indicator']):x for x in original}
    assert len(old_by)==112
    for x in ledger:
        old=old_by[x['city'],x['indicator']]
        assert all(x[k]==old[k] for k in x if k not in dynamic)

    for mapping in (core,new,frozen):
        for n,h in mapping.items():assert sha(R/n)==h,n
    files=[R/n for n in summary['source_sha256']]+[O/n for n in summary['output_sha256']]+[O/'summary.json',R/'design/task4_user_v204_snapshot.json',Path(__file__),R/'scripts/task4_audit_output.py',R/'scripts/audit_current_priority.py',R/'scripts/audit_current_point_withdrawal.py',R/'scripts/audit_current_point_source_ledger.py',R/'data/current_all16_cost_editions/comparison.csv',R/'data/current_all16_broadband_fields/comparison.csv',R/'data/current_point_source_ledger/teacher_scope.json']
    report=dict(status='pass staged operational rebase',activation_status='staged_not_active',acquisition_rows=96,exact_endpoints=192,lower_only_rows=480,interior_probes=interior,independent_scalar_evaluations=count,point_withdrawal_cases=224,withdrawal_rank_rows=3584,ledger_rows=112,classification_counts=dict(counts),teacher_reference_hashes_checked=source_count,priority_positions_changed=6,withdrawal_rank_changes=520,withdrawal_switches=changed,upstream_bindings=548,v204_new_bindings=110,source_sha256={str(p.relative_to(R)):sha(p) for p in sorted(set(files))},scope='Conditional information envelopes and hypothetical point withdrawals, not source error probabilities. Existing evidence classification is bounded; no manuscript or active registry examined.')
    emit_report(report,args,O/'verification.json',G)
if __name__=='__main__':main()
