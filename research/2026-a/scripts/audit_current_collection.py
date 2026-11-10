"""Verify bounded official-source follow-up originals without admitting new values."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json
R=Path(__file__).resolve().parents[1];O=R/'results/current_priority'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class PageText(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in {'script','style'}:self.skip+=1
 def handle_endtag(self,tag):
  if tag in {'script','style'} and self.skip:self.skip-=1
 def handle_data(self,data):
  if not self.skip:self.parts.append(data)
def text(p):
 parser=PageText();parser.feed(p.read_text());return ' '.join(' '.join(parser.parts).split())
def main():
 sources=[];D=R/'data/current_zurich_fte';m=json.loads((D/'zh_custom_requests.meta.json').read_text());sources.append((D/'zh_custom_requests.html',D/'zh_custom_requests.meta.json',m,'http_status'))
 D=R/'data/current_zurich_travel';meta=D/'retrievals.json'
 for m in json.loads(meta.read_text()):sources.append((D/m['file'],meta,m,'status'))
 checked=[]
 for p,meta,m,status in sources:
  assert sha(p)==m['sha256'] and p.stat().st_size==m['bytes'] and m[status]==200,p
  checked.append(dict(file=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size,metadata=str(meta.relative_to(R)),metadata_sha256=sha(meta)))
 assert len(checked)==3
 fte=text(sources[0][0]);assert all(x in fte for x in ['massgeschneiderte','Schulpersonal','bista@bi.zh.ch','Gemeinde'])
 country=text(R/'data/current_zurich_travel/eurostat_ch_country_metadata.html');assert country.count('20 November 2012')>=3
 city=text(R/'data/current_zurich_travel/zurich_city_commuters.html');assert 'Pendler*innen nach Wohnort und Arbeitsort, 2024' in city and 'Haupttransportmittel' in city
 priority=json.loads((O/'summary.json').read_text())
 for n,h in priority['source_sha256'].items():assert sha(R/n)==h,n
 proof=json.loads((O/'verification.json').read_text());assert proof['status']=='pass'
 report=dict(status='pass',official_original_responses=3,checks=checked,source_text_scope_checked=True,assessment='Custom education statistics route does not release matched city FTE; historical country metadata and commuter-count/mode page do not establish a matched2024duration distribution.',source_admissions=0,actual_score_width_reduction=0,active_science='V200 unchanged',model_original_inputs_and_current_four_registries_unchanged=True,source_requests_sent=False,limitations='Bounded page and response verification; no claim that the authorities cannot supply other unpublished records.',audit_script_sha256=sha(Path(__file__)))
 (O/'source_verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='pass',originals=3,admissions=0)))
if __name__=='__main__':main()
