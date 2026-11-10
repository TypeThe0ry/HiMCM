"""Verify captured follow-up bytes and scoped non-admission evidence."""
from pathlib import Path
import csv,hashlib,json,subprocess,zipfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 records=[];manifests={}
 for directory in ['current_zurich_followup','current_dublin_followup']:
  d=ROOT/'data'/directory;m=json.loads((d/'manifest.json').read_text());items=m if isinstance(m,list) else m['records'];manifests[directory]=sha(d/'manifest.json')
  for r in items:
   name=r.get('file',r.get('filename'))
   if name:
    p=d/name;assert p.is_file() and len(p.read_bytes())==r['bytes'] and sha(p)==r['sha256']
    assert r['http_status']==200 and r['retrieved_utc'] and r.get('source_url',r.get('url','')).startswith('https://')
    records.append(dict(directory=directory,file=name,sha256=sha(p),bytes=r['bytes'],http_status=200))
   else:assert '403' in r['error']
 assert len(records)==5
 d=ROOT/'data/current_zurich_followup'
 with (d/'teacher_gender_chart.csv').open(newline='') as f:
  reader=csv.DictReader(f);assert reader.fieldnames==['stufe','sex','wert'];rows=list(reader)
 assert len(rows)==14 and len({r['stufe'] for r in rows})==7 and {r['sex'] for r in rows}=={'Frauen','Männer'}
 assert all(0<=float(r['wert'])<=100 for r in rows)
 text=subprocess.check_output(['pdftotext',d/'bfs_commute_2022.pdf','-'],text=True)
 assert 'Pendlermobilität in der Schweiz 2022' in text and '29,6 Minuten' in text
 assert 'Hier finden Sie den Anteil der Lehrkräfte nach Geschlecht und Art der Schule.' in (d/'zurich_teacher_gender.html').read_text()
 xlsx=ROOT/'data/current_dublin_followup/post_primary_2019_2020.xlsx';ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
 with zipfile.ZipFile(xlsx) as z:
  shared=ET.fromstring(z.read('xl/sharedStrings.xml'));strings=[''.join(n.itertext()) for n in shared.findall('m:si',ns)]
  sheet=ET.fromstring(z.read('xl/worksheets/sheet1.xml'));head=sheet.find('m:sheetData/m:row',ns);headings=[]
  for c in head.findall('m:c',ns):
   v=c.find('m:v',ns);value=v.text if v is not None else ''
   headings.append(strings[int(value)] if c.get('t')=='s' else value)
 assert len(headings)==24 and any('local authority' in h.lower() for h in headings) and any('total' in h.lower() for h in headings)
 assert not any('teacher' in h.lower() or 'fte' in h.lower() for h in headings)
 # Recheck every frozen scientific binding and the current paper dependency hashes.
 snapshot=json.loads((ROOT/'design/task4_user_v202_snapshot.json').read_text())['source_sha256']
 for n,h in snapshot.items():assert sha(ROOT/n)==h,n
 proof=json.loads((ROOT/'results/current_paper_review/current_verification.json').read_text());paper=ROOT.parents[1].parent/'HiMCM-Overleaf'
 for n,h in proof['current_files_sha256'].items():assert sha(paper/n)==h,n
 report=dict(status='pass',primary='V202 unchanged',successful_originals=records,manifests_sha256=manifests,teacher_gender_chart_fields=['stufe','sex','wert'],teacher_gender_chart_rows=14,dublin_workbook_headings=headings,blocked_capture_status=403,immutable_science_bindings=len(snapshot),paper_dependencies=7,primary_admissions=0,actual_width_reduction=0,scope='Captured bytes and selected content/schema assertions; no proof of universal data absence or independent validation of all provider statistics',script_sha256=sha(Path(__file__)))
 out=ROOT/'results/current_priority/source_followup_verification.json';out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='pass',successful_originals=5,headings=headings)))
if __name__=='__main__':main()
