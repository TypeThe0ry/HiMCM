"""Compile a bounded per-point source ledger without changing user16 V203."""
from pathlib import Path
import csv,hashlib,json
from collections import Counter

R=Path(__file__).resolve().parents[1];G=R.parents[1];O=R/'results/current_point_source_ledger'
def read(p):return json.loads(p.read_text())
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    withdrawals=rows(R/'results/current_point_withdrawal/cases.csv')
    fixed={(r['withdrawn_city'],r['indicator']):r for r in withdrawals if r['weight_reference']=='fixed'}
    equal={(r['withdrawn_city'],r['indicator']):r for r in withdrawals if r['weight_reference']=='equal'}
    assert len(fixed)==len(equal)==112 and fixed.keys()==equal.keys()
    raw={r['city']:r for r in rows(R/'data/task4_v117_team_intake/city_indicators.csv')}
    costs={(r['city'],r['indicator']):r for r in rows(R/'data/current_all16_cost_editions/comparison.csv')}
    broadband={r['city']:r for r in rows(R/'data/current_all16_broadband_fields/comparison.csv')}
    teachers={r['city']:r for r in read(R/'data/current_point_source_ledger/teacher_scope.json')['points']}
    out=[]
    for key,case in fixed.items():
        city,indicator=key;field=case['input_field'];r=raw[city]
        assert float(r[field])==float(case['submitted_value'])
        state='not_included_in_bounded_classification';detail='No specific source classification imported here; this does not mean never reviewed.';evidence=''
        need='Find the original extraction and matching variable, year, geography and denominator; consult existing route index first.'
        if indicator=='fixed_broadband_mbps':
            b=broadband[city];state='publisher_value_match_scope_unverified' if b['exact_match_fields']=='fixedMedian' else 'publisher_match_different_statistic'
            detail='Exact city fixed-download median match.' if state.startswith('publisher_value') else 'Exact Singapore country fixed-download mean; other15use city medians.'
            evidence='data/current_all16_broadband_fields/comparison.csv';need='Original extraction and geographic/coverage definition; preserve field and rolling-period qualifications.'
        elif field in ('cli','pir'):
            c=costs[city,field];state='publisher_value_match_scope_unverified' if c['exact_matches'] else 'no_match_checked_cost_editions'
            detail='Exact publisher value in edition(s): '+c['exact_matches'] if c['exact_matches'] else 'No exact value in the three checked archived editions; no error established.'
            evidence='data/current_all16_cost_editions/comparison.csv';need='Original edition/access time and municipal boundary; matched value does not identify extraction lineage.'
        elif indicator=='upper_secondary_ptr':
            t=teachers[city];evidence='data/current_point_source_ledger/teacher_scope.json'
            if city in ('Tokyo','Singapore'):state='documented_value_match_different_stage';detail=t['limits'];need='Original stage/teacher-unit/geography definition; retain source-stage warning.'
            elif city=='Oslo':state='no_match_examined_PTR_series';detail=t['limits'];need='Original18.2source; examined SSB12.5 is not a replacement.'
            elif city in ('Vienna','Berlin'):
                state='reviewed_lineage_unresolved'
                folder='current_vienna_ptr_point' if city=='Vienna' else 'current_berlin_ptr_point'
                followup=read(R/'data'/folder/'scope.json')
                assert followup['original_lineage_verified'] is False and followup['target_scope_verified'] is False
                evidence='data/'+folder+'/README.md'
                detail=('No Vienna9.4/2023source established; examined Austria national ED3 FTE9.8 is not a city observation; municipal request403 and publication download incomplete.' if city=='Vienna' else 'No Berlin12.5/2025source established. Workbook distinguishes teacher persons from FTE; indexed different-year/school-type lead is unverified; city report429 skipped.')
                need='Original matching city/stage/teacher-unit/provider/reference record; consult new bounded source package rather than repeat blocked requests.'
            else:detail=t['limits']
        elif (city,indicator) in [('Oslo','pm25'),('Oslo','research_he_density'),('Zurich','homicide_rate')]:
            state='reviewed_lineage_unresolved'
            if indicator=='pm25':evidence='results/current_oslo_pm_source_review/verification.json';detail='Station and2023FUA records do not identify original modelled2024point.'
            elif indicator=='research_he_density':evidence='data/current_oslo_he_scope/README.md';detail='National institution categories do not verify the original roster of25institutions in Oslo.'
            else:evidence='data/current_zurich_homicide_scope/README.md';detail='Original0.14 numerator/unit/population lineage remains unresolved.'
            need='Seek new matching published evidence; user currently lacks Oslo HE roster/Zurich homicide source. Do not repeat unavailable-source request.'
        eq=equal[key];assert case['retained_utility']==eq['retained_utility']
        out.append(dict(city=city,indicator=indicator,input_field=field,original_value=r[field],original_year=r[field+'_year'],original_flag=r[field+'_flag'],retained_utility=case['retained_utility'],classification=state,evidence=evidence,scope_detail=detail,original_extraction_lineage_verified=False,measurement_fully_certified=False,next_evidence_needed=need,fixed_withdrawal_switch=case['recommendation_set_changed'],equal_withdrawal_switch=eq['recommendation_set_changed'],fixed_original_policy_excess_regret=float(case['baseline_choice_excess_regret']),equal_original_policy_excess_regret=float(eq['baseline_choice_excess_regret']),review_priority_excess_regret=max(float(case['baseline_choice_excess_regret']),float(eq['baseline_choice_excess_regret']))))
    O.mkdir(exist_ok=True)
    for name,data in [('ledger.csv',out),('review_priority.csv',sorted(out,key=lambda x:(-x['review_priority_excess_regret'],x['city'],x['indicator'])))]:
        with (O/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator='\n');w.writeheader();w.writerows(data)
    inputs=[R/'data/task4_v117_team_intake/city_indicators.csv',R/'results/current_point_withdrawal/cases.csv',R/'results/current_point_withdrawal/verification.json',R/'data/current_all16_cost_editions/comparison.csv',R/'results/current_cost_edition_review/verification.json',R/'data/current_all16_broadband_fields/comparison.csv',R/'results/current_all16_broadband_review/verification.json',R/'data/current_point_source_ledger/teacher_scope.json',R/'results/current_oslo_pm_source_review/verification.json',R/'data/current_oslo_he_scope/README.md',R/'data/current_zurich_homicide_scope/README.md',Path(__file__)]
    inputs.extend([R/'data/current_vienna_ptr_point/scope.json',R/'data/current_berlin_ptr_point/scope.json',R/'results/current_vienna_berlin_ptr_review/verification.json'])
    summary=dict(primary_model='V203 unchanged',ledger_rows=112,classification_counts=dict(Counter(x['classification'] for x in out)),original_extraction_lineages_verified=0,fully_certified_measurements=0,fixed_withdrawal_switches=sum(x['fixed_withdrawal_switch']=='True' for x in out),equal_withdrawal_switches=sum(x['equal_withdrawal_switch']=='True' for x in out),primary_admissions=0,actual_primary_width_reduction=0,source_sha256={str(p.relative_to(R)):sha(p) for p in inputs},output_sha256={n:sha(O/n) for n in ['ledger.csv','review_priority.csv']},scope='Bounded imported evidence classification of112retainedpointUTILITYcells, not all nonemptyCSVvalues.48intervalcells and supplementary inventories remain in their existing registries. Classification is not input exclusion, source-error probability or proof of original extraction. Priority imports the existing ignorance stress, not a new scoring model or empirical error estimate.')
    (O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:summary[k] for k in ['ledger_rows','classification_counts','fixed_withdrawal_switches','equal_withdrawal_switches']}))

if __name__=='__main__':main()
