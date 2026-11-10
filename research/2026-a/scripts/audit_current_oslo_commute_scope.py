"""Independent Oslo commute source and deterministic withdrawal audit."""
import csv,datetime,hashlib,json,math,pathlib,re,subprocess
from html.parser import HTMLParser
from task4_user_v203_revision import revised_bounds
from task4_user_city_indicators import SOURCE
from task4_v5_model import ROOT,NAMES
R=ROOT;O=R/'results/current_oslo_commute_scope';T=R/'data/current_oslo_travel2009';Z=R/'data/current_zurich_fte_bound'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def capture(p,m):
 assert m.get('http_status',m.get('status'))==200
 assert datetime.datetime.fromisoformat(m['utc']).utcoffset()==datetime.timedelta(0)
 assert len(p.read_bytes())==m['bytes'] and sha(p)==m['sha256']
 return {'file':str(p.relative_to(R)),'sha256':m['sha256'],'recorded_http_status':200,'recorded_utc':m['utc']}
report=read(O/'summary.json'); bindings=read(R/'design/task4_user_v203_snapshot.json')['source_sha256'];assert len(bindings)==548
for p,h in bindings.items():assert sha(R/p)==h,p
protected=report['protected_at_run'];assert len(protected)==11
for p,h in protected.items():assert sha(pathlib.Path(p))==h,p
assert sha(SOURCE)==report['original_CSV_sha256']=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
files=[capture(T/'eurostat_NO001C_2009.json',read(T/'eurostat_metadata.json'))]
for p in ['toi_2009_key_report.pdf','toi_2009_commute_factsheet.pdf']:files.append(capture(T/p,read(T/(p+'.metadata.json'))))
for m in read(Z/'provenance.json'):files.append(capture(Z/m['filename'],m))
assert len(files)==7
x=read(T/'eurostat_NO001C_2009.json');assert x['id']==['freq','indic_ur','cities','time'] and x['size']==[1,17,1,1]
d=x['dimension'];assert d['freq']['category']['index']['A']==0 and d['indic_ur']['category']['index']['TT1019V']==6 and d['cities']['category']['index']['NO001C']==0 and d['time']['category']['index']['2009']==0
assert x['value']['6']==31 and d['cities']['category']['label']['NO001C']=='Oslo (greater city)' and 'Average time of journey to work' in d['indic_ur']['category']['label']['TT1019V'] and 'status' not in x
pdf=subprocess.run(['pdftotext','-layout',str(T/'toi_2009_key_report.pdf'),'-'],text=True,check=True,stdout=subprocess.PIPE).stdout
s=pdf[pdf.index('Tabell 7.2: Arbeidsreisenes lengde og tidsbruk for ulike grupper.',pdf.index('Tabell 7.2: Arbeidsreisenes lengde og tidsbruk for ulike grupper.')+1):];s=s[:s.index('Copyright')]
assert re.search(r'Oslo\s+8,9\s+22\s+10,1\s+23\s+11,8\s+22\s+11,2\s+26',s)
assert re.search(r'Oslos omegnskommuner\s+18,3\s+27\s+18,9\s+29\s+18,8\s+26\s+20,0\s+30',s)
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,v):self.parts.append(v)
def content(p):
 t=Text();t.feed(p.read_text());return ' '.join(' '.join(t.parts).split())
staff=content(Z/'staff.html');survey=content(Z/'survey.html');pupils=content(Z/'pupils.html');pocket=content(Z/'pocket.html')
assert 'Vollzeiteinheit' in staff and 'Berufsfachschulen' in staff and 'Mittelschulen' in staff
assert 'Standort im Kanton Zürich' in survey and 'Lehr' in survey and 'Mittelschulen' in pupils and 'Berufsfachschulen' in pocket
f,lo,hi=revised_bounds();cities=f.city.tolist();i=cities.index('Oslo');j=NAMES.index('travel');assert f.iloc[i].commute_min==31 and int(f.iloc[i].commute_min_year)==2009 and f.iloc[i].commute_min_flag=='STALE'
refs={'fixed':[.1125]*6+[.05,.1125,.1125,.05],'equal':[.1]*10}
def score(row,w):
 a=math.sqrt(math.fsum(wi*float(x)**2 for wi,x in zip(w,row)));b=math.sqrt(math.fsum(wi*(1-float(x))**2 for wi,x in zip(w,row)));return 100*a/(a+b)
def compare(a,b,w):
 L=[score(row,w) for row in a];U=[score(row,w) for row in b]
 g=[max(0,max(U[k] for k in range(16) if k!=q)-L[q]) for q in range(16)]
 p=[U[q]>=max(L[k] for k in range(16) if k!=q)-1e-12 for q in range(16)]
 n=[L[q]>=max(U[k] for k in range(16) if k!=q)-1e-12 for q in range(16)]
 return L,U,g,p,n
with (O/'ranks.csv').open(newline='') as ff:ranks=list(csv.DictReader(ff))
with (O/'bounds.csv').open(newline='') as ff:bounds=list(csv.DictReader(ff))
assert len(ranks)==64 and len(bounds)==320
out=[]
for case in ['retained_V203','withdraw_Oslo_commute_proxy']:
 a=lo.copy();b=hi.copy()
 if case.startswith('withdraw'):a[i,j]=0;b[i,j]=1
 for q,city in enumerate(cities):
  for k,ind in enumerate(NAMES):
   row=next(r for r in bounds if (r['scenario'],r['city'],r['indicator'])==(case,city,ind));assert abs(float(row['lower'])-a[q,k])<1e-15 and abs(float(row['upper'])-b[q,k])<1e-15
 for ref,w in refs.items():
  L,U,G,P,N=compare(a,b,w);entries=[r for r in ranks if r['scenario']==case and r['weight_reference']==ref];assert len(entries)==16
  item=next(r for r in report['comparisons'] if r['scenario']==case and r['weight_reference']==ref)
  rec=[cities[k] for k in range(16) if G[k]<=min(G)+1e-12];assert rec==item['recommendation'] and sum(P)==item['possible_champions']==16 and sum(N)==item['necessary_champions']==0
  assert abs(math.fsum(U[k]-L[k] for k in range(16))/16-item['mean_score_width'])<1e-10
  for k,city in enumerate(cities):
   r=next(r for r in entries if r['city']==city)
   for name,v in [('score_lower',L[k]),('score_upper',U[k]),('max_regret',G[k])]:assert abs(float(r[name])-v)<1e-10
   assert (r['possible_champion']=='True')==P[k] and (r['necessary_champion']=='True')==N[k]
  out.append({'scenario':case,'weight_reference':ref,'recommendation':rec,'possible_champions':sum(P),'necessary_champions':sum(N)})
for p,h in bindings.items():assert sha(R/p)==h,p
for p,h in protected.items():assert sha(pathlib.Path(p))==h,p
result={'status':'PASS; controlled source-scope check, no source admission','raw_responses':files,'http_utc_caveat':'Recorded metadata checked against raw bytes, not independently replayed historical HTTP responses.','eurostat':{'indicator':'TT1019V','city':'NO001C','current_label':'Oslo (greater city)','year':2009,'minutes':31,'status_field_present':False,'scope':'Value/year match is a source lead; original CSV lineage and 2009 boundary remain unverified.'},'toi_2009_minutes':{'Oslo_residents':26,'surrounding_municipalities':30,'scope':'Separate work-trip group means; neither replacement nor matched duration distribution.'},'zurich_scope':'Canton-wide school personnel data do not establish a city upper-secondary teacher FTE lower bound paired with a matched pupil upper bound; no new admission.','independent_scalar_city_weight_cases':64,'comparisons':out,'science_bindings_unchanged':len(bindings),'navigation_and_manuscript_files_unchanged':len(protected),'original_csv_sha256':sha(SOURCE),'source_sha256':{str(p.relative_to(R)):sha(p) for p in [pathlib.Path(__file__),O/'summary.json',O/'ranks.csv',O/'bounds.csv',R/'design/task4_user_v203_snapshot.json']}}
(O/'verification.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps(result,indent=2,ensure_ascii=False))
