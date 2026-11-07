"""Recompute travel-scale sensitivity from retained durations and original bins.
Same scoring model, memberships, weights and sampling methods as V23.
"""
import hashlib
import importlib.util
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_roster_coverage_comparison import current_bounds
from task4_continuous_preferences import feasible_preferences
from task4_school_revision import grouped_utility


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def bins_at_scale(counts,tau):
    if not np.isfinite(tau) or tau<=0:raise ValueError('Positive finite time scale required')
    edges={str(k+1):(a,b) for k,(a,b) in enumerate(zip([0,15,30,60,120],[15,30,60,120,np.inf]))}
    rows=[]
    for code,w in counts.items():
        if code in edges:
            a,b=edges[code];lo,hi=np.exp(-b/tau),np.exp(-a/tau)
        elif code in ('','6','9'):lo,hi=0.,1.
        else:raise ValueError('Unknown school-travel code')
        rows.append(dict(weight=w,lower=lo,upper=hi))
    return pd.DataFrame(rows,columns=['weight','lower','upper'])


def local_recomputation():
    """Singapore bins, Mexico membership bins, Melbourne full weighted roster."""
    membership=module('nyc_membership_v26','data/task4_v20_nyc_travel/extract_commute.py').membership_bounds
    melb=module('melb_roster_v26','data/task4_v23_melbourne_roster/extract_roster.py')
    roster,_,_=melb.load();a=roster[(roster.agegroup=='15->19')&roster.has_person_weight].copy()
    assert len(a)==170 and int(a.has_observed_journey.sum())==107
    replicates=a[[f'perspoststratweight_GROUP_{r}' for r in range(1,11)]].to_numpy()
    mx_path=ROOT/'data/task4_v23_mexico_membership/summary.json';mexico=json.loads(mx_path.read_text())
    for r in mexico['sources']:
        p=mx_path.parent/r['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
    mx=mexico['scopes']['age3_17']
    sgpath=ROOT/'data/task4_school/sg_travel_api.json'
    sgmeta=next(r for r in json.loads((sgpath.parent/'manifest.json').read_text()) if r['file']==sgpath.name)
    assert hashlib.sha256(sgpath.read_bytes()).hexdigest()==sgmeta['sha256']
    sg=json.loads(sgpath.read_text())['result']['records']
    sg=pd.DataFrame(sg).set_index('Number')
    order=['Up to 15','16 - 30','31 - 45','46 - 60','More than 60']
    results=[]
    for tau in [15,20,30,45,60]:
        endpoints=[grouped_utility(sg.loc[order,field].to_numpy(float),tau) for field in ['Secondary_Total','Post_Secondary_Non_Tertiary_Total']]
        results.append(dict(city='Singapore',tau_minutes=tau,utility_lower=min(x[0] for x in endpoints),utility_upper=max(x[1] for x in endpoints),method='original census time bins and unknown stage-mixture weights'))
        lo,hi=membership(bins_at_scale(mx['known_time_bins'],tau),bins_at_scale(mx['corrected_optional_time_bins'],tau))
        results.append(dict(city='Mexico City',tau_minutes=tau,utility_lower=lo,utility_upper=hi,method='original time bins; optional attendance and age membership retained'))
        u=np.exp(-a.journey_elapsed_time.fillna(0).to_numpy()/tau)
        lower=np.where(a.has_observed_journey,u,0.);upper=np.where(a.has_observed_journey,u,1.)
        point=melb.weighted_bounds(lower,upper,a.perspoststratweight)
        envelope=melb.jackknife_envelope(lower,upper,a.perspoststratweight,replicates)
        results.append(dict(city='Melbourne',tau_minutes=tau,utility_lower=envelope['lower'],utility_upper=envelope['upper'],point_lower=float(point[0]),point_upper=float(point[1]),method='first person journey; unknown journeys retained; same 10 official replicate person weights'))
    return results


def main():
    records=local_recomputation()
    ny_path=ROOT/'data/task4_v26_nyc_tau/summary.json';sp_path=ROOT/'data/task4_v26_saopaulo_tau/summary.json'
    for city,path in [('New York',ny_path),('Sao Paulo',sp_path)]:
        source=json.loads(path.read_text())
        for r in source['scenarios']:
            if city=='New York' and r['age_scope']!='under19':continue
            records.append(dict(city=city,tau_minutes=r['tau_minutes'],utility_lower=r['sampling_lower'],utility_upper=r['sampling_upper'],point_lower=r['utility_lower'],point_upper=r['utility_upper'],method='same exploratory household resampling, rerun from person durations'))
    direct=pd.DataFrame(records)
    assert len(direct)==25 and not direct.duplicated(['city','tau_minutes']).any()
    lo,hi=current_bounds();j=NAMES.index('travel');base,_=summarize(lo,hi,weights())
    v25=pd.read_csv(ROOT/'results/task4_v25_travel_scale/ranks.csv')
    informative={CITIES[k] for k in range(len(CITIES)) if lo[k,j]!=0 or hi[k,j]!=1}
    assert informative==set(direct.city)
    frames=[];rows=[]
    for tau in [15,20,30,45,60]:
        l,h=lo.copy(),hi.copy()
        for r in direct[direct.tau_minutes==tau].to_dict('records'):
            i=CITIES.index(r['city']);l[i,j]=r['utility_lower'];h[i,j]=r['utility_upper']
        if tau==30:np.testing.assert_allclose(np.stack([l,h]),np.stack([lo,hi]),rtol=0,atol=1e-12)
        assert np.all((0<=l)&(l<=h)&(h<=1))
        np.testing.assert_array_equal(l[:,np.arange(len(NAMES))!=j],lo[:,np.arange(len(NAMES))!=j])
        np.testing.assert_array_equal(h[:,np.arange(len(NAMES))!=j],hi[:,np.arange(len(NAMES))!=j])
        f,d=summarize(l,h,weights());f['tau_minutes']=tau;frames.append(f)
        prior=v25[v25.tau_minutes==tau].reset_index(drop=True);assert prior.city.tolist()==CITIES
        possible=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(l))!=k])['possible']]
        rows.append(dict(tau_minutes=tau,minimax_choices=[CITIES[k] for k in d['minimax_choices']],minimax_regret=d['minimax_regret'],
            fixed_possible_champions=int(f.possible_champion.sum()),continuous_alpha_possible_champions=possible,
            changed_ranks_vs_tau30=int((f.decision_rank!=base.decision_rank).sum()),
            changed_ranks_vs_v25=int((f.decision_rank!=prior.decision_rank).sum()),
            kendall_tau_vs_tau30=float(kendalltau(f.decision_rank,base.decision_rank).statistic),
            mean_score_width=float((f.score_upper-f.score_lower).mean()),
            mean_width_change_vs_v25=float((f.score_upper-f.score_lower).mean()-(prior.score_upper-prior.score_lower).mean()),
            selected_ranks={c:int(f.iloc[CITIES.index(c)].decision_rank) for c in ['Singapore','Melbourne','Sao Paulo','New York','Mexico City','Phoenix']}))
    out=ROOT/'results/task4_v26_direct_travel_scale';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);direct.to_csv(out/'travel_bounds.csv',index=False)
    paths=[ny_path,sp_path,ROOT/'data/task4_v23_mexico_membership/summary.json',ROOT/'data/task4_school/sg_travel_api.json',ROOT/'data/task4_v23_melbourne_roster/summary.json',ROOT/'results/task4_v23_roster_coverage/utility_bounds.csv']
    (out/'summary.json').write_text(json.dumps(dict(main_admitted=False,new_observations=0,alpha_fixed_for_ranks=.1,
        alpha_range_for_possible_champions=[.05,.2],method='Direct re-evaluation of retained person durations or original time bins; same scope and sampling procedures.',
        source_inputs=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths],scenarios=rows),indent=2)+'\n')
    print(pd.DataFrame([{k:v for k,v in r.items() if k!='continuous_alpha_possible_champions'} for r in rows]).to_string(index=False))

if __name__=='__main__':main()
