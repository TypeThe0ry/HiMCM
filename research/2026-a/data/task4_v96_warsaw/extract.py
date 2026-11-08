"""Official Warsaw yearbook school-route/FTE bounds; no main-model mutation."""
import hashlib,io,json,xml.etree.ElementTree as ET,zipfile
from pathlib import Path
from pypdf import PdfReader
P=Path(__file__).resolve().parent
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def extract():
 for m in json.loads((P/'manifest.json').read_text()):
  b=(P/m['file']).read_bytes();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
 outer=zipfile.ZipFile(P/'yearbook2025_excel.zip');assert outer.testzip() is None
 member=next(n for n in outer.namelist() if n.endswith('/08_Edukacja.xlsx'))
 b=outer.read(member);assert b==(P/'education2025.xlsx').read_bytes()
 z=zipfile.ZipFile(io.BytesIO(b));assert z.testzip() is None
 strings=[''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml'))]
 def sheet(k):
  out={}
  for row in ET.fromstring(z.read(f'xl/worksheets/sheet{k}.xml')).find('s:sheetData',NS):
   for c in row:
    v=c.find('s:v',NS)
    if v is not None:out[c.attrib['r']]=strings[int(v.text)] if c.attrib.get('t')=='s' else v.text
  return out
 tab=sheet(1);gen=sheet(12);tech=sheet(13);job=sheet(7);first=sheet(8);second=sheet(10);art=sheet(14)
 assert tab['D5']==gen['D3']=='2024/25'
 assert 'Full-time equivalent (FTE)' in tab['A48']
 assert 'special job-training' in tab['A48'] and 'general art schools' in tab['A48']
 assert 'FOR YOUTH' in gen['A8'] and 'FOR ADULTS' in gen['A16']
 n=lambda s,c:int(s[c])
 students=dict(special_job_training=n(tab,'D28'),stage_I=n(tab,'D29'),stage_II=n(tab,'D30'),general_youth=n(gen,'D10'),technical_youth=n(tab,'D32'),professional_general_art=n(tab,'D33'))
 assert n(gen,'D6')==students['general_youth']+n(gen,'D18')==n(tab,'D31')
 # Separate school-type tables cross-check every non-art youth route.
 assert students['special_job_training']==n(job,'D5')
 assert students['stage_I']==n(first,'D6')
 assert students['stage_II']==n(second,'D6')
 assert students['technical_youth']==n(tech,'D6')
 teachers=dict(stage_I_and_special=n(tab,'D19'),stage_II=n(tab,'D20'),general_including_adults=n(tab,'D21'),technical_and_art=n(tab,'D22'))
 assert all(isinstance(v,int) and v>=1 for v in teachers.values())
 pdf=PdfReader(P/'yearbook2025.pdf')
 notes='\n'.join(pdf.pages[i].extract_text() for i in [155,156,157,158])
 rounding=pdf.pages[21].extract_text()
 assert 'other legal and natural' in notes and 'public and' in notes and 'non-public' in notes
 assert 'post-primary schools' in notes and 'stage II sectoral vocational schools' in notes and 'general art schools leading to professional' in notes
 assert 'full-time equivalents' in notes and 'compulsory educational' in notes
 assert 'Due to the rounding' in rounding
 # All four numeric FTE rows occur with the same 3-year series in the PDF table.
 table=pdf.pages[159].extract_text()
 for v in teachers.values():assert str(v) in table
 total=sum(students.values());known=sum(v for k,v in teachers.items() if k!='general_including_adults')
 raw=[known,sum(teachers.values())]
 guard=1.0 # Per displayed integer FTE, enclosing unit rounding/truncation; not sampling error.
 lower=sum(max(0,v-guard) for k,v in teachers.items() if k!='general_including_adults')
 upper=sum(v+guard for v in teachers.values())
 u=lambda t:15*t/(total+15*t)
 return dict(main_admitted=False,school_year='2024/25',reference_period='Beginning of school year',geography='Schools located in City of Warsaw',
  students_by_route=students,students_total=total,excluded_general_adult_students=n(gen,'D18'),teacher_fte_published=teachers,
  adult_general_teacher_allocation='Unknown; youth general FTE lies between zero and the adult-inclusive general total',
  published_total_teacher_fte_bounds=raw,rounding_guard_per_cell=guard,teacher_fte_bounds=[lower,upper],utility_bounds=[u(lower),u(upper)],
  rounding_scope='Source general note14 acknowledges rounding; table publishes whole FTE. One-FTE outward guard per cell assumes unit rounding/truncation, not exact rounding direction or protection against reporting revisions.',
  included_ownership='Government, local government and other legal/natural persons; public and non-public',
  scope='Source-defined six post-primary youth school routes, including special and professional-art schools. Excludes general adult, post-secondary and higher education. All route ages rather than an individual age14-18 subset; school location rather than residents; teacher resources rather than learning quality.',
  workbook_member=member,workbook_sha256=hashlib.sha256(b).hexdigest(),pdf_pages=dict(ownership=156,youth_routes=157,adult_scope=158,teacher_definition=159,overview=160,general_youth_adult=165,rounding=22),
  source_typo_note='English note6e says prior technical schools were3-year while Polish says4-year; current5-year definition and observed counts are unchanged.')

def main():
 result=extract();(P/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));return result
if __name__=='__main__':main()
