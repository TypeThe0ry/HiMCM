"""Recompute retained commute-policy diagnostics on staged V192 user16 evidence."""
from pathlib import Path
import hashlib,json,math
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_user_city_indicators import SOURCE,evaluate
from task4_v5_model import ROOT,NAMES,weights
O=ROOT/'results/task4_v192_source_diagnostics'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    if isinstance(value,pd.DataFrame):value.to_csv(O/(name+'.csv'),index=False)
    else:(O/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
def scalar_scores(a,w):
    out=[]
    for row in a:
        bad=math.sqrt(math.fsum(float(q)*float(u)**2 for q,u in zip(w,row)))
        good=math.sqrt(math.fsum(float(q)*(1-float(u))**2 for q,u in zip(w,row)))
        out.append(100*bad/(bad+good))
    return np.asarray(out)
def scalar_values(a,b,w):
    lower,upper=scalar_scores(a,w),scalar_scores(b,w)
    regret=np.array([max(0.,max(upper[k] for k in range(len(upper)) if k!=i)-lower[i]) for i in range(len(lower))])
    return lower,upper,regret

def main():
    import task4_user_v192_revision as staged
    f,lo,hi=staged.revised_bounds();cities=f.city.tolist();n=len(cities);j=NAMES.index('travel');z=cities.index('Zurich');means=f.commute_min.to_numpy(float);idx=np.flatnonzero(np.isfinite(means))
    assert n==16 and lo.shape==hi.shape==(16,10) and len(idx)==12
    assert [cities[i] for i in range(n) if i not in idx]==['Vienna','Warsaw','Singapore','Tokyo']
    np.testing.assert_allclose(lo[idx,j],np.exp(-means[idx]/30),rtol=0,atol=1e-15);np.testing.assert_array_equal(hi[idx,j],np.ones(12))
    counts=[int((lo==hi).sum()),int(((lo<hi)&~((lo==0)&(hi==1))).sum()),int(((lo==0)&(hi==1)).sum())];assert counts==[112,37,11]
    initial=np.stack([lo,hi]).copy();O.mkdir(exist_ok=True);max_error=0.
    save('retained_bounds',pd.DataFrame([dict(city=c,indicator=k,lower=lo[i,h],upper=hi[i,h]) for i,c in enumerate(cities) for h,k in enumerate(NAMES)]))
    def checked(a,b,w):
        nonlocal max_error
        t=evaluate(cities,a,b,w);L,U,R=scalar_values(a,b,w)
        for k,values in [('score_lower',L),('score_upper',U),('max_regret',R)]:
            err=float(np.max(np.abs(t[k].to_numpy()-values)));max_error=max(max_error,err);assert err<3e-13
        return t,L,U,R
    cases={'retained_input':[],'withdraw_Zurich_work_commute':['Zurich'],'withdraw_Dublin_work_commute':['Dublin'],'withdraw_both_work_commute':['Zurich','Dublin'],'withdraw_all_submitted_commute_means':[cities[i] for i in idx]}
    withdrawal_ranks=[];withdrawal_bounds=[];withdrawal_reports=[]
    for case,removed in cases.items():
        a=lo.copy()
        for c in removed:a[cities.index(c),j]=0
        keep=np.ones((n,10),bool)
        for c in removed:keep[cities.index(c),j]=False
        np.testing.assert_array_equal(a[keep],lo[keep])
        withdrawal_bounds.extend(dict(scenario=case,city=c,indicator=name,lower=a[i,k],upper=hi[i,k]) for i,c in enumerate(cities) for k,name in enumerate(NAMES))
        for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
            t,L,U,R=checked(a,hi,w);withdrawal_ranks.append(t.assign(scenario=case,weight_reference=ref))
            withdrawal_reports.append(dict(scenario=case,weight_reference=ref,withdrawn_commute_proxies=removed,conservative_recommendation=[cities[i] for i in range(n) if R[i]<=R.min()+1e-10],possible_champions=int(t.possible_champion.sum()),necessary_champions=int(t.necessary_champion.sum()),mean_score_interval_width=float((U-L).mean()),minimax_regret=float(R.min())))
    save('commute_withdrawal_ranks',pd.concat(withdrawal_ranks,ignore_index=True));save('commute_withdrawal_bounds',pd.DataFrame(withdrawal_bounds))
    means_thresholds=[];single_probes=[];joint_thresholds=[];joint_cases=[];joint_ranks=[];joint_bounds=[];joint_means=[];pairs=[];corners=[]
    for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
        L,U,R=scalar_values(lo,hi,w);C=np.array([np.delete(U,i).max() for i in range(n)]);other_best=float(np.delete(R,z).min());target=C[z]-other_best
        def single_gap(u):
            a=lo.copy();a[z,j]=u;v=scalar_values(a,hi,w)[2];np.testing.assert_array_equal(np.delete(v,z),np.delete(R,z));return float(v[z]-np.delete(v,z).min())
        r2=((target/100)/(1-target/100))**2
        A=math.fsum(float(w[k])*float(lo[z,k])**2 for k in range(10) if k!=j)
        B=math.fsum(float(w[k])*(1-float(lo[z,k]))**2 for k in range(10) if k!=j)
        coeff=[float(w[j])*(1-r2),2*r2*float(w[j]),A-r2*(B+float(w[j]))]
        feasible=[float(v.real) for v in np.roots(coeff) if abs(v.imag)<1e-12 and 0<=v.real<=1]
        row=dict(weight_reference=ref,retained_mean_minutes=float(means[z]),gap_at_lower_utility0=single_gap(0),gap_at_lower_utility1=single_gap(1),target_lower_score=target,quadratic_coefficients=coeff)
        if single_gap(0)>0>single_gap(1):
            root=float(brentq(single_gap,0,1,xtol=5e-16,rtol=1e-15));assert len(feasible)==1;np.testing.assert_allclose(root,feasible[0],rtol=0,atol=1e-13)
            mean=-30*math.log(root);a=lo.copy();a[z,j]=root;v=scalar_values(a,hi,w)[2]
            selected=[cities[i] for i in range(n) if v[i]<=v.min()+1e-10]
            assert single_gap(math.exp(-(mean-1e-5)/30))<0<single_gap(math.exp(-(mean+1e-5)/30))
            row.update(status='one_finite_mean_tie',tie_lower_utility=root,tie_mean_minutes=mean,tie_cities=selected,strict_rule='With all other entries fixed, Zurich uniquely minimizes regret below the mean cutoff; a tie occurs at it; above it Zurich is excluded.')
        else:
            assert single_gap(0)<0 and single_gap(1)<0 and not feasible
            row.update(status='Zurich_unique_for_all_nonnegative_means',tie_lower_utility=None,tie_mean_minutes=None,strict_rule='For this one-mean experiment the largest gap is its negative utility0 limit, so every finite nonnegative mean retains unique Zurich.')
        means_thresholds.append(row)
        for u in np.linspace(0,1,101):single_probes.append(dict(weight_reference=ref,lower_utility=float(u),implied_mean_minutes='limit_infinity' if u==0 else -30*math.log(float(u)),Zurich_regret_minus_best_other=single_gap(float(u))))
        def joint_bound(delta):
            if not 0<=delta<=1:raise ValueError('Joint radius outside [0,1]')
            m=means.copy();m[idx]*=1-delta;m[z]=means[z]*(1+delta);a=lo.copy();a[idx,j]=np.exp(-m[idx]/30)
            np.testing.assert_array_equal(np.delete(a,j,axis=1),np.delete(lo,j,axis=1));np.testing.assert_array_equal(a[np.setdiff1d(np.arange(n),idx)],lo[np.setdiff1d(np.arange(n),idx)])
            return m,a
        def joint_r(delta):return scalar_values(joint_bound(delta)[1],hi,w)[2]
        def joint_gap(delta):
            v=joint_r(delta);return float(v[z]-np.delete(v,z).min())
        assert R[z]>0 and joint_gap(0)<0<joint_gap(1)
        radius=float(brentq(joint_gap,0,1,xtol=5e-16,rtol=1e-15));v=joint_r(radius);binding=[cities[i] for i in range(n) if i!=z and abs(v[z]-v[i])<1e-10]
        assert abs(joint_gap(radius))<1e-10 and joint_gap(radius-1e-7)<0<joint_gap(radius+1e-7)
        joint_thresholds.append(dict(weight_reference=ref,sharp_radius=radius,sharp_radius_percent=100*radius,binding_rivals=binding,tie_regret=float(v[z]),gap_at0=joint_gap(0),gap_at1=joint_gap(1),signed_gap_at_root=joint_gap(radius),gap_below=joint_gap(radius-1e-7),gap_above=joint_gap(radius+1e-7),strict_guarantee='Below the exact boundary Zurich uniquely minimizes regret throughout the box. At equality Zurich remains a minimax choice throughout, but a rival can tie at the worst corner. Above it an admissible counterexample exists.'))
        for i,c in enumerate(cities):
            if i==z:continue
            def pair(d):v=joint_r(d);return float(v[z]-v[i])
            crossing=float(brentq(pair,0,1,xtol=5e-16,rtol=1e-15)) if pair(1)>=0 else None
            pairs.append(dict(weight_reference=ref,rival=c,gap_at0=pair(0),gap_at1=pair(1),crossing_radius=crossing))
        assert abs(min(x['crossing_radius'] for x in pairs if x['weight_reference']==ref and x['crossing_radius'] is not None)-radius)<1e-12
        for name,d in [('baseline',0),('five_percent',.05),('ten_percent',.1),('just_below',radius-1e-7),('boundary',radius),('just_above',radius+1e-7)]:
            m,a=joint_bound(d);t,L,U,v=checked(a,hi,w)
            chosen=[cities[i] for i in range(n) if v[i]<=v.min()+1e-10]
            joint_cases.append(dict(weight_reference=ref,case=name,delta=d,worst_signed_gap=joint_gap(d),corner_recommendation=chosen,possible_champions_in_corner=int(t.possible_champion.sum()),necessary_champions_in_corner=int(t.necessary_champion.sum()),corner_mean_score_width=float((U-L).mean())))
            joint_ranks.append(t.assign(weight_reference=ref,case=name,delta=d))
            joint_means.extend(dict(weight_reference=ref,case=name,city=cities[i],original_mean_minutes=float(means[i]),corner_mean_minutes=float(m[i])) for i in idx)
            joint_bounds.extend(dict(weight_reference=ref,case=name,city=c,indicator=k,lower=a[i,h],upper=hi[i,h]) for i,c in enumerate(cities) for h,k in enumerate(NAMES))
        for d in [.05,radius]:
            bits=(np.arange(4096)[:,None]>>np.arange(12))&1;a=np.broadcast_to(lo,(4096,n,10)).copy();a[:,idx,j]=np.exp(-means[idx][None,:]*(1+d*(2*bits-1))/30)
            bad=np.sqrt((a*a*w).sum(axis=2));good=np.sqrt(((1-a)**2*w).sum(axis=2));lower=100*bad/(bad+good)
            regs=np.maximum(0,C[None,:]-lower);gaps=regs[:,z]-np.delete(regs,z,axis=1).min(axis=1);worst=float(gaps.max())
            assert abs(worst-joint_gap(d))<1e-11;corners.append(dict(weight_reference=ref,delta=d,corners=4096,max_signed_gap=worst,scalar_analytic_corner_gap=joint_gap(d)))
    save('mean_thresholds',means_thresholds);save('single_mean_probes',pd.DataFrame(single_probes));save('joint_thresholds',joint_thresholds);save('joint_pairwise_crossings',pd.DataFrame(pairs));save('joint_corner_ranks',pd.concat(joint_ranks,ignore_index=True));save('joint_corner_bounds',pd.DataFrame(joint_bounds));save('joint_corner_means',pd.DataFrame(joint_means))
    paths=[Path(__file__),SOURCE,Path(staged.__file__),ROOT/'scripts/task4_user_city_indicators.py',ROOT/'scripts/task4_v5_model.py',ROOT/'scripts/task4_interval_decision.py']
    manifest=getattr(staged,'MANIFEST',ROOT/'design/task4_user_v192_admissions.json');paths.extend([Path(manifest),ROOT/'scripts/task4_user_v181_revision.py',ROOT/'design/task4_user_v181_admissions.json',ROOT/'design/task4_user_v181_snapshot.json'])
    for folder in ['tokyo','warsaw']:paths.extend(p for p in (ROOT/('data/task4_v191_'+folder)).iterdir() if p.is_file())
    report=dict(version='V192 staged source diagnostics',science='V192 staged; current active navigation is unchanged',paper_at_creation='V189 unchanged',retained_input_counts=counts,input_bounds_sha256=sha(O/'retained_bounds.csv'),withdrawal_rank_rows=160,withdrawal_bound_rows=800,single_mean_probe_rows=202,joint_rank_rows=192,joint_bound_rows=1920,joint_mean_rows=144,joint_pairwise_comparisons=30,joint_finite_crossing_roots=sum(x['crossing_radius'] is not None for x in pairs),joint_corner_checks=corners,scalar_vs_evaluate_max_error=max_error,withdrawal_cases=withdrawal_reports,mean_thresholds=means_thresholds,joint_thresholds=joint_thresholds,source_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(paths))},scope='Conditional input sensitivity on staged V192 user16. Original CSV values/years/flags remain. Withdrawals keep Singapore historical stage bins; one-mean and joint boxes hold all other criteria and weights fixed. No new commute observations, confidence intervals, calibrated errors, future predictions or real-world winner probabilities.',proof='All upper scores remain constant along the joint box; self-excluded regret depends on its own lower score and increases with its own mean. Zurich high and every other finite mean low jointly maximize its regret minus the best rival. Positive Zurich regret at delta0 makes this corner gap strictly increasing. The root is sharp for the declared Cartesian box, not a proof of joint physical realization.',point_possible_champion_scope='Sixteen possible/zero necessary is reported for evaluated withdrawal cases only, not asserted over the entire mean parameter domain.',MC_rerun=False)
    save('summary',report);_,a,b=staged.revised_bounds();np.testing.assert_array_equal(np.stack([a,b]),initial)
    print(json.dumps(dict(withdrawals=withdrawal_reports,one_mean=means_thresholds,joint=joint_thresholds,max_scalar_error=max_error),indent=2))
if __name__=='__main__':main()
