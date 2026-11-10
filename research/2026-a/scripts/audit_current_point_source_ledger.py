"""Read-only independent consistency and preservation checks for112point source records."""
from pathlib import Path
import csv,hashlib,json,math
from collections import Counter
from task4_audit_output import audit_parser,check_output,emit_report
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES
from audit_current_oslo_cost_ptr_sources import protected_inputs

R=Path(__file__).resolve().parents[1];G=R.parents[1];O=R/'results/current_point_source_ledger'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def main():
    a=audit_parser(__doc__).parse_args();check_output(a,O/'verification.json',G)
    s=read(O/'summary.json')
    for n,h in s['source_sha256'].items():assert sha(R/n)==h,n
    for n,h in s['output_sha256'].items():assert sha(O/n)==h,n
    ledger=rows(O/'ledger.csv');priority=rows(O/'review_priority.csv');assert len(ledger)==len(priority)==112
    keys={(x['city'],x['indicator']) for x in ledger};assert len(keys)==112
    f,l,h=revised_bounds();expected={(f.city.iloc[i],NAMES[j]) for i in range(16) for j in range(10) if l[i,j]==h[i,j]};assert keys==expected
    raw={x['city']:x for x in rows(R/'data/task4_v117_team_intake/city_indicators.csv')}
    costs={(x['city'],x['indicator']):x for x in rows(R/'data/current_all16_cost_editions/comparison.csv')}
    band={x['city']:x for x in rows(R/'data/current_all16_broadband_fields/comparison.csv')}
    stress={(x['weight_reference'],x['withdrawn_city'],x['indicator']):x for x in rows(R/'results/current_point_withdrawal/cases.csv')}
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
        elif (city,indicator) in [('Oslo','pm25'),('Oslo','research_he_density'),('Zurich','homicide_rate')]:state='reviewed_lineage_unresolved'
        assert x['classification']==state;counts[state]+=1
        assert x['measurement_fully_certified']==x['original_extraction_lineage_verified']=='False'
        if x['evidence']:assert (R/x['evidence']).is_file()
        excess=[]
        for ref in ['fixed','equal']:
            case=stress[ref,city,indicator]
            assert x[ref+'_withdrawal_switch']==case['recommendation_set_changed']
            value=float(case['baseline_choice_excess_regret']);assert float(x[ref+'_original_policy_excess_regret'])==value;excess.append(value)
        assert float(x['review_priority_excess_regret'])==max(excess)
    assert dict(counts)==s['classification_counts']
    assert sum(x['fixed_withdrawal_switch']=='True' for x in ledger)==s['fixed_withdrawal_switches']==10
    assert sum(x['equal_withdrawal_switch']=='True' for x in ledger)==s['equal_withdrawal_switches']==35
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
    protected=protected_inputs();current=read(R/'results/current_paper_review/current_verification.json')
    for n,digest in current['edition_source_sha256'].items():assert sha(R/n)==digest,n
    report=dict(status='pass',**protected,edition_entries_checked=24,retained_point_cells_checked=112,classification_counts=dict(counts),teacher_reference_hashes_checked=source_count,original_lineages_verified=0,fully_certified_measurements=0,source_priority_scope='Existing112single-pointignorancecasesperweight, noterrorprobabilities or measurement mistakes',primary_admissions=0,actual_primary_width_reduction=0,source_sha256={str(p.relative_to(R)):sha(p) for p in [O/'README.md',O/'summary.json',O/'ledger.csv',O/'review_priority.csv',R/'data/current_point_source_ledger/teacher_scope.json',R/'scripts/task4_current_point_source_ledger.py',Path(__file__),R/'scripts/task4_audit_output.py']},scope='Bounded import ledger, not anexhaustive historical review or fullmeasurement certification. Currentpaper/primarypreserved; no source exclusions, interval edits, newrankingmodel or actualdataadmission.')
    emit_report(report,a,O/'verification.json',G)

if __name__=='__main__':main()
