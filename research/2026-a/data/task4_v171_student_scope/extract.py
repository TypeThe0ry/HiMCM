"""Reproduce the existing student stage breakdown and its new provenance check."""
from pathlib import Path
import collections,hashlib,json,zipfile,xml.etree.ElementTree as E
P=Path(__file__).resolve().parent
N={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cells(z,name,strings):
 result={}
 for c in E.fromstring(z.read(name)).findall('.//s:c',N):
  v=c.find('s:v',N)
  if v is not None:result[c.get('r')]=strings[int(v.text)] if c.get('t')=='s' else v.text
 return result
if __name__=='__main__':
 x=P/'city_students_original.xlsx'
 assert sha(x)=='6234f5b6cf617af10db16c5930105df4183eade7df47564858cc5dfe010bc251'
 with zipfile.ZipFile(x) as z:
  strings=[''.join(n.itertext()) for n in E.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',N)]
  c=cells(z,'xl/worksheets/sheet5.xml',strings);s=cells(z,'xl/worksheets/sheet4.xml',strings)
 values=[];sums=collections.Counter()
 for i in range(12,101):
  stage,provider,course,value=[c.get(k+str(i),'') for k in ['A','B','C','T']]
  if value:
   v=int(value);sums[(stage,provider)]+=v
   values.append(dict(stage=stage,provider=provider,course=course,source_cell=f'T_3!T{i}',pupils=v))
 assert sum(sums.values())==int(c['T11'])==13426
 landing=(P/'city_mittelschulen_original.html').read_text()
 assert 'in der Stadt Zürich' in landing and 'BIL103T1031_Mittelschulen_und_Berufsbildung.xlsx' in landing
 result=dict(version='V171',source_sha256=sha(x),extractor_sha256=sha(Path(__file__)),
  same_bytes_as_V120=True,existing_V157_stage_breakdown_reused=True,new_city_observation=False,
  city_landing_links_workbook=True,school_year_label=2024,year_rule_cell='Erläuterungen!B1',
  year_interpretation='School year beginning after summer 2024 and ending summer 2025; not a 2025/26 measurement.',
  stage_provider_totals=[dict(stage=k[0],provider=k[1],pupils=v) for k,v in sums.items()],
  total=13426,public_upper_secondary=6582,private_upper_secondary=1999,
  public_upper_SPF_cells=[r for r in values if r['stage']=='Sekundarstufe II' and r['provider']=='öffentlich' and r['course'].startswith('SPF ')],
  public_KME=dict(cell='T_2!S12',pupils=int(s['S12']),scope='Whole school; no assumed cross-tab attribution'),
  public_Passerelle=dict(cell='T_3!T58',pupils=int(c['T58'])),
  private_Passerelle_cells=[r for r in values if r['provider']=='privat' and r['course'].startswith('Passerelle')],
  pending='Certified target subset must respect adult/bridging/remote/programme exclusions and matching school-location and census-date conventions; no student lower bound admitted just from the stage labels.',
  admissions=0,rows=values)
 (P/'student_scope.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 print('V171: original stage breakdown/provenance reproduced; zero admissions')
