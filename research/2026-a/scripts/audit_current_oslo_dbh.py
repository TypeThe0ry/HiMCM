"""Independent DBH source joins and scalar Oslo count-definition sensitivity."""
from pathlib import Path
from collections import Counter
from datetime import datetime
import csv,hashlib,json,math
from task4_audit_output import audit_parser,check_output,emit_report
from audit_current_oslo_cost_ptr_sources import protected_inputs
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES
R=Path(__file__).resolve().parents[1];G=R.parents[1]
D=R/'data/current_oslo_dbh_campus';O=R/'results/current_oslo_dbh_review'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p,sep=','):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=sep))
def key(x):return tuple(x[k] for k in ['Årstall','Semester','Institusjonskode','Stedkode campus'])
def close(a,b):assert math.isclose(float(a),float(b),rel_tol=0,abs_tol=2e-11),(a,b)
def scalar(u,w):
    a=math.sqrt(math.fsum(v*x*x for v,x in zip(w,u)))
    b=math.sqrt(math.fsum(v*(1-x)*(1-x) for v,x in zip(w,u)))
    return 100*a/(a+b)
def main():
    a=audit_parser(__doc__).parse_args();check_output(a,O/'verification.json',G)
    receipt=read(D/'retrieval.json');assert len(receipt)==8
    assert Counter(x['status'] for x in receipt)=={403:4,200:4}
    for r in receipt:
        assert sha(D/r['file'])==r['sha256'] and (D/r['file']).stat().st_size==r['bytes']
        assert datetime.fromisoformat(r['requested_utc']).utcoffset() is not None
    post=next(x for x in receipt if x.get('method')=='POST')
    assert post['public_unauthenticated'] and post['status']==200
    payload=(D/post['request_file']).read_bytes();assert payload.endswith(b'\n')
    assert hashlib.sha256(payload[:-1]).hexdigest()==post['request_body_sha256']
    q=json.loads(payload);assert q['tabell_id']==124
    assert {x['variabel']:x['selection']['values'] for x in q['filter']}=={'Årstall':['2025','2026'],'Semester':['1','3'],'Kommunenummer campus':['0301']}
    meta=rows(D/'api_002.csv');institutions=rows(D/'api_211.csv');campus=rows(D/'api_662.csv')
    assert [len(meta),len(institutions),len(campus)]==[1206,293,3698]
    assert len({x['Institusjonskode'] for x in institutions})==293
    assert next(x for x in meta if x['Tabell id']=='124' and x['Variabel navn']=='Antall')['GDPR']=='1'
    lookup={key(x):x for x in campus};assert len(lookup)==3698
    selected=[x for x in campus if x['Årstall'] in ['2025','2026'] and x['Semester'] in ['1','3'] and x['Kommunenummer campus']=='0301']
    derived=rows(D/'oslo_campus_2025_2026.csv');assert len(derived)==len(selected)==146
    assert [key(x) for x in derived]==[key(x) for x in selected]
    for raw,saved in zip(selected,derived):
        assert all(saved[k]==v for k,v in raw.items())
        assert json.loads(saved['institution_metadata_candidates_json'])==[x for x in institutions if x['Institusjonskode']==raw['Institusjonskode']]
    enrol=rows(D/'enrolment_response.csv',';');classified=rows(D/'enrolment_classified.csv')
    assert len(enrol)==len(classified)==203
    e_summary=read(D/'enrolment_summary.json')
    for raw,saved in zip(enrol,classified):
        assert all(saved[k]==v for k,v in raw.items())
        assert raw['Kommunenummer campus']=='0301' and lookup[key(raw)]['Kommunenummer campus']=='0301'
        assert saved['registry_key_match']=='True'
        assert saved['positive_public_value']==str(int(raw['Antall'])>0)
        assert saved['institution_or_study_site_mode']==str(raw['Organisering_kode'] in ['1','4'])
    periods=[('2025','1'),('2025','3'),('2026','1'),('2026','3')]
    counts=[]
    for k,(year,sem) in enumerate(periods):
        cr=[x for x in selected if (x['Årstall'],x['Semester'])==(year,sem)]
        er=[x for x in enrol if (x['Årstall'],x['Semester'])==(year,sem)]
        registry={x['Institusjonskode'] for x in cr};returned={x['Institusjonskode'] for x in er}
        positive={x['Institusjonskode'] for x in er if int(x['Antall'])>0}
        site={x['Institusjonskode'] for x in er if int(x['Antall'])>0 and x['Organisering_kode'] in ['1','4']}
        assert (len(cr),len(registry),len(er),len(positive),len(site))==([35,36,37,38][k],[26,26,26,27][k],[46,46,56,55][k],25,23)
        assert registry-returned=={'0217'}
        p=e_summary['periods'][k]
        for field,value in [('campus_registry_rows',len(cr)),('registry_distinct_institution_codes',len(registry)),('enrolment_rows',len(er)),('returned_institution_codes',len(returned)),('positive_any_mode_codes',25),('positive_mode1_or4_codes',23)]:assert p[field]==value
        assert p['positive_any_mode_code_list']==sorted(positive) and p['positive_mode1_or4_code_list']==sorted(site)
        assert p['registry_codes_not_returned']==['0217'];counts.append([len(cr),len(registry),len(er),25,23])
    assert {x['Organisering'] for x in enrol if x['Organisering_kode']=='1'}=={'Undervisning ved institusjonen'}
    assert {x['Organisering'] for x in enrol if x['Organisering_kode']=='4'}=={'Undervisning ved studiested (ny)'}
    assert sum(x['Årstall']=='2026' and x['Organisering_kode']=='1' for x in enrol)==2
    summary=read(O/'summary.json');bounds=rows(O/'bounds.csv');ranks=rows(O/'ranks.csv')
    for n,h in summary['source_sha256'].items():assert sha(R/n)==h,n
    for n,h in summary['output_sha256'].items():assert sha(O/n)==h,n
    for n,h in e_summary['source_sha256'].items():assert sha(D/n)==h,n
    campus_summary=read(D/'summary.json')
    for n,item in campus_summary['source_tables'].items():assert sha(D/n)==item['sha256']
    f,lo,hi=revised_bounds();cities=f.city.tolist();oslo=cities.index('Oslo');he=NAMES.index('research_he_density')
    assert len(bounds)==800 and len(ranks)==160 and len(summary['cases'])==10
    densities={23:31.6,25:34.4,26:35.7,27:37.1};independent={};checked=0
    for scenario in ['retained_V203']+[f'DBH_code_count_{n}' for n in densities]:
        n=None if scenario=='retained_V203' else int(scenario.rsplit('_',1)[-1]);ll=lo.tolist();hh=hi.tolist()
        if n is not None:
            close(densities[n],round(n/727797*1e6,1));value=densities[n]/10
            ll[oslo][he]=hh[oslo][he]=value/(1+value)
        if n==25:assert ll==lo.tolist() and hh==hi.tolist()
        saved={(x['city'],x['indicator']):x for x in bounds if x['scenario']==scenario};assert len(saved)==160
        for i,c in enumerate(cities):
            for j,name in enumerate(NAMES):close(saved[c,name]['lower'],ll[i][j]);close(saved[c,name]['upper'],hh[i][j])
        for ref in ['fixed','equal']:
            w=[.1]*10 if ref=='equal' else [.05 if j in [6,9] else .1125 for j in range(10)]
            lower=[scalar(x,w) for x in ll];upper=[scalar(x,w) for x in hh]
            regrets=[max(0,max(upper[k] for k in range(16) if k!=i)-lower[i]) for i in range(16)]
            ranks_expected=[1+sum(x<r-1e-10 for x in regrets) for r in regrets]
            table={x['city']:x for x in ranks if x['scenario']==scenario and x['weight_reference']==ref};assert len(table)==16
            for i,c in enumerate(cities):
                row=table[c]
                for name,value in [('score_lower',lower[i]),('score_upper',upper[i]),('max_regret',regrets[i])]:close(row[name],value)
                assert int(row['decision_rank'])==ranks_expected[i]
                possible=upper[i]>=max(lower[k] for k in range(16) if k!=i)-1e-12
                necessary=lower[i]>=max(upper[k] for k in range(16) if k!=i)-1e-12
                assert row['possible_champion']==str(possible)=='True' and row['necessary_champion']==str(necessary)=='False'
                assert int(row['best_rank'])==1+sum(lower[k]>upper[i]+1e-12 for k in range(16) if k!=i)
                assert int(row['worst_rank'])==1+sum(upper[k]>lower[i]+1e-12 for k in range(16) if k!=i)
                checked+=1
            case=next(x for x in summary['cases'] if (x['scenario'],x['weight_reference'])==(scenario,ref))
            choices=[cities[i] for i,x in enumerate(regrets) if x<=min(regrets)+1e-12]
            assert case['recommendations']==choices==(['Oslo'] if ref=='fixed' or n in [26,27] else ['Zurich'])
            assert case['possible_champions']==16 and case['necessary_champions']==0
            close(case['mean_width'],math.fsum(b-a for a,b in zip(lower,upper))/16)
            for field,value in [('Oslo_lower',lower[oslo]),('Oslo_upper',upper[oslo]),('Oslo_regret',regrets[oslo]),('Oslo_rank',ranks_expected[oslo])]:close(case[field],value)
            independent[scenario,ref]=(ranks_expected,case)
    for c in summary['contrasts']:
        rank,case=independent[c['scenario'],c['weight_reference']];base_rank,base=independent['retained_V203',c['weight_reference']]
        assert c['decision_rank_changes']==sum(a!=b for a,b in zip(rank,base_rank))
        assert c['recommendation_changed']==(case['recommendations']!=base['recommendations'])
        for name,field in [('Oslo_lower_change','Oslo_lower'),('Oslo_upper_change','Oslo_upper'),('mean_width_change','mean_width')]:close(c[name],case[field]-base[field])
    protected=protected_inputs();current=read(R/'results/current_paper_review/current_verification.json')
    for n,h in current['edition_source_sha256'].items():assert sha(R/n)==h,n
    files=[*sorted(D.glob('*')),*[O/n for n in ['README.md','summary.json','bounds.csv','ranks.csv','peer_review.json']],R/'scripts/task4_current_oslo_he_definition.py',Path(__file__)]
    report=dict(status='pass scoped DBH source and scalar definition review',**protected,edition_entries_checked=24,
                HTTP200_bodies=4,HTTP403_error_bodies=4,campus_rows_checked=146,enrolment_rows_checked=203,
                period_counts=counts,utility_bound_rows_checked=800,scalar_city_scenario_weight_cases=checked,
                count25_exactly_reproduces_primary=True,all_other159_ranges_preserved=True,
                contrasts=summary['contrasts'],municipal_provider_inventory_verified=False,original25_lineage_verified=False,
                primary_admissions=0,actual_primary_width_reduction=0,
                source_sha256={str(p.relative_to(R)):sha(p) for p in files if p.is_file()},
                scope='Visible public DBH code counts and one-point definition scenarios; no true-provider bounds, exact student counts, model replacement, future trend or manuscript change.')
    emit_report(report,a,O/'verification.json',G)
if __name__=='__main__':main()
