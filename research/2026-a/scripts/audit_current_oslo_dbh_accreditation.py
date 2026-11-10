"""Check named DBH/NOKUT bridges independently of the extractor's decisions."""
from pathlib import Path
from collections import Counter
from datetime import datetime
from urllib.parse import urlsplit
import csv,hashlib,html,json,re,unicodedata,zipfile
from task4_audit_output import audit_parser,check_output,emit_report
from audit_current_oslo_cost_ptr_sources import protected_inputs
R=Path(__file__).resolve().parents[1];G=R.parents[1]
D=R/'data/current_oslo_dbh_accreditation';O=R/'results/current_oslo_dbh_accreditation_review/verification.json'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def norm(s):return ' '.join(''.join(c for c in unicodedata.normalize('NFKD',s).casefold() if not unicodedata.combining(c)).split())
def host(s):return (urlsplit(s).hostname or '').casefold().removeprefix('www.')
def plain(p):
    text=re.sub(r'<(script|style)\b[^>]*>.*?</\1\s*>',' ',p.read_text(errors='replace'),flags=re.I|re.S)
    return norm(html.unescape(re.sub(r'<[^>]+>',' ',text)))
def main():
    a=audit_parser(__doc__).parse_args();check_output(a,O,G)
    receipts=read(D/'retrieval.json');assert len(receipts)==10
    assert Counter(x.get('status') for x in receipts)=={200:6,403:1,404:2,None:1}
    files={}
    for r in receipts:
        assert datetime.fromisoformat(r['requested_utc']).utcoffset() is not None
        if r.get('file') is None:
            assert r['status'] is None and r['error'];continue
        p=D/r['file'];assert sha(p)==r['sha256'] and p.stat().st_size==r['bytes'];files[p.name]=r
        if r['status']!=200:assert p.suffix=='.html' and ('http'+str(r['status'])) in p.name
    assert not list(D.glob('*.pdf'))
    national={x['display_name']:x for x in rows(R/'data/current_oslo_he_crosswalk/national_roster.csv')}
    raw=rows(R/'data/current_oslo_dbh_campus/api_662.csv')
    names={x['Institusjonskode']:x['Institusjonsnavn'] for x in raw if x['Årstall'] in ['2025','2026'] and x['Kommunenummer campus']=='0301'}
    with zipfile.ZipFile(R/'data/task4_v5_resources/ror_2026_10_06.zip') as z:ror={x['id']:x for x in json.loads(z.read('v2.14-2026-10-06-ror-data.json'))}
    cats=['Universities','Specialised Universities','University Colleges/Universitites of Applied Sciences','University Colleges with accredited study programmes']
    expected={**dict.fromkeys(['1110','1173','1175'],0),**dict.fromkeys(['1210','1220','1260','6220','8208','8221','8241'],1),
              **dict.fromkeys(['0217','1301','1303','8202','8223','8225','8234','8253'],2),**dict.fromkeys(['1401','1406','1407','1409','1413','8227','8254'],3)}
    cross=rows(D/'crosswalk.csv');assert len(cross)==len(names)==27 and {x['DBH_code'] for x in cross}==set(names)
    match={};official_only=[]
    for x in cross:
        code=x['DBH_code'];name=names[code];assert x['DBH_name']==name
        assert x['category_time_aligned']==x['complete_city_inventory_verified']=='False'
        proof=json.loads(x['identity_evidence_json'])
        if code not in expected:
            assert code in ['1404','1405'] and not proof and not x['NOKUT_name'] and not x['NOKUT_category']
            assert x['decision']=='unresolved_primary_identity_bridge';continue
        n=national[x['NOKUT_name']];assert n['category_heading']==x['NOKUT_category']==cats[expected[code]]
        assert x['NOKUT_url']==n['url'] and x['NOKUT_scope']==n['accreditation_scope'] and proof
        assert x['decision']=='archived_national_identity_match';match[code]=x
        if all(p['method']=='NOKUT_linked_official_page_exact_DBH_name' for p in proof):official_only.append(code)
        for p in proof:
            if p['method']=='exact_NOKUT_display_name':assert norm(name)==norm(n['display_name']) and p['value']==name
            elif p['method']=='same_ROR_record_name_or_official_host':
                r=ror[p['ror_id']];assert r['status']=='active' and norm(name) in {norm(y['value']) for y in r['names']}
                nn=[y['value'] for y in r['names'] if norm(y['value'])==norm(n['display_name'])]
                ss=[y['value'] for y in r['links'] if y['type']=='website' and host(y['value'])==host(n['url'])]
                assert p['NOKUT_matching_ROR_names']==nn and p['NOKUT_matching_ROR_websites']==ss and (nn or ss)
            else:
                assert p['method']=='NOKUT_linked_official_page_exact_DBH_name'
                receipt=files[p['file']];assert receipt['status']==200 and receipt['DBH_code']==code
                assert host(receipt['requested_url'])==host(receipt['final_url'])==host(n['url'])
                assert re.search(r'(?<!\w)'+re.escape(norm(name))+r'(?!\w)',plain(D/p['file']))
    assert set(match)==set(expected) and sorted(official_only)==['0217','8221','8225','8227','8254']
    summary=read(D/'summary.json');assert summary['national_identity_matches']==25 and summary['unresolved_codes']==['1404','1405']
    es=read(R/'data/current_oslo_dbh_campus/enrolment_summary.json')
    for p,s in zip(es['periods'],summary['periods']):
        positive=set(p['positive_any_mode_code_list']);verified=positive&set(match);site=set(p['positive_mode1_or4_code_list'])
        assert len(verified)==23 and positive-set(match)=={'1404','1405'}
        assert s['identity_matched_code_list']==sorted(verified)
        assert s['archived_NOKUT_categories']==dict(Counter(match[i]['NOKUT_category'] for i in verified))
        assert s['identity_only_vs_mode1or4']==sorted(verified-site) and s['mode1or4_only_vs_identity']==sorted(site-verified)
        assert len(verified-site)==len(site-verified)==2 and verified!=site
    prior=read(R/'results/current_oslo_dbh_review/verification.json')
    for n,h in prior['source_sha256'].items():assert sha(R/n)==h,n
    protected=protected_inputs();current=read(R/'results/current_paper_review/current_verification.json')
    for n,h in current['edition_source_sha256'].items():assert sha(R/n)==h,n
    paths=[*sorted(D.glob('*')),R/'data/current_oslo_he_crosswalk/national_roster.csv',R/'data/current_oslo_dbh_campus/api_662.csv',
           R/'data/current_oslo_dbh_campus/enrolment_summary.json',R/'data/task4_v5_resources/ror_2026_10_06.zip',R/'results/current_oslo_dbh_review/verification.json',Path(__file__)]
    report=dict(status='pass bounded national identity bridge review',**protected,edition_entries_checked=24,registry_codes_checked=27,national_identity_matches=25,
                unresolved_codes=['1404','1405'],positive_codes_each_period=25,identity_matches_among_positive_each_period=23,
                identity23_is_not_mode23=True,official_page_only_identity_codes=sorted(official_only),HTTP200_bodies=6,HTTP403_bodies=1,HTTP404_bodies=2,connection_without_response=1,
                failure_body_identity_admissions=0,category_time_alignment_verified=False,complete_city_inventory_verified=False,original25_lineage_verified=False,
                primary_admissions=0,actual_primary_width_reduction=0,source_sha256={str(p.relative_to(R)):sha(p) for p in paths if p.is_file()},
                scope='Named identity/category bridges only; unresolved is not ineligible; distinct same-sized code sets remain separate. Prior source definition runs, primary and manuscript preserved.')
    emit_report(report,a,O,G)
if __name__=='__main__':main()
