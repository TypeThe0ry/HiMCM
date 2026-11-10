"""Read-only Oslo publisher-value match in the existing official Ookla archive."""
from pathlib import Path
import csv,hashlib,html,json,re
P=Path(__file__).resolve().parent;R=P.parents[1]
source=R/'data/task4_v5_resources/ookla_global_index.html';manifest=R/'data/task4_v5_resources/manifest.json'
m=next(x for x in json.loads(manifest.read_text()) if x['file']==source.name)
raw=source.read_bytes();assert len(raw)==m['bytes'] and hashlib.sha256(raw).hexdigest()==m['sha256']
s=raw.decode('utf-8');cols=list(re.finditer(r'id="column-([^"]+)"',s));idx=next(i for i,x in enumerate(cols) if x.group(1)=='fixedMedian');part=s[cols[idx].start():cols[idx+1].start() if idx+1<len(cols) else len(s)]
rows=[x for x in re.findall(r'<tr\b[^>]*>.*?</tr>',part,re.S) if 'href="/global-index/norway?city=Oslo#fixed"' in x];assert len(rows)==1
cells=[' '.join(html.unescape(re.sub('<[^>]*>',' ',x)).split()) for x in re.findall(r'<td\b[^>]*>(.*?)</td>',rows[0],re.S)]
assert cells==['78','-2','Oslo , Norway','150.76'],cells
month=re.findall(r'<div class="month">([^<]+)</div>',s);assert month==['September 2026']
input_path=R/'data/task4_v117_team_intake/city_indicators.csv'
with input_path.open(encoding='utf-8-sig',newline='') as f:submitted=next(x for x in csv.DictReader(f) if x['city']=='Oslo')
assert float(submitted['broadband_mbps'])==float(cells[3]) and submitted['broadband_mbps_year']=='2026'
result={'status':'pass','city':'Oslo','indicator':'fixed_broadband_mbps','publisher_value':float(cells[3]),'units':'Mbps','published_measure_field':'fixedMedian','published_city_rank':78,'publication_label':month[0],'source_url':m['url'],'archive_access_date':m['accessed'],'archive_file':str(source.relative_to(R)),'archived_row_html':rows[0],'source_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,manifest,input_path]},'source_footer':'Results are updated mid-month for the previous three months.','submitted_value_matches_publisher':True,'original_extraction_lineage_verified':False,'municipal_boundary_equivalence_verified':False,'primary_admissions':0,'actual_primary_width_reduction':0,'scope':'Exact value and published field/month match in an authenticated publisher archive; this does not prove the original CSV extraction route, sampling representativeness or city-proper boundary. The publication label is 2026, not a 2025 observation.'}
assert result['source_footer'] in html.unescape(re.sub('<[^>]*>',' ',s))
print(json.dumps(result,ensure_ascii=False,indent=2))
