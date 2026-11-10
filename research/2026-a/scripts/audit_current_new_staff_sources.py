"""Bounded source checks for Zurich employer positions and Helsinki metadata."""
from pathlib import Path
from collections import Counter
from datetime import datetime
from html.parser import HTMLParser
import hashlib,json,re,subprocess
from task4_audit_output import audit_parser,check_output,emit_report
from audit_current_oslo_cost_ptr_sources import protected_inputs
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES
R=Path(__file__).resolve().parents[1];G=R.parents[1]
D=R/'data/current_zurich_kv_staff';H=R/'data/current_helsinki_teacher_metadata'
O=R/'results/current_new_staff_sources/verification.json'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class Text(HTMLParser):
    def __init__(self):super().__init__();self.p=[];self.skip=0
    def handle_starttag(self,t,a):
        if t in ['script','style']:self.skip+=1
    def handle_endtag(self,t):
        if t in ['script','style']:self.skip=max(0,self.skip-1)
    def handle_data(self,s):
        if not self.skip:self.p.append(s)
def plain(p):
    t=Text();t.feed(p.read_text());return ' '.join(' '.join(t.p).split())
def main():
    a=audit_parser(__doc__).parse_args();check_output(a,O,G)
    statuses=[]
    for directory in [D,H]:
        for r in read(directory/'retrieval.json'):
            p=directory/r['file'];assert sha(p)==r['sha256'] and p.stat().st_size==r['bytes']
            assert datetime.fromisoformat(r['requested_utc']).utcoffset() is not None;statuses.append(r['status'])
    assert Counter(statuses)=={200:2,403:3}
    pdf=D/'annual2024.pdf';assert pdf.read_bytes().startswith(b'%PDF') and pdf.stat().st_size==15401309
    cropped=subprocess.run(['/usr/bin/pdftotext','-f','10','-l','10','-r','72','-x','0','-y','0','-W','638','-H','842',str(pdf),'-'],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.decode()
    cropped=' '.join(cropped.split());assert 'Wirtschaftsschule KV Zürich' in cropped and 'KV Business School Zürich' not in cropped
    assert re.search(r'~134 Vollzeitstellen bei 185 Lehrpersonen, davon 42 Lehrpersonen im Vollzeitmodus',cropped)
    assert re.search(r'~32 Vollzeitstellen bei 40 Mitarbeitenden der Verwaltung, davon 16 Mitarbeitende im Vollzeitmodus',cropped)
    assert 'Im Durchschnitt' in cropped and 'die 166 Vollzeitstellen besetzen' in cropped and 'zirka 225 Personen' in cropped
    s=read(D/'scope.json');assert s['source_sha256']==sha(pdf)
    assert s['PDF_physical_page']==10 and s['printed_page']==18 and s['employer']=='Wirtschaftsschule KV Zürich'
    assert [s[k] for k in ['teacher_fulltime_positions_approx','teacher_people','teacher_fulltime_mode_people','administration_fulltime_positions_approx','administration_people','administration_fulltime_mode_people']]==[134,185,42,32,40,16]
    assert s['approximation_sign_preserved'] and s['published_approximation_error_bound'] is None and s['exact_observation_date'] is None
    assert s['normal_contract_teacher_FTE_permitted'] and not s['contact_hours_conversion_required']
    assert not s['all_2024_teaching_stage_allocation_verified'] and not s['all_2024_school_sites_verified']
    assert not s['forty_two_fulltime_people_converted_to_FTE'] and not s['approx134_admitted_as_hard_lower_bound']
    hs=read(H/'scope.json');guide=R/hs['archived_teacher_guide'];assert sha(guide)==hs['archived_guide_sha256']
    assert 'Viimeisimmät Opettaja-tiedonkeruun pohjalta tehdyt tilastotiedot ovat vuodelta 2019.' in plain(guide)
    assert hs['latest_collection_year_stated_in_archived_guide']==2019 and not hs['new_teacher_collection_observation']
    catalogue=plain(H/'oph_report_catalogue.html')
    section=re.search(r'Lukiokoulutus Vipusen kuukausittain.*?(?=Takaisin ylös Ammatillinen koulutus)',catalogue)[0]
    assert 'Opiskelijat ja ylioppilastutkinnon suorittaneet' in section and 'Suoritetut opinnot' in section
    assert hs['legacy_StatFin_metadata_request_status']==403 and not hs['legacy_discontinuation_year_admitted']
    assert not hs['all_Vipunen_tables_exhaustively_reviewed'] and not hs['compatible_teaching_FTE_table_found']
    f,lo,hi=revised_bounds();j=NAMES.index('upper_secondary_ptr')
    for city,scope in [('Zurich',s),('Helsinki',hs)]:
        i=f.city.tolist().index(city);assert [float(lo[i,j]),float(hi[i,j])]==scope['target_utility']==[0,1]
        assert scope['primary_admissions']==scope['actual_primary_width_reduction']==0
    protected=protected_inputs();current=read(R/'results/current_paper_review/current_verification.json')
    for n,h in current['edition_source_sha256'].items():assert sha(R/n)==h,n
    paths=[*sorted(D.glob('*')),*sorted(H.glob('*')),guide,Path(__file__),R/'scripts/task4_audit_output.py',R/'scripts/audit_current_oslo_cost_ptr_sources.py']
    report=dict(status='pass bounded teacher-source scope review',**protected,edition_entries_checked=24,new_HTTP200_bodies=2,new_HTTP403_bodies=3,
                primary_source_employer='Wirtschaftsschule KV Zürich',PDF_physical_page=10,printed_page=18,
                approximate_teacher_fulltime_positions=134,teacher_people=185,fulltime_mode_people=42,
                root_visual_review='Source spread10 viewed; left printed18teacher/admin block belongs to Wirtschaftsschule, not right printed19KV Business School',
                independent_text_reader='Fixed left-panel crop versus extractor bounding-box selection',
                Helsinki2019_scope_reused_from_existing_archive=True,failed_response_facts_admitted=0,
                hard_teacher_lower_bound_constructed=False,primary_admissions=0,actual_primary_width_reduction=0,
                source_sha256={str(p.relative_to(R)):sha(p) for p in paths if p.is_file()},
                scope='Approximate average occupied teacher positions retained as a primary source lead; exact approximation, historical stage/site and pupil alignment unverified. Normal contract FTE allowed without contact-hours conversion. No city ratio, bounds change, model or manuscript update.')
    emit_report(report,a,O,G)
if __name__=='__main__':main()
