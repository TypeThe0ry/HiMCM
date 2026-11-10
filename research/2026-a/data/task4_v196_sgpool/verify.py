"""Match original article headings to the frozen seven-venue subset, no admission."""
import ast,hashlib,json,re
from html.parser import HTMLParser
from pathlib import Path
P=Path(__file__).resolve().parent
class Headings(HTMLParser):
 def __init__(self):super().__init__();self.tag=None;self.parts=[];self.headings=[]
 def handle_starttag(self,t,a):
  if t in ['h2','h3']:self.tag=t;self.parts=[]
 def handle_data(self,s):
  if self.tag:self.parts.append(s)
 def handle_endtag(self,t):
  if t==self.tag:self.headings.append(' '.join(''.join(self.parts).split()));self.tag=None
m=json.loads((P/'retrieval.json').read_text());b=(P/m['file']).read_bytes()
assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
s=b.decode();h=Headings();h.feed(s)
numbered=[re.sub(r'^\d+\.\s*','',v) for v in h.headings if re.match(r'^\d+\.\s*',v)]
assert len(numbered)==10 and len(set(numbered))==10
old=P.parent/'task4_v117_singapore/extract.py'
tree=ast.parse(old.read_text())
items=[ast.literal_eval(n.value) for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='venues' for t in n.targets)]
assert len(items)==1;expected=[v[0] for v in items[0]]
selected=[v for v in numbered if 'SAFRA' not in v]
assert selected==expected and len(selected)==7
assert 'April 23, 2025' in s
result=dict(status='pass',original_HTTP_status=m['status'],matched_frozen_named_venues=selected,numbered_article_entries=10,excluded_entries=[v for v in numbered if v not in selected],published_date='2025-04-23',retrieval_scope='Current originalHTML corroborates seven names and displayed publication date, not immutable2025text or openinghours.',primary_admissions=0,actual_score_width_reduction=0,old_population_not_reused=True,source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'article_original.html',P/'retrieval.json',Path(__file__)]},frozen_extraction_script_sha256=hashlib.sha256(old.read_bytes()).hexdigest())
(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
