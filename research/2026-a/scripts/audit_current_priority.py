"""Independent scalar audit of V203 conditional acquisition limits."""
import hashlib
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_user_v203_revision import revised_bounds
from task4_v5_model import ROOT, NAMES

OUT=ROOT/'results/current_priority'
TOL=1e-12

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def close(a,b): np.testing.assert_allclose(a,b,atol=2e-10,rtol=0)
def scalar_scores(u,w):
    result=[]
    for row in u:
        good=math.sqrt(math.fsum(float(q)*float(x)**2 for q,x in zip(w,row)))
        bad=math.sqrt(math.fsum(float(q)*(1-float(x))**2 for q,x in zip(w,row)))
        result.append(100*good/(good+bad))
    return np.array(result)
def decision(l,u):
    regret=np.array([max(0.,max(u[k] for k in range(16) if k!=i)-l[i]) for i in range(16)])
    possible=np.array([u[i]>=max(l[k] for k in range(16) if k!=i)-TOL for i in range(16)])
    return regret,float(regret.min()),possible,np.flatnonzero(regret<=regret.min()+TOL)
def main():
    paper = ROOT.parent.parent.parent / 'HiMCM-Overleaf'
    protected = [paper/'main.tex', paper/'mcmthesis.cls', paper/'ref.bib'] + sorted((paper/'figures').glob('*'))
    protected = [p for p in protected if p.is_file()]
    assert len(protected) == 7
    paper_hashes = {str(p): sha(p) for p in protected}
    summary=json.loads((OUT/'summary.json').read_text())
    hashes=summary['source_sha256']
    for p,h in hashes.items(): assert sha(ROOT/p)==h,p
    snapshot=json.loads((ROOT/'design/task4_user_v203_snapshot.json').read_text())['source_sha256']
    assert len(snapshot)==548
    for p,h in snapshot.items(): assert hashes[p]==h and sha(ROOT/p)==h,p
    source=ROOT/'data/task4_v117_team_intake/city_indicators.csv'
    assert sha(source)=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
    f,lo,hi=revised_bounds();original=np.stack([lo,hi]).copy();cities=f.city.tolist()
    assert lo.shape==hi.shape==(16,10)
    uncertain=lo<hi;missing=(lo==0)&(hi==1)
    assert [int((lo==hi).sum()),int((uncertain&~missing).sum()),int(missing.sum())]==[112,37,11]
    references={'fixed':np.array([.1125]*6+[.05,.1125,.1125,.05]),'equal':np.full(10,.1)}
    tables={n:pd.read_csv(OUT/(n+'.csv'),float_precision='round_trip') for n in ['all_uncertain_priority','endpoints','lower_only_refinements','previous_comparison']}
    priority=tables['all_uncertain_priority'];endpoints=tables['endpoints'];lower=tables['lower_only_refinements']
    expected={(r,cities[i],NAMES[j]) for r in references for i,j in zip(*np.where(uncertain))}
    key=['weight_reference','city','indicator']
    assert len(priority)==96 and not priority.duplicated(key).any()
    assert set(priority[key].itertuples(index=False,name=None))==expected
    assert len(endpoints)==192 and len(lower)==480
    assert not endpoints.duplicated(key+['endpoint']).any()
    assert not lower.duplicated(key+['fraction_of_retained_interval']).any()
    count=0; interior=0
    def case(ref,city,indicator,x,exact=True):
        nonlocal count
        i=cities.index(city);j=NAMES.index(indicator)
        assert uncertain[i,j] and lo[i,j]-1e-14<=x<=hi[i,j]+1e-14
        a,b=lo.copy(),hi.copy();a[i,j]=x
        if exact: b[i,j]=x
        mask=np.ones((16,10),bool);mask[i,j]=False
        np.testing.assert_array_equal(a[mask],lo[mask]);np.testing.assert_array_equal(b[mask],hi[mask])
        l,u=scalar_scores(a,references[ref]),scalar_scores(b,references[ref]);count+=1
        return i,l,u,decision(l,u)
    bases={}
    for ref,w in references.items():
        l,u=scalar_scores(lo,w),scalar_scores(hi,w);d=decision(l,u);bases[ref]=(l,u,d)
        record=next(r for r in summary['baseline'] if r['weight_reference']==ref)
        close(record['minimax_regret'],d[1]);close(record['mean_score_interval_width'],(u-l).mean())
        assert record['conservative_recommendation']==';'.join(cities[k] for k in d[3])==('Oslo' if ref=='fixed' else 'Zurich')
        assert record['possible_champions']==int(d[2].sum())==16
    for row in priority.itertuples():
        ref,city,ind=row.weight_reference,row.city,row.indicator;i=cities.index(city);j=NAMES.index(ind)
        left,right=float(lo[i,j]),float(hi[i,j]);close([row.current_lower,row.current_upper],[left,right])
        assert row.current_information==('fully_missing' if missing[i,j] else 'partial_interval')
        def branches(x):
            _,_,_,d=case(ref,city,ind,x)
            return float(d[0][i]),float(np.delete(d[0],i).min())
        def difference(x):a,b=branches(x);return a-b
        candidates=[left,right]
        if difference(left)*difference(right)<0:candidates.append(brentq(difference,left,right,xtol=1e-14))
        best=min(min(branches(x)) for x in [left,right]);worst=max(min(branches(x)) for x in candidates)
        risk=bases[ref][2][1]
        close([row.best_post_regret,row.worst_post_regret,row.guaranteed_exact_resolution_regret_reduction,row.best_possible_exact_resolution_regret_reduction],[best,worst,risk-worst,risk-best])
        endpoint_cases=[case(ref,city,ind,x)[3] for x in [left,right]]
        ceiling=max(16-int(d[2].sum()) for d in endpoint_cases)
        assert row.optimistic_champion_exclusions==ceiling
        for x in np.linspace(left,right,103)[1:-1]:
            _,_,_,d=case(ref,city,ind,float(x));interior+=1
            assert best-2e-10<=d[1]<=worst+2e-10
            assert 16-int(d[2].sum())<=ceiling
        e=endpoints[(endpoints.weight_reference==ref)&(endpoints.city==city)&(endpoints.indicator==ind)]
        assert set(e.endpoint)=={'lower','upper'}
        for label,x,d in [('lower',left,endpoint_cases[0]),('upper',right,endpoint_cases[1])]:
            saved=e[e.endpoint==label].iloc[0]
            close(saved.resolved_utility,x);close(saved.minimax_regret,d[1]);assert saved.possible_count==int(d[2].sum())
        low=lower[(lower.weight_reference==ref)&(lower.city==city)&(lower.indicator==ind)]
        assert set(low.fraction_of_retained_interval)=={0.,.25,.5,.75,1.}
        for item in low.itertuples():
            x=left+item.fraction_of_retained_interval*(right-left)
            _,l,u,d=case(ref,city,ind,x,False)
            close([item.utility_lower,item.utility_upper,item.minimax_regret,item.regret_reduction],[x,right,d[1],risk-d[1]])
            np.testing.assert_array_equal(u,bases[ref][1])
            assert item.possible_count==int(d[2].sum())
            assert item.conservative_recommendation==';'.join(cities[k] for k in d[3])
    old=pd.read_csv(OUT/'previous_V202.csv',float_precision='round_trip')
    paired=priority.merge(old,on=key,suffixes=('_current','_V202'),validate='one_to_one')
    assert len(paired)==96
    for name in ['guaranteed_exact_resolution_regret_reduction','best_possible_exact_resolution_regret_reduction','optimistic_champion_exclusions']:
        paired[name+'_change']=paired[name+'_current']-paired[name+'_V202']
    pd.testing.assert_frame_equal(paired,tables['previous_comparison'],check_exact=False,atol=2e-12,rtol=0)
    assert set(map(tuple, priority[key].to_numpy())) == set(map(tuple, old[key].to_numpy()))
    changed = paired[paired.current_lower_current != paired.current_lower_V202]
    assert len(changed) == 2 and set(changed.weight_reference) == set(references)
    assert set(changed[['city', 'indicator']].itertuples(index=False, name=None)) == {('Oslo', 'public_transport_density')}
    from task4_user_v202_revision import revised_bounds as old_bounds
    _, old_lo, old_hi = old_bounds()
    delta = np.argwhere(lo != old_lo)
    assert len(delta) == 1
    ii, jj = delta[0]
    assert (cities[ii], NAMES[jj]) == ('Oslo', 'public_transport_density')
    close(changed.current_lower_V202, [old_lo[ii,jj]]*2)
    close(changed.current_lower_current, [lo[ii,jj]]*2)
    np.testing.assert_array_equal(hi, old_hi)
    assert (paired.current_upper_current == paired.current_upper_V202).all()
    assert (paired.current_information_current == paired.current_information_V202).all()
    nav = [f'design/task4_user_current_{n}.json' for n in ['model','extensions','review','delivery']]
    assert all(p in hashes and sha(ROOT/p) == hashes[p] for p in nav)
    _,a,b=revised_bounds();np.testing.assert_array_equal(original,np.stack([a,b]))
    for p,h in hashes.items():assert sha(ROOT/p)==h,p
    assert all(sha(Path(p)) == h for p,h in paper_hashes.items())
    report=dict(paper_file_sha256=paper_hashes,status='pass',science='V203 bindings unchanged',paper='not modified',exact_information_envelopes=96,endpoint_cases=192,lower_only_cases=480,dense_interior_probes=interior,independent_scalar_evaluations=count,weights_once_in_squared_norm=True,self_excluded_regret_and_champion_checks=True,unchanged_160_bounds=True,immutable_snapshot_bindings=548,original_CSV_sha256=sha(source),current_four_navigation_hashes_unchanged=True,comparison_rows=96,changed_bounds_rows=2,changed_information_rows=0,primary_admissions=0,actual_score_width_reduction=0,source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),OUT/'summary.json',*[OUT/(n+'.csv') for n in tables]]})
    (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
