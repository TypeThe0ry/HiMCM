"""Verify original DST responses and source-dated school teacher count."""
from pathlib import Path
import csv,hashlib,json,re,subprocess
P=Path(__file__).resolve().parent
for r in json.loads((P/'manifest.json').read_text()):
 b=(P/r['file']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
meta={t:json.loads((P/(t+'_metadata.json')).read_text()) for t in ['inst02','inst11','inst12','laby48']}
assert next(v for v in meta['inst02']['variables'] if v['id']=='Tid')['values'][-1]['id']=='2014'
assert next(v for v in meta['inst11']['variables'] if v['id']=='Tid')['values'][-1]['id']=='2025'
rows=[]
for t in ['inst11','inst12']:
 rr=list(csv.DictReader((P/(t+'_prefix101_2025.csv')).open(encoding='utf-8-sig'),delimiter=';'))
 for r in rr:
  assert r['INSTI'].startswith('101') and r['TID']=='2025' and r['FSTATUS']=='Students per 1st October'
  assert int(r['INDHOLD'])>=0
  rows.append(dict(table=t,**r))
rys=next(r for r in rows if r['INSTI'].startswith('101115'))
assert int(rys['INDHOLD'])==1177
pages=subprocess.check_output(['pdftotext','-layout',str(P/'rysensteen_resources2024_25.pdf'),'-'],text=True).split('\f')
clean=lambda s:re.sub(r'[\u202a-\u202e]','',s)
a=' '.join(clean(pages[14]).split());b=' '.join(clean(pages[15]).split())
assert 'I alt 46 51 97' in a and 'Antal personer' in a
assert 'status 2. kvartal 2024' in b
(P/'school_source_extract.txt').write_text('\n\n'.join('PDF page '+str(i+1)+'\n'+clean(pages[i]) for i in [13,14,15]))
out=dict(source_retrieved_date='2026-11-08',school='Rysensteen Gymnasium',institution='101115',
 teacher_headcount=97,teacher_reference='2024 Q2, PDF15–16, sourced by school to Isola.modt.dk',
 students=1177,student_reference='1 October 2025, DST INST11',same_reference_period=False,
 school_total_staff_fte_2024_25=109,fte_is_not_teacher_headcount=True,
 prefix101_counts=[dict(table=t,rows=sum(r['table']==t for r in rows),students=sum(int(r['INDHOLD']) for r in rows if r['table']==t)) for t in ['inst11','inst12']],
 prefix_is_not_verified_current_city_boundary=True,city_teacher_universe_verified=False,
 teacher_student_register_access='Official DST announcement: authorized researchers via Danmarks Datavindue; no access requested.',
 teacher_student_register_source='https://www.dst.dk/da/presse/Pressemeddelelser/2024/2024-03-15-nyt-banebrydende-register-giver-nye-forskningsmuligheder-paa-uddannelsesomraadet',
 main_admitted=False,changed_model_cells=0)
(P/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
