"""Offline extraction of a named Warsaw metro-complex subset; no model writes."""
from pathlib import Path
import csv,hashlib,json,re,subprocess,html
D=Path(__file__).resolve().parent;R=D.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def text(pdf,first=None,last=None):
 args=['pdftotext']
 if first:args+=['-f',str(first),'-l',str(last or first)]
 return subprocess.check_output(args+['-layout',str(pdf),'-'],text=True)
def main():
 receipts=json.loads((D/'retrievals.json').read_text());assert len(receipts)==4
 for r in receipts:
  assert r['http_status']==200 and r['file'];p=D/r['file'];assert sha(p)==r['sha256'] and p.stat().st_size==r['bytes']
 appearance=[]
 for line in ['M1','M2']:
  filename=line.lower()+'_original.html';s=(D/filename).read_text()
  pattern=r'<div\s+id="([^"]+)"[^>]*class="elementor-tab-title"[^>]*>.*?<a class="elementor-accordion-title"[^>]*>\s*Stacja\s+&quot;(.*?)&quot;</a>'
  rows=re.findall(pattern,s,re.S)
  if not rows:
   pattern=pattern.replace('&quot;','"');rows=re.findall(pattern,s,re.S)
  assert len(rows)==(21 if line=='M1' else 18),(line,len(rows))
  assert len({name for _,name in rows})==len(rows)
  for pos,(element,name) in enumerate(rows,1):appearance.append(dict(line=line,line_order=pos,station_name=html.unescape(name),source_file=filename,source_locator='#'+element+' .elementor-accordion-title',locator_type='native_HTML_element_ID;not_a_stable_station_identifier'))
 m1={r['station_name'] for r in appearance if r['line']=='M1'};m2={r['station_name'] for r in appearance if r['line']=='M2'}
 assert m1&m2=={'Świętokrzyska'} and len(m1|m2)==38
 for omitted in ['Karolin','Chrzanów','Lazurowa','STP Karolin','Plac Konstytucji','Muranów']:assert omitted not in m1|m2
 plan=text(D/'network_plan_original.pdf');assert '21 stacji' in plan and '18 stacji' in plan and 'W WARSZAWIE' in plan
 scope=text(D/'fire_service_2025_original.pdf',4,5);normalized=' '.join(scope.split())
 assert 'Na terenie m. st. Warszawy zlokalizowanych jest 21 stacji metra I linii (M1) oraz 18 stacji metra II linii (M2).' in normalized
 assert 'budowy' in normalized and '2026' in normalized
 assert scope==(D/'fire_service_scope_extracted.txt').read_text()
 source=R/'data/task4_v117_team_intake/city_indicators.csv';assert sha(source)=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
 with source.open(encoding='utf-8-sig') as stream:row=next(x for x in csv.DictReader(stream) if x['city']=='Warsaw')
 pop=int(row['population']);assert pop==1863800 and row['population_year']=='2024' and not row['transit_share_pct']
 density=38*100000/pop;lower=density/(50+density)
 complexes=[dict(station_name=n,lines='|'.join(line for line in ['M1','M2'] if n in (m1 if line=='M1' else m2)),appearance_count=sum(a['station_name']==n for a in appearance)) for n in sorted(m1|m2)]
 for name,rows in [('station_appearances.csv',appearance),('station_complexes.csv',complexes)]:
  with (D/name).open('w') as stream:
   w=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
 findings=dict(version='V191Warsawcandidate',status='candidate_only;not_primary_admission',city='Warsaw',indicator='public_transport_density',line_station_appearances=39,line_counts={'M1':21,'M2':18},shared_complex='Świętokrzyska',station_complex_count=38,population=pop,population_year=2024,density_per100000=density,utility_lower=lower,utility_upper=1,anchor=50,reference_time='Operator catalogue snapshot accessed2026-11-09UTC;not a2025census',geography='Warsaw city proper;2025fire-service report explicitly locates21M1and18M2stations within m.st.Warszawy',deduplication='Exact official station headings;sole common nameŚwiętokrzyska merged across lines, as the official schematic intersection;no platforms/exits/STP/under-construction stations counted',native_station_IDs_available=False,native_HTML_locator_IDs_not_station_IDs=True,other_modes_unmeasured=True,complete_city_inventory_claim=False,operational_or_student_access_claim=False,map_metadata='Official PDF labels current and planned networks separately;PDFcreation2024-05-14,uploadURL2026/02 does not redate its contents',source_scope_caveat='Fire-service report2025 gives city scope/counts but its p5 narrative says Bródno-Bemowo completed2023;not used to establish historical opening dates. Catalogued supply does not verify access-day station openings.',source_sha256={str(p.relative_to(D)):sha(p) for p in [D/r['file'] for r in receipts]},original_csv_sha256=sha(source),primary_data_changed=False)
 (D/'findings.json').write_text(json.dumps(findings,ensure_ascii=False,indent=2)+'\n')
 observation=dict(city='Warsaw',indicator='public_transport_density',raw_count=38,population=pop,population_year=2024,utility_lower=lower,utility_upper=1,anchor=50,inventory_reference_year=2026,inventory_date_basis='2026-11-09UTCoperatorcataloguesnapshot;notdated2025censusorindependent2026operatinginventory',supporting_map_reference_year=2024,supporting_city_scope_report_reference_year=2025,source_scope='38namedWarsawcitymetrostationcomplexes:21M1+18M2appearancesminussharedŚwiętokrzyska;othermodesunknown',status='candidate_only;not_primary_admission')
 (D/'observations.json').write_text(json.dumps([observation],ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:findings[k] for k in ['station_complex_count','population','density_per100000','utility_lower','utility_upper']},indent=2))
if __name__=='__main__':main()
