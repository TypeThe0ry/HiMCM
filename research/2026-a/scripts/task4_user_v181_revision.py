"""One-cell evidence update: Amsterdam mapped metro subset on V154 user16."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from task4_user_v154_revision import revised_bounds as previous_bounds
from task4_user_v136_revision import without_historical_proxy
from task4_user_city_indicators import SOURCE, evaluate
from task4_v5_model import NAMES, ROOT, SPEC, weights
from task4_ahp_mc_baseline import score_many, interval_metrics, rank_metrics

OUT = ROOT / 'results/task4_user_v181_revision'
MANIFEST = ROOT / 'design/task4_user_v181_admissions.json'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def revised_bounds(include_amsterdam=True):
    frame, lo, hi = previous_bounds()
    before = np.stack([lo, hi]).copy()
    manifest = json.loads(MANIFEST.read_text())
    assert sha(SOURCE) == manifest['input_sha256']
    for n, h in manifest['source_hashes'].items():
        assert sha(ROOT / n) == h, n
    row = manifest['observations'][0]
    assert row['city'] == 'Amsterdam' and row['indicator'] == 'public_transport_density'
    assert row['raw_count'] == 32 and row['inventory_metadata_year'] == 2026
    assert row['population_year'] == 2025 and row['lower_bound_only']
    assert not row['screen_is_positional_error_bound']
    i, j = frame.city.tolist().index('Amsterdam'), NAMES.index('public_transport_density')
    assert lo[i, j] == 0 and hi[i, j] == 1
    assert float(frame.iloc[i].population) == row['population']
    density = row['raw_count'] * 100000 / row['population']
    if include_amsterdam:
        lo[i, j] = density / (SPEC[j][2] + density)
        np.testing.assert_allclose([lo[i, j], hi[i, j]], row['utility_after'], atol=1e-15, rtol=0)
    protected = np.ones((16, 10), dtype=bool)
    protected[i, j] = False
    np.testing.assert_array_equal(np.stack([lo, hi])[:, protected], before[:, protected])
    return frame, lo, hi


def main():
    frame, lo0, hi0 = previous_bounds()
    _, lo, hi = revised_bounds()
    cities = frame.city.tolist()
    OUT.mkdir(exist_ok=True)
    cases = [('before_V154', lo0, hi0), ('after_conditional', lo, hi),
             ('withdraw_Amsterdam_mapped_inventory', lo0, hi0),
             ('withdraw_historical_stage_proxy', *without_historical_proxy(frame, lo, hi))]
    ranks, bounds, reports, mc = [], [], [], []
    for label, l, h in cases:
        for ref, w in [('fixed', weights(.1)), ('equal', np.ones(10) / 10)]:
            t = evaluate(cities, l, h, w)
            ranks.append(t.assign(scenario=label, weight_reference=ref))
            reports.append(dict(scenario=label, weight_reference=ref,
                                possible_champions=t.loc[t.possible_champion, 'city'].tolist(),
                                necessary_champions=t.loc[t.necessary_champion, 'city'].tolist(),
                                minimax_choices=t.loc[t.decision_rank == 1, 'city'].tolist(),
                                mean_width=float((t.score_upper - t.score_lower).mean())))
        bounds.extend(dict(scenario=label, city=c, indicator=n, lower=l[i,j], upper=h[i,j])
                      for i,c in enumerate(cities) for j,n in enumerate(NAMES))
    for ref, center in [('fixed', weights(.1)), ('equal', np.ones(10) / 10)]:
        for concentration in [20, 100, 500]:
            draws = np.random.default_rng(np.random.SeedSequence([20261108, concentration])).dirichlet(concentration * center, 10000)
            for label, l, h in cases:
                lower, upper = score_many(l, draws), score_many(h, draws)
                regret, possible, _, _, _ = interval_metrics(lower, upper)
                rank, recommended, _ = rank_metrics(regret, descending=False)
                for i, city in enumerate(cities):
                    mc.append(dict(scenario=label, weight_reference=ref, concentration=concentration, city=city,
                                   minimax_recommendation_frequency=float(recommended[:,i].mean()),
                                   mean_decision_rank=float(rank[:,i].mean()), possible_champion_frequency=float(possible[:,i].mean())))
    ranks = pd.concat(ranks, ignore_index=True)
    ranks.to_csv(OUT / 'all_ranks.csv', index=False)
    ranks[ranks.scenario == 'after_conditional'].to_csv(OUT / 'current_ranks.csv', index=False)
    pd.DataFrame(bounds).to_csv(OUT / 'utility_bounds.csv', index=False)
    pd.DataFrame(mc).to_csv(OUT / 'mc_city_summary.csv', index=False)
    result = dict(version='V181', activation_status='staged_not_active', baseline='V154 user16', results=reports,
                  changed_cells=1, unchanged_cells=159, protected_nonmissing_cells=146,
                  point_cells=112, partial_cells=35, fully_missing_cells=13,
                  cumulative_supplements=23, input_sha256=sha(SOURCE), admissions_sha256=sha(MANIFEST),
                  mc_seed=20261108, mc_draws_per_setting=10000,
                  scope='Conditional mixed-vintage inventory; no user value, weight, anchor or interval rule changed; explicit Amsterdam inventory and Singapore stage-proxy withdrawal cases')
    (OUT / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print('V181 staged primary: 112 point / 35 partial / 13 unknown; 23 cumulative supplements')


if __name__ == '__main__':
    main()
