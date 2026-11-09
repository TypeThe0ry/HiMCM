"""Sharp joint-box sensitivity of the retained twelve commute means (user16 V181)."""
import hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_user_v181_revision import revised_bounds
from task4_user_city_indicators import SOURCE,evaluate
from task4_v5_model import ROOT,NAMES,weights,score
O=ROOT/'results/task4_v187_joint_means'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    O.mkdir(exist_ok=True)
    f,lo,hi=revised_bounds();cities=f.city.tolist();z=cities.index('Zurich');j=NAMES.index('travel')
    means=f.commute_min.to_numpy(float);idx=np.flatnonzero(np.isfinite(means));assert len(cities)==16 and len(idx)==12
    np.testing.assert_allclose(lo[idx,j],np.exp(-means[idx]/30),rtol=0,atol=1e-15)
    np.testing.assert_array_equal(hi[idx,j],np.ones(12))
    protected=[SOURCE,ROOT/'design/task4_user_current_model.json',ROOT/'design/task4_user_current_extensions.json']
    hashes={str(p.relative_to(ROOT)):sha(p) for p in protected}
    def bounds(delta):
        if not 0<=delta<=1:raise ValueError('Declared box radius must be in [0,1]')
        adjusted=means.copy();adjusted[idx]*=1-delta;adjusted[z]=means[z]*(1+delta)
        a=lo.copy();a[idx,j]=np.exp(-adjusted[idx]/30)
        np.testing.assert_array_equal(np.delete(a,j,axis=1),np.delete(lo,j,axis=1))
        np.testing.assert_array_equal(a[np.setdiff1d(np.arange(16),idx)],lo[np.setdiff1d(np.arange(16),idx)])
        return adjusted,a
    thresholds=[];pairs=[];cases=[];ranks=[];vectors=[];bounds_rows=[];corner_checks=[]
    for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
        def table(delta):return evaluate(cities,bounds(delta)[1],hi,w)
        def gap(delta):
            r=table(delta).max_regret.to_numpy();return float(r[z]-np.delete(r,z).min())
        assert gap(0)<0<gap(1)
        root=float(brentq(gap,0,1,xtol=5e-16,rtol=1e-15))
        t=table(root);r=t.max_regret.to_numpy();binding=[cities[i] for i in range(16) if i!=z and abs(r[i]-r[z])<1e-10]
        assert binding==['Oslo'] and abs(gap(root))<1e-10
        threshold=dict(weight_reference=ref,sharp_radius=root,sharp_radius_percent=100*root,binding_rivals=binding,tie_regret=float(r[z]),signed_gap_at_root=gap(root),gap_below=gap(root-1e-7),gap_above=gap(root+1e-7),strict_guarantee='Zurich is the unique minimax-regret recommendation for every mean vector in the box when delta < sharp_radius; at equality a tie is attainable; above it a counterexample exists.')
        assert threshold['gap_below']<0<threshold['gap_above'];thresholds.append(threshold)
        for i,c in enumerate(cities):
            if i==z:continue
            def pair(delta):
                v=table(delta).max_regret.to_numpy();return float(v[z]-v[i])
            crossing=float(brentq(pair,0,1,xtol=5e-16,rtol=1e-15)) if pair(1)>=0 else None
            pairs.append(dict(weight_reference=ref,rival=c,gap_at0=pair(0),gap_at1=pair(1),crossing_radius=crossing))
        finite=[p['crossing_radius'] for p in pairs if p['weight_reference']==ref and p['crossing_radius'] is not None]
        assert abs(min(finite)-root)<1e-12
        for name,delta in [('baseline',0),('five_percent',.05),('ten_percent',.1),('just_below',root-1e-7),('boundary',root),('just_above',root+1e-7)]:
            adjusted,a=bounds(delta);t=table(delta);v=t.max_regret.to_numpy();selected=[cities[i] for i in range(16) if v[i]<=v.min()+1e-10]
            cases.append(dict(weight_reference=ref,case=name,delta=delta,worst_signed_gap=gap(delta),Zurich_strict_for_entire_box=gap(delta)<-1e-10,corner_recommendation=selected,possible_champions_in_corner=int(t.possible_champion.sum()),necessary_champions_in_corner=int(t.necessary_champion.sum()),corner_mean_score_width=float((t.score_upper-t.score_lower).mean())))
            ranks.append(t.assign(weight_reference=ref,case=name,delta=delta))
            vectors.extend(dict(weight_reference=ref,case=name,city=cities[i],original_mean_minutes=float(means[i]),corner_mean_minutes=float(adjusted[i])) for i in idx)
            bounds_rows.extend(dict(weight_reference=ref,case=name,city=c,indicator=n,lower=float(a[i,k]),upper=float(hi[i,k])) for i,c in enumerate(cities) for k,n in enumerate(NAMES))
        # All 4096 box corners corroborate the analytic continuum proof at two radii.
        for delta in [.05,root]:
            bits=((np.arange(4096)[:,None]>>np.arange(12))&1)
            a=np.broadcast_to(lo,(4096,16,10)).copy()
            a[:,idx,j]=np.exp(-means[idx][None,:]*(1+delta*(2*bits-1))/30)
            lower=100*np.sqrt((a*a*w).sum(axis=2))/(np.sqrt((a*a*w).sum(axis=2))+np.sqrt(((1-a)**2*w).sum(axis=2)))
            U=score(hi,w);other=np.array([np.delete(U,i).max() for i in range(16)])
            regrets=np.maximum(0,other[None,:]-lower)
            gaps=regrets[:,z]-np.delete(regrets,z,axis=1).min(axis=1)
            assert abs(float(gaps.max())-gap(delta))<1e-11
            corner_checks.append(dict(weight_reference=ref,delta=delta,corners=4096,max_signed_gap=float(gaps.max()),analytic_corner_gap=gap(delta)))
    pd.concat(ranks,ignore_index=True).to_csv(O/'corner_ranks.csv',index=False)
    for name,rows in [('pairwise_crossings',pairs),('corner_means',vectors),('corner_bounds',bounds_rows)]:pd.DataFrame(rows).to_csv(O/(name+'.csv'),index=False)
    paths=protected+[Path(__file__),ROOT/'scripts/task4_user_v181_revision.py',ROOT/'scripts/task4_user_city_indicators.py',ROOT/'scripts/task4_v5_model.py',ROOT/'scripts/task4_interval_decision.py']
    report=dict(version='V187',primary='V181 unchanged',paper_at_creation='V186',primary_admissions=0,actual_baseline_width_change=0,box_domain=[0,1],means_cities=[cities[i] for i in idx],retained_nonmean_cities=[c for i,c in enumerate(cities) if i not in idx],thresholds=thresholds,cases=cases,corner_checks=corner_checks,source_sha256={str(p.relative_to(ROOT)):sha(p) for p in paths},scope='Declared independent relative box on twelve supplied mean minutes. Other utility entries and all upper bounds fixed; Singapore stage bins retained. Radius is an assumption, not an observed error, confidence level, probability or future trend. Box attainability concerns declared input scenarios, not proof of joint physical realization.',proof='Upper scores constant. Each self-excluded regret depends only on its own lower score and increases with its own mean. Zurich high and all eleven other means low simultaneously maximize R_Z - min(other R). Continuity and monotonicity plus signed endpoint crossings yield the sharp radius.',baseline_mean_width={ref:float((evaluate(cities,lo,hi,w).score_upper-evaluate(cities,lo,hi,w).score_lower).mean()) for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]})
    (O/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    for p in protected:assert sha(p)==hashes[str(p.relative_to(ROOT))]
    _,a,b=revised_bounds();np.testing.assert_array_equal(a,lo);np.testing.assert_array_equal(b,hi)
    print(json.dumps(thresholds,indent=2))
if __name__=='__main__':main()
