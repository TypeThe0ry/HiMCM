"""Independent PM route/receipt checks and scalar criterion-block stress."""
from pathlib import Path
from datetime import datetime
import csv,hashlib,json,math,xml.etree.ElementTree as ET
from task4_audit_output import audit_parser,check_output,emit_report
from audit_current_oslo_cost_ptr_sources import protected_inputs
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES
R=Path(__file__).resolve().parents[1];G=R.parents[1]
D=R/'data/current_all16_pm_sources';O=R/'results/current_pm_block_withdrawal'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def close(a,b):assert math.isclose(float(a),float(b),rel_tol=0,abs_tol=2e-11),(a,b)
def scalar(u,w):
    a=math.sqrt(math.fsum(x*x*v for x,v in zip(u,w)));b=math.sqrt(math.fsum((1-x)*(1-x)*v for x,v in zip(u,w)))
    return 100*a/(a+b)
def main():
    a=audit_parser(__doc__).parse_args();check_output(a,O/'verification.json',G)
    receipt=read(D/'retrieval.json');assert len(receipt)==2 and all(x['status']==403 for x in receipt)
    for r in receipt:
        p=D/r['file'];assert sha(p)==r['sha256'] and p.stat().st_size==r['bytes']
        assert datetime.fromisoformat(r['requested_utc']).utcoffset() is not None
        assert ',1.5/' in r['requested_url'] or '/1.5?' in r['requested_url']
    mapped=read(D/'area_map.json');assert mapped['metadata_flow_version']=='1.2' and mapped['codelist_version']=='1.1'
    for n,h in mapped['source_sha256'].items():assert sha(R/n)==h,n
    tree=ET.parse(R/'data/current_oslo_pm_model/structure.xml');cl=next(x for x in tree.findall('.//{*}Codelist') if x.get('id')=='CL_FUA_CITY')
    codes={c.get('id'):c for c in cl.findall('./{*}Code')}
    prefixes=['AT001','CH002','FI001','DE001','UK001','NL001','SE001','FR001','ES001','IT002','IE001','NO001','CZ001','PL001',None,'JPN01']
    raw=rows(R/'data/task4_v117_team_intake/city_indicators.csv');assert len(mapped['cities'])==len(raw)==16
    requested=set(next(x['target_area_codes'] for x in receipt if 'target_area_codes' in x))
    expected_codes={p+s for p in prefixes if p for s in ['C','F']};assert requested==expected_codes
    for original,m,prefix in zip(raw,mapped['cities'],prefixes):
        assert [m[k] for k in ['city','original_iso2','original_country','original_PM_value','original_year','original_flag']]==[original[k] for k in ['city','iso2','country','pm25_ugm3','pm25_ugm3_year','pm25_ugm3_flag']]
        assert not m['current_v1_5_code_validity_verified'] and not m['numeric_original_PM_verified']
        if prefix is None:
            assert m['city']=='Singapore' and m['country_root']=='SGP' and 'SGP' not in codes and not m['areas'];continue
        assert {x['code'] for x in m['areas']}=={prefix+'C',prefix+'F'}
        for area in m['areas']:
            c=area['code'];chain=[c]
            while codes[c].find('./{*}Parent/Ref') is not None:
                c=codes[c].find('./{*}Parent/Ref').get('id');assert c not in chain;chain.append(c)
            assert chain==area['parent_chain'] and chain[-1]==m['country_root']
            assert area['label'] in [n.text for n in codes[area['code']].findall('./{*}Name')]
            assert area['kind']==('CITY' if area['code'].endswith('C') else 'FUA')
    assert mapped['mapped_city_pairs']==15 and mapped['unmapped_cities']==['Singapore'] and mapped['new_PM_observations']==0
    old=rows(R/'data/current_oslo_pm_model/oslo_exposure.csv');assert len(old)==6 and max(int(x['TIME_PERIOD']) for x in old)==2023
    summary=read(O/'summary.json');bounds=rows(O/'bounds.csv');ranks=rows(O/'ranks.csv')
    for n,h in summary['source_sha256'].items():assert sha(R/n)==h,n
    for n,h in summary['output_sha256'].items():assert sha(O/n)==h,n
    f,lo,hi=revised_bounds();cities=f.city.tolist();pm=NAMES.index('pm25');assert len(bounds)==320 and len(ranks)==64
    for i,row in enumerate(raw):
        assert row['city']==cities[i] and row['pm25_ugm3_flag']=='MODELLED' and row['pm25_ugm3_year']=='2024'
        close(lo[i,pm],15/(15+float(row['pm25_ugm3'])));assert lo[i,pm]==hi[i,pm]
    independent={};checked=0
    for scenario in ['retained_V203','all_PM_points_withdrawn']:
        selected={(x['city'],x['indicator']):x for x in bounds if x['scenario']==scenario};assert len(selected)==160
        ll=lo.tolist();hh=hi.tolist()
        if scenario=='all_PM_points_withdrawn':
            for i in range(16):ll[i][pm]=0;hh[i][pm]=1
        for i,c in enumerate(cities):
            for j,name in enumerate(NAMES):close(selected[c,name]['lower'],ll[i][j]);close(selected[c,name]['upper'],hh[i][j])
        for ref in ['fixed','equal']:
            w=[.1]*10 if ref=='equal' else [.05 if j in [6,9] else .1125 for j in range(10)]
            lower=[scalar(x,w) for x in ll];upper=[scalar(x,w) for x in hh]
            regret=[max(0,max(upper[k] for k in range(16) if k!=i)-lower[i]) for i in range(16)]
            ranking=[1+sum(v<r-1e-10 for v in regret) for r in regret]
            saved={x['city']:x for x in ranks if (x['scenario'],x['weight_reference'])==(scenario,ref)};assert len(saved)==16
            for i,c in enumerate(cities):
                row=saved[c]
                for key,value in [('score_lower',lower[i]),('score_upper',upper[i]),('max_regret',regret[i])]:close(row[key],value)
                assert int(row['decision_rank'])==ranking[i]
                possible=upper[i]>=max(lower[k] for k in range(16) if k!=i)-1e-12
                necessary=lower[i]>=max(upper[k] for k in range(16) if k!=i)-1e-12
                assert row['possible_champion']==str(possible)=='True' and row['necessary_champion']==str(necessary)=='False'
                assert int(row['best_rank'])==1+sum(lower[k]>upper[i]+1e-12 for k in range(16) if k!=i)
                assert int(row['worst_rank'])==1+sum(upper[k]>lower[i]+1e-12 for k in range(16) if k!=i);checked+=1
            case=next(x for x in summary['cases'] if (x['scenario'],x['weight_reference'])==(scenario,ref))
            choices=[cities[i] for i,x in enumerate(regret) if x<=min(regret)+1e-12]
            assert case['recommendations']==choices==(['Oslo'] if (scenario,ref)==('retained_V203','fixed') else ['Zurich'])
            assert case['possible_champions']==16 and case['necessary_champions']==0
            width=math.fsum(b-a for a,b in zip(lower,upper))/16;close(case['mean_width'],width)
            independent[scenario,ref]=(lower,upper,regret,ranking,width,choices)
    assert len(summary['contrasts'])==2
    for c in summary['contrasts']:
        ref=c['weight_reference'];b=independent['retained_V203',ref];n=independent['all_PM_points_withdrawn',ref]
        assert c['baseline_recommendations']==b[5] and c['withdrawal_recommendations']==n[5]
        assert c['recommendation_changed']==(b[5]!=n[5]) and c['decision_rank_changes']==sum(x!=y for x,y in zip(b[3],n[3]))
        close(c['mean_width_change'],n[4]-b[4])
        assert all(x<=y+1e-12 for x,y in zip(n[0],b[0])) and all(x>=y-1e-12 for x,y in zip(n[1],b[1])) and all(x>=y-1e-12 for x,y in zip(n[2],b[2]))
    protected=protected_inputs();current=read(R/'results/current_paper_review/current_verification.json')
    for n,h in current['edition_source_sha256'].items():assert sha(R/n)==h,n
    files=[*sorted(D.glob('*')),*[O/n for n in ['README.md','summary.json','bounds.csv','ranks.csv']],R/'data/current_oslo_pm_model/structure.xml',R/'data/current_oslo_pm_model/oslo_exposure.csv',R/'scripts/task4_current_pm_block_withdrawal.py',Path(__file__)]
    report=dict(status='pass bounded PM routing and scalar block-withdrawal review',**protected,edition_entries_checked=24,
                historical_city_FUA_pairs_verified=15,original_PM_numeric_source_values_verified=0,new_PM_observations=0,current_v1_5_code_validity_verified=False,
                current_v1_5_HTTP403_bodies=2,old_Oslo_response_latest_year=2023,source_year_not_transferred_to_current_version=True,
                withdrawn_PM_points=16,other144_ranges_exact=True,utility_bound_rows_checked=320,scalar_city_scenario_weight_cases=checked,
                box_expansion_monotonicity_checked=True,contrasts=summary['contrasts'],primary_admissions=0,actual_primary_width_reduction=0,
                source_sha256={str(p.relative_to(R)):sha(p) for p in files if p.is_file()},
                scope='Historical metadata and blocked current routes separated. Information-withdrawal utility box, not pollution error range/distribution/probability or original-source finding. Core model and manuscript unchanged.')
    emit_report(report,a,O/'verification.json',G)
if __name__=='__main__':main()
