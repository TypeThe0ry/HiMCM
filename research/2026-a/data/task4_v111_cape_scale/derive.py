"""Cape Town travel-scale sensitivity; aggregate-only release and offline replay.
Run --rebuild to recompute sufficient statistics from the existing ignored ZIP.
"""
import argparse,hashlib,json
from pathlib import Path
from zipfile import ZipFile
import numpy as np
import pandas as pd
from scipy.stats import t
P=Path(__file__).resolve().parent;OLD=P.parent/'task4_v63_cape_travel';ROOT=P.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rebuild():
 manifest=json.loads((OLD/'manifest.json').read_text());entry=next(x for x in manifest if x['file']=='GHS2025.zip');assert sha(OLD/'GHS2025.zip')==entry['sha256']
 with ZipFile(OLD/'GHS2025.zip') as z:f=pd.read_csv(z.open('PERSON2025.csv'))
 assert not f[['uqnr','personnr']].duplicated().any()
 strata=f.loc[f.metro_code==2,'stratum'].unique();f=f.loc[f.stratum.isin(strata)].reset_index(drop=True)
 assert (f.metro_code==2).all() and (f.groupby('psu').stratum.nunique()==1).all()
 domain=(f.edu_attend.eq(1)&f.edu_edui.eq(2)&f.edu_corr.eq(2)&f.edu_grde.isin([10,11,12])&f.age.between(14,18))
 assert json.loads((OLD/'summary.json').read_text())['ages14_18']['optional']['n']==0
 w=f.person_wgt.to_numpy();assert np.isfinite(w).all() and (w>0).all()
 bins=f.edu_time.where(f.edu_time.isin([1,2,3,4,5]),0).astype(int)
 x=np.column_stack([w*domain*(bins==k) for k in range(6)])
 work=pd.DataFrame(x);work['stratum']=f.stratum;work['psu']=f.psu
 psu=work.groupby(['stratum','psu']).sum();counts=psu.groupby(level=0).size();assert (counts>=2).all()
 cov=np.zeros((6,6))
 for _,block in psu.groupby(level=0):
  v=block.to_numpy();center=v-v.mean(0);cov+=len(v)/(len(v)-1)*(center.T@center)
 result=dict(bin_order=['unknown','0-15','15-30','30-60','60-90','90-infinity'],weighted_totals=x.sum(0).tolist(),centered_psu_crossproduct=cov.tolist(),n=int(domain.sum()),weighted_population=float(w[domain].sum()),psus=len(psu),strata=len(counts),domain_psus=int(f.loc[domain,['stratum','psu']].drop_duplicates().shape[0]),zero_target_psus=int((psu.sum(1)==0).sum()),degrees_of_freedom=int(len(psu)-len(counts)),source_zip_sha256=entry['sha256'])
 (P/'aggregate_moments.json').write_text(json.dumps(result,indent=2)+'\n')
def derive():
 m=json.loads((P/'aggregate_moments.json').read_text());tot=np.array(m['weighted_totals']);cov=np.array(m['centered_psu_crossproduct']);den=tot.sum();critical=t.ppf(.9875,m['degrees_of_freedom']);results=[]
 for tau in [15,20,30,45,60]:
  low=np.r_[0,np.exp(-np.array([15,30,60,90,np.inf])/tau)];high=np.r_[1,np.exp(-np.array([0,15,30,60,90])/tau)]
  estimates=[];ses=[]
  for values in [low,high]:
   est=values@tot/den;gradient=(values-est)/den;var=gradient@cov@gradient
   estimates.append(float(est));ses.append(float(np.sqrt(max(0,var))))
  envelope=[max(0,estimates[0]-critical*ses[0]),min(1,estimates[1]+critical*ses[1])]
  results.append(dict(tau_minutes=tau,point_bounds=estimates,endpoint_standard_errors=ses,joint_95_percent_approximate_envelope=envelope))
 old=json.loads((OLD/'inference_summary.json').read_text())['age14_18'];r=results[2]
 for key in ['point_bounds','endpoint_standard_errors','joint_95_percent_approximate_envelope']:np.testing.assert_allclose(r[key],old[key],rtol=0,atol=2e-14)
 current=pd.read_csv(ROOT/'results/task4_v108_intake/utility_bounds.csv');row=current[(current.city=='Cape Town')&(current.indicator=='travel')].iloc[0]
 np.testing.assert_allclose(r['joint_95_percent_approximate_envelope'],[row.lower,row.upper],rtol=0,atol=2e-14)
 sources=[OLD/'manifest.json',OLD/'extract.py',OLD/'inference.py',OLD/'inference_summary.json',P.parent/'task4_v30_cape_town/inference.py',ROOT/'results/task4_v108_intake/utility_bounds.csv',P/'aggregate_moments.json',P/'derive.py']
 result=dict(city='Cape Town',survey='GHS2025',population='Resident formal in-person pupils in grades10-12, ages14-18',n=m['n'],weighted_population=m['weighted_population'],psus=m['psus'],strata=m['strata'],domain_psus=m['domain_psus'],zero_target_psus=m['zero_target_psus'],degrees_of_freedom=m['degrees_of_freedom'],critical_value=float(critical),tau30_matches_current=True,results=results,scenarios=[dict(city='Cape Town',tau_minutes=r['tau_minutes'],utility_lower=r['joint_95_percent_approximate_envelope'][0],utility_upper=r['joint_95_percent_approximate_envelope'][1],point_bounds=r['point_bounds']) for r in results],source_hashes={str(p.relative_to(ROOT)):sha(p) for p in sources},source_zip_sha256=m['source_zip_sha256'],method='Same stratified-PSU Taylor ratio linearization and Bonferroni two endpoint intervals as V63; compressed six-bin moments retain zero-domain PSUs.',limitations='Calibrated weights treated as fixed; no FPC or calibration residual adjustment. Approximate per-scale 95% endpoint envelopes, not a simultaneous band over five scales. Conservative bin closures; unknown time [0,1]; no within-bin imputation. Survey coverage/recorded eligibility conditional. Scale choice changes utility preferences, not observed travel.',main_admitted=False,new_observations=0)
 (P/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(results,indent=2))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--rebuild',action='store_true');args=parser.parse_args()
 if args.rebuild:rebuild()
 derive()
