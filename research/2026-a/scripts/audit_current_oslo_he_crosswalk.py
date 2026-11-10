"""Independent archived NOKUT roster, Oslo identity and role-source checks."""
from pathlib import Path
from collections import Counter
from datetime import datetime
from urllib.parse import urlsplit
import csv, hashlib, html, json, re, unicodedata, zipfile
from task4_audit_output import audit_parser,check_output,emit_report
from audit_current_oslo_cost_ptr_sources import protected_inputs,plain_text

R=Path(__file__).resolve().parents[1];G=R.parents[1]
D=R/'data/current_oslo_he_crosswalk';S=R/'data/current_oslo_he_scope'
O=R/'results/current_oslo_he_crosswalk_review/verification.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def rows(p):
    with p.open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def clean(s):return ' '.join(html.unescape(re.sub('<[^>]+>','',s)).split())
def norm(s):return ' '.join(''.join(c for c in unicodedata.normalize('NFKD',s).casefold() if not unicodedata.combining(c)).split())
def host(s):return (urlsplit(s).hostname or '').casefold().removeprefix('www.')

def main():
    a=audit_parser(__doc__).parse_args();check_output(a,O,G)
    receipts=read(S/'retrieval_metadata.json')['records']
    for r in receipts:assert sha(S/r['file'])==r['sha256'] and (S/r['file']).stat().st_size==r['bytes']
    assert sha(S/'nokut_institutions.html')=='4590fa854abdce56f291c371b715cc0245b22f4972244249427382491623efe1'
    categories=['Universities','Specialised Universities','University Colleges/Universitites of Applied Sciences','University Colleges with accredited study programmes']
    parsed=[]
    for block in re.split(r'<a href="#collapsibleContent_[^"]+"[^>]*>',(S/'nokut_institutions.html').read_text())[1:]:
        category=clean(block.split('</a>')[0])
        if category not in categories:continue
        for attrs,label in re.findall(r'<li><a\b([^>]*)>(.*?)</a>',block,re.S):
            url=html.unescape(re.search(r'href="([^"]+)"',attrs)[1])
            parsed.append((category,clean(label),url))
    national=rows(D/'national_roster.csv')
    assert [(x['category_heading'],x['display_name'],x['url']) for x in national]==parsed
    assert [sum(x[0]==c for x in parsed) for c in categories]==[11,9,15,13]
    assert len(parsed)==48
    assert 'without institutional accreditation' in plain_text(S/'nokut_institutions.html')
    old=read(S/'scope.json')['national_snapshot'];assert old['institutions']==49 and old['categories']==[11,9,15,14]
    archive=R/'data/task4_v5_resources/ror_2026_10_06.zip'
    assert sha(archive)=='555b38a4b586759de1fa278b0e751433a13dd541f375097db53b186cfcdc768a'
    with zipfile.ZipFile(archive) as z:records=json.loads(z.read('v2.14-2026-10-06-ror-data.json'))
    oslo={r['id']:r for r in records if r['status']=='active' and 'education' in r['types'] and any(l['geonames_id']==3143244 and l['geonames_details']['country_code']=='NO' for l in r['locations'])}
    cross=rows(D/'oslo_crosswalk.csv');assert len(cross)==len(oslo)==28 and {x['ror_id'] for x in cross}==set(oslo)
    expected={
        '04q12yn84':0,'01xtthb56':0,
        '01qafy255':1,'052dy9793':1,'0543h9a62':1,'045016w83':1,'04a7x2s11':1,'0191b3351':1,'03ez40v33':1,
        '00kxk0k30':2,'026eeyk15':2,'015rzvz05':2,'05486d596':2,'03gss5916':2,'02vfz9j23':2,
        '030xrgd02':3}
    methods=Counter()
    for x in cross:
        r=oslo[x['ror_id']];rid=x['ror_id'].rsplit('/',1)[-1]
        assert x['ror_display']==next(n['value'] for n in r['names'] if 'ror_display' in n['types'])
        assert x['city_inventory_scope_verified']=='False'
        candidates=[]
        for n in national:
            names=[y['value'] for y in r['names'] if norm(y['value'])==norm(n['display_name'])]
            sites=[y['value'] for y in r['links'] if y['type']=='website' and host(y['value'])==host(n['url'])]
            if names or sites:candidates.append((n,names,sites))
        assert len(candidates)<=1
        if rid not in expected:
            assert not candidates and not x['identity_match_basis'] and not x['nokut_name']
            assert x['decision']=='no_match_under_declared_identity_rules';continue
        assert len(candidates)==1
        n,names,sites=candidates[0]
        assert x['nokut_category']==n['category_heading']==categories[expected[rid]]
        assert x['nokut_name']==n['display_name'] and x['nokut_url']==n['url']
        assert json.loads(x['matching_ROR_names'])==names and json.loads(x['matching_ROR_websites'])==sites
        assert x['identity_match_basis']==';'.join((['exact_ROR_name'] if names else [])+(['same_official_website_host'] if sites else []))
        assert x['decision']=='national_identity_match_only'
        scope='programme-accredited only' if expected[rid]==3 else 'institutionally accredited'
        assert x['nokut_accreditation_scope']==n['accreditation_scope']==scope
        methods[x['identity_match_basis']]+=1
    role=read(D/'role_retrieval.json');assert len(role)==3
    for r in role:
        assert r['status']==200 and sha(D/r['file'])==r['sha256'] and (D/r['file']).stat().st_size==r['bytes']
        assert datetime.fromisoformat(r['requested_utc']).utcoffset() is not None
    assert 'interest organisation' in plain_text(D/'uhr_role.html') and 'cooperative body' in plain_text(D/'uhr_role.html')
    assert 'Nobel Committee secretariat' in plain_text(D/'nobel_role.html')
    assert 'sosial entreprenør' in plain_text(D/'forskerfabrikken_role.html') and 'barn' in plain_text(D/'forskerfabrikken_role.html')
    protected=protected_inputs();current=read(R/'results/current_paper_review/current_verification.json')
    for n,h in current['edition_source_sha256'].items():assert sha(R/n)==h,n
    prior=read(R/'results/current_all16_ror_review/verification.json')
    for n,h in prior['source_sha256'].items():assert sha(R/n)==h,n
    sources=[archive,*sorted(S.glob('*')),*sorted(D.glob('*')),Path(__file__)]
    report=dict(status='pass bounded identity and source-role review',**protected,edition_entries_checked=24,
                national_roster_entries=48,national_category_counts=[11,9,15,13],separate_January2026_national_total=49,
                ROR_Oslo_label_records=28,national_identity_matches=16,institutionally_accredited_category_matches=15,
                programme_only_category_matches=1,unmatched_by_declared_rules=12,identity_method_counts=dict(methods),
                new_official_HTTP200_bodies=3,municipal_HE_inventory_verified=False,original25_lineage_verified=False,
                primary_admissions=0,actual_primary_width_reduction=0,
                source_sha256={str(p.relative_to(R)):sha(p) for p in sources if p.is_file()},
                scope='Named national identities and explicit source roles, not an Oslo accredited-provider count. No inference of ineligibility from unmatched names, no deduplication, no primary or manuscript change.')
    emit_report(report,a,O,G)

if __name__=='__main__':main()
