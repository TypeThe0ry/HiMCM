"""Separate student-weighted school-attributed resource target, not pooled PTR."""
import hashlib,json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_delhi_school_revision import delhi_bounds
from task4_continuous_preferences import feasible_preferences

def resource_bounds(students,teacher_caps,anchor=15.):
    s=np.asarray(students,dtype=float);t=np.asarray(teacher_caps,dtype=float)
    if s.ndim!=1 or s.shape!=t.shape or not len(s) or np.any(~np.isfinite(s)) or np.any(s<=0) or np.any(np.isinf(t)) or np.any(t[~np.isnan(t)]<0) or not np.isfinite(anchor) or anchor<=0:raise ValueError('Invalid school counts')
    known=~np.isnan(t);caps=np.ones(len(s));caps[known]=anchor*t[known]/(s[known]+anchor*t[known]);p=s/s.sum()
    return 0.,float(p@caps),float(p[~known].sum()),caps

def main():
    src=ROOT/'data/task4_v36_london'
    for m in json.loads((src/'manifest.json').read_text()):
        assert hashlib.sha256((src/m['file']).read_bytes()).hexdigest()==m['sha256']
    a=pd.read_csv(src/'school_match.csv');a=a[a.upper_students>0].copy();assert a.urn.is_unique
    assert len(a)==411 and a.upper_students.sum()==106046
    low,cap,missing,caps=resource_bounds(a.upper_students,a.teacher_headcount)
    assert a.loc[a.teacher_headcount.isna(),'upper_students'].sum()==772
    a['student_weight']=a.upper_students/a.upper_students.sum();a['resource_lower']=0.;a['resource_upper']=caps
    oldlo,oldhi=delhi_bounds();j=NAMES.index('upper_secondary_ptr');i=CITIES.index('London')
    # New target in ALL cities. Pooled PTR values cannot be carried over as points.
    lo,hi=oldlo.copy(),oldhi.copy();lo[:,j]=0.;hi[:,j]=1.
    baseline,_=summarize(lo,hi,weights());frames=[];stats=[]
    for name in ['new_target_unknown','new_target_london_school_cap']:
        l,h=lo.copy(),hi.copy()
        if name.endswith('school_cap'):l[i,j],h[i,j]=low,cap
        np.testing.assert_array_equal(l[:,np.arange(l.shape[1])!=j],oldlo[:,np.arange(l.shape[1])!=j])
        np.testing.assert_array_equal(h[:,np.arange(h.shape[1])!=j],oldhi[:,np.arange(h.shape[1])!=j])
        f,d=summarize(l,h,weights());f['scenario']=name;frames.append(f)
        stats.append(dict(scenario=name,choice=[CITIES[k] for k in d['minimax_choices']],possible_champions=int(f.possible_champion.sum()),continuous_alpha_possible=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(l))!=k])['possible']],changed_ranks_vs_same_target=int((f.decision_rank!=baseline.decision_rank).sum()),kendall_tau_vs_same_target=float(kendalltau(f.decision_rank,baseline.decision_rank).statistic),london=f.iloc[i][['score_lower','score_upper','decision_rank','max_regret']].to_dict()))
    out=ROOT/'results/task4_v37_school_resources';out.mkdir(parents=True,exist_ok=True)
    a.to_csv(out/'school_bounds.csv',index=False);pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    result=dict(main_model_changed=False,new_target=True,new_admitted_pooled_ptr_cells=0,school_resource_bounds=[low,cap],unknown_student_mass=missing,other_cities_new_target='unknown [0,1], never copy pooled PTR point values',definition='Student-weighted mean of f(attributed upper-stage teacher equivalents / Year12-13 pupils) in London state-funded secondary schools. November2024 school-attributed headcounts bound unknown allocation; January2025 pupil weights. Reporting-rule and two-snapshot historical index, not actual individual teacher exposure, measured FTE or current performance.',source_hashes={p:hashlib.sha256((src/p).read_bytes()).hexdigest() for p in ['manifest.json','school_match.csv','summary.json','extract.py']},scenarios=stats)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='source_hashes'},indent=2))
if __name__=='__main__':main()
