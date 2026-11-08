"""Offline official-school-flow extraction; durations are not inferred."""
import csv,hashlib,json,zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def sheets(path):
 with zipfile.ZipFile(path) as z:
  assert z.testzip() is None
  ss=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',NS)]
  relns='{http://schemas.openxmlformats.org/package/2006/relationships}'
  rels={x.attrib['Id']:x.attrib['Target'] for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels')).findall(relns+'Relationship')}
  out={}
  for s in ET.fromstring(z.read('xl/workbook.xml')).findall('m:sheets/m:sheet',NS):
   target=rels[s.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
   path=target.lstrip('/') if target.startswith('/') else 'xl/'+target
   rows=[]
   for row in ET.fromstring(z.read(path)).findall('.//m:row',NS):
    d={}
    for c in row:
     v=c.find('m:v',NS)
     if v is not None:d[c.attrib['r'].rstrip('0123456789')]=ss[int(v.text)] if c.attrib.get('t')=='s' else v.text
    rows.append(d)
   out[s.attrib['name']]=rows
  return out

def main():
 for m in json.loads((P/'manifest.json').read_text()):
  b=(P/m['file']).read_bytes();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
 data=sheets(P/'flows_2024_25.xlsx');tables=sheets(P/'tables_2024_25.xlsx');code='1465011'
 result={'main_admitted':False,'school_year':'2024/2025','reference_date':'2024-09-30','city':'Warszawa','teryt':code,'school_stages':{}}
 extracted=[]
 for prefix in ['Podstawowe','Ponadpodstawowe']:
  matrix=data[prefix+'-macierz'][1:]
  assert len({(r['A'],r['C']) for r in matrix})==len(matrix)
  assert all(r['A']!=r['C'] and int(r['E'])>=3 for r in matrix)
  stage={'published_od_rows_national':len(matrix)}
  for label,col,total_sheet in [('outbound','A',prefix+'-wyjeżdżający'),('inbound','C',prefix+'-przyjeżdżający')]:
   rr=[r for r in matrix if r[col]==code];agg=[r for r in data[total_sheet][1:] if r.get('A')==code];assert len(agg)==1
   total=int(agg[0]['C']);visible=sum(int(r['E']) for r in rr);assert visible<=total
   stage[label]={'official_total_students':total,'published_od_rows':len(rr),'published_od_students':visible,'unallocated_aggregate_residual':total-visible}
   for r in rr:extracted.append(dict(stage=prefix,direction=label,residence_teryt=r['A'],residence_name=r['B'],school_teryt=r['C'],school_name=r['D'],published_students=int(r['E'])))
  result['school_stages'][prefix]=stage
 # Independent workbook checks: total primary+upper-secondary municipal flows.
 for table,direction in [('Tablica 2','outbound'),('Tablica 3','inbound')]:
  r=[r for r in tables[table] if r.get('A')==code];assert len(r)==1
  assert sum(result['school_stages'][p][direction]['official_total_students'] for p in result['school_stages'])==int(r[0]['C'])
 national=[r for r in tables['Tablica 1'] if r.get('A')=='POLSKA'][0]
 assert sum(int(r['C']) for r in data['Ponadpodstawowe-wyjeżdżający'][1:])==int(national['D'])
 assert sum(int(r['C']) for r in data['Ponadpodstawowe-przyjeżdżający'][1:])==int(national['D'])
 result['national_upper_secondary_intermunicipal_students']=int(national['D'])
 result['suppression_rule']='Intermunicipal OD cells below 3 students are omitted; official aggregate totals are retained separately. No omitted cell is reconstructed.'
 result['scope']='Administrative residence-municipality versus school-municipality flows for children/youth schools. No travel duration, mode, individual age or within-municipality students; no observed-trip or city travel-utility inference.'
 with (P/'warsaw_published_flows.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(extracted[0]));w.writeheader();w.writerows(extracted)
 (P/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
