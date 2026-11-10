"""Verify original directory cards against the frozen seven-name subset."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
class Cards(HTMLParser):
 def __init__(self):super().__init__();self.card=None;self.slot=None;self.rows=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='stzh-card-navigation':self.card=dict(href=a['href'],heading='',description='')
  if tag=='stzh-clamp' and self.card is not None:self.slot={'lead':'description'}.get(a.get('slot'),a.get('slot'))
 def handle_data(self,data):
  if self.card is not None and self.slot in self.card:self.card[self.slot]+=data
 def handle_endtag(self,tag):
  if tag=='stzh-clamp':self.slot=None
  if tag=='stzh-card-navigation' and self.card is not None:
   self.rows.append({k:' '.join(v.split()) for k,v in self.card.items()});self.card=None
r=json.loads((P/'retrieval.json').read_text());raw=(P/r['file']).read_bytes()
assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
text=raw.decode('utf-8');assert 'Sieben Hallenbäder' in text
parser=Cards();parser.feed(text)
old=json.loads((ROOT/'data/task4_v118_pools/observations.json').read_text())[0]
assert old['city']=='Zurich' and old['raw_count']==7
names=set(old['venues']);matched=[x for x in parser.rows if x['heading'] in names]
assert len(matched)==7 and set(x['heading'] for x in matched)==names
assert len({x['href'] for x in matched})==7
school=[x for x in parser.rows if x['heading'].startswith('Schulschwimmanlage ') and x['description']=='Mit öffentlichem Schwimmen']
assert len(school)==6 and len({x['href'] for x in school})==6
report=dict(status='pass',raw_original_sha256=r['sha256'],frozen_observation_sha256=hashlib.sha256((ROOT/'data/task4_v118_pools/observations.json').read_bytes()).hexdigest(),frozen_named_subset_confirmed=matched,current_additional_school_cards=school,seven_distinct_directory_targets=True,addresses_available_in_directory_cards=False,observation_date='2026-11-10 retrieval; source inventory reference date unstated',primary_admissions=0,actual_score_width_reduction=0,scope='OriginalHTMLconfirms seven retained venue names and separate directory targets; does not establish address uniqueness, continuous operation,2025 inventory or individualstudentaccess. Six publicswimming schoolcards are candidates only, not a new admitted count.')
(P/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS: originalSHA/bytes,7retainednames/targets,6additionalpublic-schoolcardsseparate;noadmission')
