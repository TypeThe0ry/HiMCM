"""Extract calendar-year enrollment; do not assume matching teacher census date."""
import hashlib,json
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as E
P=Path(__file__).resolve().parent
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def sheets(path):
 with ZipFile(path) as z:
  ss=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml'))]
  rel={x.attrib['Id']:x.attrib['Target'] for x in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
  out={}
  for sh in E.fromstring(z.read('xl/workbook.xml')).find('s:sheets',NS):
   t=rel[sh.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']];t=t.lstrip('/') if t.startswith('/') else 'xl/'+t
   cells={}
   for c in E.fromstring(z.read(t)).findall('.//s:c',NS):
    v=c.find('s:v',NS)
    if v is not None: cells[c.attrib['r']]=ss[int(v.text)] if c.attrib.get('t')=='s' else v.text
   out[sh.attrib['name']]=cells
  return out

def main():
 raw=P/'../task4_v40_education/knbs2025_education.xlsx'
 assert hashlib.sha256(raw.read_bytes()).hexdigest()=='7d823302b501a78919cf2ae9e513580b5b39e533930cc2d3cf8c168dcc572854'
 c=sheets(raw)['TAB 15.6'];assert c['A51'].strip()=='Nairobi City' and c['G4']=='2023' and c['G51']=='123566'
 out=dict(city='Nairobi City',secondary_enrollment_2023=123566,cell='TAB 15.6!G51',
   original_reused='../task4_v40_education/knbs2025_education.xlsx',source_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),
   teacher_lead=dict(source='../task4_v45_nairobi/audit.json',year=2023,reference='TSC March 2023, PWPER Appendix4.6',teachers_excluding_heads=2650,teachers_including_heads=2851,scope='public secondary TSC; BOM/private additional staffing unknown',raw_download_verified=False),
   same_calendar_year=True,same_reference_date_verified=False,main_admitted=False,changed_model_cells=0,
   conditional_only_utility_lower=15*2650/(123566+15*2650),
   conditional_assumptions=['Accept teacher source transcription','Accept March staffing as subset at enrollment reference date','Accept all county secondary enrollment as complete denominator'],
   conclusion='2023 calendar-year matching alone does not establish a common census; conditional lower bound is not admitted.')
 if (P/'knbs2024_education.xlsx').exists():
  old=sheets(P/'knbs2024_education.xlsx')['Table 15.6'];assert old['A50'].strip()=='Nairobi City' and old['H50']=='123566' and old['H3']=='2023*'
  manifest=json.loads((P/'download_manifest.json').read_text());record=next(x for x in manifest if x['file']=='knbs2024_education.xlsx');assert hashlib.sha256((P/'knbs2024_education.xlsx').read_bytes()).hexdigest()==record['sha256']
  out['prior_release_confirmed']=dict(file='knbs2024_education.xlsx',cell='Table 15.6!H50',students=123566)
 (P/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
