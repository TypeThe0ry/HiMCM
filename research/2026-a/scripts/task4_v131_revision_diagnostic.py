"""Controlled point-scenario versus interval decision on frozen V130 user16.

This is a diagnostic model comparison, not a claimed historical initial model,
new evidence admission, or change to the authoritative V130 ranking.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kendalltau

from task4_user_city_indicators import SOURCE, evaluate
from task4_user_v121_revision import revised_bounds as previous_bounds
from task4_user_v130_revision import MANIFEST, revised_bounds
from task4_v123_revision_diagnostic import independent_scores, independent_intervals
from task4_v5_model import NAMES, ROOT, score as production_score, weights

OUT = ROOT/'results/task4_v131_revision_diagnostic'
OLD = ROOT/'results/task4_v123_revision_diagnostic'
INTERMEDIATE = ROOT/'results/task4_v125_revision_diagnostic'
SNAPSHOT = ROOT/'design/task4_user_v130_snapshot.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    snapshot = json.loads(SNAPSHOT.read_text())
    assert snapshot['version'] == 'V130'
    for path, expected in snapshot['source_sha256'].items():
        assert digest(ROOT/path) == expected, path
    paths = [SOURCE, MANIFEST, ROOT/'design/task4_user_current_model.json',
             SNAPSHOT, *[p for p in sorted(INTERMEDIATE.iterdir()) if p.is_file()],
             ROOT/'scripts/task4_user_v130_revision.py', ROOT/'scripts/task4_v5_model.py',
             ROOT/'scripts/task4_v123_revision_diagnostic.py',
             *[p for p in sorted(OLD.iterdir()) if p.is_file()],
             ROOT/'scripts/task4_interval_decision.py',
             *[(ROOT/'results/task4_user_v130_revision'/name) for name in
               ['current_ranks.csv', 'utility_bounds.csv', 'all_ranks.csv', 'summary.json', 'mc_city_summary.csv']]]
    protected = {str(p.relative_to(ROOT)): digest(p) for p in paths}
    assert protected[str(SOURCE.relative_to(ROOT))] == '430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
    registry = json.loads((ROOT/'design/task4_user_current_model.json').read_text())
    assert registry['version'] in {'V127','V130'}
    previous_frame, previous_lo, previous_hi = previous_bounds()
    frame, lo, hi = revised_bounds()
    cities = frame.city.tolist()
    original = np.stack([lo, hi]).copy()
    assert lo.shape == (16, 10) and len(cities) == 16
    assert cities == previous_frame.city.tolist()
    uncertain, point = hi > lo, hi == lo
    assert uncertain.sum() == 48 and point.sum() == 112
    assert np.sum((lo == 0) & (hi == 1)) == 16
    intermediate_inputs = pd.read_csv(INTERMEDIATE/'utility_inputs.csv').set_index(['city', 'indicator'])
    input_index = pd.MultiIndex.from_product([cities, NAMES], names=['city', 'indicator'])
    intermediate_inputs = intermediate_inputs.loc[input_index]
    intermediate_lo = intermediate_inputs.lower.to_numpy().reshape(16, 10)
    intermediate_hi = intermediate_inputs.upper.to_numpy().reshape(16, 10)
    new_keys = {(cities[i], NAMES[j]) for i, j in zip(*np.where((lo != intermediate_lo) | (hi != intermediate_hi)))}
    # CSV float roundtrips may differ at machine epsilon; compare actual gains.
    new_keys = {(cities[i], NAMES[j]) for i, j in zip(*np.where(
        (abs(lo-intermediate_lo) > 1e-14) | (abs(hi-intermediate_hi) > 1e-14)))}
    assert new_keys == {('Prague', 'public_transport_density'), ('Vienna', 'public_transport_density'), ('Berlin', 'public_transport_density')}
    assert np.all(lo >= intermediate_lo-1e-14) and np.all(hi <= intermediate_hi+1e-14)
    midpoint = (lo+hi)/2
    current = pd.read_csv(ROOT/'results/task4_user_v130_revision/current_ranks.csv')
    comparisons, ranks, scenarios, scenario_bounds, witness_proofs, reports = [], [], [], [], [], []
    audit_rows = []
    references = [('fixed', weights(.1)), ('equal', np.ones(10)/10)]
    old_comparison = pd.read_csv(OLD/'rank_comparison.csv')
    control_checks, evidence_comparisons = [], []
    intermediate_ranks = pd.read_csv(INTERMEDIATE/'rank_comparison.csv')
    intermediate_summary = json.loads((INTERMEDIATE/'summary.json').read_text())
    intermediate_comparisons, intermediate_rows = [], []
    for ref, w in references:
        if ref == 'fixed':
            np.testing.assert_array_equal(w, np.array([.1125]*6+[.05,.1125,.1125,.05]))
        assert np.isclose(w.sum(), 1)
        revised = independent_intervals(lo, hi, w)
        shared = evaluate(cities, lo, hi, w)
        saved = current[(current.weight_reference == ref) & (current.scenario == 'after_conditional')].set_index('city').loc[cities]
        for key, value in revised.items():
            np.testing.assert_allclose(shared[key], value, atol=1e-12, rtol=0)
            np.testing.assert_allclose(saved[key], value, atol=1e-12, rtol=0)
        point_score = independent_scores(midpoint, w)
        point_rank = np.array([1+sum(point_score > x) for x in point_score])
        point_decision = independent_intervals(midpoint, midpoint, w)
        np.testing.assert_array_equal(point_decision['decision_rank'], point_rank)
        previous_midpoint = (previous_lo+previous_hi)/2
        previous_score = independent_scores(previous_midpoint, w)
        previous_point_rank = np.array([1+sum(previous_score > x) for x in previous_score])
        previous_interval = independent_intervals(previous_lo, previous_hi, w)
        previous_point_decision = independent_intervals(previous_midpoint, previous_midpoint, w)
        old = old_comparison[old_comparison.weight_reference == ref].set_index('city').loc[cities]
        control_columns = dict(midpoint_scenario_score=previous_score,
            midpoint_scenario_rank=previous_point_rank,
            midpoint_collapsed_max_regret=previous_point_decision['max_regret'],
            interval_score_lower=previous_interval['score_lower'],
            interval_score_upper=previous_interval['score_upper'],
            interval_max_regret=previous_interval['max_regret'],
            interval_decision_rank=previous_interval['decision_rank'],
            rank_change_positive_improves=previous_point_rank-previous_interval['decision_rank'],
            possible_champion=previous_interval['possible_champion'],
            necessary_champion=previous_interval['necessary_champion'],
            evidence_best_rank=previous_interval['best_rank'],
            evidence_worst_rank=previous_interval['worst_rank'])
        for column, value in control_columns.items():
            np.testing.assert_allclose(old[column], value, atol=1e-12, rtol=0)
        control_checks.append(dict(weight_reference=ref,
            changed_city_decision_ranks=int(np.sum(previous_point_rank != previous_interval['decision_rank'])),
            kendall_tau_b=float(kendalltau(previous_point_rank, previous_interval['decision_rank']).statistic),
            all_V123_rank_columns_reproduced=True))
        evidence_comparisons.append(dict(weight_reference=ref,
            changed_midpoint_ranks_V121_to_V130=int(np.sum(previous_point_rank != point_rank)),
            changed_interval_decision_ranks_V121_to_V130=int(np.sum(previous_interval['decision_rank'] != revised['decision_rank'])),
            previous_diagnostic_tau_b=float(kendalltau(previous_point_rank, previous_interval['decision_rank']).statistic),
            current_diagnostic_tau_b=float(kendalltau(point_rank, revised['decision_rank']).statistic)))
        assert revised['possible_champion'].sum() == 16 and not revised['necessary_champion'].any()
        winner = int(np.argmax(point_score))
        choice = int(np.argmin(revised['max_regret']))
        assert winner == choice == cities.index('Zurich')
        other = [k for k in range(16) if k != choice]
        adversary = other[int(np.argmax(revised['score_upper'][other]))]
        assert cities[adversary] == 'Dublin'

        # A full endpoint completion in the model's declared closed rectangle.
        endpoint = lo.copy(); endpoint[adversary] = hi[adversary]
        # A strict-interior counterexample avoids relying on open raw tails.
        interior = midpoint.copy(); interior[winner] = lo[winner]+.1*(hi[winner]-lo[winner])
        cases = [('midpoint_diagnostic', midpoint), ('adversarial_endpoint_Dublin', endpoint),
                 ('interior_counterexample', interior)]
        witness_summaries = []
        for label, z in cases:
            assert z.shape == lo.shape and np.all(z >= lo) and np.all(z <= hi)
            np.testing.assert_array_equal(z[point], lo[point])
            if label == 'adversarial_endpoint_Dublin':
                assert np.all((z == lo) | (z == hi))
            if label == 'interior_counterexample':
                assert np.all(z[uncertain] > lo[uncertain]) and np.all(z[uncertain] < hi[uncertain])
            values = independent_scores(z, w)
            np.testing.assert_allclose(production_score(z, w), values, atol=1e-12, rtol=0)
            scenario_rank = np.array([1+sum(values > x) for x in values])
            first = int(np.argmax(values))
            if label != 'midpoint_diagnostic':
                assert first == adversary and values[first] > values[winner]+1e-10
            gap = float(values[first]-values[choice])
            if label == 'adversarial_endpoint_Dublin':
                np.testing.assert_allclose(gap, revised['max_regret'][choice], atol=1e-12, rtol=0)
            witness_summaries.append(dict(scenario=label, first_city=cities[first],
                first_score=float(values[first]), midpoint_first_city=cities[winner],
                midpoint_first_score_in_this_completion=float(values[winner]),
                midpoint_first_rank_in_this_completion=int(scenario_rank[winner]),
                score_gap_first_minus_revised_choice=gap,
                completion_scope='A chosen utility completion within the retained rectangle, not an observation'))
            for i, city in enumerate(cities):
                scenarios.append(dict(weight_reference=ref, scenario=label, city=city,
                    score=float(values[i]), scenario_rank=int(scenario_rank[i]),
                    conditional_first=bool(scenario_rank[i] == 1)))
                for j, indicator in enumerate(NAMES):
                    scenario_bounds.append(dict(weight_reference=ref, scenario=label, city=city,
                        indicator=indicator, utility=float(z[i, j]), lower=float(lo[i, j]), upper=float(hi[i, j]),
                        point_identified=bool(point[i, j])))

        # Each possible city gets an explicit score witness in the rectangle.
        for i, city in enumerate(cities):
            z = lo.copy(); z[i] = hi[i]
            values = independent_scores(z, w)
            margin = float(values[i]-max(np.delete(values, i)))
            assert margin > 0 and revised['possible_champion'][i]
            np.testing.assert_allclose(values[i], revised['score_upper'][i], atol=1e-12, rtol=0)
            witness_proofs.append(dict(weight_reference=ref, focal_city=city,
                construction='focal city upper endpoint, all other cities lower endpoint',
                focal_score=float(values[i]), strongest_competitor_score=float(max(np.delete(values, i))),
                strict_win_margin=margin, within_closed_rectangular_model=True))

        for i, city in enumerate(cities):
            rows = dict(weight_reference=ref, city=city, midpoint_scenario_score=float(point_score[i]),
                midpoint_scenario_rank=int(point_rank[i]),
                midpoint_collapsed_max_regret=float(point_decision['max_regret'][i]),
                interval_score_lower=float(revised['score_lower'][i]), interval_score_upper=float(revised['score_upper'][i]),
                interval_max_regret=float(revised['max_regret'][i]), interval_decision_rank=int(revised['decision_rank'][i]),
                rank_change_positive_improves=int(point_rank[i]-revised['decision_rank'][i]),
                possible_champion=bool(revised['possible_champion'][i]),
                necessary_champion=bool(revised['necessary_champion'][i]),
                evidence_best_rank=int(revised['best_rank'][i]), evidence_worst_rank=int(revised['worst_rank'][i]))
            comparisons.append(rows)
        for i, city in enumerate(cities):
            for j, indicator in enumerate(NAMES):
                ranks.append(dict(city=city, indicator=indicator, lower=float(lo[i, j]),
                                  upper=float(hi[i, j]), midpoint_diagnostic=float(midpoint[i, j])))
        report = dict(weight_reference=ref, midpoint_scenario_first=cities[winner],
            interval_minimax_choices=[cities[k] for k in np.flatnonzero(revised['decision_rank'] == 1)],
            recommendation_changed=False,
            changed_city_decision_ranks=int(np.sum(point_rank != revised['decision_rank'])),
            kendall_tau_b=float(kendalltau(point_rank, revised['decision_rank']).statistic),
            possible_champions=[cities[k] for k in np.flatnonzero(revised['possible_champion'])],
            necessary_champions=[cities[k] for k in np.flatnonzero(revised['necessary_champion'])],
            conditional_point_scenario_first_count=int(np.sum(point_rank == 1)),
            point_scenario_certifies_a_necessary_champion=False,
            interval_mean_score_width=float(np.mean(revised['score_upper']-revised['score_lower'])),
            revised_choice_max_regret=float(revised['max_regret'][choice]),
            chosen_completion_counterexamples=witness_summaries)
        reports.append(report)
        middle = intermediate_ranks[intermediate_ranks.weight_reference == ref].set_index('city').loc[cities]
        middle_report = next(x for x in intermediate_summary['results'] if x['weight_reference'] == ref)
        current_rows = pd.DataFrame([row for row in comparisons if row['weight_reference'] == ref]).set_index('city').loc[cities]
        intermediate_comparisons.append(dict(weight_reference=ref,
            previous_extension='V125', previous_input='V124', current_extension='V131', current_input='V130',
            previous_changed_city_decision_ranks=middle_report['changed_city_decision_ranks'],
            current_changed_city_decision_ranks=report['changed_city_decision_ranks'],
            previous_diagnostic_tau_b=middle_report['kendall_tau_b'], current_diagnostic_tau_b=report['kendall_tau_b'],
            changed_midpoint_ranks=int((middle.midpoint_scenario_rank != current_rows.midpoint_scenario_rank).sum()),
            changed_interval_decision_ranks=int((middle.interval_decision_rank != current_rows.interval_decision_rank).sum()),
            previous_interval_mean_width=middle_report['interval_mean_score_width'],
            current_interval_mean_width=report['interval_mean_score_width'],
            previous_minimax_choices=middle_report['interval_minimax_choices'],
            current_minimax_choices=report['interval_minimax_choices']))
        intermediate_rows.append(current_rows.reset_index().merge(middle.reset_index(), on='city', suffixes=('_v130', '_v124')))
        audit_rows.append(dict(weight_reference=ref, production_scores_and_saved_V130_match=True,
                               self_excluded_regret_rank_champion_checks=True,
                               midpoint_collapsed_decision_equals_score_order=True,
                               endpoint_completion_has_all160_entries_at_endpoints=True,
                               all112_point_entries_unchanged_in_every_completion=True,
                               strict_interior_counterexample=True,
                               all16_model_possible_champion_witnesses=True,
                               endpoint_witness_realizes_revised_choice_maximum_regret=True))
    OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(comparisons).to_csv(OUT/'rank_comparison.csv', index=False)
    # Utility inputs are shared across weight references; retain one copy.
    pd.DataFrame(ranks).drop_duplicates().to_csv(OUT/'utility_inputs.csv', index=False)
    pd.DataFrame(scenarios).to_csv(OUT/'witness_scores.csv', index=False)
    pd.DataFrame(scenario_bounds).to_csv(OUT/'witness_utilities.csv', index=False)
    pd.DataFrame(witness_proofs).to_csv(OUT/'possible_champion_witnesses.csv', index=False)
    (OUT/'v121_control_rank_comparison.csv').write_bytes((OLD/'rank_comparison.csv').read_bytes())
    pd.concat(intermediate_rows, ignore_index=True).to_csv(OUT/'v125_v131_rank_comparison.csv', index=False)
    summary = dict(version='V131 diagnostic; staged evidence V130 user16',
        comparison='Same160 utility bounds, weights, anchors and TOPSIS score; chosen midpoint collapse versus retained intervals and minimax regret',
        historical_status='Controlled formulation comparison, not a claim that a midpoint model was previously the team historical initial model',
        model_change='Retain evidence uncertainty and replace a conditional point-score ordering with a conservative interval decision rule',
        scope='Illustrative completions are not evidence admissions, estimated missing values or empirical counterfactual predictions',
        endpoint_scope='Endpoints are legal in the declared closed rectangular utility model. Some are closures/suprema for unbounded raw quantities and need not be physically attained; no raw-population joint-attainability claim is made.',
        interior_scope='All48 uncertain utilities are strictly inside their retained intervals. This removes reliance on exact boundary endpoints but remains a chosen model completion, not an observed world.',
        calibration_limit='No accuracy, empirical coverage, representativeness or new-data gain is inferred from this controlled comparison',
        point_cells=112, partial_interval_cells=32, fully_missing_cells=16,
        uncertain_cells_retained=48, authoritative_model_changed=False,
        results=reports, V121_control=control_checks,
        controlled_V121_V130=evidence_comparisons,
        controlled_V125_V131=intermediate_comparisons,
        V124_to_V130_changed_keys=sorted([list(key) for key in new_keys]),
        primary_snapshot_sha256=digest(SNAPSHOT), primary_snapshot_sources_verified=True,
        source_sha256=protected)
    (OUT/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    for path, expected in protected.items():
        assert digest(ROOT/path) == expected, path
    for path, expected in snapshot['source_sha256'].items():
        assert digest(ROOT/path) == expected, path
    _, final_l, final_u = revised_bounds()
    np.testing.assert_array_equal(original, np.stack([final_l, final_u]))
    audit = dict(status='pass', checks=audit_rows,
                 source_CSV_registry_saved_rank_files_and_source_hashes_unchanged=True,
                 authoritative_V130_all160_bounds_exactly_unchanged=True,
                 V121_control_reproduces_V123_all_rank_columns=True,
                 V121_control_csv_byte_equal=True,
                 V125_V124_to_V131_V130_actual_input_comparison=True,
                 snapshot_hash_and_all_primary_snapshot_sources_unchanged=True,
                 main_input_shape=[16, 10], legacy25_used=False,
                 output_sha256={p.name: digest(p) for p in sorted(OUT.glob('*.csv'))})
    (OUT/'audit.json').write_text(json.dumps(audit, indent=2)+'\n')
    print(json.dumps(reports, indent=2))


if __name__ == '__main__':
    main()
