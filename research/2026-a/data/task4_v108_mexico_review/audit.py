"""Independent aggregate-only raw-data replay of 24-dimensional PSU moments."""
import csv,io,json,hashlib,zipfile,subprocess
from pathlib import Path
from collections import defaultdict,Counter
import numpy as np
from pypdf import PdfReader
P=Path(__file__).resolve().parent;S=P.parent/'task4_v108_mexico_design';RAW=P.parent/'task4_v107_mexico'
m=json.loads((S/'manifest.json').read_text());mom=json.loads((S/m['file']).read_text())
assert hashlib.sha256((S/m['file']).read_bytes()).hexdigest()==m['sha256']
raw=RAW/'local_only/eic2025_micro_09_csv.zip'
assert hashlib.sha256(raw.read_bytes()).hexdigest()==m['source_raw_sha256']
for f,key in [('eic2025_sampling_design.pdf','source_design_sha256'),('eic2025_micro_fd.xlsx','source_dictionary_sha256')]:assert hashlib.sha256((RAW/f).read_bytes()).hexdigest()==m[key]
text=' '.join(' '.join(page.extract_text().split()) for page in PdfReader(RAW/'eic2025_sampling_design.pdf').pages)
assert 'probabilístico, estratificado y por conglomerados' in text and 'una sola etapa' in text and 'sin reemplazo' in text
codes=['1','2','3','4','5','6','9',''];groups=['prepa_conditional','boundary3','other_optional'];v={};weights=defaultdict(set);seen=set();count=0
with zipfile.ZipFile(raw) as z:
 for r in csv.DictReader(io.TextIOWrapper(z.open('personas09.csv'),encoding='utf-8-sig')):
  count+=1;assert r['CVE_ENT']=='09';pid=(r['ID_VIV'],r['ID_PERSONA']);assert pid not in seen;seen.add(pid)
  key=(r['ESTRATO'],r['UPM']);a=v.setdefault(key,np.zeros(24,dtype=np.longdouble));w=int(r['FACTOR']);assert w>0;weights[key].add(w)
  age=int(r['EDAD']);attendance=r['ASISTEN'];level=int(r['NIVACAD'] or 99);grade=int(r['ESCOLARI'] or 99)
  if age!=999 and not 14<=age<=18:continue
  if attendance=='3':continue
  prepa=level in {4,5,7} and grade in {0,1,2};boundary=(level,grade)==(3,3)
  if not(prepa or boundary or level==99 or grade==99):continue
  group=2
  if age!=999 and attendance=='1':group=0 if prepa else 1 if boundary else 2
  a[group*8+codes.index(r['TIE_TRASLADO_ESCU'])]+=w
strata=defaultdict(list)
for (h,j),a in v.items():strata[h].append(a)
assert len(strata)==49 and len(v)==3433 and min(map(len,strata.values()))>1 and count==442778
assert all(len(x)==1 for x in weights.values())
totals=sum(v.values());cross=np.zeros((24,24),dtype=np.longdouble)
# Independent second-moment identity, rather than source's row-wise centering.
for values in strata.values():
 a=np.array(values);n=len(a);s=a.sum(axis=0)
 cross+=(a.T@a-np.outer(s,s)/n)*np.longdouble(n)/(n-1)
assert mom['labels']==[g+':'+(c or 'blank') for g in groups for c in codes]
assert np.array_equal(totals,np.array(mom['weighted_totals']))
saved=np.array(mom['centered_crossproduct'],dtype=np.longdouble);err=float(np.max(abs(cross-saved)))
assert np.allclose(cross,saved,rtol=1e-11,atol=1e-7)
assert np.max(abs(saved-saved.T))<1e-7
assert np.linalg.eigvalsh(np.array(saved,dtype=float)).min()>-1e-6
d=mom['diagnostics'];zero=sum(not np.any(x) for x in v.values())
assert d['psus_zero_target_vector']==zero and d['degrees_freedom']==3384
assert d['stratum_psu_count_distribution']=={str(k):v for k,v in Counter(map(len,strata.values())).items()}
for path in [raw,S/'local_only/psu_weighted_bins.json']:
 assert subprocess.run(['/usr/bin/arch','-arm64','/usr/bin/git','check-ignore','-q',str(path)],cwd=P.parents[3]).returncode==0
ratios=json.loads((S/'candidate_ratios.json').read_text());checked=0;maxse=0.
for scenario in ratios['scenarios'].values():
 for side in scenario.values():
  for r in side['candidates']:
   a=np.array(r['numerator_coefficients'],dtype=np.longdouble);b=np.array(r['denominator_coefficients'],dtype=np.longdouble)
   A=a@totals;B=b@totals;ratio=A/B;g=a-ratio*b;se=np.sqrt(g@cross@g)/B
   assert abs(float(ratio)-r['ratio'])<1e-12 and abs(float(se)-r['taylor_se'])<1e-12
   maxse=max(maxse,float(se));checked+=1
out=dict(decision='Verified sufficient moments for a labeled fixed-weight WR approximation, not the full official design variance',source_moments_sha256=m['sha256'],person_rows=count,strata=49,psus=3433,singleton_strata=0,degrees_freedom=3384,zero_target_psus_retained=zero,checked_dimensions=24,crossproduct_max_absolute_difference=err,checked_candidate_ratio_variances=checked,maximum_candidate_se=maxse,local_raw_and_psu_files_gitignored=True,
 official_design='Single-stage stratified cluster simple random sampling without replacement; full selected areas surveyed.',
 approximation='Source uses final expansion weights as fixed and omits FPC. Final nonresponse adjustment does not establish calibration weights; no natural selection weights or stratum population PSU totals reconstructed.',
 limitations=['Only person-file observed PSUs included; wholly nonresponding sampled PSUs unknown.','Selected-extremum SE is not simultaneous confidence coverage.','Completed schooling remains a current-stage assumption.','No PSU/person IDs or dates are published by this audit.'])
(P/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
