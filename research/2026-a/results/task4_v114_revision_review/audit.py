"""Independent V114 source arithmetic, ablation and interval-ranking audit."""
from pathlib import Path
import hashlib, json, sys, csv, subprocess
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'scripts'))
from task4_v113_evidence_revision import evidence_bounds
from task4_v5_model import CITIES, NAMES
OUT = Path(__file__).resolve().parent

def score(z, w):
    good = np.einsum('ij,j->i', z*z, w)
    bad = np.einsum('ij,j->i', (1-z)**2, w)
    return 100/(1+np.sqrt(bad/good))

def run():
    source = ROOT/'data/task4_v114_istanbul_facilities'
    pop = json.loads((ROOT/'data/task4_v7_istanbul/official_web_verified_values.json').read_text())['population2025']['value']
    assert pop == 15754053
    pdf = subprocess.check_output(['pdftotext','-layout', str(source/'iett2025.pdf'), '-']).decode()
    assert '2025 yılı itibarıyla İstanbul genelinde bulunan 12.426 adet durağa' in ' '.join(pdf.split())
    names = [r['name'] for r in csv.DictReader((source/'pool_venues2025.csv').open())]
    assert len(names) == len(set(names)) == 24
    expected = {'public_transport_density':12426*100000/(12426*100000+50*pop),
                'public_pool_density':24*100000/(24*100000+pop)}
    for r in json.loads((source/'observations.json').read_text()):
        assert r['city']=='Istanbul' and r['lower_bound_only']
        np.testing.assert_allclose(r['utility_after'], [expected[r['indicator']],1], atol=1e-15, rtol=0)
    lo0, hi0 = evidence_bounds()
    data = ROOT/'results/task4_v114_istanbul_revision'
    bound = pd.read_csv(data/'utility_bounds.csv',float_precision='round_trip')
    ranks = pd.read_csv(data/'ranks.csv',float_precision='round_trip')
    signatures, checks = set(), []
    i = CITIES.index('Istanbul')
    for scenario in bound.scenario.unique():
        b = bound[bound.scenario==scenario]
        assert b.city.tolist()==[c for c in CITIES for _ in NAMES]
        assert b.indicator.tolist()==NAMES*len(CITIES)
        lo = b.lower.to_numpy().reshape(25,10)
        hi = b.upper.to_numpy().reshape(25,10)
        np.testing.assert_array_equal(hi,hi0)
        active = []
        target = lo0.copy()
        for indicator, value in expected.items():
            j = NAMES.index(indicator)
            if lo[i,j] != lo0[i,j]:
                target[i,j] = value
                active.append(indicator)
        np.testing.assert_allclose(lo,target,atol=1e-15,rtol=0)
        assert np.all(lo>=lo0)
        signatures.add(tuple(sorted(active)))
        for mode,w in [('inherited',np.array([.05 if n in expected else .1125 for n in NAMES])),('equal',np.ones(10)/10)]:
            selected=ranks[(ranks.scenario==scenario)&(ranks.weight_reference==mode)]
            assert selected.city.tolist()==CITIES
            lower,upper=score(lo,w),score(hi,w)
            regret=np.array([max(0,np.delete(upper,k).max()-lower[k]) for k in range(25)])
            decision=1+(regret[:,None]>regret[None,:]).sum(axis=1)
            possible=np.array([upper[k]>=np.delete(lower,k).max()-1e-12 for k in range(25)])
            necessary=np.array([lower[k]>=np.delete(upper,k).max()-1e-12 for k in range(25)])
            best=np.array([1+np.sum(np.delete(lower,k)>upper[k]+1e-12) for k in range(25)])
            worst=np.array([1+np.sum(np.delete(upper,k)>lower[k]+1e-12) for k in range(25)])
            for col, values in [('score_lower',lower),('score_upper',upper),('max_regret',regret),('decision_rank',decision),('possible_champion',possible),('necessary_champion',necessary),('best_rank',best),('worst_rank',worst)]:
                np.testing.assert_allclose(selected[col],values,atol=5e-13,rtol=0,err_msg=col)
            checks.append(dict(scenario=scenario,weights=mode,possible=int(possible.sum()),recommendation=CITIES[int(np.argmin(regret))],istanbul_rank=int(decision[i]),istanbul_lower=float(lower[i]),istanbul_upper=float(upper[i])))
    assert signatures=={(),('public_pool_density',),('public_transport_density',),tuple(sorted(expected))}
    result=dict(status='passed',ablation_scenarios=4,weight_scenarios=2,cities_per_scenario=25,
        independent_formula=True,derived_observation_values=expected,unchanged_non_target_cells=248,
        all_upper_bounds_unchanged=True,checks=checks,
        baseline_bounds_sha256=hashlib.sha256(np.stack([lo0,hi0]).astype('<f8').tobytes()).hexdigest(),
        source_qualification='Physical-stop inventory subset and named municipal swimming venues: lower bounds only, not teenage actual accessibility or full-year operation.')
    (OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    run()
