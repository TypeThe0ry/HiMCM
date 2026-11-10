"""Complete two provider identity bridges; keep campus geography unresolved."""
import argparse,csv,json,re,unicodedata
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
R=Path(__file__).resolve().parents[1];D=R/'data/current_oslo_he_identity_completion'

def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def read(p):return json.loads(p.read_text())
def norm(s):return ' '.join(''.join(c for c in unicodedata.normalize('NFKD',s).casefold() if not unicodedata.combining(c)).split())
def host(s):return (urlsplit(s if '://' in s else 'https://'+s).hostname or '').casefold().removeprefix('www.')
class Links(HTMLParser):
    def __init__(self):super().__init__();self.current=None;self.items=[]
    def handle_starttag(self,t,a):
        if t=='a':self.current=[dict(a).get('href',''),'']
    def handle_data(self,s):
        if self.current is not None:self.current[1]+=s
    def handle_endtag(self,t):
        if t=='a' and self.current is not None:self.items.append(self.current);self.current=None
def write(p,rr):
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rr[0]),lineterminator='\n');w.writeheader();w.writerows(rr)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,required=True)
    out=ap.parse_args().output_dir.resolve()
    if out.exists():raise FileExistsError('Use a new output directory')
    block=(D/'nokut_no.html').read_text().split('Høgskular med akkrediterte studietilbod (utan institusjonsakkreditering)',1)[1]
    block=re.search(r'<ul[^>]*>(.*?)</ul>',block,re.S)[1];links=Links();links.feed(block)
    old=rows(R/'data/current_oslo_dbh_accreditation/crosswalk.csv')
    national=rows(R/'data/current_oslo_he_crosswalk/national_roster.csv')
    campus=rows(R/'data/current_oslo_dbh_campus/oslo_campus_2025_2026.csv')
    locations=[]
    for row in old:
        code=row['DBH_code']
        if code not in ['1404','1405']:continue
        assert row['decision']=='unresolved_primary_identity_bridge'
        matches=[(u,n) for u,n in links.items if norm(n)==norm(row['DBH_name'])]
        assert len(matches)==1;url,name=matches[0]
        en=[n for n in national if host(n['url'])==host(url)];assert len(en)==1
        n=en[0];assert n['accreditation_scope']=='programme-accredited only'
        company=read(D/f'brreg_{code}.json')
        cc=[c for c in campus if c['Institusjonskode']==code]
        assert {c['Organisasjonsnr'] for c in cc}=={company['organisasjonsnummer']}
        assert host(company['hjemmeside'])==host(url)
        proof=[dict(method='NOKUT_Norwegian_exact_DBH_name_and_same_English_roster_host',
                    file='data/current_oslo_he_identity_completion/nokut_no.html',
                    Norwegian_name=name,Norwegian_url=url,English_url=n['url']),
               dict(method='DBH_organisation_number_matches_government_registry',
                    file=f'data/current_oslo_he_identity_completion/brreg_{code}.json',
                    organisation_number=company['organisasjonsnummer'],legal_name=company['navn'])]
        row.update(NOKUT_name=n['display_name'],NOKUT_category=n['category_heading'],
                   NOKUT_scope=n['accreditation_scope'],NOKUT_url=n['url'],
                   identity_evidence_json=json.dumps(proof,ensure_ascii=False),
                   decision='archived_national_identity_match')
        address=company['forretningsadresse'];municipalities=sorted({c['Kommunenummer campus'] for c in cc})
        locations.append(dict(DBH_code=code,organisation_number=company['organisasjonsnummer'],
            DBH_campus_municipalities=json.dumps(municipalities),
            registry_business_municipality=address['kommunenummer'],
            registry_business_municipality_name=address['kommune'],
            registry_business_postplace=address['poststed'],
            address_vs_campus_discrepancy=address['kommunenummer'] not in municipalities,
            decision='flag_only_no_city_exclusion'))
    assert len(old)==27 and all(x['decision']=='archived_national_identity_match' for x in old)
    periods=[]
    for p in read(R/'data/current_oslo_dbh_campus/enrolment_summary.json')['periods']:
        ids=p['positive_any_mode_code_list'];assert len(ids)==25
        assert set(ids)<={x['DBH_code'] for x in old}
        periods.append(dict(year=p['year'],semester=p['semester'],positive_codes=25,
                            identity_matches=25,teaching_mode1_or4_codes=p['positive_mode1_or4_codes']))
    summary=dict(registry_codes=27,previous_identity_matches=25,national_identity_matches=27,
        newly_bridged_codes=['1404','1405'],unresolved_identity_codes=[],periods=periods,
        inherited25_identity_proof_base='data/current_oslo_dbh_accreditation',
        category_scope='Inherited25 archived English roster bridges plus two current Norwegian roster bridges; not historical semester accreditation certification',
        location_discrepancy_codes=['1405'],automatic_city_exclusions=0,
        original25_lineage_verified=False,complete_city_inventory_verified=False,
        category_time_alignment_verified=False,primary_admissions=0,
        actual_primary_width_reduction=0,changes_primary_model=False,changes_manuscript=False)
    out.mkdir(parents=True);write(out/'crosswalk.csv',old);write(out/'location_flags.csv',locations)
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ['national_identity_matches','newly_bridged_codes',
                                           'location_discrepancy_codes','primary_admissions']}))
if __name__=='__main__':main()
