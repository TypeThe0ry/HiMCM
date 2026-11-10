"""Conditional V203 commute-source diagnostics; no Monte Carlo or source admission."""
from pathlib import Path
import hashlib, json, math
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_user_city_indicators import SOURCE, evaluate
from task4_v5_model import ROOT, NAMES, weights
O=ROOT/'results/task4_v205_source_diagnostics'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def scalar(a,b,w):
    def score(x):
        bad=np.sqrt(np.sum(w*x*x,axis=-1)); good=np.sqrt(np.sum(w*(1-x)**2,axis=-1))
        return 100*bad/(bad+good)
    l,u=score(a),score(b); c=np.array([max(np.delete(u,i)) for i in range(len(u))]);return l,u,np.maximum(0,c-l)
def main():
    import task4_user_v205_revision as staged
    import task4_user_v204_revision as previous
    snapshot=ROOT/'design/task4_user_v205_snapshot.json'; snap=json.loads(snapshot.read_text()); bindings={**snap['upstream_source_sha256'],**snap['source_sha256']}; assert len(bindings)==773
    for name,h in bindings.items():assert sha(ROOT/name)==h,name
    f,lo,hi=staged.revised_bounds();oldf,oldlo,oldhi=previous.revised_bounds()
    cities=f.city.tolist(); n=len(cities); j=NAMES.index('travel'); z=cities.index('Zurich'); means=f.commute_min.to_numpy(float); idx=np.flatnonzero(np.isfinite(means)); assert n==16 and len(idx)==12 and cities==oldf.city.tolist()
    np.testing.assert_array_equal(hi,oldhi)
    changed=np.argwhere(lo!=oldlo); assert changed.tolist()==[[cities.index('Prague'),NAMES.index('public_transport_density')]]
    np.testing.assert_allclose(lo[idx,j],np.exp(-means[idx]/30),atol=1e-15,rtol=0);np.testing.assert_array_equal(hi[idx,j],np.ones(12))
    assert [cities[i] for i in range(n) if i not in idx]==['Vienna','Warsaw','Singapore','Tokyo']
    O.mkdir(parents=True,exist_ok=False)
    def save(name,data):
        if isinstance(data,pd.DataFrame):data.to_csv(O/(name+'.csv'),index=False)
        else:(O/(name+'.json')).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    maxerr=0
    def checked(a,w):
        nonlocal maxerr
        t=evaluate(cities,a,hi,w); l,u,r=scalar(a,hi,w)
        for key,x in [('score_lower',l),('score_upper',u),('max_regret',r)]:
            e=float(np.max(np.abs(t[key].to_numpy()-x)));maxerr=max(maxerr,e);assert e<3e-13
        return t,l,u,r
    cases={'retained_input':[],'withdraw_Zurich_work_commute':['Zurich'],'withdraw_Dublin_work_commute':['Dublin'],'withdraw_both_work_commute':['Zurich','Dublin'],'withdraw_all_submitted_commute_means':[cities[i] for i in idx]}
    ranks=[];bounds=[];withdrawals=[]; singles=[];probes=[];joints=[];corners=[];cases_joint=[];pairs=[]
    for name,removed in cases.items():
        a=lo.copy()
        for c in removed:a[cities.index(c),j]=0
        bounds.extend(dict(scenario=name,city=c,indicator=k,lower=a[i,h],upper=hi[i,h]) for i,c in enumerate(cities) for h,k in enumerate(NAMES))
        for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
            t,l,u,r=checked(a,w);ranks.append(t.assign(scenario=name,weight_reference=ref));withdrawals.append(dict(scenario=name,weight_reference=ref,withdrawn=removed,conservative_recommendation=[cities[i] for i in range(n) if r[i]<=r.min()+1e-10],possible_champions=int(t.possible_champion.sum()),necessary_champions=int(t.necessary_champion.sum())))
    for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
        t,L,U,R=checked(lo,w); targets=np.flatnonzero(R<=R.min()+1e-10);assert len(targets)==1; target=int(targets[0]); target_name=cities[target]
        C=np.array([np.delete(U,i).max() for i in range(n)])
        def single(u):
            a=lo.copy();a[z,j]=u;r=scalar(a,hi,w)[2];np.testing.assert_allclose(np.delete(r,z),np.delete(R,z),rtol=0,atol=1e-12);return float(r[z]-np.delete(r,z).min())
        g0,g1=single(0),single(1); assert g0>=g1-1e-12
        row={'weight_reference':ref,'target':'Zurich','baseline_recommendation':target_name,'gap_at_utility_0':g0,'gap_at_utility_1':g1,'retained_mean_minutes':float(means[z]),'tie_mean_minutes':None}
        if g0>0 and g1<0:
            root=float(brentq(single,0,1,xtol=5e-16,rtol=1e-15));row.update(status='finite_tie',tie_mean_minutes=-30*math.log(root),tie_lower_utility=root)
        elif g0<0:row['status']='zurich_unique_all_finite_nonnegative_means'
        elif g1>0:row['status']='zurich_not_minimax_any_finite_nonnegative_mean'
        else:row['status']='endpoint_tie_or_degenerate_requires_review'
        singles.append(row)
        for u in np.linspace(0,1,101):probes.append(dict(weight_reference=ref,lower_utility=float(u),zurich_regret_minus_best_other=single(float(u))))
        def corner(d):
            assert 0<=d<=1
            m=means.copy();m[idx]*=1-d
            if target in idx:m[target]=means[target]*(1+d)
            a=lo.copy();a[idx,j]=np.exp(-m[idx]/30);return a
        def regret(d):return scalar(corner(d),hi,w)[2]
        def gap(d):
            r=regret(d);return float(r[target]-np.delete(r,target).min())
        grid=[gap(float(x)) for x in np.linspace(0,1,101)];assert all(b>=a-1e-10 for a,b in zip(grid,grid[1:]));assert grid[0]<-1e-10
        end=gap(1)
        if end>0:
            radius=float(brentq(gap,0,1,xtol=5e-16,rtol=1e-15)); status='finite_boundary';assert gap(max(0,radius-1e-7))<0<gap(min(1,radius+1e-7))
        elif abs(end)<=1e-10:radius=1.;status='tie_at_box_limit'
        else:radius=None;status='unique_through_box_limit'
        sample=radius if radius is not None else 1.;vr=regret(sample)
        binding=[cities[i] for i in range(n) if i!=target and abs(vr[target]-vr[i])<1e-9]
        joints.append(dict(weight_reference=ref,target=target_name,status=status,sharp_radius=radius,binding_rivals=binding,gap_at_zero=gap(0),gap_at_one=end,gap_at_tested_boundary=gap(sample),rule='Target is uniquely minimax for every point below the boundary; at a finite boundary a rival ties at the worst corner; above it that corner is a counterexample.' if status=='finite_boundary' else 'See status and signed gaps; evaluated over radii up to one.'))
        for i,c in enumerate(cities):
            if i==target:continue
            def pg(d):r=regret(d);return float(r[target]-r[i])
            x0,x1=pg(0),pg(1); crossing=float(brentq(pg,0,1)) if x0<0<x1 else None;pairs.append(dict(weight_reference=ref,target=target_name,rival=c,gap_at_zero=x0,gap_at_one=x1,crossing_radius=crossing))
        for label,d in [('baseline',0),('five_percent',.05),('ten_percent',.1),('boundary_or_limit',sample)]:
            tt,l,u,r=checked(corner(d),w); cases_joint.append(dict(weight_reference=ref,target=target_name,case=label,radius=d,gap=gap(d),recommendation=[cities[i] for i in range(n) if r[i]<=r.min()+1e-10]))
        # Enumerate every one of 2^12 corners at each of two radii for each weighting.
        for d in [.05,sample]:
            bits=(np.arange(4096)[:,None]>>np.arange(12))&1;a=np.broadcast_to(lo,(4096,n,10)).copy();a[:,idx,j]=np.exp(-means[idx][None,:]*(1+d*(2*bits-1))/30)
            bad=np.sqrt((a*a*w).sum(axis=2));good=np.sqrt(((1-a)**2*w).sum(axis=2));lower=100*bad/(bad+good);rr=np.maximum(0,C[None,:]-lower);g=rr[:,target]-np.delete(rr,target,axis=1).min(axis=1); worst=float(g.max());assert abs(worst-gap(d))<1e-10
            corners.append(dict(weight_reference=ref,target=target_name,radius=d,corners=4096,max_signed_gap=worst,analytic_corner_gap=gap(d)))
    save('commute_withdrawal_ranks',pd.concat(ranks,ignore_index=True));save('commute_withdrawal_bounds',pd.DataFrame(bounds));save('single_mean_probes',pd.DataFrame(probes));save('joint_pairwise_crossings',pd.DataFrame(pairs));save('joint_cases',pd.DataFrame(cases_joint));save('mean_thresholds',singles);save('joint_thresholds',joints)
    save('summary',dict(version='V205 controlled source diagnostics',source_admission='conditional; verify independent source admission before use',source_sha256={str(Path(x).relative_to(ROOT)):sha(x) for x in [SOURCE,Path(staged.__file__),Path(previous.__file__),Path(__file__),snapshot]},changed_cell=['Prague','public_transport_density'],old_lower=float(oldlo[tuple(changed[0])]),new_lower=float(lo[tuple(changed[0])]),withdrawal_cases=withdrawals,mean_thresholds=singles,joint_thresholds=joints,corner_checks=corners,total_corner_evaluations=sum(x['corners'] for x in corners),scalar_vs_evaluate_max_error=maxerr,scope='Original means and Singapore historical stage bins retained except stated commute withdrawals; no new commute observation, confidence interval, prediction or MC rerun. Box is a sensitivity assumption, not a claim of physically joint realization.',proof='Upper scores are fixed. Each self-excluded regret depends only on its own lower score and increases as its own commute mean rises. Thus target high and all other means low maximize target regret minus the best rival; enumeration checks all corners and a radius grid checks monotonicity.'))
    for name,h in bindings.items():assert sha(ROOT/name)==h,name
    print(json.dumps({'single':singles,'joint':joints,'corner_evaluations':sum(x['corners'] for x in corners),'error':maxerr},indent=2))
if __name__=='__main__':main()
