"""Read-only bounded provenance checks for selected retained Oslo/Zurich points."""
from pathlib import Path
from html.parser import HTMLParser
import csv,gzip,hashlib,html,json,re,subprocess,sys
from task4_audit_output import audit_parser,check_output,emit_report
R=Path(__file__).resolve().parents[1];G=R.parents[1];P=G.parent/'HiMCM-Overleaf';D=R/'data';O=R/'results/current_point_source_review/verification.json'
a=audit_parser(__doc__).parse_args();check_output(a,O,G)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def txt(p):return ' '.join(html.unescape(re.sub('<[^>]+>',' ',p.read_text())).split())
core=read(R/'design/task4_user_v203_snapshot.json')['source_sha256'];v=read(R/'results/current_paper_review/current_verification.json');extra={}
for k,d in v.items():
 if k.startswith('additional_') and k.endswith('_sha256'):extra.update(d)
assert len(core)==548 and len(extra)==77
for n,h in {**core,**extra}.items():assert sha(R/n)==h,n
for n,h in v['current_files_sha256'].items():assert sha(P/n)==sha(G/'paper/current'/n)==h,n
receipts=0;inputs=[]
for name,manifest in [('current_oslo_he_scope','retrieval_metadata.json'),('current_zurich_homicide_scope','retrievals.json')]:
 p=D/name;rows=read(p/manifest);rows=rows['records'] if isinstance(rows,dict) else rows
 for row in rows:
  f=p/row['file'];assert row['status']==200 and f.stat().st_size==row['bytes'] and sha(f)==row['sha256'];receipts+=1
 inputs.extend(sorted(x for x in p.iterdir() if x.is_file()))
p=D/'current_oslo_broadband_scope';m=read(p/'publisher_match.json');assert json.loads(subprocess.check_output([sys.executable,str(p/'extract.py')],text=True))==m
for n,h in m['source_sha256'].items():assert sha(R/n)==h,n
class Rows(HTMLParser):
 def __init__(self):super().__init__();self.depth=0;self.active=None;self.row=None;self.cell=None;self.rows=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='div':
   self.depth+=1
   if a.get('id')=='column-fixedMedian':self.active=self.depth
  if tag=='tr' and self.active:self.row={'cells':[],'links':[]}
  if tag=='td' and self.row is not None:self.cell=[]
  if tag=='a' and self.row is not None:self.row['links'].append(a.get('href'))
 def handle_data(self,data):
  if self.cell is not None:self.cell.append(data)
 def handle_endtag(self,tag):
  if tag=='td' and self.cell is not None:self.row['cells'].append(' '.join(''.join(self.cell).split()));self.cell=None
  if tag=='tr' and self.row is not None:self.rows.append(self.row);self.row=None
  if tag=='div':
   if self.depth==self.active:self.active=None
   self.depth-=1
parser=Rows();parser.feed((R/m['archive_file']).read_text());found=[x for x in parser.rows if '/global-index/norway?city=Oslo#fixed' in x['links']]
assert len(found)==1 and found[0]['cells']==['78','-2','Oslo, Norway','150.76'],found
assert m['publication_label']=='September 2026' and m['published_measure_field']=='fixedMedian' and m['publisher_value']==150.76
assert not m['original_extraction_lineage_verified'] and not m['municipal_boundary_equivalence_verified']
he=read(D/'current_oslo_he_scope/scope.json');assert he['national_snapshot']['institutions']==sum(he['national_snapshot']['categories'])==49 and not he['city_roster_obtained'] and he['primary_admissions']==0
national=txt(D/'current_oslo_he_scope/nokut_general_education.html');assert '49 accredited' in national and 'January 2026' in national and '14 non-accredited' in national
population=txt(D/'current_zurich_homicide_scope/zurich_population_2024.html');assert '448 664' in population and 'Ende 2024' in population
catalogue=txt(D/'current_zurich_homicide_scope/municipal_pks_catalogue.html');assert 'pro 1000 Einwohner' in catalogue and 'Vorjahr' in catalogue
z=D/'current_zurich_homicide_scope';zs=read(z/'scope.json')
with (z/'municipal_pks_grouped_offences.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
assert len(rows)==zs['archived_grouped_csv']['rows']==8190
assert sorted({r['Ausgangsjahr'] for r in rows})==zs['archived_grouped_csv']['years']==list(map(str,range(2009,2023)))
assert sorted({r['Haupttitel'] for r in rows})==zs['archived_grouped_csv']['haupttitel_categories']
assert len(zs['archived_grouped_csv']['haupttitel_categories'])==13 and not zs['archived_grouped_csv']['homicide_specific_category_present']
assert zs['city_municipal_residents_2024_end']==448664 and zs['city_municipal_residents_2023_end_derived']==448664-1582
assert not zs['original_rate_source_and_definition_established'] and zs['offence_count_is_not_verified_victim_count']
archive=D/'task4_v144_homicide/zurich2025_original.pdf.gz';assert sha(archive)==zs['prior_pks_2025_compressed_archive_sha256']
assert hashlib.sha256(gzip.decompress(archive.read_bytes())).hexdigest()==zs['prior_pks_2025_uncompressed_pdf_sha256']
inputs.append(archive)
inputs.extend(sorted(x for x in p.iterdir() if x.is_file()));inputs.extend([Path(__file__),R/'scripts/task4_audit_output.py'])
report={'status':'pass','raw_receipts_checked':receipts,'publisher_value_matches':1,'grouped_offence_rows_checked':8190,'offence_groups_checked':13,'broadband_independent_parser':'HTMLParser, fixedMedian Oslo row; extractor uses regex','national_institutions_not_city_count':49,'primary_admissions':0,'actual_primary_width_reduction':0,'core_bindings_checked':548,'supplemental_bindings_checked':77,'paper_dependencies_each_copy':7,'source_sha256':{str(x.relative_to(R)):sha(x) for x in inputs},'scope':'Bounded publisher-value and scope verification. Original extraction lineage and city boundary remain unproved; original higher-education and homicide points are not corrected. No new primary measurements or paper changes.'}
emit_report(report,a,O,G)
