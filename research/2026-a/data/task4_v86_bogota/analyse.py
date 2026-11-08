#!/usr/bin/env python3
"""Bogotá PISA2022 domain means and paired contrasts using 10 PVs, 80 Fay-BRR weights.
Usage: python analyse.py  (reads the checked-in derived subset; writes summary/CSV)
"""
import json, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent
SUBJECTS={'MATH':'mathematics','READ':'reading','SCIE':'science'}
REPS=[f'W_FSTURWT{i}' for i in range(1,81)]

def combine(point,rep):
    """point shape(M,), rep shape(M,R); use paired arrays for contrasts."""
    assert point.shape==(10,) and rep.shape==(10,80)
    sampling=(4/80*((rep-point[:,None])**2).sum(axis=1)).mean()
    between=point.var(ddof=1)
    total=sampling+(1+1/len(point))*between
    mean=point.mean();se=np.sqrt(total)
    return {'mean':float(mean),'standard_error':float(se),
            'sampling_variance':float(sampling),'between_pv_variance':float(between),
            'total_variance':float(total),'normal_approx_95_lower':float(mean-1.96*se),
            'normal_approx_95_upper':float(mean+1.96*se)}

def domain_estimates(df,mask,subject):
    d=df.loc[mask]
    pv=d[[f'PV{i}{subject}' for i in range(1,11)]].to_numpy(float)
    w=d.W_FSTUWT.to_numpy(float)
    rw=d[REPS].to_numpy(float)
    assert np.isfinite(pv).all() and np.isfinite(w).all() and np.isfinite(rw).all()
    assert (w>0).all() and (rw>=0).all() and (rw.sum(axis=0)>0).all()
    return (pv*w[:,None]).sum(axis=0)/w.sum(), (pv.T@rw)/rw.sum(axis=0)

def main():
    manifest=json.loads((HERE/'manifest.json').read_text())
    source=HERE/manifest['derived_file']
    assert hashlib.sha256(source.read_bytes()).hexdigest()==manifest['derived_sha256'],'Subset checksum mismatch'
    for filename,expected in manifest['validation_baseline'].items():
        baseline=HERE.parent/'task4_v85_pisa_city'/filename
        assert hashlib.sha256(baseline.read_bytes()).hexdigest()==expected,f'Baseline checksum mismatch: {filename}'
    df=pd.read_csv(source)
    assert len(df)==1986 and set(df.REGION.astype(int))=={17001}
    assert set(df.STRATUM)=={'COL01','COL02','COL03'}
    allmask=np.ones(len(df),dtype=bool);hs=df.ST001D01T.isin([10,11])
    assert hs.any() and not hs.all()
    domains={'all_pisa_grades':allmask,'current_grades_10_11':hs}
    info={}
    for name,mask in domains.items():
        d=df.loc[mask]
        info[name]={'sample_n':len(d),'schools_n':d.CNTSCHID.nunique(),
                    'weighted_population':float(d.W_FSTUWT.sum()),
                    'age_min':float(d.AGE.min()),'age_max':float(d.AGE.max()),
                    'age_missing_n':int(d.AGE.isna().sum()),
                    'grade_counts':{str(k):int(v) for k,v in d.ST001D01T.value_counts(dropna=False).sort_index().items()},
                    'stratum_counts':{str(k):int(v) for k,v in d.STRATUM.value_counts().sort_index().items()}}
    info['current_grades_10_11']['weighted_share_of_all_pisa']=float(df.loc[hs,'W_FSTUWT'].sum()/df.W_FSTUWT.sum())
    records=[];pv_audit=[]
    old=json.loads((HERE.parent/'task4_v85_pisa_city/summary.json').read_text())['outcomes']
    validation=[]
    for subject,label in SUBJECTS.items():
        a,ar=domain_estimates(df,allmask,subject);h,hr=domain_estimates(df,hs,subject)
        for name,p,r in [('all_pisa_grades',a,ar),('current_grades_10_11',h,hr),('paired_highschool_minus_all',h-a,hr-ar)]:
            rec={'city':'Bogota','year':2022,'subject':label,'domain':name,**combine(p,r)}
            records.append(rec)
            for m in range(10):
                pv_audit.append({'subject':label,'domain':name,'pv':m+1,'estimate':float(p[m]),
                    **{f'replicate_{i+1}':float(r[m,i]) for i in range(80)}})
        published=next(o for o in old if o['subject']==label)
        actual=combine(a,ar)
        validation.append({'subject':label,'microdata_mean':actual['mean'],'published_mean':published['mean'],
                           'mean_difference':actual['mean']-published['mean'],
                           'microdata_standard_error':actual['standard_error'],
                           'published_standard_error':published['standard_error'],
                           'standard_error_difference':actual['standard_error']-published['standard_error']})
    # Original microdata rounded PV/weights can differ slightly from production precision.
    assert max(abs(v['mean_difference']) for v in validation)<0.02,validation
    assert max(abs(v['standard_error_difference']) for v in validation)<0.02,validation
    summary={'city':'Bogota','year':2022,'domains':info,'outcomes':records,'published_validation':validation,
      'method':{'plausible_values':10,'replicates':80,'fay_coefficient':0.5,
                'sampling_variance':'mean_m[4/80 sum_r(theta_mr-theta_m)^2]',
                'between_pv_variance':'sample variance of 10 point estimates',
                'total_variance':'sampling_variance + 1.1 * between_pv_variance',
                'paired_difference':'For each PV and replicate first subtract all-grade estimate from grade10/11 estimate, then apply the same variance rules; overlapping domains retain covariance.'},
      'scope':'PISA2022 sampled eligible age-cohort students in Bogota schools, restricted by current grade10 or11. Not a census of all secondary-school students, not all ages14-18, and not a causal school-quality effect. Current grade restriction selects progression as well as learning.',
      'main_admitted':False,
      'interval_scope':'Individual normal-approximate95% uncertainty for population means/paired differences; not simultaneous, not ranges of individual student achievement, not missing-data identified bounds.'}
    (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    pd.DataFrame(records).to_csv(HERE/'outcomes.csv',index=False)
    pd.DataFrame(pv_audit).to_csv(HERE/'plausible_value_replicate_estimates.csv',index=False)
    print(json.dumps({'domains':info,'outcomes':records,'published_validation':validation},indent=2))
if __name__=='__main__':main()
