"""Observed-record HS allocation outer bounds; never a city census estimate."""
from pathlib import Path
import hashlib,json,zipfile
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent

def utility(n,t):return 15*t/(n+15*t)

def extract():
    for item in json.loads((HERE/'reused_sources.json').read_text()):
        raw=(HERE.parent/item['file']).read_bytes()
        assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
    p=HERE.parent/'task4_v83_phoenix_private'
    ids=pd.read_csv(p/'released_city_records.csv').PPIN.tolist()
    with zipfile.ZipFile(p/'pss2324_pu_csv.zip') as z:
        assert z.testzip() is None
        raw=pd.read_csv(z.open('pss2324_pu.csv'),encoding='cp1252',low_memory=False)
    assert raw.PPIN.is_unique and len(ids)==len(set(ids))==76
    f=raw[raw.PPIN.isin(ids)].copy();assert len(f)==76
    # Q4 pairs include ungraded, pre-K, transitional grades and grades K-12.
    offers=[f'P{k}' for k in range(135,296,10)]
    counts=[f'P{k+5}' for k in range(135,296,10)]
    for offer,count in zip(offers,counts):
        assert f[offer].isin([1,2]).all()
        assert f.loc[f[offer]==2,count].isna().all()
        assert f.loc[f[offer]==1,count].notna().all()
        assert (f.loc[f[offer]==1,count]>0).all()
    filled=f[counts].fillna(0)
    f['hs_students']=filled[['P270','P280','P290','P300']].sum(axis=1)
    f['ungraded_students']=filled.P140
    # Nursery/pre-K omitted: Q10 teacher time explicitly excludes pre-K-only teaching.
    f['lower_stage_students']=filled[[f'P{k}' for k in range(160,261,10)]].sum(axis=1)
    f['pure_hs']=(f.hs_students>0)&(f.ungraded_students==0)&(f.lower_stage_students==0)
    f['possible_hs']=(f.hs_students>0)|(f.ungraded_students>0)
    tc=['P385','P390','P395','P400','P405'];x=f[tc].to_numpy(float)
    assert np.isfinite(x).all() and (x>=0).all()
    f['allstage_time_lower']=x@np.array([1,.75,.5,.25,0])
    f['allstage_time_upper']=x@np.array([1,1,.75,.5,.25])
    f['unrounded_midpoint_fte']=x@np.array([1,.875,.625,.375,.125])
    assert np.max(abs(f.unrounded_midpoint_fte-f.NUMTEACH))<=.050000001
    f['hs_time_lower']=np.where(f.pure_hs,f.allstage_time_lower,0)
    f['hs_time_upper']=np.where(f.possible_hs,f.allstage_time_upper,0)
    mode=['P411','P412','P413'];assert f[mode].isin([1,2]).all().all()
    relevant=offers+counts+tc+mode
    f['relevant_flagged']=(f[['F_'+c for c in relevant]]!=0).any(axis=1)
    hs=f[f.hs_students>0];possible=f[f.possible_hs]
    assert len(hs)==33 and len(possible)==36 and f.pure_hs.sum()==7
    assert not possible.relevant_flagged.any()
    assert possible.P411.eq(1).all() # availability, not actual attendance
    n=float(hs.hs_students.sum());ug=float(f.ungraded_students.sum())
    low=float(f.hs_time_lower.sum());upper=float(hs.allstage_time_upper.sum());upper_ug=float(possible.allstage_time_upper.sum())
    assert (n,ug,low,upper,upper_ug)==(6109.,91.,201.25,909.5,974.5)
    naive_mid=float(hs.NUMTEACH.sum());naive_lower=float(hs.allstage_time_lower.sum())
    b0=[utility(n,naive_lower),utility(n,upper)]
    b1=[utility(n,low),utility(n,upper)]
    b2=[utility(n+ug,low),utility(n,upper_ug)]
    record=dict(school_year='2023-2024',scope='Unweighted released private-school records within the V83 current-boundary overlay; not full city, residents or exact ages14-18',city_released_records=len(f),explicit_hs_records=len(hs),pure_hs_records=int(f.pure_hs.sum()),potential_hs_including_ungraded_records=len(possible),ungraded_records=int((f.ungraded_students>0).sum()),ungraded_only_additional_records=int(((f.hs_students==0)&(f.ungraded_students>0)).sum()),explicit_hs_students=int(n),potential_ungraded_hs_students_upper=int(ug),relevant_flagged_possible_records=int(possible.relevant_flagged.sum()),mode_availability=dict(inperson_records=int(possible.P411.eq(1).sum()),virtual_records=int(possible.P412.eq(1).sum()),hybrid_records=int(possible.P413.eq(1).sum()),inperson_only_records=int((possible.P412.eq(2)&possible.P413.eq(2)).sum())),same_explicit_grade_cohort_comparison=dict(student_count=int(n),allstage_midpoint_teacher_fte=naive_mid,naive_allstage_midpoint_utility=utility(n,naive_mid),allstage_worktime_interval=[naive_lower,upper],allstage_worktime_only_utility_interval=b0,hs_allocation_teacher_interval=[low,upper],hs_allocation_utility_interval=b1,worktime_only_width=b0[1]-b0[0],hs_allocation_width=b1[1]-b1[0],width_ratio=(b1[1]-b1[0])/(b0[1]-b0[0]),lower_endpoint_drop=b0[0]-b1[0],interpretation='Common explicit9-12 N. Allstage-midpoint and worktime-only calculations allocate every reported K12 teaching hour to HS and are contrast scenarios, not valid observed HS PTRs.'),including_potential_ungraded=dict(student_interval=[n,n+ug],teacher_interval=[low,upper_ug],utility_outer_interval=b2,sharp_identified_set_claimed=False,interpretation='Broader potential-stage population; UG allocation and teacher allocation are both unknown. Rectangular outer bounds, not a sample confidence interval.'),main_admitted=False,city_bound_unchanged=[0,1],population_conditions='Unobserved schools, nonresponse, modality shares, public/private year alignment and historical boundary remain unresolved; finite observed-subset bounds do not bound entire-city N or T.')
    cols=['PPIN','PINST','hs_students','ungraded_students','lower_stage_students','pure_hs','possible_hs','allstage_time_lower','allstage_time_upper','NUMTEACH','hs_time_lower','hs_time_upper','relevant_flagged']+mode+tc
    f[cols].to_csv(HERE/'school_allocation.csv',index=False,lineterminator='\n')
    (HERE/'summary.json').write_text(json.dumps(record,indent=2)+'\n');return record
if __name__=='__main__':print(json.dumps(extract(),indent=2))
