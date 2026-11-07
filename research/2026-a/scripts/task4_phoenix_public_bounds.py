"""Evidence-limited public-school FTE target; snapshot compatibility stays conditional."""
import hashlib,json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_singapore_coverage_revision import singapore_bounds
from task4_continuous_preferences import feasible_preferences
SOURCE=ROOT/'data/task4_v42_phoenix_coverage'


def utility_lower(student_upper,teacher_lower):
    if np.isnan(student_upper) or student_upper<=0 or not np.isfinite(teacher_lower) or teacher_lower<0:
        raise ValueError('Positive student cap and finite nonnegative FTE required')
    return 0. if np.isinf(student_upper) else 15*teacher_lower/(student_upper+15*teacher_lower)


def main():
    for source in json.loads((SOURCE/'manifest.json').read_text()):
        raw=(SOURCE/source['file']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==source['sha256']
        if 'bytes' in source:assert len(raw)==source['bytes']
    hope_source=json.loads((SOURCE/'hope_source_audit.json').read_text())
    assert hashlib.sha256((SOURCE/hope_source['file']).read_bytes()).hexdigest()==hope_source['sha256']
    a=pd.read_csv(SOURCE/'phoenix_secondary_roster.csv',dtype={'NCESSCH':str})
    assert len(a)==144 and a.NCESSCH.is_unique
    non_target=['PK','KG']+[f'G{x:02d}' for x in range(1,9)]+['G13','UG','AE']
    # In a declared within-9--12 school, N codes outside that range are structural.
    # UG/AE must explicitly be zero/not applicable; missing M/-9 never qualifies.
    eligible=a.within_9_12_only & a[non_target].isin([0,-2]).all(axis=1) & a.FTE.ge(0)
    t=float(a.loc[eligible,'FTE'].sum());s=float(a.target_enrollment_lower.sum())
    missing=a[a.target_enrollment_upper.isna()]
    assert missing.NCESSCH.tolist()==['040386003535']
    assert float(missing.target_enrollment_lower.iloc[0])==0
    known_student_upper=float(a.loc[a.target_enrollment_upper.notna(),'target_enrollment_upper'].sum())
    assert s==70678 and abs(t-2512.97)<1e-8
    api=json.loads((SOURCE/'hope_enrollment_fy2025.json').read_text())
    api=[r for r in api if r['subgroups']=='All']
    assert all(r['educationOrganizationId']==969999 and r['fiscalYear']==2025 for r in api)
    assert len({r['gradeUIDescription'] for r in api})==len(api)==5
    by_grade={r['gradeUIDescription']:r['total'] for r in api}
    count=sum(by_grade[f'Grade {g}'] for g in range(9,13));assert count==by_grade['ALL']==1178
    conditional_upper=known_student_upper+count
    bounded=utility_lower(conditional_upper,t)
    assert utility_lower(np.inf,t)==0 and utility_lower(conditional_upper,0)==0
    # Larger student uncertainty cannot improve a conservative lower utility.
    assert utility_lower(conditional_upper+100,t)<bounded<utility_lower(conditional_upper,t+1)
    for total in [conditional_upper,conditional_upper-1,s]:
        for staff in [t,t+1,t+100]:assert utility_lower(total,staff)>=bounded
    oldlo,oldhi=singapore_bounds();j=NAMES.index('upper_secondary_ptr');i=CITIES.index('Phoenix')
    lo,hi=oldlo.copy(),oldhi.copy();lo[:,j]=0.;hi[:,j]=1.
    baseline,_=summarize(lo,hi,weights());frames=[];stats=[]
    scenarios=[('public_target_unknown',0.),('public_target_snapshot_compatibility_assumed',bounded)]
    for label,value in scenarios:
        l,h=lo.copy(),hi.copy();l[i,j]=value
        keep=np.ones(l.shape,bool);keep[i,j]=False
        np.testing.assert_array_equal(l[keep],lo[keep]);np.testing.assert_array_equal(h,hi)
        f,d=summarize(l,h,weights());f['scenario']=label;frames.append(f)
        stats.append(dict(scenario=label,choice=[CITIES[k] for k in d['minimax_choices']],
            possible_champions=int(f.possible_champion.sum()),changed_ranks_vs_same_target=int((f.decision_rank!=baseline.decision_rank).sum()),
            continuous_alpha_possible=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(l))!=k])['possible']],
            phoenix=f.iloc[i][['score_lower','score_upper','decision_rank','max_regret']].to_dict()))
    # Separate original-target reference; no source assumptions written into it.
    reference,_=summarize(oldlo,oldhi,weights());reference['scenario']='original_v38_reference'
    out=ROOT/'results/task4_v42_phoenix_public';out.mkdir(parents=True,exist_ok=True)
    pd.concat([reference]+frames).to_csv(out/'ranks.csv',index=False)
    a['included_in_FTE_lower']=eligible;a.to_csv(out/'school_resource_audit.csv',index=False)
    result=dict(main_model_changed=False,new_target='Public nonvirtual operational school-location grades9-12 attributed FTE, not all-school headcount or resident access',
        observed_student_lower=s,unconditional_student_upper=None,known_FTE_lower=t,
        hope_official_reported_count=count,hope_snapshot_compatibility_verified=False,
        conditional_student_upper=conditional_upper,conditional_education_lower=bounded,
        unconditional_public_education_bounds=[0,1],upper_endpoint='1 is closure when missing teacher FTE has no finite upper bound',
        source_hashes={p:hashlib.sha256((SOURCE/p).read_bytes()).hexdigest() for p in ['manifest.json','phoenix_secondary_roster.csv','hope_enrollment_fy2025.json','hope_source_audit.json']},scenarios=stats)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
