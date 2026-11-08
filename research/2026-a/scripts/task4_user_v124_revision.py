"""Evidence-only update of the authoritative sixteen-city V121 bounds."""
import hashlib
import json

import numpy as np
import pandas as pd

from task4_ahp_mc_baseline import interval_metrics, rank_metrics, score_many
from task4_user_city_indicators import SOURCE, evaluate
from task4_user_v121_revision import revised_bounds as previous_bounds
from task4_v5_model import NAMES, ROOT, SPEC, weights

MANIFEST = ROOT / 'design/task4_user_v124_admissions.json'
OUT = ROOT / 'results/task4_user_v124_revision'


def revised_bounds(selected=None):
    frame, lo, hi = previous_bounds()
    before = np.stack([lo, hi]).copy()
    manifest = json.loads(MANIFEST.read_text())
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == manifest['input_sha256']
    for path, digest in manifest['source_hashes'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    seen = set()
    for row in manifest['observations']:
        key = (row['city'], row['indicator'])
        assert key not in seen, key
        seen.add(key)
        if selected is not None and key not in selected:
            continue
        i = frame.city.tolist().index(row['city'])
        j = NAMES.index(row['indicator'])
        np.testing.assert_array_equal([lo[i, j], hi[i, j]], [0, 1])
        anchor = SPEC[j][2]
        if row.get('kind') == 'ratio_interval':
            assert row['indicator'] == 'upper_secondary_ptr'
            low, high = row['ratio_bounds']
            assert 0 <= low <= high
            new = [anchor / (anchor + high), anchor / (anchor + low)]
        else:
            assert row['indicator'] in {'public_transport_density', 'public_pool_density'}
            assert float(frame.iloc[i].population) == row['population']
            assert row['raw_count'] > 0 and row['lower_bound_only']
            density = row['raw_count'] * 100000 / row['population']
            new = [density / (anchor + density), 1]
        np.testing.assert_allclose(new, row['utility_after'], atol=1e-12, rtol=0)
        lo[i, j], hi[i, j] = new
    protected = ~((before[0] == 0) & (before[1] == 1))
    np.testing.assert_array_equal(np.stack([lo, hi])[:, protected], before[:, protected])
    assert np.all(lo >= before[0]) and np.all(hi <= before[1]) and np.all(lo <= hi)
    return frame, lo, hi


def without_historical_proxy(frame, lo, hi):
    lo, hi = lo.copy(), hi.copy()
    i, j = frame.city.tolist().index('Singapore'), NAMES.index('travel')
    lo[i, j], hi[i, j] = 0, 1
    return lo, hi


def main():
    frame, lo0, hi0 = previous_bounds()
    _, lo, hi = revised_bounds()
    cities = frame.city.tolist()
    observations = json.loads(MANIFEST.read_text())['observations']
    keys = {(r['city'], r['indicator']) for r in observations}
    cases = [('before', lo0, hi0)]
    for key in sorted(keys):
        _, l, h = revised_bounds({key})
        cases.append(('only:' + ':'.join(key), l, h))
    cases.append(('after_conditional', lo, hi))
    for key in sorted(keys):
        _, l, h = revised_bounds(keys - {key})
        cases.append(('without:' + ':'.join(key), l, h))
    historical_keys = {(r['city'], r['indicator']) for r in observations
                       if r.get('historical_inventory_proxy')}
    _, l, h = revised_bounds(keys - historical_keys)
    cases.append(('withdraw_new_historical_inventories', l, h))
    _, l, h = revised_bounds(set())
    np.testing.assert_array_equal(l, lo0)
    np.testing.assert_array_equal(h, hi0)
    cases.append(('withdraw_all_new', l, h))
    cases.append(('before_withdraw_historical_stage_proxy', *without_historical_proxy(frame, lo0, hi0)))
    cases.append(('withdraw_historical_stage_proxy', *without_historical_proxy(frame, lo, hi)))
    ranks, bounds, summaries = [], [], []
    for name, l, h in cases:
        for reference, w in [('fixed', weights(.1)), ('equal', np.ones(10) / 10)]:
            old = evaluate(cities, lo0, hi0, w)
            result = evaluate(cities, l, h, w)
            result['previous_decision_rank'] = old.decision_rank
            result['rank_change_positive_improves'] = old.decision_rank - result.decision_rank
            ranks.append(result.assign(scenario=name, weight_reference=reference))
            summaries.append(dict(
                scenario=name, weight_reference=reference,
                possible_champions=result.loc[result.possible_champion, 'city'].tolist(),
                necessary_champions=result.loc[result.necessary_champion, 'city'].tolist(),
                minimax_choices=result.loc[result.decision_rank == 1, 'city'].tolist(),
                mean_width=float((result.score_upper - result.score_lower).mean())))
        bounds.extend(dict(scenario=name, city=c, indicator=n, lower=l[i, j], upper=h[i, j])
                      for i, c in enumerate(cities) for j, n in enumerate(NAMES))
    OUT.mkdir(parents=True, exist_ok=True)
    all_ranks = pd.concat(ranks, ignore_index=True)
    all_ranks.to_csv(OUT / 'all_ranks.csv', index=False)
    all_ranks[all_ranks.scenario == 'after_conditional'].to_csv(OUT / 'current_ranks.csv', index=False)
    pd.DataFrame(bounds).to_csv(OUT / 'utility_bounds.csv', index=False)
    mc = []
    mc_cases = [case for case in cases if case[0] in {
        'before', 'after_conditional', 'before_withdraw_historical_stage_proxy',
        'withdraw_historical_stage_proxy'}]
    for reference, center in [('fixed', weights(.1)), ('equal', np.ones(10) / 10)]:
        for concentration in (20, 100, 500):
            w = np.random.default_rng(np.random.SeedSequence([20261108, concentration])).dirichlet(
                concentration * center, 10000)
            for name, l, h in mc_cases:
                lower, upper = score_many(l, w), score_many(h, w)
                regret, possible, _, _, _ = interval_metrics(lower, upper)
                rank, recommended, _ = rank_metrics(regret, descending=False)
                np.testing.assert_allclose(recommended.sum(axis=1), 1)
                for i, city in enumerate(cities):
                    mc.append(dict(scenario=name, weight_reference=reference,
                                   concentration=concentration, city=city,
                                   minimax_recommendation_frequency=float(recommended[:, i].mean()),
                                   mean_decision_rank=float(rank[:, i].mean()),
                                   possible_champion_frequency=float(possible[:, i].mean())))
    pd.DataFrame(mc).to_csv(OUT / 'mc_city_summary.csv', index=False)
    summary = dict(
        version='V124', baseline='V121 user16', results=summaries,
        changed_cells=int(np.sum((lo != lo0) | (hi != hi0))),
        unchanged_cells=int(np.sum((lo == lo0) & (hi == hi0))),
        protected_nonmissing_cells=int(np.sum(~((lo0 == 0) & (hi0 == 1)))),
        point_cells=int(np.sum(lo == hi)),
        partial_cells=int(np.sum((lo < hi) & ((lo > 0) | (hi < 1)))),
        fully_missing_cells=int(np.sum((lo == 0) & (hi == 1))),
        input_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        admissions_sha256=hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
        mc_seed=20261108, mc_draws_per_setting=10000,
        scope='Conditional mixed-vintage evidence; historical Singapore stage proxy '
              'separately withdrawn in both comparison arms. Weight frequencies are not actual winning probabilities.')
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
