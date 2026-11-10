"""Check identity completion without certifying a municipal provider census."""
import csv,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
from task4_audit_output import audit_parser,check_output,emit_report
from audit_current_oslo_cost_ptr_sources import protected_inputs
R=Path(__file__).resolve().parents[1];G=R.parents[1]
D=R/'data/current_oslo_he_identity_completion';O=R/'results/current_oslo_he_identity_completion'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def main():
    a=audit_parser(__doc__).parse_args();canonical=O/'verification.json';check_output(a,canonical,G)
    protection=protected_inputs();receipts=list(D.glob('*.receipt.json'));assert len(receipts)==5
    for p in receipts:
        m=read(p);body=D/p.name.removesuffix('.receipt.json')
        assert m['status']==200 and sha(body)==m['sha256'] and body.stat().st_size==m['bytes']
    prior=read(R/'results/current_oslo_dbh_accreditation_review/verification.json')
    assert prior['national_identity_matches']==25
    for n,h in prior['source_sha256'].items():assert sha(R/n)==h
    old={r['DBH_code']:r for r in rows(R/'data/current_oslo_dbh_accreditation/crosswalk.csv')}
    new={r['DBH_code']:r for r in rows(O/'crosswalk.csv')};assert old.keys()==new.keys() and len(new)==27
    for code in set(old)-{'1404','1405'}:assert old[code]==new[code],code
    html=(D/'nokut_no.html').read_text()
    section=html.split('Høgskular med akkrediterte studietilbod (utan institusjonsakkreditering)',1)[1].split('</ul>',1)[0]
    campus=rows(R/'data/current_oslo_dbh_campus/oslo_campus_2025_2026.csv')
    for code,name,org,domain in [('1404','NSKI Høyskole','993396486','nski.no'),
                                 ('1405','Norsk Gestaltinstitutt','977266718','gestalt.no')]:
        assert re.search(r'<a\b[^>]*href="https?://(?:www\.)?'+re.escape(domain)+r'/"[^>]*>'+re.escape(name)+r'</a>',section)
        company=read(D/f'brreg_{code}.json')
        assert company['organisasjonsnummer']==org
        assert company['hjemmeside'].removeprefix('www.')==domain
        assert {r['Organisasjonsnr'] for r in campus if r['Institusjonskode']==code}=={org}
        assert new[code]['DBH_name']==name and new[code]['NOKUT_scope']=='programme-accredited only'
        assert new[code]['category_time_aligned']==new[code]['complete_city_inventory_verified']=='False'
    s=read(O/'summary.json')
    assert s['national_identity_matches']==27 and s['unresolved_identity_codes']==[]
    assert [p['identity_matches'] for p in s['periods']]==[25]*4
    assert not s['original25_lineage_verified'] and not s['complete_city_inventory_verified']
    flags={r['DBH_code']:r for r in rows(O/'location_flags.csv')}
    assert flags['1404']['registry_business_municipality']=='0301'
    assert flags['1405']['registry_business_municipality']=='3201'
    assert flags['1405']['address_vs_campus_discrepancy']=='True'
    assert json.loads(flags['1405']['DBH_campus_municipalities'])==['0301']
    pdf=D/'ngi_2024.pdf';assert pdf.read_bytes().startswith(b'%PDF')
    text=subprocess.check_output(['/usr/bin/pdftotext','-f','7','-l','7','-layout',str(pdf),'-'],text=True)
    assert 'Høyskolen holder til i Sandvika i Bærum kommune.' in ' '.join(text.split())
    course=(D/'ngi_course.html').read_text()
    assert 'Studiested' in course and 'Kjørbokollen' in course and 'Sandvika' in course
    with tempfile.TemporaryDirectory(prefix='himcm-he-identity-',dir='/data/scratch') as tmp:
        dest=Path(tmp)/'replay'
        subprocess.run([sys.executable,str(R/'scripts/task4_current_oslo_he_identity_completion.py'),
                        '--output-dir',str(dest)],check=True,stdout=subprocess.PIPE)
        for n in ['summary.json','crosswalk.csv','location_flags.csv']:assert (O/n).read_bytes()==(dest/n).read_bytes()
    assert protected_inputs()==protection
    paper=read(R/'results/current_paper_review/current_verification.json')
    for n,h in paper['edition_source_sha256'].items():assert sha(R/n)==h
    sources=[*sorted(D.iterdir()),O/'summary.json',O/'crosswalk.csv',O/'location_flags.csv',O/'README.md',
             R/'data/current_oslo_dbh_accreditation/crosswalk.csv',
             R/'results/current_oslo_dbh_accreditation_review/verification.json',
             R/'data/current_oslo_he_crosswalk/national_roster.csv',
             R/'data/current_oslo_dbh_campus/oslo_campus_2025_2026.csv',
             R/'data/current_oslo_dbh_campus/enrolment_summary.json',Path(__file__),
             R/'scripts/task4_current_oslo_he_identity_completion.py',
             R/'scripts/audit_current_oslo_cost_ptr_sources.py',R/'scripts/task4_audit_output.py']
    report=dict(status='pass bounded identity completion and location scope',**protection,
        edition_entries_checked=24,HTTP200_bodies=5,registry_codes_checked=27,
        national_identity_matches=27,inherited_rows_preserved=25,newly_bridged_codes=['1404','1405'],
        identity_matches_among_positive_each_period=25,programme_only_new_identities=True,
        address_discrepancy_codes=['1405'],PDF_location_physical_page=7,
        original25_lineage_verified=False,city_count_corrected=False,
        output_files_bytewise_reproduced=3,primary_admissions=0,actual_primary_width_reduction=0,
        changes_primary_model=False,changes_manuscript=False,
        source_sha256={str(p.relative_to(R)):sha(p) for p in sources if p.is_file()},
        scope='Combined-archive provider identities; current business and course/2024 report geography flag, not historical accreditation, complete Oslo locations, original25 roster or count correction.')
    emit_report(report,a,canonical,G)
if __name__=='__main__':main()
