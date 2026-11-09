"""Independent raw-record, scalar-decision and paired-weight checks for V153."""
from pathlib import Path
import csv
import hashlib
import json
import math
import numpy as np
import pandas as pd
from task4_user_v136_revision import revised_bounds

R = Path(__file__).resolve().parents[1]
P = Path('/data/projects/HiMCM-Overleaf')
D = R / 'data/task4_v153_milan'
O = R / 'results/task4_v153_milan_proposal'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def direct_scores(z, draws):
    positive = np.sqrt(np.einsum('ij,kj->ki', z * z, draws))
    negative = np.sqrt(np.einsum('ij,kj->ki', (1 - z) ** 2, draws))
    return 100 * positive / (positive + negative)


def main():
    extraction = json.loads((D / 'extraction.json').read_text())
    for n, h in {**extraction['originals_sha256'], **extraction['derived_sha256']}.items():
        assert sha(D / n) == h, n
    assert sha(D / 'extract.py') == extraction['extractor_sha256']
    raw = json.loads((D / 'stations_original.geojson').read_text())['features']
    ids = json.loads((D / 'ids_original.json').read_text())['objectIds']
    assert len(raw) == len(set(ids)) == 130
    assert {f['properties']['OBJECTID'] for f in raw} == set(ids)
    municipal = [f for f in raw if f['properties']['comune'] == 'Milano' and f['properties']['cod_istat'] == '015146']
    assert len(municipal) == 109
    with (D / 'retained_hubs.csv').open() as handle:
        hubs = list(csv.DictReader(handle))
    assert len(hubs) == 104
    assigned = [int(i) for h in hubs for i in h['objectids'].split('|')]
    assert len(assigned) == len(set(assigned)) == 109
    assert set(assigned) == {f['properties']['OBJECTID'] for f in municipal}
    expected = {frozenset(pair) for pair in [
        ['SAN AMBROGIO', 'S.AMBROGIO'], ['LOTTO M5', 'LOTTO FIERAMILANOCITY'],
        ['LORETO M2', 'LORETO M1'], ['DUOMO M3', 'DUOMO M1'], ['CADORNA FN M2', 'CADORNA FN M1']]}
    assert {frozenset(h['names'].split(' | ')) for h in hubs if int(h['line_station_records']) > 1} == expected
    assert extraction['map_visual_review']
    proposal = json.loads((O / 'summary.json').read_text())
    for n, h in proposal['source_sha256'].items():
        assert sha(R / n) == h, n
    for n, h in proposal['result_sha256'].items():
        assert sha(O / n) == h, n
    assert sha(R / 'scripts/task4_v153_milan_proposal.py') == proposal['generator_sha256']
    frame, old_lo, old_hi = revised_bounds()
    cities = frame.city.tolist()
    assert len(cities) == 16
    focal = cities.index('Milan')
    j = 6  # Current schema: transport-density anchor is 50, not mode share.
    assert old_lo[focal, j] == 0 and old_hi[focal, j] == 1
    population = float(frame.iloc[focal].population)
    assert population == proposal['population'] == 1399079
    u = (104 * 100000 / population) / (50 + 104 * 100000 / population)
    assert math.isclose(u, proposal['utility_proposed'][0], abs_tol=1e-15)
    new_lo = old_lo.copy()
    new_lo[focal, j] = u
    ranking = pd.read_csv(O / 'rank_comparison.csv')
    monte = pd.read_csv(O / 'paired_weight_summary.csv')
    scalar_checked, mc_checked = 0, 0
    for ref, center in [('fixed', np.array([.1125] * 6 + [.05, .1125, .1125, .05])), ('equal', np.ones(10) / 10)]:
        for scenario, lo in [('V136_active', old_lo), ('V153_proposed', new_lo)]:
            lower = direct_scores(lo, center[None, :])[0]
            upper = direct_scores(old_hi, center[None, :])[0]
            rows = ranking[(ranking.weight_reference == ref) & (ranking.scenario == scenario)].set_index('city').loc[cities]
            np.testing.assert_allclose(rows.score_lower, lower, atol=1e-12, rtol=0)
            np.testing.assert_allclose(rows.score_upper, upper, atol=1e-12, rtol=0)
            for i in range(16):
                others = [k for k in range(16) if k != i]
                assert math.isclose(rows.iloc[i].max_regret, max(0, upper[others].max() - lower[i]), abs_tol=1e-12)
                assert rows.iloc[i].possible_champion == (upper[i] >= lower[others].max() - 1e-12)
                scalar_checked += 1
        for concentration in [20, 100, 500]:
            draws = np.random.default_rng(np.random.SeedSequence([20261108, concentration])).dirichlet(concentration * center, 10000)
            for scenario, lo in [('V136_active', old_lo), ('V153_proposed', new_lo)]:
                lower, upper = direct_scores(lo, draws), direct_scores(old_hi, draws)
                regret = np.column_stack([np.maximum(0, upper[:, [k for k in range(16) if k != i]].max(axis=1) - lower[:, i]) for i in range(16)])
                for i, city in enumerate(cities):
                    ahead = (regret < regret[:, [i]] - 1e-12).sum(axis=1)
                    ties = (np.abs(regret - regret[:, [i]]) <= 1e-12).sum(axis=1)
                    frequency = np.clip((1 - ahead) / ties, 0, 1).mean()
                    rank = (1 + ahead + (ties - 1) / 2).mean()
                    other = [k for k in range(16) if k != i]
                    possible = (upper[:, i] >= lower[:, other].max(axis=1) - 1e-12).mean()
                    row = monte[(monte.weight_reference == ref) & (monte.concentration == concentration) & (monte.scenario == scenario) & (monte.city == city)].iloc[0]
                    np.testing.assert_allclose([row.minimax_recommendation_frequency, row.mean_decision_rank, row.possible_champion_frequency], [frequency, rank, possible], atol=1e-12, rtol=0)
                    mc_checked += 1
    baseline = json.loads((R / 'results/task4_v151_shared_entry/verification.json').read_text())
    science = baseline['scientific_file_sha256']
    papers = dict(baseline['manuscript_files_unchanged_sha256'])
    papers.update(json.loads((R / 'results/task4_v151_shared_entry/delivery.json').read_text())['support_file_sha256'])
    papers.update(json.loads((R / 'results/task4_v152_tail_access/delivery.json').read_text())['selected_file_sha256'])
    for n, h in science.items():
        assert sha(R / n) == h, n
    for n, h in papers.items():
        assert sha(P / n) == h, n
    audit = dict(status='pass', iteration='V153', raw_ID_completeness=True,
                 original_records=130, matched_municipal_records=109, distinct_hubs=104,
                 scalar_city_cases=scalar_checked, MC_summary_rows=mc_checked,
                 paired_weight_draws_per_arm=60000, source_and_result_hashes=True,
                 protected_scientific_files=len(science), unchanged_manuscript_files=len(papers),
                 active_primary_data_admissions=0, proposed_lower_bound_additions=1,
                 current_registry_unchanged=True, no_current_service_or_age_access_claim=True,
                 source_sha256={str(p.relative_to(R)): sha(p) for p in [D / 'extraction.json', O / 'summary.json', O / 'rank_comparison.csv', O / 'paired_weight_summary.csv']},
                 verifier_sha256=sha(Path(__file__)))
    (O / 'audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    print(json.dumps({k: audit[k] for k in ['status', 'distinct_hubs', 'scalar_city_cases', 'MC_summary_rows', 'protected_scientific_files', 'unchanged_manuscript_files']}, indent=2))


if __name__ == '__main__':
    main()
