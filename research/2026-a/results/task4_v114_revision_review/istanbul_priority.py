"""Endpoint-only acquisition diagnostic. No hypothetical values enter the model."""
from pathlib import Path
import itertools
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'results/task4_v114_istanbul_revision/utility_bounds.csv'
frame = pd.read_csv(SOURCE)
indicators = frame.indicator.drop_duplicates().tolist()
cities = frame.city.drop_duplicates().tolist()
i = cities.index('Istanbul')

def score(u, w):
    dm = np.sqrt(np.sum(w*u*u, axis=-1))
    dp = np.sqrt(np.sum(w*(1-u)**2, axis=-1))
    return 100*dm/(dm+dp)

results = []
for scenario in ['v113', 'v114']:
    data = frame[frame.scenario == scenario]
    lo = data.pivot(index='city', columns='indicator', values='lower').loc[cities, indicators].to_numpy()
    hi = data.pivot(index='city', columns='indicator', values='upper').loc[cities, indicators].to_numpy()
    uncertain = np.flatnonzero(hi[i] > lo[i])
    for reference in ['inherited', 'equal']:
        w = np.array([.05 if x in ['public_transport_density', 'public_pool_density'] else .1125 for x in indicators]) if reference == 'inherited' else np.ones(10)/10
        other_lower = score(lo, w)
        other_lower[i] = -np.inf
        threshold = float(other_lower.max())
        witness = cities[int(other_lower.argmax())]
        excluded, minimal = [], []
        for size in range(1, len(uncertain)+1):
            for subset in itertools.combinations(uncertain, size):
                endpoint = hi[i].copy()
                endpoint[list(subset)] = lo[i,list(subset)]
                upper = float(score(endpoint, w))
                if upper < threshold - 1e-12:
                    names = [indicators[j] for j in subset]
                    excluded.append(dict(cells=names, upper_score=upper, exclusion_margin=threshold-upper))
                    if not any(set(m['cells']).issubset(names) for m in minimal):
                        minimal.append(excluded[-1])
        results.append(dict(scenario=scenario, weight_reference=reference,
            uncertain_cells=[indicators[j] for j in uncertain],
            comparator_city=witness, comparator_lower_score=threshold,
            original_upper_score=float(score(hi[i],w)),
            tested_subsets=2**len(uncertain)-1, excluding_subsets=len(excluded),
            minimum_cells=min(map(lambda r:len(r['cells']),minimal),default=None),
            minimal_excluding_bundles=minimal))

out = dict(scope='Hypothetically resolve selected Istanbul uncertain cells exactly to their CURRENT lower endpoints, leaving all other upper endpoints and all other cities unchanged. This is a best-case exclusion feasibility diagnostic, not observed data, a forecast, or a probability. Non-exclusion at these most adverse legal endpoints proves the selected bundle alone cannot exclude Istanbul under this fixed-weight rectangular-bound model.',
           no_model_mutation=True, scenarios=results)
Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(results, indent=2))
