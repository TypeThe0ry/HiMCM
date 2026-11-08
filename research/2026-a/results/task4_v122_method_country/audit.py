"""Independent loops check saved V122 point methods and separate case summaries."""
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
summary = json.loads((HERE/'summary.json').read_text())
for path, value in summary['input_sha256'].items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == value, path
ranks = pd.read_csv(HERE/'method_ranks.csv')
bounds = pd.read_csv(HERE/'method_utility_inputs.csv')
components = pd.read_csv(HERE/'method_components.csv')
order = ['homicide_rate', 'pm25', 'cost_living_index', 'price_income_ratio',
         'upper_secondary_ptr', 'research_he_density', 'public_transport_density',
         'travel', 'fixed_broadband_mbps', 'public_pool_density']

def scaled(x):
    low, high = min(x), max(x)
    return [(v-low)/(high-low) if high-low > 1e-14 else 0 for v in x]


def score(x, w):
    dm = math.sqrt(sum(weight*u*u for weight, u in zip(w, x)))
    dp = math.sqrt(sum(weight*(1-u)**2 for weight, u in zip(w, x)))
    return 100*dm/(dm+dp)


checks = []
for (version, reference), saved in ranks.groupby(['evidence_version', 'weight_reference'], sort=False):
    w = [.1]*10 if reference == 'equal' else [.05 if i in (6, 9) else .1125 for i in range(10)]
    cities = saved.city.tolist()
    z = [[float(bounds[(bounds.evidence_version == version) & (bounds.city == c) & (bounds.indicator == j)].midpoint.iloc[0]) for j in order] for c in cities]
    worst = [min(row[j] for row in z) for j in range(10)]
    best = [max(row[j] for row in z) for j in range(10)]
    t, S, R = [], [], []
    for c, row in zip(cities, z):
        losses = [w[j]*(best[j]-row[j])/(best[j]-worst[j]) if best[j]-worst[j] > 1e-14 else 0 for j in range(10)]
        t.append(score(row, w)); S.append(sum(losses)); R.append(max(losses))
        seen = components[(components.evidence_version == version) & (components.weight_reference == reference) & (components.city == c)].set_index('indicator').loc[order]
        np.testing.assert_allclose(seen.vikor_weighted_relative_shortfall, losses, rtol=0, atol=1e-12)
    Q = [.5*s + .5*r for s, r in zip(scaled(S), scaled(R))]
    for name, values in [('topsis_midpoint_score', t), ('vikor_S', S), ('vikor_R', R), ('vikor_Q', Q)]:
        np.testing.assert_allclose(saved[name], values, rtol=0, atol=1e-12)
    np.testing.assert_array_equal(saved.topsis_rank, [1+sum(q > v for q in t) for v in t])
    np.testing.assert_array_equal(saved.vikor_rank, [1+sum(q < v for q in Q) for v in Q])
    checks.append(dict(version=version, weight_reference=reference, cities=len(cities), independent_scores_shortfalls_and_ranks=True))

legacy = pd.read_csv(ROOT/'results/task4_v117_city_revision/utility_bounds.csv').query("scenario == 'v117'")
for row in pd.read_csv(HERE/'country_score_comparison.csv').itertuples():
    for city, lower, upper in [(row.city_a, row.a_score_lower, row.a_score_upper), (row.city_b, row.b_score_lower, row.b_score_upper)]:
        cell = legacy[legacy.city == city].set_index('indicator').loc[order]
        np.testing.assert_allclose([score(cell.lower.tolist(), [.05 if i in (6,9) else .1125 for i in range(10)]),
                                   score(cell.upper.tolist(), [.05 if i in (6,9) else .1125 for i in range(10)])],
                                  [lower, upper], rtol=0, atol=1e-12)
    assert not row.a_necessarily_strictly_better and not row.b_necessarily_strictly_better

raw = json.loads((ROOT/'data/task4_v32_shanghai/extracted.json').read_text())
district = pd.read_csv(HERE/'shanghai_district_resources.csv')
np.testing.assert_array_equal(district.students, [r['values'][2] for r in raw['tables']['students'][1:]])
np.testing.assert_array_equal(district.teachers, [r['values'][-1] for r in raw['tables']['teachers'][1:]])
u = 15/(15+district.students/district.teachers)
p = district.students/district.students.sum()
local = float(np.sum(p*u)); pooled = 15/(15+district.students.sum()/district.teachers.sum())
pd.testing.assert_series_equal(u, district.resource_utility, check_names=False, atol=1e-14, rtol=0)
low = pd.DataFrame({'u':u, 'p':p}).sort_values('u')
lo_mass = np.minimum(low.p, np.maximum(0, .2-(low.p.cumsum()-low.p)))
np.testing.assert_allclose([pooled, local, pooled-local, np.sum(low.u*lo_mass)/.2],
    [summary['equity']['pooled_utility'], summary['equity']['student_weighted_district_utility'], summary['equity']['aggregation_gap'], summary['equity']['bottom20_student_mass_district_utility']], rtol=0, atol=1e-14)

age = json.loads((ROOT/'data/task4_v116_ibb/aggregate_results.json').read_text())
control = json.loads((ROOT/'data/task4_v116_ibb_review/aggregate_controls.json').read_text())
assert sum(g['weight_total'] for g in age['age_groups'].values()) == control['known']['weight']
assert control['optional']['weight'] == 4487
assert sum(g['weight_optional_known_age'] for g in age['age_groups_optional_membership'].values()) + 612 == 4487
for row in pd.read_csv(HERE/'istanbul_historical_age_groups.csv').itertuples():
    group = age['age_groups'][row.age_group]
    extra = age['age_groups_optional_membership'][row.age_group]
    mass = group['weight_total'] + extra['weight_optional_known_age'] + 612
    lo = group['utility_known_numerator']/mass
    hi = (group['utility_known_numerator']+group['weight_unknown']+mass-group['weight_total'])/mass
    np.testing.assert_allclose([lo, hi], [row.marginal_utility_lower, row.marginal_utility_upper], rtol=0, atol=1e-14)

out = dict(status='pass', method_cases=checks, historical_country_scores=True,
           shanghai_source_counts_and_bottom20=True, historical_age_mass_and_marginals=True,
           input_hashes_unchanged=True, no_main_registry_or_raw_input_edits=True,
           scope='Independent arithmetic audit; source scope limitations remain as documented.')
(HERE/'audit.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
