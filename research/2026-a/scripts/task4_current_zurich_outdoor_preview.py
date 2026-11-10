"""Isolated four-venue preview against V205; does not activate new evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from task4_user_v205_revision import revised_bounds
from task4_user_city_indicators import SOURCE, evaluate
from task4_v5_model import NAMES, weights
from task4_ahp_mc_baseline import score_many, interval_metrics, rank_metrics

R = Path(__file__).resolve().parents[1]
D = R / 'data/current_zurich_outdoor_pool_route'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(output):
    if output.exists():
        raise ValueError('Use a new preview output directory')
    for record in json.loads((D / 'retrievals.json').read_text()):
        assert sha(D / record['file']) == record['sha256']
    evidence = json.loads((D / 'extraction.json').read_text())
    venues = evidence['four_candidate_venues_not_admitted']
    assert {v['name'] for v in venues} == {
        'Freibad Allenmoos', 'Freibad Heuried', 'Freibad Letzigraben', 'Freibad Seebach'}
    assert all(v['municipality'] == 'Zürich' for v in venues)
    f, lower, upper = revised_bounds()
    before = np.stack([lower, upper]).copy()
    cities = f.city.tolist()
    z, j = cities.index('Zurich'), NAMES.index('public_pool_density')
    population = int(f.iloc[z].population)
    assert population == evidence['population_retained_as_given'] == 440935
    assert f.iloc[z].population_year == evidence['population_year_as_given'] == 2025
    assert abs(lower[z, j] - 1200000 / (population + 1200000)) < 1e-15
    candidate = lower.copy()
    candidate[z, j] = 1600000 / (population + 1600000)
    mask = np.ones(lower.shape, dtype=bool)
    mask[z, j] = False
    np.testing.assert_array_equal(candidate[mask], lower[mask])
    references = [('fixed', weights(.1)), ('equal', np.full(10, .1))]
    ranks, summaries, mc = [], [], []
    for reference, center in references:
        base_width = None
        for label, a in [('retained_V205', lower), ('candidate_16_not_admitted', candidate)]:
            table = evaluate(cities, a, upper, center)
            width = float((table.score_upper - table.score_lower).mean())
            if base_width is None:
                base_width = width
            summaries.append(dict(scenario=label, weight_reference=reference,
                choices=table.loc[table.decision_rank.eq(1), 'city'].tolist(),
                possible_champions=int(table.possible_champion.sum()),
                necessary_champions=int(table.necessary_champion.sum()),
                mean_width=width, conditional_mean_width_reduction=base_width-width))
            ranks.append(table.assign(scenario=label, weight_reference=reference))
        for concentration in [20, 100, 500]:
            draws = np.random.default_rng(np.random.SeedSequence([20261108, concentration])).dirichlet(
                concentration * center, 10000)
            for label, a in [('retained_V205', lower), ('candidate_16_not_admitted', candidate)]:
                regret, possible, _, _, _ = interval_metrics(score_many(a, draws), score_many(upper, draws))
                rank, recommended, _ = rank_metrics(regret, descending=False)
                mc.extend(dict(scenario=label, weight_reference=reference, concentration=concentration,
                    city=city, minimax_recommendation_frequency=float(recommended[:, k].mean()),
                    mean_decision_rank=float(rank[:, k].mean()),
                    possible_champion_frequency=float(possible[:, k].mean())) for k, city in enumerate(cities))
    np.testing.assert_array_equal(np.stack(revised_bounds()[1:]), before)
    files = list(D.iterdir()) + [Path(__file__).resolve(), SOURCE,
        R/'data/task4_v196_zurichpool/school_candidates.json', R/'design/task4_user_v205_snapshot.json']
    files += [Path(m.__file__).resolve() for m in list(sys.modules.values())
              if getattr(m, '__file__', None) and Path(m.__file__).resolve().parent == R/'scripts']
    output.mkdir(parents=True)
    pd.concat(ranks, ignore_index=True).to_csv(output/'city_cases.csv', index=False)
    pd.DataFrame(mc).to_csv(output/'mc_city_summary.csv', index=False)
    report = dict(status='pass isolated candidate preview', primary_model='V205 unchanged',
        results=summaries, raw_count_before=12, candidate_count=16,
        candidate_utility_lower=float(candidate[z, j]), other159_lower_and_all160_upper_preserved=True,
        source_sha256={str(p.relative_to(R)): sha(p) for p in sorted(set(files)) if p.is_file()},
        output_sha256={n: sha(output/n) for n in ['city_cases.csv', 'mc_city_summary.csv']},
        scalar_city_rows=64, paired_MC_settings=12, draws_per_setting=10000, seed=20261108,
        primary_admissions=0, actual_primary_width_reduction=0,
        changes_primary_model=False, changes_manuscript=False,
        scope='Four seasonal outdoor artificial-pool venues; retained2025 population with2026 capture/schedules. '
              'Address-based municipal screen, source-defined venue supply, not a complete census, '
              'winter opening, universal student access or observed operation. '
              'Full controlled extensions, qualification, activation and manuscript migration remain separate. '
              'MC frequencies are conditional simulation frequencies, not empirical city win probabilities.')
    (output/'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'status': report['status'], 'results': summaries}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    main(parser.parse_args().output)
