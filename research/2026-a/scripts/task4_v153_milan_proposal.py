"""Admission-ready Milan inventory proposal on frozen V136; registry unchanged."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from task4_user_v136_revision import revised_bounds
from task4_user_city_indicators import evaluate
from task4_v5_model import NAMES, SPEC, weights
from task4_ahp_mc_baseline import score_many, interval_metrics, rank_metrics

R = Path(__file__).resolve().parents[1]
D = R / 'data/task4_v153_milan'
O = R / 'results/task4_v153_milan_proposal'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def proposed_bounds():
    frame, lo, hi = revised_bounds()
    source = json.loads((D / 'extraction.json').read_text())
    for name, h in {**source['originals_sha256'], **source['derived_sha256']}.items():
        assert sha(D / name) == h, name
    i, j = frame.city.tolist().index('Milan'), NAMES.index('public_transport_density')
    assert lo[i, j] == 0 and hi[i, j] == 1
    count = source['municipal_unique_station_hubs']
    population = float(frame.iloc[i].population)
    density = count * 100000 / population
    lo[i, j] = density / (SPEC[j][2] + density)
    return frame, lo, hi


def main():
    O.mkdir(exist_ok=True)
    frame, before_lo, before_hi = revised_bounds()
    _, after_lo, after_hi = proposed_bounds()
    cities = frame.city.tolist()
    focal = cities.index('Milan')
    indicator = NAMES.index('public_transport_density')
    summaries, frames = [], []
    for reference, w in [('fixed', weights(.1)), ('equal', np.ones(10) / 10)]:
        for scenario, lo, hi in [('V136_active', before_lo, before_hi), ('V153_proposed', after_lo, after_hi)]:
            evaluated = evaluate(cities, lo, hi, w)
            frames.append(evaluated.assign(scenario=scenario, weight_reference=reference))
            summaries.append(dict(weight_reference=reference, scenario=scenario,
                                  mean_score_interval_width=float((evaluated.score_upper - evaluated.score_lower).mean()),
                                  minimax_choices=evaluated.loc[evaluated.decision_rank == 1, 'city'].tolist(),
                                  possible_champions=evaluated.loc[evaluated.possible_champion, 'city'].tolist(),
                                  necessary_champions=evaluated.loc[evaluated.necessary_champion, 'city'].tolist(),
                                  milan_score_lower=float(evaluated.iloc[focal].score_lower),
                                  milan_score_upper=float(evaluated.iloc[focal].score_upper),
                                  milan_decision_rank=int(evaluated.iloc[focal].decision_rank)))
    pd.concat(frames, ignore_index=True).to_csv(O / 'rank_comparison.csv', index=False)
    mc = []
    for reference, center in [('fixed', weights(.1)), ('equal', np.ones(10) / 10)]:
        for concentration in [20, 100, 500]:
            draws = np.random.default_rng(np.random.SeedSequence([20261108, concentration])).dirichlet(concentration * center, 10000)
            for scenario, lo, hi in [('V136_active', before_lo, before_hi), ('V153_proposed', after_lo, after_hi)]:
                lower, upper = score_many(lo, draws), score_many(hi, draws)
                regret, possible, _, _, _ = interval_metrics(lower, upper)
                rank, recommended, _ = rank_metrics(regret, descending=False)
                for i, city in enumerate(cities):
                    mc.append(dict(weight_reference=reference, concentration=concentration,
                                   scenario=scenario, city=city,
                                   minimax_recommendation_frequency=float(recommended[:, i].mean()),
                                   mean_decision_rank=float(rank[:, i].mean()),
                                   possible_champion_frequency=float(possible[:, i].mean())))
    pd.DataFrame(mc).to_csv(O / 'paired_weight_summary.csv', index=False)
    assert np.count_nonzero(after_lo != before_lo) == 1
    np.testing.assert_array_equal(after_hi, before_hi)
    pop = float(frame.iloc[focal].population)
    source_files = [D / 'extraction.json', R / 'design/task4_user_current_model.json', R / 'data/task4_v117_team_intake/city_indicators.csv']
    result = dict(iteration='V153', status='validated proposal; not activated',
                  primary_version_unchanged='V136', extensions_unchanged='V137', paper_unchanged='V148',
                  city='Milan', indicator=NAMES[indicator], raw_count=104, population=pop,
                  population_year=2025, inventory_date='2024-10-16', historical_inventory_proxy=True,
                  density_per_100000=104 * 100000 / pop, anchor=SPEC[indicator][2],
                  utility_before=[0, 1], utility_proposed=[float(after_lo[focal, indicator]), 1],
                  changed_proposed_cells=1, unchanged_proposed_cells=159,
                  proposed_counts=dict(point=112, partial=34, unknown=14),
                  comparisons=summaries, MC_seed=20261108, draws_per_setting=10000,
                  MC_scope='Paired preference perturbations only; no random completion of missing values or real-world winning probability',
                  active_primary_data_admissions=0,
                  activation_work_remaining='Rebase current extensions and manuscript outputs as one reviewed transition; do not relabel the frozen V136/V137/V148 outputs.',
                  source_sha256={str(p.relative_to(R)): sha(p) for p in source_files},
                  result_sha256={n: sha(O / n) for n in ['rank_comparison.csv', 'paired_weight_summary.csv']},
                  generator_sha256=sha(Path(__file__)))
    (O / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['raw_count', 'population', 'density_per_100000', 'utility_proposed']}, indent=2))
    for old, new in zip(summaries[::2], summaries[1::2]):
        print(old['weight_reference'], old['mean_score_interval_width'], '->', new['mean_score_interval_width'], new['minimax_choices'])


if __name__ == '__main__':
    main()
