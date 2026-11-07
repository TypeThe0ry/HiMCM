"""Independent source/design audit; does not modify original data or main model."""
import csv,io,json,hashlib,math,importlib.util
from pathlib import Path
from collections import Counter,defaultdict
from zipfile import ZipFile
import numpy as np
import pandas as pd
from scipy.stats import t
P=Path(__file__).resolve().parent
source=P/'../task4_v63_cape_travel'
with ZipFile(source/'GHS2025.zip') as z:
 rows=list(csv.DictReader(io.TextIOWrapper(z.open('PERSON2025.csv'),encoding='utf-8-sig')))
city=[r for r in rows if int(r['metro_code'])==2]
assert len({(r['uqnr'],r['personnr']) for r in rows})==len(rows)
assert all(math.isfinite(float(r['person_wgt'])) and float(r['person_wgt'])>0 for r in city)
strata=set(r['stratum'] for r in city)
assert not any(r['stratum'] in strata and int(r['metro_code'])!=2 for r in rows)
psu_strata=defaultdict(set)
for r in rows:psu_strata[r['psu']].add(r['stratum'])
assert all(len(a)==1 for a in psu_strata.values())
def member(r):return int(r['edu_attend'])==1 and int(r['edu_edui'])==2 and int(r['edu_corr'])==2 and int(r['edu_grde']) in (10,11,12) and 14<=int(r['age'])<=18
selected=[r for r in city if member(r)]
assert len(selected)==182 and Counter(r['edu_time'] for r in selected)==Counter({'1':82,'2':68,'3':25,'4':5,'5':2})
bins={1:(0,15),2:(15,30),3:(30,60),4:(60,90),5:(90,math.inf)}
def u(r,k):
 a,b=bins.get(int(r['edu_time']),(0,math.inf));return math.exp(-(b if k==0 else a)/30)
W=sum(float(r['person_wgt']) for r in selected)
psus=defaultdict(set)
for r in city:psus[r['stratum']].add(r['psu'])
assert min(map(len,psus.values()))>=2
df=sum(map(len,psus.values()))-len(psus)
est=[];se=[]
for k in (0,1):
 mean=sum(float(r['person_wgt'])*u(r,k) for r in selected)/W
 cluster={(s,p):0. for s,a in psus.items() for p in a}
 for r in selected:cluster[r['stratum'],r['psu']]+=float(r['person_wgt'])*(u(r,k)-mean)/W
 variance=0
 for s,a in psus.items():
  vals=[cluster[s,p] for p in a];m=len(vals);bar=sum(vals)/m
  variance+=m/(m-1)*sum((v-bar)**2 for v in vals)
 est.append(mean);se.append(math.sqrt(variance))
crit=float(t.ppf(.9875,df));envelope=[max(0,est[0]-crit*se[0]),min(1,est[1]+crit*se[1])]
# Cross-check prior implementation without allowing it to write any artifacts.
spec=importlib.util.spec_from_file_location('legacy',P/'../task4_v30_cape_town/inference.py');legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
frame=pd.DataFrame(city)
for c in ['person_wgt','stratum','psu']:frame[c]=pd.to_numeric(frame[c])
old=legacy.endpoint_envelope(frame,[member(r) for r in city],[u(r,0) for r in city],[u(r,1) for r in city])
np.testing.assert_allclose(envelope,old['joint_95_percent_approximate_envelope'],rtol=0,atol=1e-14)
spec=importlib.util.spec_from_file_location('classifier',P/'../task4_v30_cape_town/extract.py');classifier=importlib.util.module_from_spec(spec);spec.loader.exec_module(classifier)
classes=Counter(classifier.classify(r,(14,18)) for r in city);assert classes['optional']==0
meta=(source/'metadata.txt').read_text();question=(source/'questionnaire.txt').read_text()
for term in ['02 = WC – City of Cape Town','Which grade is','one\n          direction only','two-stage, stratified design','person_wgt']:
 assert term in meta,term
assert 'EDU8:' in question and 'EDU12:' in question
result=dict(source_files={n:hashlib.sha256((source/n).read_bytes()).hexdigest() for n in ['GHS2025.zip','metadata.pdf','questionnaire.pdf']},
 national_person_rows=len(rows),city_person_rows=len(city),target_n=len(selected),target_households=len({r['uqnr'] for r in selected}),
 target_psus=len({r['psu'] for r in selected}),all_city_psus=sum(map(len,psus.values())),strata=len(psus),min_psus_per_stratum=min(map(len,psus.values())),degrees_of_freedom=df,
 eligibility_classes=dict(classes),time_codes=dict(Counter(r['edu_time'] for r in selected)),point_bounds=est,endpoint_standard_errors=se,critical_value=crit,approximate_joint95_envelope=envelope,
 prior_inference_function_matches=True,current_grade_verified=True,time_bin_codes_unchanged=True,city_design_strata_exclusive=True,positive_weights=True,
 uncertainty_limitations=['Public calibrated weights treated fixed; calibration estimation omitted.','No FPC or replicate weights supplied to this calculation.','Ultimate-cluster Taylor approximation to two-stage PPS design; not exact confidence set.','No causal inference or paired-year trend test; 2023/2025 overlap/covariance not established.','Collective student hostels excluded by source; source excludes unweightable item-nonresponse records.'],
 metadata_notes=['Design chapter labels 2013 master sample while stratum field description refers to2006; retain documented IDs, do not infer redesign from stale field prose.','Actual design counts are recomputed from2025 public file rather than copied from2023.'])
(P/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
