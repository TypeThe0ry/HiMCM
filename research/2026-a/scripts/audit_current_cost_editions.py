"""Read-only independent audit of all16 cost-edition source and ranking comparisons."""
from pathlib import Path
import csv,hashlib,json,math,subprocess,sys
from decimal import Decimal
from task4_audit_output import audit_parser,check_output,emit_report
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES
from audit_current_oslo_cost_ptr_sources import table_rows,plain_text,protected_inputs
from audit_current_broadband_definition import scalar

R=Path(__file__).resolve().parents[1];G=R.parents[1]
D=R/'data/current_all16_cost_editions';O=R/'results/current_cost_edition_review'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def close(a,b):assert math.isclose(float(a),float(b),abs_tol=2e-11,rel_tol=0),(a,b)

def main():
    a=audit_parser(__doc__).parse_args();check_output(a,O/'verification.json',G)
    protected=protected_inputs();current=read(R/'results/current_paper_review/current_verification.json')
    for name,digest in current['edition_source_sha256'].items():assert sha(R/name)==digest,name
    original=rows(R/'data/task4_v117_team_intake/city_indicators.csv');classified=rows(D/'comparison.csv');assert len(original)==16 and len(classified)==32
    assert subprocess.check_output([sys.executable,str(D/'extract.py')],text=True)==(D/'comparison.csv').read_text()
    source_summary=read(D/'summary.json');assert source_summary['scope']['cells_available']==96
    for name,record in source_summary['source_files'].items():
        path=G/name;assert sha(path)==record['sha256'] and path.stat().st_size==record['bytes']
    specs=[('cli','cost-of-living','Cost of Living Index','cost_living_index',100),('pir','property-investment','Price To Income Ratio','price_income_ratio',10)]
    expected={};match_counts={name:{edition:0 for edition in ['2026','mid','current']} for name,*_ in specs};unmatched=[]
    source_cache={}
    for indicator,kind,header,model_name,anchor in specs:
        for edition in ['2026','mid','current']:
            path=R/f'data/city_matrix_25_audit/sources/{kind}_{edition}.html';table=table_rows(path)
            head=next(r for r in table if 'City' in r and header in r);ci=head.index('City');vi=head.index(header)
            title=('Current '+('Cost of Living Index' if indicator=='cli' else 'Property Prices Index')) if edition=='current' else (('Cost of Living Index' if indicator=='cli' else 'Property Prices Index')+' by City 2026'+(' Mid-Year' if edition=='mid' else ''))
            assert title in plain_text(path)
            data=[]
            for row in table:
                if len(row)<=vi or ', ' not in row[ci]:continue
                try:Decimal(row[vi])
                except Exception:continue
                data.append(row)
            source_cache[indicator,edition]=(data,ci,vi)
        for original_row in original:
            city=original_row['city'];country='Czech Republic' if original_row['country']=='Czechia' else original_row['country'];label=city+', '+country
            row=next(x for x in classified if x['city']==city and x['indicator']==indicator)
            assert row['country']==original_row['country']
            assert row['input_value']==original_row[indicator] and row['input_year']==original_row[indicator+'_year'] and row['input_flag']==original_row[indicator+'_flag']
            matches=[]
            for edition in ['2026','mid','current']:
                table,ci,vi=source_cache[indicator,edition];selected=[(i,r) for i,r in enumerate(table,1) if r[ci]==label];assert len(selected)==1,label
                rank,source_row=selected[0];assert Decimal(source_row[vi])==Decimal(row[edition+'_value']) and int(row[edition+'_rank'])==rank
                expected[edition,city,model_name]=float(source_row[vi])
                if Decimal(source_row[vi])==Decimal(original_row[indicator]):matches.append(edition);match_counts[indicator][edition]+=1
            assert row['exact_matches']=='|'.join(matches)
            if not matches:unmatched.append({'city':city,'indicator':indicator,'submitted':float(row['input_value'])})
    assert match_counts==source_summary['exact_match_counts_by_indicator_edition']
    assert len(unmatched)==4
    summary=read(O/'summary.json')
    for name,digest in summary['source_sha256'].items():assert sha(R/name)==digest,name
    for name,digest in summary['output_sha256'].items():assert sha(O/name)==digest,name
    exported_values=rows(O/'edition_values.csv');assert len(exported_values)==96
    for row in exported_values:close(row['publisher_value'],expected[row['edition'],row['city'],row['indicator']])
    frame,lo,hi=revised_bounds();cities=frame.city.tolist();bounds=rows(O/'bounds.csv');ranks=rows(O/'ranks.csv');assert len(bounds)==640 and len(ranks)==128
    independent={};score_cases=0
    for scenario in ['retained_V203','2026','mid','current']:
        saved={(x['city'],x['indicator']):x for x in bounds if x['scenario']==scenario};assert len(saved)==160
        ll=[];hh=[];changed=0
        for i,city in enumerate(cities):
            lower=[];upper=[]
            for j,name in enumerate(NAMES):
                low,high=float(lo[i,j]),float(hi[i,j])
                if scenario!='retained_V203' and name in ['cost_living_index','price_income_ratio']:
                    anchor=100 if name=='cost_living_index' else 10;value=expected[scenario,city,name];low=high=anchor/(anchor+value)
                    changed+=int(low!=lo[i,j])
                record=saved[city,name];close(record['lower'],low);close(record['upper'],high);lower.append(low);upper.append(high)
            ll.append(lower);hh.append(upper)
        if scenario!='retained_V203':assert changed==summary['actually_changed_point_cells'][scenario]
        for ref in ['fixed','equal']:
            w=[.1]*10 if ref=='equal' else [.05 if j in (6,9) else .1125 for j in range(10)]
            low=[scalar(z,w) for z in ll];high=[scalar(z,w) for z in hh];regret=[max(0,max(high[k] for k in range(16) if k!=i)-low[i]) for i in range(16)]
            decision_rank=[1+sum(x<r-1e-10 for x in regret) for r in regret]
            saved_ranks={x['city']:x for x in ranks if x['scenario']==scenario and x['weight_reference']==ref};assert len(saved_ranks)==16
            for i,city in enumerate(cities):
                row=saved_ranks[city]
                for name,value in [('score_lower',low[i]),('score_upper',high[i]),('max_regret',regret[i])]:close(row[name],value)
                assert int(row['decision_rank'])==decision_rank[i]
                possible=high[i]>=max(low[k] for k in range(16) if k!=i)-1e-12;necessary=low[i]>=max(high[k] for k in range(16) if k!=i)-1e-12
                assert row['possible_champion']==str(possible)=='True' and row['necessary_champion']==str(necessary)=='False'
                assert int(row['best_rank'])==1+sum(low[k]>high[i]+1e-12 for k in range(16) if k!=i)
                assert int(row['worst_rank'])==1+sum(high[k]>low[i]+1e-12 for k in range(16) if k!=i);score_cases+=1
            case=next(x for x in summary['cases'] if x['scenario']==scenario and x['weight_reference']==ref)
            assert case['recommendations']==[cities[i] for i,r in enumerate(regret) if r<=min(regret)+1e-12]==(['Oslo'] if ref=='fixed' else ['Zurich'])
            assert case['top_three']==[cities[i] for i in sorted(range(16),key=lambda i:decision_rank[i])[:3]]
            width=math.fsum(b-a for a,b in zip(low,high))/16;close(case['mean_width'],width)
            assert case['possible_champions']==16 and case['necessary_champions']==0
            independent[scenario,ref]=(decision_rank,width,low,high)
    for case in summary['contrasts']:
        before=independent['retained_V203',case['weight_reference']];after=independent[case['edition'],case['weight_reference']]
        changed=[city for city,a,b in zip(cities,before[0],after[0]) if a!=b]
        assert case['changed_cities']==changed and case['changed_decision_ranks']==len(changed)
        close(case['mean_width_change'],after[1]-before[1]);close(case['largest_absolute_lower_score_change'],max(abs(a-b) for a,b in zip(before[2],after[2])));close(case['largest_absolute_upper_score_change'],max(abs(a-b) for a,b in zip(before[3],after[3])))
    peer=read(O/'peer_review.json');assert peer['status']=='reviewed_scoped'
    for name,digest in peer['reviewed_inputs_sha256'].items():assert sha(R/name)==digest,name
    inputs=[*sorted(p for p in D.iterdir() if p.is_file()),O/'README.md',O/'peer_review.json',O/'summary.json',O/'bounds.csv',O/'ranks.csv',O/'edition_values.csv',Path(__file__),R/'scripts/task4_current_cost_editions.py',R/'scripts/audit_current_oslo_cost_ptr_sources.py',R/'scripts/audit_current_broadband_definition.py',R/'scripts/task4_audit_output.py']
    inputs.extend(R/name for name in summary['source_sha256'])
    report=dict(status='pass',**protected,edition_entries_checked=len(current['edition_source_sha256']),independent_source_reader='HTMLParser versus regex classifier',source_cells_checked=96,source_match_counts=match_counts,unmatched_original_points=unmatched,independent_scalar_cases=score_cases,bound_rows_checked=640,contrasts=summary['contrasts'],primary_admissions=0,actual_primary_width_reduction=0,source_sha256={str(p.relative_to(R)):sha(p) for p in inputs},scope='Edition-defined source alternatives; original input lineage and municipal geography remain unverified. No time trend, calendar-year measurement, student-budget validation or precision gain established. Primary values, intervals, weights, manuscript and PDF preserved; no Monte Carlo replay.')
    emit_report(report,a,O/'verification.json',G)

if __name__=='__main__':main()
