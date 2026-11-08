"""Verify published aggregates without downloading or storing individual data."""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / 'aggregate_results.json').read_text())
controls = json.loads((HERE.parent / 'task4_v116_ibb_review' / 'aggregate_controls.json').read_text())
summary = data['summary']
hist = data['duration_histogram']
reasons = data['unknown_reasons']
assert sum(v['n'] for v in hist.values()) == summary['n_observed'] == 1811
assert sum(v['weight'] for v in hist.values()) == summary['weight_observed'] == 499950
assert sum(v['n'] for v in reasons.values()) == controls['known']['count'] == 2463
assert sum(v['weight'] for v in reasons.values()) == controls['known']['weight'] == 677016
numerator = sum(v['weight'] * math.exp(-float(t) / 30) for t, v in hist.items())
assert math.isclose(numerator, summary['utility_known_numerator'], rel_tol=1e-12)
optional = controls['optional']['weight']
assert optional == 4487
assert controls['optional']['count'] == 15
denominator = summary['weight_total'] + optional
bound = data['historical_conditional_bounds']
assert denominator == bound['weight_maximum_denominator'] == 681503
assert math.isclose(bound['lower'], numerator / denominator, rel_tol=1e-12)
assert math.isclose(bound['upper'], (numerator + summary['weight_unknown'] + optional) / denominator, rel_tol=1e-12)
assert summary['weight_unknown'] == 177066
assert data['sampling_confidence_interval'] is None
assert data['strict_current_year_bounds']['lower'] == 0
assert data['strict_current_year_bounds']['upper'] == 1
assert sum(v['weight_total'] for v in data['age_groups'].values()) == summary['weight_total']
assert sum(v['weight_total'] for v in data['districts']) == summary['weight_total']
for label, known_optional in [('14–15', 1442), ('16–18', 2433)]:
    group = data['age_groups'][label]
    marginal = data['age_groups_optional_membership'][label]
    optional_marginal = known_optional + 612
    den = group['weight_total'] + optional_marginal
    assert math.isclose(marginal['lower'], group['utility_known_numerator'] / den, rel_tol=1e-12)
    assert math.isclose(marginal['upper'], (group['utility_known_numerator'] + group['weight_unknown'] + optional_marginal) / den, rel_tol=1e-12)
print('PASS histogram, roster mass, independent optional membership, age marginals, historical endpoints, strict current-year bounds')
