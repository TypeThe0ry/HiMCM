"""Single-cell source uncertainty and full-withdrawal diagnostics.

No measured bound is changed. A certified prefix covers epsilon and alpha;
withdrawal certificates cover alpha at epsilon=1 only, not the intervening gap.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from task4_current_model import current_bounds
from task4_joint_uncertainty_stress import expand, certify_prefix, protect_output
from task4_continuous_recommendation import certify
from task4_v5_model import ROOT, CITIES, NAMES, score, weights, summarize


def regrets(lo, hi, alpha):
    lower, upper = score(lo, weights(alpha)), score(hi, weights(alpha))
    return np.array([max(0., np.delete(upper, i).max()-lower[i]) for i in range(len(lo))])


def cell_bounds(lo, hi, epsilon, cell):
    if (not isinstance(cell, tuple) or len(cell) != 2
        or any(not isinstance(k, (int, np.integer)) for k in cell)
        or not 0 <= cell[0] < len(lo) or not 0 <= cell[1] < 10):
        raise ValueError('A valid city/indicator tuple is required')
    return expand(lo, hi, epsilon, cell)


def run(out):
    lo, hi, config = current_bounds()
    before = np.stack([lo, hi]).astype('<f8').tobytes()
    digest = hashlib.sha256(before).hexdigest()
    protect_output(out, lo, hi, config)
    base_regrets = regrets(lo, hi, config['fixed_alpha'])
    if np.count_nonzero(base_regrets == base_regrets.min()) != 1:
        raise ValueError('A unique fixed-preference baseline recommendation is required')
    choice = int(np.argmin(base_regrets))
    amin, amax = config['alpha_range']
    alpha_points = sorted(set([amin, config['fixed_alpha'], amax]))
    records, prefixes, withdrawals, cases, witness_frames = [], [], [], [], []
    for i, city in enumerate(CITIES):
        for j, indicator in enumerate(NAMES):
            cell = (i, j)
            key = dict(target_city=city, target_indicator=indicator, city_index=i, indicator_index=j)
            prefix = certify_prefix(lo, hi, choice, emax=.2, amin=amin, amax=amax,
                                    max_depth=12, target=cell)
            prefixes.extend({**key, **r} for r in prefix)
            withdrawn_lo, withdrawn_hi = cell_bounds(lo, hi, 1., cell)
            withdrawal = certify(withdrawn_lo, withdrawn_hi, amin, amax, max_depth=12)
            for r in withdrawal:
                r['winner_city'] = None if r['winner'] is None else CITIES[r['winner']]
                withdrawals.append({**key, **r})
            rec = {**key, 'initial_lower': lo[cell], 'initial_upper': hi[cell],
                   'withdrawal_changes_input': bool(lo[cell] > 0 or hi[cell] < 1),
                   'prefix_leaves': len(prefix),
                   'prefix_unresolved': sum(not r['certified'] for r in prefix),
                   'prefix_minimum_gap_lower': min(r['gap_lower'] for r in prefix),
                   'withdrawal_leaves': len(withdrawal),
                   'withdrawal_unresolved': sum(not r['certified'] for r in withdrawal),
                   'withdrawal_certified_winners': '|'.join(sorted({r['winner_city'] for r in withdrawal if r['certified']})),
                   'withdrawal_point_witnesses': 0}
            for epsilon in (.2, 1.):
                l, h = cell_bounds(lo, hi, epsilon, cell)
                for alpha in alpha_points:
                    rr = regrets(l, h, alpha)
                    gap = float(np.delete(rr, choice).min()-rr[choice])
                    winner = int(np.argmin(rr))
                    row = {**key, 'epsilon': epsilon, 'alpha': alpha,
                           'baseline_choice_gap': gap, 'minimum_regret_city': CITIES[winner],
                           'minimum_regret': float(rr[winner]), 'baseline_choice_regret': float(rr[choice]),
                           'strict_failure_witness': gap < -1e-8}
                    cases.append(row)
                    if row['strict_failure_witness']:
                        frame, _ = summarize(l, h, weights(alpha))
                        witness_frames.append(frame.assign(**key, epsilon=epsilon, alpha=alpha))
                        if epsilon == 1.: rec['withdrawal_point_witnesses'] += 1
            records.append(rec)
    assert before == np.stack([lo, hi]).astype('<f8').tobytes()
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([dict(city=c, indicator=n, lower=lo[i,j], upper=hi[i,j])
                  for i,c in enumerate(CITIES) for j,n in enumerate(NAMES)]).to_csv(out/'baseline_bounds.csv', index=False)
    pd.DataFrame(records).to_csv(out/'cells.csv', index=False)
    pd.DataFrame(prefixes).to_csv(out/'prefix_certificates.csv', index=False)
    pd.DataFrame(withdrawals).to_csv(out/'withdrawal_certificates.csv', index=False)
    pd.DataFrame(cases).to_csv(out/'point_cases.csv', index=False)
    if witness_frames:
        pd.concat(witness_frames).to_csv(out/'failure_witness_ranks.csv', index=False)
    else:
        pd.DataFrame(columns=['city','target_city','target_indicator','epsilon','alpha']).to_csv(out/'failure_witness_ranks.csv', index=False)
    result = dict(model_version=config['model_version'], input_bounds_sha256=digest,
        fixed_alpha=config['fixed_alpha'], alpha_range=config['alpha_range'],
        baseline_choice=CITIES[choice], cells=len(records), admitted_cells_changed=0,
        informative_cells=sum(r['withdrawal_changes_input'] for r in records),
        already_unknown_cells=sum(not r['withdrawal_changes_input'] for r in records),
        prefix_epsilon_range=[0,.2], prefix_certified_cells=sum(r['prefix_unresolved']==0 for r in records),
        prefix_leaves=len(prefixes), prefix_unresolved=sum(not r['certified'] for r in prefixes),
        withdrawal_epsilon=1., withdrawal_leaves=len(withdrawals),
        withdrawal_unresolved=sum(not r['certified'] for r in withdrawals),
        withdrawal_cells_with_alternative_certified_winner=[dict(city=r['target_city'], indicator=r['target_indicator'])
            for r in records if any(c != CITIES[choice] for c in r['withdrawal_certified_winners'].split('|') if c)],
        point_cases=len(cases), failure_point_cases=sum(r['strict_failure_witness'] for r in cases),
        score_padding=1e-9, strict_tolerance=1e-8, max_depth=12, main_admitted=False,
        interpretation='Numerical single-cell sensitivity scenarios, not observed source errors, acquisition values, probabilities or certified behavior for epsilon between .2 and 1.')
    (out/'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT/'results/task4_v99_cell_stress')
    run(parser.parse_args().output)
