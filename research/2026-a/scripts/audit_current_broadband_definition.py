"""Independent embedded-JSON and scalar audit of all16 broadband field checks."""
from pathlib import Path
import csv, hashlib, json, math, subprocess, sys
from decimal import Decimal
from urllib.parse import urlsplit, parse_qs
from task4_audit_output import audit_parser, check_output, emit_report
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES

R=Path(__file__).resolve().parents[1];G=R.parents[1];P=G.parent/'HiMCM-Overleaf'
D=R/'data/current_all16_broadband_fields';O=R/'results/current_all16_broadband_review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def close(a,b):assert math.isclose(float(a),float(b),rel_tol=0,abs_tol=2e-11),(a,b)
def scalar(z,w):
    bad=math.sqrt(math.fsum(a*x*x for a,x in zip(w,z)))
    good=math.sqrt(math.fsum(a*(1-x)*(1-x) for a,x in zip(w,z)))
    return 100*bad/(bad+good)

def main():
    args=audit_parser(__doc__).parse_args();canonical=O/'verification.json';check_output(args,canonical,G)
    source=R/'data/task4_v5_resources/ookla_global_index.html'
    source_record=next(x for x in read(R/'data/task4_v5_resources/manifest.json') if x['file']==source.name)
    assert sha(source)==source_record['sha256'] and source.stat().st_size==source_record['bytes']
    data=json.JSONDecoder().raw_decode(source.read_text().split('var results = ',1)[1])[0]
    original=rows(R/'data/task4_v117_team_intake/city_indicators.csv');classified=rows(D/'comparison.csv')
    assert len(original)==len(classified)==16
    exported=read(D/'summary.json');assert json.loads(subprocess.check_output([sys.executable,str(D/'deterministic_offline_extract.py')],text=True))==exported
    date_records=[];counts={'fixedMedian':0,'fixedMean':0,'mobileMedian':0,'mobileMean':0}
    for original_row,classified_row in zip(original,classified):
        assert original_row['city']==classified_row['city'] and original_row['iso2']==classified_row['iso2']
        assert Decimal(original_row['broadband_mbps'])==Decimal(classified_row['input_value_mbps'])
        assert original_row['broadband_mbps_year']==classified_row['input_year'] and original_row['broadband_mbps_flag']==classified_row['input_flag']
        city='Zürich' if original_row['city']=='Zurich' else original_row['city'];singapore=original_row['iso2']=='SG'
        for field in counts:
            key=field if singapore else (field.replace('Median','CitiesMedian') if field.endswith('Median') else None)
            candidates=[] if key is None else [x for x in data[key] if x['country']['country_code']==original_row['iso2'] and (singapore or x['city_name']==city)]
            if not candidates:
                assert not classified_row[field+'_value'] and classified_row[field+'_geography_level']=='unavailable'
                assert classified_row[field+'_exact_value_match']=='false';continue
            assert len(candidates)==1
            record=candidates[0];assert Decimal(record['download_mbps'])==Decimal(classified_row[field+'_value'])
            assert int(record['rank'])==int(classified_row[field+'_rank'])
            assert classified_row[field+'_geography_level']==('country' if singapore else 'city')
            assert classified_row[field+'_country']==record['country']['country_name']
            link=urlsplit(classified_row[field+'_link']);assert link.path=='/global-index/'+record['country']['slug']
            assert link.fragment==('fixed' if field.startswith('fixed') else 'mobile')
            assert parse_qs(link.query)==({} if singapore else {'city':[city]})
            matched=Decimal(record['download_mbps'])==Decimal(original_row['broadband_mbps'])
            assert classified_row[field+'_exact_value_match']==str(matched).lower()
            if matched:counts[field]+=1;date_records.append(record)
        assert classified_row['exact_match_fields']==('fixedMean' if singapore else 'fixedMedian')
    assert counts=={'fixedMedian':15,'fixedMean':1,'mobileMedian':0,'mobileMean':0}
    assert all(exported['counts'][k]==v for k,v in counts.items())
    dates={name:sorted({x[name] for x in date_records}) for name in ['month','global_index_date','aggregate_date','time_period_type']}
    assert dates=={'month':['2026-09'],'global_index_date':['2026-09-01'],'aggregate_date':['2026-07-01 00:00:00'],'time_period_type':['rolling_quarter']}
    summary=read(O/'summary.json')
    for name,digest in summary['source_sha256'].items():assert sha(R/name)==digest,name
    for name,digest in summary['output_sha256'].items():assert sha(O/name)==digest,name
    f,low,high=revised_bounds();cities=f.city.tolist();sg=cities.index('Singapore');col=NAMES.index('fixed_broadband_mbps')
    for i,row in enumerate(original):
        expected=float(row['broadband_mbps'])/(100+float(row['broadband_mbps']))
        close(low[i,col],expected);assert low[i,col]==high[i,col]
    bounds=rows(O/'bounds.csv');ranks=rows(O/'ranks.csv');assert len(bounds)==320 and len(ranks)==64
    checked=0;comparisons=[];independent_ranks={};independent_widths={}
    for scenario in ['retained_V203','Singapore_median_alternative']:
        selected={(x['city'],x['indicator']):x for x in bounds if x['scenario']==scenario};assert len(selected)==160
        ll=[];hh=[]
        for i,city in enumerate(cities):
            a=[];b=[]
            for j,name in enumerate(NAMES):
                expected_low=low[i,j];expected_high=high[i,j]
                if scenario.endswith('alternative') and i==sg and j==col:expected_low=expected_high=476.02/(100+476.02)
                record=selected[city,name];close(record['lower'],expected_low);close(record['upper'],expected_high)
                a.append(float(record['lower']));b.append(float(record['upper']))
            ll.append(a);hh.append(b)
        for reference in ['fixed','equal']:
            w=[.1]*10 if reference=='equal' else [.05 if j in (6,9) else .1125 for j in range(10)]
            lower=[scalar(z,w) for z in ll];upper=[scalar(z,w) for z in hh]
            regret=[max(0,max(upper[k] for k in range(16) if k!=i)-lower[i]) for i in range(16)]
            decision_ranks=[1+sum(x<r-1e-10 for x in regret) for r in regret]
            independent_ranks[scenario,reference]=decision_ranks
            independent_widths[scenario,reference]=math.fsum(b-a for a,b in zip(lower,upper))/16
            selected_ranks={x['city']:x for x in ranks if x['scenario']==scenario and x['weight_reference']==reference};assert len(selected_ranks)==16
            for i,city in enumerate(cities):
                record=selected_ranks[city]
                for key,value in [('score_lower',lower[i]),('score_upper',upper[i]),('max_regret',regret[i])]:close(record[key],value)
                assert int(record['decision_rank'])==decision_ranks[i]
                possible=upper[i]>=max(lower[k] for k in range(16) if k!=i)-1e-12
                necessary=lower[i]>=max(upper[k] for k in range(16) if k!=i)-1e-12
                assert record['possible_champion']==str(possible)=='True' and record['necessary_champion']==str(necessary)=='False'
                assert int(record['best_rank'])==1+sum(lower[k]>upper[i]+1e-12 for k in range(16) if k!=i)
                assert int(record['worst_rank'])==1+sum(upper[k]>lower[i]+1e-12 for k in range(16) if k!=i)
                checked+=1
            case=next(x for x in summary['cases'] if x['scenario']==scenario and x['weight_reference']==reference)
            assert case['recommendations']==(['Oslo'] if reference=='fixed' else ['Zurich'])
            assert case['recommendations']==[cities[i] for i,r in enumerate(regret) if r<=min(regret)+1e-12]
            assert case['possible_champions']==16 and case['necessary_champions']==0
            close(case['mean_width'],math.fsum(b-a for a,b in zip(lower,upper))/16)
            comparisons.append({'scenario':scenario,'weight_reference':reference,'Singapore_lower':lower[sg],'Singapore_upper':upper[sg],'Singapore_rank':int(selected_ranks['Singapore']['decision_rank'])})
    for contrast in summary['contrasts']:
        assert contrast['decision_rank_changes']==0 and contrast['recommendation_changed'] is False
        ref=contrast['weight_reference']
        assert sum(a!=b for a,b in zip(independent_ranks['retained_V203',ref],independent_ranks['Singapore_median_alternative',ref]))==0
        before,after=[x for x in comparisons if x['weight_reference']==contrast['weight_reference']]
        close(contrast['Singapore_lower_change'],after['Singapore_lower']-before['Singapore_lower'])
        close(contrast['Singapore_upper_change'],after['Singapore_upper']-before['Singapore_upper'])
        assert contrast['mean_width_change']>0
        close(contrast['mean_width_change'],independent_widths['Singapore_median_alternative',ref]-independent_widths['retained_V203',ref])
    current=read(R/'results/current_paper_review/current_verification.json');core=read(R/'design/task4_user_v203_snapshot.json')['source_sha256'];extra={}
    for name,group in current.items():
        if name.startswith('additional_') and name.endswith('_sha256'):extra.update(group)
    assert len(core)==548 and len(extra)==77
    for name,digest in {**core,**extra,**current['withdrawal_source_sha256'],**current['edition_source_sha256']}.items():assert sha(R/name)==digest,name
    for name,digest in current['current_files_sha256'].items():assert sha(P/name)==sha(G/'paper/current'/name)==digest
    assert sha(G/'paper/current/main.pdf')==current['pdf_sha256']
    inputs=[*sorted(D.iterdir()),O/'README.md',O/'summary.json',O/'bounds.csv',O/'ranks.csv',Path(__file__),R/'scripts/task4_current_broadband_definition.py',source,R/'data/task4_v5_resources/manifest.json',R/'scripts/task4_audit_output.py']
    report=dict(status='pass',field_classification_counts=counts,independent_source_reader='Embedded JSON versus regex HTML',source_date_fields=dates,scalar_city_scenario_weight_cases=checked,utility_bounds_checked=320,contrasts=summary['contrasts'],primary_admissions=0,actual_primary_width_reduction=0,science_bindings_checked=548,supplemental_bindings_checked=77,withdrawal_entries_checked=10,edition_entries_checked=24,paper_dependencies_each_copy=7,current_PDF_unchanged=True,source_sha256={str(p.relative_to(R)):sha(p) for p in inputs},scope='All16 publisher fields classified; Singapore-only statistical-definition alternative. No original extraction lineage or municipal-boundary harmonization established; raw dates are not interpreted as exact rolling-window boundaries. PrimaryCSV/values/rules and paper unchanged; no Monte Carlo replay or empirical uncertainty reduction.')
    emit_report(report,args,canonical,G)

if __name__=='__main__':main()
