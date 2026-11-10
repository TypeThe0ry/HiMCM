"""Independent source and scalar audit of unadmitted OCBC venue scenario."""
import csv, hashlib, json, math, re
from pathlib import Path
from html.parser import HTMLParser
from task4_user_v200_revision import revised_bounds
from task4_v5_model import ROOT, NAMES

D=ROOT/'data/current_sg_sportshub'; O=ROOT/'results/current_sportshub_candidate'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
class Text(HTMLParser):
 def __init__(self): super().__init__(); self.out=[]; self.hide=0
 def handle_starttag(self,t,a):
  if t in ('script','style'): self.hide+=1
 def handle_endtag(self,t):
  if t in ('script','style') and self.hide:self.hide-=1
 def handle_data(self,s):
  if not self.hide:self.out.append(s)
def page(p):
 x=Text(); x.feed(p.read_text()); return ' '.join(' '.join(x.out).split())
def close(a,b): assert abs(float(a)-float(b)) < 3e-10,(a,b)
def score(row,w):
 p=math.sqrt(math.fsum(q*x*x for q,x in zip(w,row)))
 n=math.sqrt(math.fsum(q*(1-x)**2 for q,x in zip(w,row)))
 return 100*p/(p+n)
def main():
 snapshot=read(ROOT/'design/task4_user_v200_snapshot.json')['source_sha256']; assert len(snapshot)==407
 nav=[ROOT/'design'/('task4_user_current_'+n+'.json') for n in ['model','extensions','review','delivery']]
 paper=ROOT.parent.parent.parent/'HiMCM-Overleaf'
 files=[paper/'main.tex',paper/'ref.bib',paper/'mcmthesis.cls']+sorted((paper/'figures').glob('*'))
 assert len(files)==7
 guard={str(p):sha(p) for p in nav+files}
 for path,h in snapshot.items(): assert sha(ROOT/path)==h,path
 raw=ROOT/'data/task4_v117_team_intake/city_indicators.csv'; assert sha(raw)=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
 preview=read(O/'preview.json')
 for path,h in preview['source_sha256'].items(): assert sha(ROOT/path)==h,path
 for name in ('venue','swimming'):
  p=D/(name+'.html'); m=read(D/(name+'.html.json'))
  assert m['http_status']==200 and m['bytes']==p.stat().st_size and m['sha256']==sha(p)
  assert m['retrieved_utc'].startswith('2026-11-10') and m['url'].startswith('https://www.thekallang.com.sg/')
 assert '404' in read(D/'conditions.pdf.json')['failure']
 v=page(D/'venue.html'); s=page(D/'swimming.html')
 assert all(x in v for x in ['7 Stadium Drive','397632','general public','competition and training pools open for public swimming','5 to 28 December 2026','Training Pool availability will be limited'])
 assert all(x in s for x in ['Per entry rates','Child (under 18 years old)','aged 16 years and above','applicable for all ages','15 years and below','closed every Tuesday','30 Oct'])
 old=read(ROOT/'data/task4_v199_sgpool/venues.json')['venues']; admission=read(ROOT/'design/task4_user_v200_admissions.json')['observations'][0]
 assert len(old)==25 and len({x['postal_code'] for x in old})==25
 assert [x['name'] for x in old]==admission['venues'] and [x['provider_id'] for x in old]==admission['provider_page_ids']
 aliases=['ocbc','aquatic centre','sports hub','kallang','stadium drive','397632']
 for item in old:
  combined=' '.join([item['name'],item['address'],item['postal_code'],item['provider_id']]).lower()
  assert all(a not in combined for a in aliases),item['name']
 assert set(admission['withheld_notice_venues'])=={'clementi-swimming-complex','jurong-east-swimming-complex','katong-swimming-complex'}
 f,lo,hi=revised_bounds(); cities=f.city.tolist(); i=cities.index('Singapore'); j=NAMES.index('public_pool_density')
 assert int(f.iloc[i].population)==6036900 and int(f.iloc[i].population_year)==2024
 with (O/'scores.csv').open() as file: rows=list(csv.DictReader(file))
 assert len(rows)==128 and len({(r['scenario'],r['weight_reference'],r['city']) for r in rows})==128
 refs={'fixed':[.1125]*6+[.05,.1125,.1125,.05], 'equal':[.1]*10}
 cases={'active_V200_25':25,'candidate_inventory26':26,'withdraw_new_venue25':25,'withhold4_notice_venues22':22}
 summary={(x['scenario'],x['weight_reference']):x for x in preview['summaries']}; assert len(summary)==8
 for label,n in cases.items():
  a=lo.copy(); density=n*100000/6036900; a[i,j]=density/(1+density)
  for ref,w in refs.items():
   l=[score(row,w) for row in a]; u=[score(row,w) for row in hi]; mid=[score((a[k]+hi[k])/2,w) for k in range(16)]
   regrets=[max(0,max(u[k] for k in range(16) if k!=z)-l[z]) for z in range(16)]
   group={r['city']:r for r in rows if r['scenario']==label and r['weight_reference']==ref}; assert set(group)==set(cities)
   for z,city in enumerate(cities):
    r=group[city]; others=[k for k in range(16) if k!=z]
    for name,x in [('score_lower',l[z]),('score_upper',u[z]),('max_regret',regrets[z]),('midpoint_illustrative_score',mid[z])]:close(r[name],x)
    assert int(r['best_rank'])==1+sum(l[k]>u[z]+1e-12 for k in others)
    assert int(r['worst_rank'])==1+sum(u[k]>l[z]+1e-12 for k in others)
    assert (r['possible_champion']=='True')==(u[z]>=max(l[k] for k in others)-1e-12)
    assert (r['necessary_champion']=='True')==(l[z]>=max(u[k] for k in others)-1e-12)
    assert int(r['decision_rank'])==1+sum(x<regrets[z] for x in regrets)
    assert int(r['midpoint_illustrative_rank'])==1+sum(x>mid[z] for x in mid)
   q=summary[label,ref]; close(q['utility_lower'],a[i,j]); close(q['mean_score_width'],math.fsum(y-x for x,y in zip(l,u))/16)
   close(q['Singapore_regret_gap_to_best_other'],regrets[i]-min(regrets[k] for k in range(16) if k!=i))
   assert q['conservative_recommendation']==[cities[k] for k in range(16) if regrets[k]<=min(regrets)+1e-12]
   assert q['possible_champions']==sum(u[z]>=max(l[k] for k in range(16) if k!=z)-1e-12 for z in range(16))
   assert q['necessary_champions']==sum(l[z]>=max(u[k] for k in range(16) if k!=z)-1e-12 for z in range(16))
 for path,h in snapshot.items(): assert sha(ROOT/path)==h,path
 assert all(sha(Path(p))==h for p,h in guard.items())
 proof={'status':'pass','source_qualification':'PASS: one physical public-venue candidate, subject to temporal and access scope; not admitted','candidate_deduplicated_against_all_25':True,'scalar_city_weight_cases':128,'independent_squared_norm_and_self_exclusion':True,'snapshot_bindings':407,'raw_csv_sha256':sha(raw),'navigation_and_paper_hashes':guard,'limitations':'2026 capture does not establish 2025 inventory, current opening, individual universal access, or complete conditions; 404 recorded; 22 is a sensitivity withholding count, not an open count.','source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),O/'preview.json',O/'scores.csv',D/'venue.html',D/'venue.html.json',D/'swimming.html',D/'swimming.html.json',D/'conditions.pdf.json',ROOT/'data/task4_v199_sgpool/venues.json']}}
 (O/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print('PASS: source and 128 scalar cases')
if __name__=='__main__':main()
