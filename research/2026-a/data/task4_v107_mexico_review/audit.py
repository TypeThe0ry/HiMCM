"""Aggregate-only independent audit; never emit individual record values."""
import csv,hashlib,io,json,math,subprocess,zipfile
from collections import Counter
from pathlib import Path
from pypdf import PdfReader
P=Path(__file__).resolve().parent;S=P.parent/'task4_v107_mexico'
manifest=json.loads((S/'manifest.json').read_text())
for item in manifest:
 b=(S/item['file']).read_bytes();assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
s=json.loads((S/'summary.json').read_text());q=' '.join(PdfReader(S/'eic2025_cuestionario.pdf').pages[8].extract_text().split())
assert 'último año o grado aprobado' in q and 'No se traslada' in q and '16 a 30 minutos' in q
assert 'Preparatoria o bachillerato general' in q and 'Bachillerato tecnológico' in q
sampling=' '.join(' '.join(p.extract_text().split()) for p in PdfReader(S/'eic2025_sampling_design.pdf').pages)
assert 'probabilístico, estratificado y por conglomerados' in sampling
assert 'estrato y UPM' in sampling and '2025' in sampling
weight={g:Counter() for g in s['groups']};count={g:Counter() for g in s['groups']};n=pop=0;seen=set()
with zipfile.ZipFile(S/'local_only/eic2025_micro_09_csv.zip') as z:
 assert z.testzip() is None
 for row in csv.DictReader(io.TextIOWrapper(z.open('personas09.csv'),encoding='utf-8-sig')):
  n+=1;assert row['CVE_ENT']=='09';w=int(row['FACTOR']);assert w>0;pop+=w
  key=(row['ID_VIV'],row['ID_PERSONA']);assert key not in seen;seen.add(key)
  age=int(row['EDAD']);attendance=row['ASISTEN'];level=int(row['NIVACAD'] or 99);grade=int(row['ESCOLARI'] or 99)
  if age!=999 and not 14<=age<=18:continue
  if attendance=='3':continue
  assert attendance in ['1','9','']
  prepa=level in {4,5,7} and grade in {0,1,2};boundary=level==3 and grade==3;unspecified=level==99 or grade==99
  if not(prepa or boundary or unspecified):continue
  group='other_optional'
  if age!=999 and attendance=='1':
   if prepa:group='prepa_conditional'
   elif boundary:group='boundary3'
  code=row['TIE_TRASLADO_ESCU'];assert code in ['1','2','3','4','5','6','9','']
  count[group][code]+=1;weight[group][code]+=w
assert n==s['person_rows'] and pop==s['expanded_private_household_population']
for g in weight:
 assert dict(weight[g])==s['groups'][g]['weighted'] and dict(count[g])==s['groups'][g]['sample']
ends={str(i+1):(0 if b is None else math.exp(-b/30),math.exp(-a/30)) for i,(a,b) in enumerate([(0,15),(15,30),(30,60),(60,120),(120,None)])}
ends.update({c:(0,1) for c in ['6','9','']})
# Independent fractional-program root: choose optional bin mass whenever its
# coefficient has the favorable sign in numerator - trial_ratio*denominator.
def extreme(base,optional,col,maximum):
 a,b=0.,1.
 for _ in range(80):
  mid=(a+b)/2;value=sum(w*(ends[c][col]-mid) for c,w in base.items())
  value+=sum((max if maximum else min)(0,w*(ends[c][col]-mid)) for c,w in optional.items())
  if value>0:a=mid
  else:b=mid
 return (a+b)/2
base=weight['prepa_conditional'];boundary=weight['boundary3'];other=weight['other_optional'];comparisons={}
for label,known,opt in [('legacy_progression',base+boundary,other),('boundary3_optional',base,boundary+other)]:
 lower=extreme(known,opt,0,False);upper=extreme(known,opt,1,True)
 assert abs(lower-s['scenarios'][label]['utility_lower'])<1e-12 and abs(upper-s['scenarios'][label]['utility_upper'])<1e-12
 comparisons[label]=[lower,upper]
assert not s['current_stage_directly_observed'] and not s['sampling_uncertainty_included'] and not s['main_admission']
repo=P.parents[3]
# No path or row content from the raw microdata is emitted.
ignored=subprocess.run(['/usr/bin/arch','-arm64','/usr/bin/git','check-ignore','-q',str(S/'local_only/eic2025_micro_09_csv.zip')],cwd=repo).returncode==0
assert ignored
out=dict(decision='Verified conditional aggregate descriptors; not city high-school observations',source_summary_sha256=hashlib.sha256((S/'summary.json').read_bytes()).hexdigest(),person_rows=n,weighted_private_household_population=pop,aggregates_reproduced=True,duplicate_person_keys=False,raw_zip_gitignored=True,utility_bounds_independent_fractional_root=comparisons,
 limitations=['Highest completed level/grade is observed; current enrollment stage is inferred under progression restrictions. Boundary3_optional relaxes one such assumption, not all stage ambiguity.','Codes6(no travel),9 and blank retain full uncertainty; bins16/31 use conservative15/30 lower closures.','Expansion weights do not include sampling confidence intervals; ESTRATO/UPM clustered design must be respected in future variance analysis.','Residents in private households, not institutionalized population; school destination may be outside CDMX.','Only aggregate outputs are saved; person keys are used in memory for uniqueness, never published.'])
(P/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
