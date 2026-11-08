"""Current-source direct travel-scale diagnostics; no scale is selected by rank."""
import json,hashlib
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_current_model import current_bounds
from task4_travel_scale_sensitivity import mean_utility_bounds
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify
from task4_joint_uncertainty_stress import protect_output
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize

SCALES=[15,20,30,45,60]
SOURCES=['task4_v111_mexico_scale','task4_v111_cape_scale','task4_v111_saopaulo_scale','task4_v111_melbourne_scale']

def load_direct():
    records=[];manifest=[]
    for name in SOURCES:
        p=ROOT/'data'/name/'summary.json';r=json.loads(p.read_text())
        records.extend(r['scenarios']);manifest.append(dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    f=pd.DataFrame(records)
    if len(f)!=25 or f.duplicated(['city','tau_minutes']).any():raise ValueError('Need exactly five source cities at five scales')
    for city,g in f.groupby('city'):
        if sorted(g.tau_minutes.tolist())!=SCALES:raise ValueError('Scale coverage differs: '+city)
    return f,manifest

def main():
    lo,hi,config=current_bounds();out=ROOT/'results/task4_v111_travel_scale';protect_output(out,lo,hi,config)
    direct,sources=load_direct();j=NAMES.index('travel');known=(lo[:,j]!=0)|(hi[:,j]!=1)
    if set(np.array(CITIES)[known])!=set(direct.city):raise ValueError('Sources do not match current informative cities')
    baseline,_=summarize(lo,hi,weights(config['fixed_alpha']));frames=[];bounds=[];certificates=[];reports=[]
    for method in ['direct','mean_only']:
        for tau in SCALES:
            l,h=lo.copy(),hi.copy()
            if method=='direct':
                for r in direct[direct.tau_minutes==tau].to_dict('records'):
                    k=CITIES.index(r['city']);l[k,j]=r['utility_lower'];h[k,j]=r['utility_upper']
            else:l[:,j],h[:,j]=mean_utility_bounds(lo[:,j],hi[:,j],tau)
            if tau==30:np.testing.assert_allclose([l,h],[lo,hi],rtol=0,atol=1e-12)
            for a,b in zip([l,h],[lo,hi]):np.testing.assert_array_equal(a[:,np.arange(len(NAMES))!=j],b[:,np.arange(len(NAMES))!=j])
            assert np.all(l[~known,j]==0) and np.all(h[~known,j]==1)
            assert np.isfinite([l,h]).all() and np.all((0<=l)&(l<=h)&(h<=1))
            f,d=summarize(l,h,weights(config['fixed_alpha']));frames.append(f.assign(method=method,tau_minutes=tau));cert=certify(l,h,*config['alpha_range'])
            certificates.extend(dict(**r,method=method,tau_minutes=tau) for r in cert)
            reports.append(dict(method=method,tau_minutes=tau,changed_ranks=int((f.decision_rank!=baseline.decision_rank).sum()),kendall_tau=float(kendalltau(f.decision_rank,baseline.decision_rank).statistic),choice=[CITIES[k] for k in d['minimax_choices']],possible_champions=int(f.possible_champion.sum()),continuous_possible_champions=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(CITIES))!=k],*config['alpha_range'])['possible']],continuous_recommendation=dict(unresolved=sum(not r['certified'] for r in cert),winners=sorted({CITIES[r['winner']] for r in cert if r['certified']})),mean_score_width=float((f.score_upper-f.score_lower).mean())))
            bounds.extend(dict(method=method,tau_minutes=tau,city=c,indicator=n,lower=l[k,m],upper=h[k,m]) for k,c in enumerate(CITIES) for m,n in enumerate(NAMES))
    out.mkdir(exist_ok=True);pd.concat(frames).to_csv(out/'ranks.csv',index=False);pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False);pd.DataFrame(certificates).to_csv(out/'recommendation_certificate.csv',index=False)
    direct.drop(columns=['candidates'],errors='ignore').to_csv(out/'direct_travel_bounds.csv',index=False)
    result=dict(model_version=config['model_version'],fixed_alpha=config['fixed_alpha'],alpha_range=config['alpha_range'],input_bounds_sha256=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest(),main_admitted=False,new_observations=0,source_summaries=sources,scenarios=reports,scope='Five prespecified time scales only; continuous certificates concern alpha, not all intermediate tau. Current memberships, missing mass and source-specific sampling procedures retained. Direct re-extraction and mean-only propagation are alternative sensitivity calculations, not interval intersections or evidence that one nominal CI contains another. Main scale remains30; no tuning to a desired winner.')
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps([{k:v for k,v in r.items() if k!='continuous_possible_champions'} for r in reports],indent=2))
if __name__=='__main__':main()
