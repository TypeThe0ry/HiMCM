"""Independent scalar audit of V187's declared twelve-mean box certificate."""
import hashlib,itertools,json,math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_user_v181_revision import revised_bounds
R=Path(__file__).resolve().parents[1]
O=R/'results/task4_v187_joint_means'
NAMES=['homicide_rate','pm25','cost_living_index','price_income_ratio','upper_secondary_ptr','research_he_density','public_transport_density','travel','fixed_broadband_mbps','public_pool_density']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def scalar(row,w):
    a=math.sqrt(math.fsum(float(q)*float(x)**2 for q,x in zip(w,row)))
    b=math.sqrt(math.fsum(float(q)*(1-float(x))**2 for q,x in zip(w,row)))
    return 100*a/(a+b)
def close(a,b,tol=2e-11):assert abs(float(a)-float(b))<tol,(a,b)
def main():
    summary=load(O/'summary.json');frame,lo,hi=revised_bounds();cities=frame.city.tolist()
    assert len(cities)==16 and lo.shape==hi.shape==(16,10)
    z=cities.index('Zurich');travel=7;means=frame.commute_min.to_numpy(float)
    idx=[i for i in range(16) if math.isfinite(means[i])]
    excluded=[cities[i] for i in range(16) if i not in idx]
    assert len(idx)==12 and excluded==['Vienna','Warsaw','Singapore','Tokyo']
    assert summary['means_cities']==[cities[i] for i in idx] and summary['retained_nonmean_cities']==excluded
    for i in idx:close(lo[i,travel],math.exp(-means[i]/30),1e-15);assert hi[i,travel]==1
    snapshot=load(R/'design/task4_user_v181_snapshot.json')['source_sha256']
    mutable={'design/task4_user_current_model.json','design/task4_user_current_extensions.json'}
    for name,h in snapshot.items():
        if name not in mutable:assert sha(R/name)==h,name
    assert len(snapshot)==245
    assert load(R/'design/task4_user_current_model.json')['version']=='V181'
    assert load(R/'design/task4_user_current_extensions.json')['extension_version']=='V181'
    assert sha(R/'data/task4_v117_team_intake/city_indicators.csv')=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
    for name,h in summary['source_sha256'].items():assert sha(R/name)==h,name
    frozen=pd.read_csv(R/'results/task4_user_v181_revision/utility_bounds.csv')
    frozen=frozen.loc[frozen.scenario.eq('after_conditional')].set_index(['city','indicator'])
    assert len(frozen)==160
    for i,c in enumerate(cities):
        for j,key in enumerate(NAMES):
            close(frozen.loc[(c,key)].lower,lo[i,j],5e-15);close(frozen.loc[(c,key)].upper,hi[i,j],5e-15)
    raw=pd.read_csv(O/'corner_ranks.csv');bound=pd.read_csv(O/'corner_bounds.csv');vectors=pd.read_csv(O/'corner_means.csv');paircsv=pd.read_csv(O/'pairwise_crossings.csv')
    assert len(raw)==192 and len(bound)==1920 and len(vectors)==144 and len(paircsv)==30
    records=[];maxerr=0.;corner_tests=[]
    for ref,w in [('fixed',[.1125]*6+[.05,.1125,.1125,.05]),('equal',[.1]*10)]:
        upper=[scalar(row,w) for row in hi]
        constants=[max(v for k,v in enumerate(upper) if k!=i) for i in range(16)]
        def endpoints(d):
            a=lo.copy();adjusted=means.copy()
            for i in idx:
                adjusted[i]=means[i]*(1+d if i==z else 1-d)
                a[i,travel]=math.exp(-adjusted[i]/30)
            L=[scalar(row,w) for row in a]
            regrets=[max(0.,constants[i]-L[i]) for i in range(16)]
            return a,adjusted,L,regrets
        def gap(d):
            v=endpoints(d)[3];return v[z]-min(v[i] for i in range(16) if i!=z)
        threshold=next(t for t in summary['thresholds'] if t['weight_reference']==ref)
        root=float(brentq(gap,0.,1.,xtol=5e-16,rtol=1e-15));close(root,threshold['sharp_radius'],2e-14)
        assert gap(0)<0<gap(1) and gap(root-1e-7)<0<gap(root+1e-7)
        _,_,_,rr=endpoints(root);ties=[cities[i] for i in range(16) if abs(rr[i]-min(rr))<1e-10]
        assert ties==['Zurich','Oslo'] and threshold['binding_rivals']==['Oslo']
        close(rr[z],threshold['tie_regret']);close(gap(root),threshold['signed_gap_at_root'])
        for i,c in enumerate(cities):
            if i==z:continue
            def pg(d):v=endpoints(d)[3];return v[z]-v[i]
            p=paircsv.loc[paircsv.weight_reference.eq(ref)&paircsv.rival.eq(c)].iloc[0]
            close(pg(0),p.gap_at0);close(pg(1),p.gap_at1)
            if pg(1)<0:assert pd.isna(p.crossing_radius)
            else:close(brentq(pg,0.,1.,xtol=5e-16,rtol=1e-15),p.crossing_radius,2e-14)
        for case in [c for c in summary['cases'] if c['weight_reference']==ref]:
            name=case['case'];d=case['delta'];a,adj,L,rr=endpoints(d)
            t=raw.loc[raw.weight_reference.eq(ref)&raw['case'].eq(name)].set_index('city')
            bb=bound.loc[bound.weight_reference.eq(ref)&bound['case'].eq(name)].set_index(['city','indicator'])
            mm=vectors.loc[vectors.weight_reference.eq(ref)&vectors['case'].eq(name)].set_index('city')
            assert len(t)==16 and len(bb)==160 and len(mm)==12
            for i,c in enumerate(cities):
                if i in idx:close(mm.loc[c].original_mean_minutes,means[i]);close(mm.loc[c].corner_mean_minutes,adj[i])
                for j,key in enumerate(NAMES):
                    row=bb.loc[(c,key)];close(row.lower,a[i,j],5e-15);close(row.upper,hi[i,j],5e-15)
                    if j!=travel or i not in idx:assert a[i,j]==lo[i,j]
                row=t.loc[c];err=max(abs(row.score_lower-L[i]),abs(row.score_upper-upper[i]),abs(row.max_regret-rr[i]));maxerr=max(maxerr,err);assert err<2e-11
                best=1+sum(L[k]>upper[i]+1e-12 for k in range(16) if k!=i)
                worst=1+sum(upper[k]>L[i]+1e-12 for k in range(16) if k!=i)
                possible=upper[i]>=max(L[k] for k in range(16) if k!=i)-1e-12
                necessary=L[i]>=max(upper[k] for k in range(16) if k!=i)-1e-12
                assert (int(row.best_rank),int(row.worst_rank),bool(row.possible_champion),bool(row.necessary_champion))==(best,worst,possible,necessary)
                if name!='boundary':assert int(row.decision_rank)==1+sum(r<rr[i] for r in rr)
            chosen=[cities[i] for i in range(16) if rr[i]<=min(rr)+1e-10]
            assert chosen==case['corner_recommendation'];close(gap(d),case['worst_signed_gap'])
            assert case['Zurich_strict_for_entire_box']==(gap(d)<-1e-10)
            assert case['possible_champions_in_corner']==int(t.possible_champion.sum())
            assert case['necessary_champions_in_corner']==int(t.necessary_champion.sum())
            close(math.fsum(upper[i]-L[i] for i in range(16))/16,case['corner_mean_score_width'])
            if name=='baseline':
                close(case['corner_mean_score_width'],summary['baseline_mean_width'][ref])
                assert chosen==['Zurich'] and case['possible_champions_in_corner']==16 and case['necessary_champions_in_corner']==0
        for item in [c for c in summary['corner_checks'] if c['weight_reference']==ref]:
            d=item['delta'];regrets={}
            # Each city has two scalar endpoint regrets. Enumerate every product
            # corner by lookup, independently of the runner's vectorized scoring.
            for i in idx:
                regrets[i]=[]
                for sign in [-1,1]:
                    row=lo[i].copy();row[travel]=math.exp(-means[i]*(1+sign*d)/30)
                    regrets[i].append(max(0.,constants[i]-scalar(row,w)))
            fixed=endpoints(0)[3];maximum=-float('inf');count=0
            for bits in itertools.product([0,1],repeat=12):
                v=list(fixed)
                for k,i in enumerate(idx):v[i]=regrets[i][bits[k]]
                maximum=max(maximum,v[z]-min(v[i] for i in range(16) if i!=z));count+=1
            assert count==item['corners']==4096;close(maximum,gap(d));close(maximum,item['max_signed_gap']);close(maximum,item['analytic_corner_gap'])
            corner_tests.append(dict(weight_reference=ref,delta=d,corners=count,independent_max_gap=maximum))
        # Strict increase requires Zurich regret >0 across the corner path.
        assert endpoints(0)[3][z]>0
        records.append(dict(weight_reference=ref,independent_root=root,percentage=100*root,tie_cities=ties,root_gap=gap(root),below_gap=gap(root-1e-7),above_gap=gap(root+1e-7)))
    note=(O/'proof_review.md').read_text();assert 'Cartesian-domain assumption' in note and 'not probabilistic independence' in note and 'Oslo' in note and 'Above the zero' in note
    assert summary['primary_admissions']==0 and summary['actual_baseline_width_change']==0
    paths=[p for p in O.iterdir() if p.is_file() and p.name!='verification.json']
    result=dict(status='pass',version='V187 independent audit',rank_rows=192,bound_rows=1920,mean_rows=144,pairwise_roots=30,scalar_max_score_or_regret_error=maxerr,roots=records,exhaustive_corner_checks=corner_tests,immutable_science_bindings_verified=243,historical_mutable_navigation_bindings=sorted(mutable),total_snapshot_bindings=245,original_CSV_preserved=True,active_V181_bounds_preserved=True,primary_admissions=0,actual_baseline_width_change=0,boundary_decision_rank_scope='Raw exact-float ranking may split a numerical tie; all numerical regrets verified and the certified Zurich/Oslo tie is checked with tolerance 1e-10. Nonboundary decision ranks verified exactly.',proof_scope='Analytic separability and monotonicity cover the complete declared box; corner enumeration corroborates it at the recorded radii. No empirical error model, probability, future trend or physical joint attainability is inferred.',source_sha256={**summary['source_sha256'],str(Path(__file__).relative_to(R)):sha(Path(__file__)), 'design/task4_user_v181_snapshot.json':sha(R/'design/task4_user_v181_snapshot.json')},audited_output_sha256={str(p.relative_to(R)):sha(p) for p in sorted(paths)})
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','rank_rows','bound_rows','scalar_max_score_or_regret_error','roots']},indent=2))
if __name__=='__main__':main()
