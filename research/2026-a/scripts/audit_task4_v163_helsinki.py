"""Independent JSON-stat and native OOXML audit of the national-envelope candidate."""
from pathlib import Path
import hashlib,json,posixpath,subprocess,zipfile,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];D=R/'data/task4_v163_helsinki_envelope';O=R/'results/task4_v163_helsinki_envelope';P=Path('/data/projects/HiMCM-Overleaf')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def xcell(path,sheet,ref):
 ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};rel='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
 with zipfile.ZipFile(path) as z:
  book=ET.fromstring(z.read('xl/workbook.xml'));sid=next(x for x in book.find('s:sheets',ns) if x.attrib['name']==sheet).attrib['{'+rel+'}id']
  rels=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'));target=next(x for x in rels if x.attrib['Id']==sid).attrib['Target'];target=target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
  strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
  page=ET.fromstring(z.read(target));c=next(x for x in page.iter('{'+ns['s']+'}c') if x.attrib['r']==ref);v=c.find('s:v',ns).text
  return strings[int(v)] if c.attrib.get('t')=='s' else v

def main():
 s=read(D/'scope_audit.json');receipts=read(D/'retrieval.json');assert len(receipts)==8
 for r in receipts:assert r['status']==200 and sha(D/r['file'])==r['sha256']
 assert sha(D/'extract.py')==s['extractor_sha256']
 for y,total in [('2023',19586),('2024',19825)]:
  data=read(D/f'FI_ED3_{y}_original.json');selection={'worktime':'TOT_FTE','sex':'T','sector':'TOT_SEC'};index=0
  for name,size in zip(data['id'],data['size']):index=index*size+data['dimension'][name]['category']['index'].get(selection.get(name),0)
  assert data['value'][str(index)]==total
  assert data.get('status',{}).get(str(index)) is None
 cell=xcell(D/'FI_annexIII_original.xlsx','15.2.2','F10')
 assert hashlib.sha256(cell.encode()).hexdigest()==s['authoritative_variable_specific_method']['cell_text_sha256']
 assert 'estimate' in cell and 'FTE numbers' in cell
 assert xcell(D/'FI_annexIII_original.xlsx','18.1','B29')=='Employment statistics/register data of Statistics Finland.'
 students=read(D/'FI_11c4_students_original.json');assert students['size']==[3,1,1,1] and students['value']==[17789,18177,18661]
 assert students['dimension']['alue_23_20250101']['category']['label']=={'KU091':'Helsinki'}
 assert s['observations']==[] and s['city_PTR_bound'] is None and not s['national_teacher_upper_superset_verified']
 old=s['yearbook_comparison'];assert sha(R/old['reused_file'])==old['sha256'];assert old['year_2023']==old['native_API_year_2023'] and old['year_2022']!=old['native_API_year_2022']
 snapshot=read(R/'design/task4_user_v154_snapshot.json')['source_sha256']
 for n,h in snapshot.items():assert sha(R/n)==h,n
 guard=O/'protected_files.json'
 if guard.exists():protected=read(guard)['manuscript']
 else:
  names=subprocess.check_output(['git','-C',str(P),'ls-files','-z']).decode().split('\0');protected={n:sha(P/n) for n in names if n}
 for n,h in protected.items():assert sha(P/n)==h,n
 review=read(R/'design/task4_user_current_review.json');assert review['version']=='V160' and sha(P/review['pdf'])==review['pdf_sha256']
 (O/'protected_files.json').write_text(json.dumps({'science':snapshot,'manuscript':protected},indent=2)+'\n')
 report=dict(status='pass',iteration='V163',original_responses_verified=8,independent_method='Native OOXML F10 / B29 + mixed-radix JSON-stat indices; extractor uses openpyxl and Cartesian decoding',national_FTE_2024=19825,city_students_2022_2023_2024=[17789,18177,18661],FTE_estimation_specific_metadata_verified=True,guaranteed_national_upper_bound_not_established=True,source_workbook_not_edited_or_exported=True,scientific_files_unchanged=len(snapshot),manuscript_files_unchanged=len(protected),current_model='V154 unchanged',current_review='V160 unchanged',current_review_pdf_sha256=review['pdf_sha256'],primary_data_admissions=0,primary_score_width_change=0,PDF_authored=False,scope_audit_sha256=sha(D/'scope_audit.json'),retrieval_sha256=sha(D/'retrieval.json'),verifier_sha256=sha(Path(__file__)))
 (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
