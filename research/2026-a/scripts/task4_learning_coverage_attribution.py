"""Account for V87 rank changes due to measurement and evidence coverage.

Eight hybrid states are algebraic diagnostics, not alternative coherent city
rankings. Three disjoint interventions transform resource baseline into the
conditional learning model. Average marginal changes over all six orders;
report their range to expose order dependence. This is not causal attribution.
"""
import hashlib
import itertools
import json
from math import factorial
import numpy as np
import pandas as pd
from task4_current_model import current_bounds
from task4_learning_stage_sensitivity import learning_bounds
from task4_v5_model import ROOT, CITIES, NAMES, weights, summarize
from scipy.stats import norm

ACTIONS = ('withdraw_resource_only', 'replace_common_measure', 'add_learning_only')
METRICS = ('decision_rank', 'max_regret', 'score_lower', 'score_upper')


def interventions(base, target, column):
    known_base = (base[0][:, column] > 0) | (base[1][:, column] < 1)
    known_target = (target[0][:, column] > 0) | (target[1][:, column] < 1)
    return (known_base & ~known_target, known_base & known_target,
            ~known_base & known_target)


def apply_actions(base, target, masks, subset, column):
    result = [a.copy() for a in base]
    for k in subset:
        for dest, source in zip(result, target):
            dest[masks[k], column] = source[masks[k], column]
    return tuple(result)


def attribute(states, metric):
    """Exact permutation accounting, with ranges of marginal changes."""
    rows = []
    marginal = {k: [] for k in range(3)}
    for order in itertools.permutations(range(3)):
        visited = frozenset()
        for action in order:
            after = visited | {action}
            marginal[action].append(states[after][metric].to_numpy() - states[visited][metric].to_numpy())
            visited = after
    total = states[frozenset(range(3))][metric].to_numpy() - states[frozenset()][metric].to_numpy()
    contributions = []
    for k, action in enumerate(ACTIONS):
        changes = np.array(marginal[k])
        mean = changes.mean(axis=0)
        contributions.append(mean)
        for i, city in enumerate(CITIES):
            rows.append(dict(city=city, metric=metric, action=action,
                average_marginal_change=mean[i], minimum_order_change=changes[:, i].min(),
                maximum_order_change=changes[:, i].max(), total_change=total[i]))
    np.testing.assert_allclose(np.sum(contributions, axis=0), total, rtol=0, atol=1e-12)
    return rows


def main():
    source = ROOT/'data/task4_v87_pisa_cities/outcomes.csv'
    records = pd.read_csv(source)
    records['city'] = records.city.replace({'Greater London': 'London'})
    records = records.loc[records.metric.eq('math_level2_fraction') & records.domain.isin(['grade_ge10', 'isced3'])]
    assert len(records) == 10
    base_lo, base_hi, config = current_bounds()
    base = (base_lo, base_hi)
    target = learning_bounds(base, records, 'isced3', norm.ppf(1-.05/20))
    j = NAMES.index('upper_secondary_ptr')
    masks = interventions(base, target, j)
    assert not any(np.any(a & b) for a, b in itertools.combinations(masks, 2))
    for a, b in zip(apply_actions(base, target, masks, range(3), j), target):
        np.testing.assert_array_equal(a, b)
    # Anchor both endpoints to the already-reviewed V87 numerical artifacts.
    old = pd.read_csv(ROOT/'results/task4_v87_learning_stage/ranks.csv')
    states, frames, reports = {}, [], []
    for size in range(4):
        for subset in itertools.combinations(range(3), size):
            lower, upper = apply_actions(base, target, masks, subset, j)
            frame, decision = summarize(lower, upper, weights(config['fixed_alpha']))
            key = frozenset(subset); states[key] = frame
            if size in (0, 3):
                reference = old.loc[old.scenario.eq('resource_baseline' if size == 0 else 'isced3')]
                assert reference.city.tolist() == CITIES
                np.testing.assert_allclose(frame[list(METRICS)], reference[list(METRICS)], rtol=0, atol=1e-12)
            label = '+'.join(ACTIONS[k] for k in subset) or 'resource_baseline'
            frames.append(frame.assign(scenario=label))
            reports.append(dict(scenario=label, actions=list(subset),
                possible_champions=int(frame.possible_champion.sum()),
                minimax_choices=[CITIES[i] for i in decision['minimax_choices']]))
    rows = [row for metric in METRICS for row in attribute(states, metric)]
    out = ROOT/'results/task4_v88_coverage_attribution'
    out.mkdir(parents=True, exist_ok=True)
    pd.concat(frames).to_csv(out/'diagnostic_states.csv', index=False)
    pd.DataFrame(rows).to_csv(out/'attribution.csv', index=False)
    rank = pd.DataFrame(rows).query("metric == 'decision_rank'").pivot(index='city', columns='action', values='average_marginal_change')
    rank['baseline_rank'] = states[frozenset()].set_index('city').decision_rank
    rank['learning_rank'] = states[frozenset(range(3))].set_index('city').decision_rank
    rank.to_csv(out/'rank_attribution.csv')
    result = dict(baseline_model=config['model_version'], main_admitted=False,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        endpoint_ranks_sha256=hashlib.sha256((ROOT/'results/task4_v87_learning_stage/ranks.csv').read_bytes()).hexdigest(),
        actions={a:[c for i,c in enumerate(CITIES) if masks[k][i]] for k,a in enumerate(ACTIONS)},
        permutations=factorial(3), states=reports, endpoint_validation=True, conservation_verified=True,
        interpretation='Exact accounting over six orders; hybrid states mix distinct constructs and are diagnostics only. Rank units and regret-point changes are not causal effects or improvements in city conditions.',
        continuous_endpoint_evidence='Endpoints reproduce V87; main-model continuous ranking separately rerun in V88 intake.')
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(rank.to_string())


if __name__ == '__main__':
    main()
