"""Exact per-city impossibility certificates for perfect future measurements.

No simulated observations enter the city model. The worst completion for each
candidate simultaneously minimizes its remaining upper score and maximizes
every rival's remaining lower score for every allowed alpha.
"""
import json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT, CITIES, NAMES, score, weights, summarize
from task4_melbourne_observed_travel import melbourne_bounds
from task4_continuous_preferences import feasible_preferences


def certificate(lower, upper, measured):
    lo, hi = np.asarray(lower, float), np.asarray(upper, float)
    mask = np.asarray(measured)
    if lo.ndim != 2 or lo.shape != hi.shape or lo.shape[1] != 10 or len(lo) < 2:
        raise ValueError('At least two cities with ten indicators required')
    if mask.shape != lo.shape or mask.dtype != bool:
        raise ValueError('Boolean measured-cell mask required')
    if not (np.isfinite(lo).all() and np.isfinite(hi).all()
            and np.all((0 <= lo) & (lo <= hi) & (hi <= 1))):
        raise ValueError('Finite ordered utility intervals in [0,1] required')
    worst_upper = np.where(mask, lo, hi)
    best_lower = np.where(mask, hi, lo)
    upper_scores = score(worst_upper, weights())
    lower_scores = score(best_lower, weights())
    rows = []
    for i in range(len(lo)):
        others = np.arange(len(lo)) != i
        margin = float(upper_scores[i] - lower_scores[others].max())
        continuous = feasible_preferences(worst_upper[i], best_lower[others])
        witness = continuous['witness_alpha']
        if witness is not None:
            checked = score(np.vstack([worst_upper[i], best_lower[others]]), weights(witness))
            assert checked[0] >= checked[1:].max() - 1e-8
        rows.append(dict(index=i, fixed_unavoidable=margin >= -1e-10,
                         worst_fixed_margin=margin,
                         continuous_unavoidable=continuous['possible'],
                         witness_alpha=witness))
    return rows


def checks():
    # Exhaust all completions for a small two-cell binary example; this checks
    # the universal quantifier rather than just one favorable completion.
    lo = np.full((3, 10), .2)
    hi = np.full((3, 10), .8)
    mask = np.zeros_like(lo, bool)
    mask[0, 4] = mask[1, 7] = True
    certified = certificate(lo, hi, mask)
    fixed_all = np.ones(3, bool)
    continuous_all = np.ones(3, bool)
    for a in (0, 1):
        for b in (0, 1):
            l, h = lo.copy(), hi.copy()
            l[0, 4] = h[0, 4] = [.2, .8][a]
            l[1, 7] = h[1, 7] = [.2, .8][b]
            ls, us = score(l, weights()), score(h, weights())
            for i in range(3):
                others = np.arange(3) != i
                fixed_all[i] &= us[i] >= ls[others].max() - 1e-10
                continuous_all[i] &= feasible_preferences(h[i], l[others])['possible']
    assert fixed_all.tolist() == [r['fixed_unavoidable'] for r in certified]
    assert continuous_all.tolist() == [r['continuous_unavoidable'] for r in certified]
    # Full revelation allows each nondegenerate equal candidate to lose.
    assert not any(r['continuous_unavoidable'] for r in certificate(lo, hi, np.ones_like(mask)))
    # Known ties cannot be excluded even after every cell is measured.
    assert all(r['continuous_unavoidable'] for r in certificate(lo, lo, np.ones_like(mask)))
    try:
        certificate(hi, lo, mask)
    except ValueError:
        pass
    else:
        raise AssertionError('Reversed intervals accepted')


def main():
    checks()
    lo, hi = melbourne_bounds()
    original = (lo.copy(), hi.copy())
    education, travel = NAMES.index('upper_secondary_ptr'), NAMES.index('travel')
    scopes = [('all_education', [education], None), ('all_travel', [travel], None),
              ('all_education_and_travel', [education, travel], None),
              ('phoenix_education_and_travel', [education, travel], CITIES.index('Phoenix'))]
    scopes += [('both_plus_' + name, [education, travel, j], None)
               for j, name in enumerate(NAMES) if j not in (education, travel)]
    rows, summaries = [], []
    for label, indicators, city in scopes:
        mask = np.zeros_like(lo, bool)
        if city is None:
            mask[:, indicators] = True
        else:
            mask[city, indicators] = True
        cert = certificate(lo, hi, mask)
        for r in cert:
            rows.append(dict(scenario=label, city=CITIES[r['index']], **r))
        fixed = [CITIES[r['index']] for r in cert if r['fixed_unavoidable']]
        continuous = [CITIES[r['index']] for r in cert if r['continuous_unavoidable']]
        summaries.append(dict(scenario=label, measured_indicators=[NAMES[j] for j in indicators],
            selected_cells=int(mask.sum()), currently_nonpoint_cells=int((mask & (lo < hi)).sum()),
            fixed_unavoidable_cities=fixed, continuous_unavoidable_cities=continuous,
            fixed_champion_count_lower_bound=max(1, len(fixed)),
            continuous_champion_count_lower_bound=max(1, len(continuous))))
        if label == 'all_education_and_travel':
            a, b = np.where(mask, lo, hi), np.where(mask, hi, lo)
            sa, sb = score(a, weights(.2)), score(b, weights(.2))
            margins = [float(sa[i] - np.delete(sb, i).max()) for i in range(len(lo))]
            assert min(margins) > 0
            summaries[-1]['common_alpha_certificate'] = dict(alpha=.2,
                minimum_score_margin=min(margins), city=CITIES[int(np.argmin(margins))])
    for x, y in zip(original, (lo, hi)):
        np.testing.assert_array_equal(x, y)
    out = ROOT / 'results/task4_v45_acquisition_limits'
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out / 'certificates.csv', index=False)
    rank, decision = summarize(lo, hi, weights())
    prior = pd.read_csv(ROOT / 'results/task4_v44_melbourne/ranks.csv')
    prior = prior[prior.scenario == 'v44_destination_check_same_inference'].reset_index(drop=True)
    assert rank.city.tolist() == prior.city.tolist()
    for key in ['score_lower', 'score_upper', 'decision_rank', 'max_regret', 'possible_champion']:
        np.testing.assert_allclose(rank[key], prior[key], rtol=0, atol=1e-12)
    rank.to_csv(out / 'ranks.csv', index=False)
    result = dict(baseline='V44 melbourne_bounds', new_admitted_cells=0,
        fixed_alpha=.1, alpha_range=[.05, .2],
        claim='Cities remain possible under every exact completion of selected cells within existing utility intervals; all other intervals and definitions fixed.',
        count_bound_is_not_generally_joint_minimum=True,
        fixed_score_tolerance=1e-10, continuous_polynomial_tolerance=1e-12,
        choice=[CITIES[k] for k in decision['minimax_choices']],
        possible_champions=int(rank.possible_champion.sum()), scenarios=summaries)
    (out / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps([{k: v for k, v in r.items() if not k.endswith('_cities')}
                      for r in summaries], indent=2))


if __name__ == '__main__':
    main()
