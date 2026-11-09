"""Separate a historical resident-worker proxy profile from retained user inputs.

Also locate the one-mean decision boundary under the unchanged Jensen rule.
No source-population intersection, primary admission, CI conversion or forecast.
"""
import hashlib,json,math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_user_v181_revision import revised_bounds
from task4_user_city_indicators import SOURCE,evaluate
from task4_v5_model import ROOT,NAMES,weights,score
O=ROOT/'results/task4_v185_commute_candidate'
D=ROOT/'data/task4_v185_dublin_bins'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    O.mkdir(exist_ok=True);f,lo,hi=revised_bounds();cities=f.city.tolist();initial=np.stack([lo,hi]).copy();z=cities.index('Zurich');d=cities.index('Dublin');j=NAMES.index('travel')
    source=json.loads((D/'cso2011_dublin_four_counties.json').read_text())[0]
    assert source['geography_label']=='Dublin City' and source['census_year']==2011 and source['sex']=='Both sexes'
    values=source['values'];labels=['Journey time < 15 mins','Journey time 15 mins - < 30 mins','Journey time 30 mins - < 45 mins','Journey time 45 mins - < 60 mins','Journey time 60 mins - < 90 mins','Journey time 90 mins and over']
    counts=[int(values[k]) for k in labels];N=int(values['Total Persons']);unknown=int(values['Journey time not stated'])
    assert counts==[34770,75667,57683,17420,11337,2226] and unknown==16281 and N==215384 and sum(counts)+unknown==N
    edges=[0,15,30,45,60,90,float('inf')]
    lower=math.fsum(n*(0 if math.isinf(edges[k+1]) else math.exp(-edges[k+1]/30)) for k,n in enumerate(counts))/N
    upper=(math.fsum(n*math.exp(-edges[k]/30) for k,n in enumerate(counts))+unknown)/N
    assert lower<lo[d,j]<upper<hi[d,j] # non-nested profiles: do not intersect.
    bin_rows=[dict(bin=labels[k],count=n,minutes_lower=edges[k],minutes_upper='unbounded' if math.isinf(edges[k+1]) else edges[k+1],utility_lower=0 if math.isinf(edges[k+1]) else math.exp(-edges[k+1]/30),utility_upper=math.exp(-edges[k]/30)) for k,n in enumerate(counts)]
    bin_rows.append(dict(bin='Not stated',count=unknown,minutes_lower='unknown',minutes_upper='unknown',utility_lower=0,utility_upper=1));pd.DataFrame(bin_rows).to_csv(O/'candidate_bins.csv',index=False)
    mean_indices=np.flatnonzero(f.commute_min.notna().to_numpy());assert len(mean_indices)==12
    profiles={
      'retained_input':(lo.copy(),hi.copy()),
      'Dublin2011_resident_bins':(lo.copy(),hi.copy()),
      'Dublin2011_resident_bins_withdraw_Zurich_mean':(lo.copy(),hi.copy()),
      'Dublin2011_resident_bins_withdraw_other11_means':(lo.copy(),hi.copy())}
    for case,(a,b) in profiles.items():
        if case!='retained_input':a[d,j],b[d,j]=lower,upper
        if case.endswith('withdraw_Zurich_mean'):a[z,j],b[z,j]=0,1
        if case.endswith('withdraw_other11_means'):
            for i in mean_indices:
                if i!=d:a[i,j],b[i,j]=0,1
    ranks=[];bound_rows=[];reports=[];thresholds=[];probes=[]
    for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
        for case,(a,b) in profiles.items():
            assert np.array_equal(a[:,:j],lo[:,:j]) and np.array_equal(a[:,j+1:],lo[:,j+1:])
            assert np.array_equal(b[:,:j],hi[:,:j]) and np.array_equal(b[:,j+1:],hi[:,j+1:])
            table=evaluate(cities,a,b,w);ranks.append(table.assign(profile=case,weight_reference=ref))
            reports.append(dict(profile=case,weight_reference=ref,conservative_recommendation=table.loc[table.decision_rank.eq(1),'city'].tolist(),possible_champions=int(table.possible_champion.sum()),necessary_champions=int(table.necessary_champion.sum()),mean_score_interval_width=float((table.score_upper-table.score_lower).mean())))
        # Only Zurich's supplied mean varies; upper utility remains1 under Jensen.
        L,U=score(lo,w),score(hi,w);table=evaluate(cities,lo,hi,w)
        best_other=float(table.drop(z).max_regret.min());competitor_upper=float(np.delete(U,z).max());target_score=competitor_upper-best_other
        def gap(u):
            a=lo.copy();a[z,j]=u;t=evaluate(cities,a,hi,w)
            return float(t.iloc[z].max_regret-t.drop(z).max_regret.min())
        c=target_score/100;r2=(c/(1-c))**2
        a=math.fsum(float(w[k])*float(lo[z,k])**2 for k in range(10) if k!=j)
        b=math.fsum(float(w[k])*(1-float(lo[z,k]))**2 for k in range(10) if k!=j)
        coefficients=[float(w[j])*(1-r2),2*r2*float(w[j]),a-r2*(b+float(w[j]))]
        roots=np.roots(coefficients);feasible=[float(x.real) for x in roots if abs(x.imag)<1e-12 and 0<=x.real<=1]
        record=dict(weight_reference=ref,retained_mean_minutes=float(f.iloc[z].commute_min),gap_at_lower_utility0=gap(0),gap_at_lower_utility1=gap(1),target_lower_score=target_score,quadratic_coefficients=coefficients)
        if gap(0)*gap(1)<0:
            u=float(brentq(gap,0,1,xtol=1e-14));assert len(feasible)==1;np.testing.assert_allclose(u,feasible[0],atol=1e-13,rtol=0)
            cutoff=-30*math.log(u)
            for shift,sign in [(-1e-5,-1),(1e-5,1)]:assert sign*gap(math.exp(-(cutoff+shift)/30))>0
            record.update(status='one_finite_mean_tie',tie_lower_utility=u,tie_mean_minutes=cutoff,strict_rule='Zurich uniquely selected below mean cutoff; tie at cutoff; above it another city minimizes regret, other data fixed.')
        else:
            assert not feasible and gap(0)<0 and gap(1)<0
            record.update(status='Zurich_unique_for_all_nonnegative_means',tie_lower_utility=None,tie_mean_minutes=None,strict_rule='Maximum gap occurs at utility0; it is strictlynegative, so no finite mean crosses; this is an algebraic one-input sensitivity statement.')
        thresholds.append(record)
        for u in np.linspace(0,1,101):probes.append(dict(weight_reference=ref,lower_utility=float(u),implied_mean_minutes='limit_infinity' if u==0 else -30*math.log(float(u)),Zurich_regret_minus_best_other=gap(float(u))))
    for case,(a,b) in profiles.items():bound_rows.extend(dict(profile=case,city=c,indicator=n,lower=a[i,k],upper=b[i,k]) for i,c in enumerate(cities) for k,n in enumerate(NAMES))
    pd.concat(ranks,ignore_index=True).to_csv(O/'profile_ranks.csv',index=False);pd.DataFrame(bound_rows).to_csv(O/'profile_bounds.csv',index=False);pd.DataFrame(probes).to_csv(O/'threshold_probes.csv',index=False)
    (O/'mean_thresholds.json').write_text(json.dumps(thresholds,indent=2)+'\n')
    paths=[Path(__file__),SOURCE,ROOT/'scripts/task4_user_v181_revision.py',ROOT/'design/task4_user_current_model.json',ROOT/'design/task4_user_current_extensions.json']
    for package in ['dublin_bins','zurich_bins','madrid_teacher']:paths.extend(p for p in (ROOT/('data/task4_v185_'+package)).iterdir() if p.is_file())
    summary=dict(version='V185 source-scoped alternative profile; not primary admission',primary='V181 unchanged',paper='V184 unchanged',primary_admissions=0,actual_baseline_width_change=0,profile_rank_rows=128,profile_bound_rows=640,candidate_city='Dublin City',candidate_population='2011resident/presentworkers15+;mainlyhomeworkersexcluded;notcurrenthighschoolstudents',candidate_total=N,candidate_known=sum(counts),candidate_unknown=unknown,candidate_utility_bounds=[lower,upper],published_mean27_1_not_used_as_moment_constraint=True,original28_8_not_intersected=True,profiles_are_not_nested=True,all_current160_bounds_unchanged=True,profiles=reports,thresholds=thresholds,source_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(paths))},scope='Historical residence-worker profile is a different proxy population. Cross-profile width differences are not baseline precision gains or pure information effects. Binendpoints/open-tail/unknownmass rules retained; no fabricated tail cap, no CI conversion, no measured future trend or real-world winner probability.',MC_rerun=False)
    (O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');_,a,b=revised_bounds();np.testing.assert_array_equal(initial,np.stack([a,b]));print(json.dumps(dict(candidate_utility=[lower,upper],thresholds=thresholds,profiles=reports),indent=2))
if __name__=='__main__':main()
