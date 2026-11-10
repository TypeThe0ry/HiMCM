"""Extract the correct employer panel; retain approximation and scope limits."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re,subprocess,xml.etree.ElementTree as ET
D=Path(__file__).resolve().parent;R=D.parents[1];H=R/'data/current_helsinki_teacher_metadata'
class Text(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.skip=0
    def handle_starttag(self,t,a):
        if t in ['script','style']:self.skip+=1
    def handle_endtag(self,t):
        if t in ['script','style']:self.skip=max(0,self.skip-1)
    def handle_data(self,s):
        if not self.skip:self.parts.append(s)
def plain(p):
    t=Text();t.feed(p.read_text());return ' '.join(' '.join(t.parts).split())
def main():
    pdf=D/'annual2024.pdf';assert pdf.read_bytes().startswith(b'%PDF')
    raw=subprocess.run(['/usr/bin/pdftotext','-f','10','-l','10','-bbox-layout',str(pdf),'-'],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
    page=ET.fromstring(raw).find('.//{*}page');width=float(page.get('width'))
    left=[w for w in page.findall('.//{*}word') if float(w.get('xMax'))<width/2]
    text=' '.join(w.text or '' for w in left)
    assert 'Wirtschaftsschule KV Zürich' in text and '8. Anzahl Vollzeitstellen' in text
    teacher=re.search(r'~(\d+) Vollzeitstellen bei (\d+) Lehrpersonen, davon (\d+) Lehrpersonen im Vollzeitmodus',text)
    admin=re.search(r'~(\d+) Vollzeitstellen bei (\d+) Mitarbeitenden der Verwaltung, davon (\d+) Mitarbeitende im Vollzeitmodus',text)
    assert teacher and admin
    assert tuple(map(int,teacher.groups()))==(134,185,42) and tuple(map(int,admin.groups()))==(32,40,16)
    assert 'Im Durchschnitt' in text and 'die 166 Vollzeitstellen besetzen' in text
    assert 'zirka 225 Personen' in text
    scope=dict(source='Kaufmännischer Verband Zürich annual report2024',employer='Wirtschaftsschule KV Zürich',
               source_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),PDF_physical_page=10,printed_page=18,
               spread_width_points=width,selected_region='left panel xMax<spread_width/2; right KV Business School panel excluded',
               report_year=2024,exact_observation_date=None,source_reporting_basis='Average occupied full-time positions; publisher says Im Durchschnitt; exact averaging window/method not supplied here',
               teacher_fulltime_positions_approx=134,teacher_people=185,teacher_fulltime_mode_people=42,
               administration_fulltime_positions_approx=32,administration_people=40,administration_fulltime_mode_people=16,
               total_fulltime_positions_displayed=166,total_people_approx=225,
               approximation_sign_preserved=True,published_approximation_error_bound=None,
               normal_contract_teacher_FTE_permitted=True,contact_hours_conversion_required=False,
               all_2024_teaching_stage_allocation_verified=False,all_2024_school_sites_verified=False,
               whole_city_provider_coverage_verified=False,matched_pupil_count_obtained=False,
               forty_two_fulltime_people_converted_to_FTE=False,approx134_admitted_as_hard_lower_bound=False,
               target_utility=[0,1],primary_admissions=0,actual_primary_width_reduction=0,
               decision='Retain approximate occupied-position evidence, do not construct city ratio or guaranteed bound')
    (D/'scope.json').write_text(json.dumps(scope,ensure_ascii=False,indent=2)+'\n')
    guide=R/'data/task4_v184_helsinki_teacher/oph_teachers_original.html';g=plain(guide)
    assert 'Viimeisimmät Opettaja-tiedonkeruun pohjalta tehdyt tilastotiedot ovat vuodelta 2019.' in g
    catalogue=plain(H/'oph_report_catalogue.html')
    section=re.search(r'Lukiokoulutus Vipusen kuukausittain.*?(?=Takaisin ylös Ammatillinen koulutus)',catalogue)
    assert section and 'Opiskelijat ja ylioppilastutkinnon suorittaneet' in section[0] and 'Suoritetut opinnot' in section[0]
    hs=dict(archived_teacher_guide='data/task4_v184_helsinki_teacher/oph_teachers_original.html',
            archived_guide_sha256=hashlib.sha256(guide.read_bytes()).hexdigest(),latest_collection_year_stated_in_archived_guide=2019,
            new_teacher_collection_observation=False,catalogue_checked='General-upper-secondary section links student, matriculation and completed-study reports',
            compatible_teaching_FTE_table_found=False,all_Vipunen_tables_exhaustively_reviewed=False,
            legacy_StatFin_metadata_request_status=403,legacy_discontinuation_year_admitted=False,
            target_utility=[0,1],primary_admissions=0,actual_primary_width_reduction=0,
            decision='Reuse existing2019scope evidence, skip blocked legacy route; no pupil/headcount conversion')
    (H/'scope.json').write_text(json.dumps(hs,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(Zurich_approx_teacher_positions=134,Helsinki_new_FTE=False,primary_admissions=0)))
if __name__=='__main__':main()
