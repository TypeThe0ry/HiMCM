"""Observed Shanghai district aggregation diagnostic; no new city observations."""
import hashlib,json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_school_stage_revision import school_bounds
from task4_continuous_preferences import feasible_preferences

def resource_gap(students,teachers,a=15.):
    s=np.asarray(students,dtype=float);t=np.asarray(teachers,dtype=float)
    if s.ndim!=1 or s.shape!=t.shape or not len(s) or np.any(~np.isfinite(s)) or np.any(~np.isfinite(t)) or np.any(s<=0) or np.any(t<0) or not np.isfinite(a) or a<=0:raise ValueError('Invalid matched district counts or anchor')
    p=s/s.sum();q=t/s;mean=t.sum()/s.sum()
    district=a*q/(1+a*q);pooled=a*mean/(1+a*mean);student_mean=p@district
    gap=a*a/(1+a*mean)**2*(p@((q-mean)**2/(1+a*q)))
    np.testing.assert_allclose(pooled-student_mean,gap,rtol=0,atol=1e-14)
    return pooled,float(student_mean),float(gap),district

def main():
    source=ROOT/'data/task4_v32_shanghai';r=json.loads((source/'extracted.json').read_text())
    for m in json.loads((source/'manifest.json').read_text()):
        assert hashlib.sha256((source/m['file']).read_bytes()).hexdigest()==m['sha256']
    ss=r['tables']['students'][1:];tt=r['tables']['teachers'][1:]
    assert [x['district'] for x in ss]==[x['district'] for x in tt]
    s=np.array([x['values'][2] for x in ss]);t=np.array([x['values'][-1] for x in tt])
    assert len(s)==16 and s.sum()==r['students'] and t.sum()==r['teachers']
    pooled,local,gap,u=resource_gap(s,t)
    lo,hi=school_bounds();i=CITIES.index('Shanghai');j=NAMES.index('upper_secondary_ptr')
    np.testing.assert_allclose([lo[i,j],hi[i,j]],[pooled]*2,atol=1e-12,rtol=0)
    base,_=summarize(lo,hi,weights());frames=[];stats=[]
    for label in ['v32_pooled','district_student_weighted']:
        l,h=lo.copy(),hi.copy()
        if label!='v32_pooled':l[i,j]=h[i,j]=local
        keep=np.ones(l.shape,bool);keep[i,j]=False
        np.testing.assert_array_equal(l[keep],lo[keep]);np.testing.assert_array_equal(h[keep],hi[keep])
        f,d=summarize(l,h,weights());f['scenario']=label;frames.append(f)
        possible=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(l))!=k])['possible']]
        stats.append(dict(scenario=label,choice=[CITIES[k] for k in d['minimax_choices']],possible_champions=int(f.possible_champion.sum()),continuous_alpha_possible=possible,changed_ranks=int((f.decision_rank!=base.decision_rank).sum()),kendall_tau=float(kendalltau(f.decision_rank,base.decision_rank).statistic),shanghai=f.iloc[i][['score_lower','score_upper','decision_rank','max_regret']].to_dict()))
    out=ROOT/'results/task4_v33_district_resources';out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(dict(district=[x['district'] for x in ss],students=s,teachers=t,student_weight=s/s.sum(),ptr=s/t,utility=u)).to_csv(out/'districts.csv',index=False)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    result=dict(main_model_changed=False,new_observations=0,pooled_utility=pooled,student_weighted_district_utility=local,aggregation_gap=gap,relative_gap=gap/pooled,source_sha256=hashlib.sha256((source/'extracted.json').read_bytes()).hexdigest(),assumption='District school-location counts, not student home or individual teacher exposure. District-homogeneity sensitivity only; no within-district equality evidence. No citywide comparability improvement claimed.',scenarios=stats)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
