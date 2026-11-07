"""Expand Singapore student coverage with explicit SIS teacher allocation bounds."""
import hashlib
import importlib.util
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT, CITIES, NAMES, weights, summarize
from task4_delhi_school_revision import delhi_bounds
from task4_continuous_preferences import feasible_preferences

SOURCE = ROOT/'data/task4_v38_singapore'


def observation():
    spec = importlib.util.spec_from_file_location('singapore_extract', SOURCE/'extract.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    record = module.extract()
    assert record == json.loads((SOURCE/'observation.json').read_text()), 'Re-run extraction'
    return record


def allocation_utility(students, baseline_teachers, additional_pool):
    if students <= 0 or baseline_teachers < 0 or additional_pool < 0:
        raise ValueError('Positive pupils and nonnegative teacher counts required')
    return tuple(15*t/(15*t+students) for t in (baseline_teachers, baseline_teachers+additional_pool))


def singapore_bounds(strict_withdrawal=False):
    record = observation()
    lo, hi = delhi_bounds()
    i, j = CITIES.index('Singapore'), NAMES.index('upper_secondary_ptr')
    prior = 15/(15+record['prior_matched_students']/record['classified_preuniversity_teacher_headcount'])
    np.testing.assert_allclose([lo[i,j], hi[i,j]], prior, rtol=0, atol=1e-12)
    bounds = allocation_utility(record['students'], record['classified_preuniversity_teacher_headcount'], record['specialised_independent_teacher_pool'])
    np.testing.assert_allclose(bounds, [record['utility_lower'], record['utility_upper']], rtol=0, atol=1e-12)
    lo[i,j], hi[i,j] = (0,1) if strict_withdrawal else bounds
    return lo, hi


def checks():
    # Endpoint enumeration verifies allocation monotonicity without a distribution assumption.
    r = observation()
    grid = np.arange(r['specialised_independent_teacher_pool']+1)
    actual = 15*(1979+grid)/(15*(1979+grid)+25130)
    np.testing.assert_allclose([actual.min(),actual.max()],allocation_utility(25130,1979,404))
    assert np.all(np.diff(actual)>0)
    assert allocation_utility(10,0,0)==(0,0)
    assert allocation_utility(10,2,0)[0]==allocation_utility(10,2,0)[1]
    for bad in [(0,1,1),(1,-1,1),(1,1,-1)]:
        try: allocation_utility(*bad)
        except ValueError: pass
        else: raise AssertionError('Invalid count accepted')
    lo,hi=delhi_bounds();l,h=singapore_bounds();s,t=singapore_bounds(True)
    i,j=CITIES.index('Singapore'),NAMES.index('upper_secondary_ptr')
    keep=np.ones(lo.shape,bool);keep[i,j]=False
    for a,b in [(l,h),(s,t)]:
        np.testing.assert_array_equal(a[keep],lo[keep]);np.testing.assert_array_equal(b[keep],hi[keep])
        assert np.all((0<=a)&(a<=b)&(b<=1))
    assert l[i,j]<lo[i,j]<h[i,j], 'Coverage revision must not pretend to narrow prior subset point'
    assert np.all(s<=l) and np.all(h<=t)


def main():
    checks()
    before=delhi_bounds();base,_=summarize(*before,weights())
    frames=[];rows=[];stats=[]
    scenarios=[('v34_before',before),('expanded_coverage_allocation',singapore_bounds()),('strict_withdrawal',singapore_bounds(True))]
    for label,(lo,hi) in scenarios:
        f,d=summarize(lo,hi,weights());f['scenario']=label;frames.append(f)
        possible=[c for k,c in enumerate(CITIES) if feasible_preferences(hi[k],lo[np.arange(len(lo))!=k])['possible']]
        stats.append(dict(scenario=label,choice=[CITIES[k] for k in d['minimax_choices']],minimax_regret=float(d['minimax_regret']),
            possible_champions=f.loc[f.possible_champion,'city'].tolist(),continuous_alpha_possible=possible,
            changed_ranks=int((f.decision_rank!=base.decision_rank).sum()),kendall_tau=float(kendalltau(f.decision_rank,base.decision_rank).statistic),
            singapore=f.loc[f.city=='Singapore',['score_lower','score_upper','decision_rank','max_regret']].iloc[0].to_dict(),
            phoenix_rank=int(f.loc[f.city=='Phoenix','decision_rank'].iloc[0])))
        rows.extend(dict(scenario=label,city=c,indicator=n,lower=float(lo[i,j]),upper=float(hi[i,j])) for i,c in enumerate(CITIES) for j,n in enumerate(NAMES))
    out=ROOT/'results/task4_v38_singapore';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);pd.DataFrame(rows).to_csv(out/'utility_bounds.csv',index=False)
    result=dict(main_admitted=False,primary_scenario='expanded_coverage_allocation',baseline='V34 delhi_bounds()',
        changed_city_indicator_cells=1,alpha_fixed=.1,alpha_range=[.05,.2],
        scope=observation()['scope'],prior_and_revised_population_differ=True,
        checks='Source SHA256/size, XLSX labels and totals, derived-record equality, allocation endpoint enumeration, monotonicity, invalid inputs, unchanged other cells, strict containment',
        sources=[dict(file=p,sha256=hashlib.sha256((SOURCE/p).read_bytes()).hexdigest()) for p in ['manifest.json','observation.json','extract.py']],scenarios=stats)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(stats,indent=2))

if __name__=='__main__':main()
