"""Isolated 2012 Istanbul travel scenarios; the V114 registry stays unchanged."""
import hashlib
import json
import math

import numpy as np
import pandas as pd
from scipy.stats import kendalltau

from task4_v114_istanbul_revision import istanbul_bounds
from task4_v5_model import ROOT, CITIES, NAMES, weights, summarize

OUT = ROOT / 'results/task4_v116_historical_travel'
DATA = ROOT / 'data/task4_v116_ibb/aggregate_results.json'
CONTROLS = ROOT / 'data/task4_v116_ibb_review/aggregate_controls.json'


def verified_observations():
    data = json.loads(DATA.read_text())
    control = json.loads(CONTROLS.read_text())
    known = data['summary']
    hist = data['duration_histogram']
    numerator = sum(v['weight'] * math.exp(-float(t) / 30) for t, v in hist.items())
    assert math.isclose(numerator, known['utility_known_numerator'], rel_tol=1e-12)
    assert sum(v['weight'] for v in hist.values()) == known['weight_observed']
    assert known['weight_total'] == control['known']['weight']
    assert known['n'] == control['known']['count']
    assert known['weight_total'] - known['weight_observed'] == known['weight_unknown']
    optional = control['optional']['weight']
    den = known['weight_total'] + optional
    bound = data['historical_conditional_bounds']
    assert bound['weight_maximum_denominator'] == den
    assert math.isclose(bound['lower'], numerator / den, rel_tol=1e-12)
    assert math.isclose(bound['upper'], (numerator + known['weight_unknown'] + optional) / den, rel_tol=1e-12)
    assert data['strict_current_year_bounds']['lower'] == 0
    assert data['strict_current_year_bounds']['upper'] == 1
    assert data['sampling_confidence_interval'] is None
    return data


def run():
    data = verified_observations()
    OUT.mkdir(parents=True, exist_ok=True)
    base = istanbul_bounds()
    assert base[0].shape == base[1].shape == (25, 10)
    i, j = CITIES.index('Istanbul'), NAMES.index('travel')
    np.testing.assert_array_equal([base[0][i, j], base[1][i, j]], [0, 1])
    known, bound = data['summary'], data['historical_conditional_bounds']
    cases = [('current_v114', (0, 1)),
             ('2012_known_cohort', (known['utility_lower'], known['utility_upper'])),
             ('2012_optional_membership', (bound['lower'], bound['upper'])),
             ('withdrawal', (0, 1))]
    mask = np.ones((25, 10), dtype=bool)
    mask[i, j] = False
    frames, reports, utility_rows = [], [], []
    for label, travel in cases:
        lo, hi = (a.copy() for a in base)
        lo[i, j], hi[i, j] = travel
        np.testing.assert_array_equal(lo[mask], base[0][mask])
        np.testing.assert_array_equal(hi[mask], base[1][mask])
        assert np.all((0 <= lo) & (lo <= hi) & (hi <= 1))
        if label in {'current_v114', 'withdrawal'}:
            np.testing.assert_array_equal(lo, base[0])
            np.testing.assert_array_equal(hi, base[1])
        for ref, w in [('inherited', weights(.1)), ('equal', np.ones(10) / 10)]:
            old, _ = summarize(*base, w)
            frame, decision = summarize(lo, hi, w)
            if label == 'withdrawal':
                pd.testing.assert_frame_equal(frame, old, check_exact=True)
            frame['previous_decision_rank'] = old.decision_rank
            frame['rank_change_positive_improves'] = old.decision_rank - frame.decision_rank
            frame['score_width'] = frame.score_upper - frame.score_lower
            frame['score_width_before'] = old.score_upper - old.score_lower
            frame['score_width_reduction'] = frame.score_width_before - frame.score_width
            frames.append(frame.assign(scenario=label, weight_reference=ref))
            reports.append(dict(scenario=label, weight_reference=ref,
                changed_cells=int(np.count_nonzero((lo != base[0]) | (hi != base[1]))),
                changed_ranks=int((frame.decision_rank != old.decision_rank).sum()),
                kendall_tau_b=float(kendalltau(old.decision_rank, frame.decision_rank, variant='b').statistic),
                possible_champions=frame.loc[frame.possible_champion, 'city'].tolist(),
                necessary_champions=frame.loc[frame.necessary_champion, 'city'].tolist(),
                minimax_choices=[CITIES[k] for k in decision['minimax_choices']],
                minimax_regret=decision['minimax_regret'],
                mean_score_width=float(frame.score_width.mean()),
                istanbul=frame.loc[frame.city == 'Istanbul'].iloc[0].to_dict()))
        utility_rows.extend(dict(scenario=label, city=c, indicator=n,
            lower=lo[ci, ni], upper=hi[ci, ni])
            for ci, c in enumerate(CITIES) for ni, n in enumerate(NAMES))
    pd.concat(frames, ignore_index=True).to_csv(OUT / 'ranks.csv', index=False)
    pd.DataFrame(utility_rows).to_csv(OUT / 'utility_bounds.csv', index=False)
    age_rows = []
    for group, observed in data['age_groups'].items():
        optional = data['age_groups_optional_membership'][group]
        age_rows.append(dict(city='Istanbul', year=2012, age_group=group,
            **observed, optional_member_lower=optional['lower'],
            optional_member_upper=optional['upper'],
            optional_known_age_weight=optional['weight_optional_known_age'],
            optional_unknown_age_weight=optional['weight_optional_unknown_age']))
    pd.DataFrame(age_rows).to_csv(OUT / 'istanbul_age_groups.csv', index=False)
    result = dict(model_version='V116 historical conditional comparison', baseline_model='V114',
        main_registry_changed=False, scenarios=reports,
        unchanged_cells_per_scenario=249, withdrawal_exactly_restores_baseline=True,
        weights_and_transforms_unchanged=True, sampling_confidence_interval=None,
        scope='Only Istanbul travel is replaced in isolated 2012 empirical scenarios. This is not a 2025 measurement or a sampling CI. Decision rank orders worst-case regret, not identified city quality.',
        age_scope=data['age_groups_optional_membership_note'],
        weights={ref: dict(zip(NAMES, w.tolist())) for ref, w in [('inherited', weights(.1)), ('equal', np.ones(10)/10)]},
        input_bounds_sha256=hashlib.sha256(np.stack(base).astype('<f8').tobytes()).hexdigest(),
        aggregate_sha256=hashlib.sha256(DATA.read_bytes()).hexdigest(),
        membership_controls_sha256=hashlib.sha256(CONTROLS.read_bytes()).hexdigest())
    (OUT / 'summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps([dict(scenario=r['scenario'], weights=r['weight_reference'],
        istanbul_rank=r['istanbul']['decision_rank'],
        champions=len(r['possible_champions']), kendall=r['kendall_tau_b'],
        score_width=r['istanbul']['score_width']) for r in reports], indent=2))
    return result


if __name__ == '__main__':
    run()
