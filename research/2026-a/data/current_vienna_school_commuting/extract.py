"""Read-only scope extraction of the national Austrian education-commuting workbook."""
from pathlib import Path
import hashlib,json,zipfile,xml.etree.ElementTree as E
P=Path(__file__).resolve().parent
for r in json.loads((P/'retrievals.json').read_text()):
 raw=(P/r['file']).read_bytes();assert r['status']==200 and len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
ns={'t':'urn:oasis:names:tc:opendocument:xmlns:table:1.0'}
with zipfile.ZipFile(P/'students_2011_2024.ods') as z:root=E.fromstring(z.read('content.xml'))
tables=root.findall('.//t:table',ns);assert len(tables)==1;table=tables[0];rows=[]
for row in table.findall('t:table-row',ns):
 vals=[]
 for c in row.findall('t:table-cell',ns):
  text=''.join(c.itertext()).strip();repeat=int(c.get('{'+ns['t']+'}number-columns-repeated','1'))
  if not text and repeat>100:break
  vals.extend([text]*repeat)
 rows.append(vals)
assert len(rows)==186 and rows[171][1]=='2024'
selected=rows[172:184];assert len(selected)==12
assert selected[6][0]=='AHS Oberstufe' and selected[7][0]=='Berufsbildende mittlere Schule' and selected[8][0]=='Berufsbildende höhere Schule'
out={'status':'pass','geography':'Austria national table; no Wien row in this workbook','title':rows[0][0],'sheet':table.get('{'+ns['t']+'}name'),'header':rows[1][:7],'selected_year':2024,'selected_rows':[{'ods_row':i+173,'cells':r[:7]} for i,r in enumerate(selected)],'source_note':rows[184][0],'contains_Wien_row':any('Wien' in ' '.join(r) for r in rows),'primary_admissions':0,'actual_primary_width_reduction':0,'scope':'Counts by formal education and administrative commuting category, not journey-time bins or mean minutes. This national workbook does not supply the missing Vienna travel utility; other linked products are not exhaustively characterized.'}
assert not out['contains_Wien_row'] and 'Record Swapping' in out['source_note']
print(json.dumps(out,ensure_ascii=False,indent=2))
