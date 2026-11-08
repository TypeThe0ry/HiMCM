"""V108: selection-aware approximate sampling envelopes for Mexico travel."""
import importlib.util,json,hashlib
import numpy as np
import pandas as pd
from scipy.stats import t,kendalltau
from task4_mexico_2025_revision import mexico_2025_bounds
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify

def inference():
    spec=importlib.util.spec_from_file_location('design108',ROOT/'data/task4_v108_mexico_design/derive_design.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    source=mod.derive_from_moments();df=3433-49;results={}
    for name,sides in source['scenarios'].items():
        result={'point':[sides[s]['estimate'] for s in ['lower','upper']]}
        for label,tail in [('outer',.05/2),('familywise',.05/18)]:
            critical=float(t.ppf(1-tail,df));ends=[];selected=[]
            for side,sign in [('lower',-1),('upper',1)]:
                candidates=sides[side]['candidates']
                assert len(candidates)==9
                values=[r['ratio']+sign*critical*r['taylor_se'] for r in candidates]
                k=int(np.argmin(values) if sign<0 else np.argmax(values))
                ends.append(float(np.clip(values[k],0,1)));selected.append(k)
            result[label]=ends;result[label+'_prefixes']=selected;result[label+'_critical']=critical
        result['candidates']=sides;results[name]=result
    return dict(df=df,nominal_level=.95,input_moments_sha256=source['input_moments_sha256'],scenarios=results,
        qualification='Approximate fixed-final-weight Taylor outer envelope, no FPC. Conditional stage and household coverage; not a finite-sample guarantee or joint confidence claim across cities. Zero observed categories cannot identify unseen population mass.')

def mexico_sampling_bounds(withdraw=False,familywise=False):
    lo,hi=mexico_2025_bounds()
    if not withdraw:
        i,j=CITIES.index('Mexico City'),NAMES.index('travel')
        lo[i,j],hi[i,j]=inference()['scenarios']['boundary3_optional']['familywise' if familywise else 'outer']
    return lo,hi

def main():
    baseline=mexico_2025_bounds();current=mexico_sampling_bounds();back=mexico_sampling_bounds(True)
    i,j=CITIES.index('Mexico City'),NAMES.index('travel');mask=np.ones(baseline[0].shape,bool);mask[i,j]=False
    for a,b,c in zip(baseline,current,back):
        np.testing.assert_array_equal(a[mask],b[mask]);np.testing.assert_array_equal(a,c)
    base,_=summarize(*baseline,weights());frames=[];bounds=[];certs=[];reports=[]
    cases=[('v107_point',baseline),('v108_outer',current),('v108_familywise',mexico_sampling_bounds(familywise=True)),('v108_withdrawn',back)]
    for label,(lo,hi) in cases:
        f,d=summarize(lo,hi,weights());frames.append(f.assign(scenario=label));cert=certify(lo,hi)
        certs.extend(dict(**r,scenario=label) for r in cert)
        reports.append(dict(scenario=label,mexico_travel_interval=[lo[i,j],hi[i,j]],mexico=f.iloc[i][['decision_rank','score_lower','score_upper','max_regret']].to_dict(),changed_ranks=int((f.decision_rank!=base.decision_rank).sum()),kendall_tau=float(kendalltau(f.decision_rank,base.decision_rank).statistic),choice=[CITIES[k] for k in d['minimax_choices']],possible_champions=int(f.possible_champion.sum()),continuous_possible_champions=[c for k,c in enumerate(CITIES) if feasible_preferences(hi[k],lo[np.arange(len(CITIES))!=k])['possible']],continuous_recommendation=dict(unresolved=sum(not r['certified'] for r in cert),winners=sorted({CITIES[r['winner']] for r in cert if r['certified']}))))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=lo[k,m],upper=hi[k,m]) for k,c in enumerate(CITIES) for m,n in enumerate(NAMES))
    out=ROOT/'results/task4_v108_mexico_sampling';out.mkdir(exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False);pd.DataFrame(certs).to_csv(out/'recommendation_certificate.csv',index=False)
    (out/'inference.json').write_text(json.dumps(inference(),indent=2)+'\n')
    summary=dict(model_version='V108',baseline_model='V107',main_admitted=True,changed_cells=1,unchanged_other_cells=249,withdrawal_restores_v107=True,input_bounds_sha256=hashlib.sha256(np.stack(current).astype('<f8').tobytes()).hexdigest(),scenarios=reports)
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(reports,indent=2))
if __name__=='__main__':main()
