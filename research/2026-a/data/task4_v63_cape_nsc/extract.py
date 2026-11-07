"""Match official 2025 DBE NSC examination outcomes to municipal school IDs."""
import csv,hashlib,json,re,subprocess
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as E
P=Path(__file__).resolve().parent
RAW=P/'nsc_school_performance2025.pdf'
ROSTER=P/'../task4_v62_cape_school_roster/western_cape_q3_2025.xlsx'
manifest=json.loads((P/'manifest.json').read_text())
for key,path in [('report',RAW),('roster',ROSTER)]:
 assert hashlib.sha256(path.read_bytes()).hexdigest()==manifest[key]['sha256']
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with ZipFile(ROSTER) as z:
 ss=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml'))]
 rows=[]
 for row in E.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('s:sheetData/s:row',NS):
  cells={}
  for c in row:
   v=c.find('s:v',NS)
   if v is not None:cells[re.sub('[0-9]','',c.attrib['r'])]=ss[int(v.text)] if c.attrib.get('t')=='s' else v.text
  rows.append(cells)
 header=rows[0]
 roster=[{name:r.get(col,'') for col,name in header.items()} for r in rows[1:] if r.get('A','')]
assert len(roster)==1935 and len({r['NatEmis'] for r in roster})==1935
lookup={r['NatEmis']:r for r in roster}
pages=subprocess.check_output(['pdftotext','-layout',str(RAW),'-'],text=True).split('\f')
exam=[]
for page,text in enumerate(pages,1):
 if page<139:continue  # Western Cape detailed results begin PDF139/printed137 map, first table140/138.
 lines=text.splitlines()
 for n,line in enumerate(lines):
  m=re.search(r'(\d{9})\s+(\d{7})\s+(.*)',line)
  if not m:continue
  tail=m[3]
  if not re.search(r'\d+\.\d\s*$',tail):tail+=' '+lines[n+1].strip()
  # 2023/24 columns can merge in layout extraction; last three fields are
  # the rightmost 2025 wrote/achieved/percent columns, visually verified.
  w,a,percent=map(float,tail.split()[-3:])
  assert int(w)==w and int(a)==a and 0<=a<=w
  assert w==0 or abs(100*a/w-percent)<=.051
  r=lookup[m[1]]  # Fail rather than silently omit any unknown school ID.
  assert r['DataYear']=='2025' and r['Status']=='OPEN' and r['LMunName']
  exam.append(dict(emis=m[1],centre_no=m[2],school_name=r['Official_Institution_Name'],municipality=r['LMunName'],sector=r['Sector'],phase=r['Phase_PED'],wrote=int(w),achieved=int(a),percent_reported=percent,pdf_page=page,roster_exam_no=r['ExamNo'],exam_no_agrees=m[2]==r['ExamNo'],cape_town=r['LMunName']=='CITY OF CAPE TOWN'))
assert len(exam)==469 and len({r['emis'] for r in exam})==469 and len({r['centre_no'] for r in exam})==469
assert sum(r['wrote'] for r in exam)==65965 and sum(r['achieved'] for r in exam)==58181
city=[r for r in exam if r['cape_town']]
assert len(city)==299
# Selected original PDF144 visual checks cover extraction-wrapped rows.
byid={r['emis']:r for r in exam}
for emis,w,a in [('103323918',213,190),('107323136',291,256),('106324086',249,235),('100000696',1,1),('107008229',72,57)]:
 assert (byid[emis]['wrote'],byid[emis]['achieved'])==(w,a)
def save(name,items,fields=None):
 with (P/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(items[0]),lineterminator='\n');w.writeheader();w.writerows(items)
save('western_cape_all_exam_matches.csv',exam)
save('cape_town_exam_matches.csv',city)
save('exam_number_mismatches.csv',[r for r in city if not r['exam_no_agrees']])
missing=[{k:r[k] for k in ['NatEmis','Official_Institution_Name','Sector','Phase_PED','ExamNo']} for r in roster if r['LMunName']=='CITY OF CAPE TOWN' and r['Status']=='OPEN' and r['Phase_PED']=='SECONDARY SCHOOL' and r['NatEmis'] not in byid]
assert len(missing)==27
save('roster_secondary_without_dbe_result.csv',missing)
groups=[]
for sector,phase in sorted({(r['sector'],r['phase']) for r in city}):
 part=[r for r in city if (r['sector'],r['phase'])==(sector,phase)]
 groups.append(dict(sector=sector,phase=phase,schools=len(part),wrote=sum(r['wrote'] for r in part),achieved=sum(r['achieved'] for r in part)))
save('cape_town_phase_outcomes.csv',groups)
n=sum(r['wrote'] for r in city);g=sum(r['achieved'] for r in city)
assert (n,g)==(44071,39056)
out=dict(year=2025,target='Candidates reported in DBE 2025 NSC school-performance tables at schools whose NatEmis maps to City of Cape Town in the 2025 Q3 roster',school_location_not_residence=True,source_wc_centres=469,source_wc_all_geographies_matched=True,unknown_geography_centres=0,city_centres=len(city),outside_city_centres=len(exam)-len(city),city_wrote=n,city_achieved=g,city_not_achieved=n-g,city_exam_pass_fraction=g/n,city_unweighted_school_mean_fraction=sum(r['achieved']/r['wrote'] for r in city)/len(city),city_exam_number_disagreements=sum(not r['exam_no_agrees'] for r in city),city_secondary_roster_without_result=len(missing),missing_result_is_not_zero=True,groups=groups,main_admitted=False,core_resource_cell_changed=False,reason='Exam-taker attainment is distinct from entry-cohort graduation, teacher resources, and quality adjusted for intake; non-DBE assessment and non-exam students not established as covered. No claim of full city high-school coverage.',date='2026-11-08')
(P/'audit.json').write_text(json.dumps(out,indent=2)+'\n')
(P/'scope_excerpt.txt').write_text('\n\n'.join('PDF PAGE '+str(i+1)+'\n'+pages[i] for i in [3]))
print(json.dumps(out,indent=2))
