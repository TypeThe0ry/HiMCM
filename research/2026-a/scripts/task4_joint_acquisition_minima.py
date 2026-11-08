"""Match universal count bounds with one shared hypothetical exact revelation.

The canonical completion is a witness search, not a general optimizer. A count
is certified minimal only when its attained count matches a universal bound.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from task4_acquisition_limits import certificate
from task4_continuous_preferences import feasible_preferences
from task4_current_model import current_bounds, run as run_current
from task4_joint_uncertainty_stress import protect_output
from task4_v5_model import ROOT, CITIES, NAMES, score, weights

KIND = 'joint_acquisition_count_minima'
FIXED_TOL = 1e-10


def joint_completion(lo, hi, mask, lower_certificates, mode, preferred_anchor=0,
                     fixed_alpha=.1, alpha_range=(.05, .2)):
    """Return shared bounds, per-city results and the proven count interval."""
    lo, hi, mask = np.asarray(lo, float), np.asarray(hi, float), np.asarray(mask)
    if mode not in ('fixed', 'continuous'):
        raise ValueError('Mode must be fixed or continuous')
    if not isinstance(preferred_anchor, (int, np.integer)) or not 0 <= preferred_anchor < len(lo):
        raise ValueError('Preferred anchor must be a city index')
    # Validation and certificate generation belong to the public analyse entry.
    required = [r['index'] for r in lower_certificates if r[mode+'_unavoidable']]
    anchors = required or [preferred_anchor]
    high_rows = np.zeros(len(lo), bool)
    high_rows[anchors] = True
    point = np.where(high_rows[:, None], hi, lo)
    lower, upper = np.where(mask, point, lo), np.where(mask, point, hi)
    assert np.all(lower[mask] == upper[mask])
    np.testing.assert_array_equal(lower[~mask], lo[~mask])
    np.testing.assert_array_equal(upper[~mask], hi[~mask])
    assert np.all(lo <= lower) and np.all(upper <= hi)
    lower_scores = score(lower, weights(fixed_alpha))
    upper_scores = score(upper, weights(fixed_alpha))
    rows = []
    for i in range(len(lo)):
        others = np.arange(len(lo)) != i
        margin = float(upper_scores[i]-lower_scores[others].max())
        if mode == 'fixed':
            possible = margin >= -FIXED_TOL
            detail = dict(witness_alpha=fixed_alpha if possible else None,
                          feasible_interval_closures=[], feasible_boundary_points=[],
                          partition_count=0, tolerance=FIXED_TOL)
        else:
            detail = feasible_preferences(upper[i], lower[others], *alpha_range)
            possible = detail.pop('possible')
        if possible:
            alpha = detail['witness_alpha']
            values = score(np.vstack([upper[i], lower[others]]), weights(alpha))
            assert values[0] >= values[1:].max()-1e-8
        rows.append(dict(index=i, possible=bool(possible),
                         fixed_score_margin=margin, **detail))
    survivors = [r['index'] for r in rows if r['possible']]
    assert set(required) <= set(survivors)
    bound, attained = max(1, len(required)), len(survivors)
    assert attained >= bound
    result = dict(mode=mode, unavoidable_indices=required, anchor_indices=anchors,
                  universal_count_lower_bound=bound, attained_count_upper_bound=attained,
                  joint_minimum_certified=bound == attained,
                  certified_minimum=attained if bound == attained else None,
                  surviving_indices=survivors,
                  status='matched_bound' if bound == attained else 'unresolved_gap')
    return lower, upper, rows, result


def analyse(lo, hi, mask, fixed_alpha=.1, alpha_range=(.05, .2), preferred_anchor=0):
    cert = certificate(lo, hi, mask, fixed_alpha, alpha_range)
    answers = [joint_completion(lo, hi, mask, cert, mode, preferred_anchor,
                                fixed_alpha, alpha_range) for mode in ('fixed', 'continuous')]
    return cert, answers


def run(out):
    out = Path(out)
    lo, hi, config = current_bounds()
    summary_file = out/'summary.json'
    if summary_file.exists() and json.loads(summary_file.read_text()).get('analysis_kind') != KIND:
        raise ValueError('Refusing to overwrite a different analysis kind')
    protect_output(out, lo, hi, config)
    run_current(out/'baseline')
    original = np.stack([lo, hi]).copy()
    edu, travel = NAMES.index('upper_secondary_ptr'), NAMES.index('travel')
    scopes = [('all_education', [edu], None), ('all_travel', [travel], None),
              ('all_education_and_travel', [edu, travel], None),
              ('phoenix_education_and_travel', [edu, travel], CITIES.index('Phoenix'))]
    scopes += [('both_plus_'+name, [edu, travel, j], None)
               for j, name in enumerate(NAMES) if j not in (edu, travel)]
    lower_rows, witness_cells, feasibility, summaries = [], [], [], []
    for label, columns, city in scopes:
        mask = np.zeros_like(lo, bool)
        if city is None:
            mask[:, columns] = True
        else:
            mask[city, columns] = True
        cert, answers = analyse(lo, hi, mask, config['fixed_alpha'], config['alpha_range'],
                                CITIES.index('Singapore'))
        lower_rows.extend(dict(scenario=label, city=CITIES[r['index']], **r) for r in cert)
        for lower, upper, city_rows, result in answers:
            mode = result['mode']
            for i, j in zip(*np.where(mask)):
                witness_cells.append(dict(scenario=label, mode=mode, city=CITIES[i],
                    indicator=NAMES[j], previous_lower=lo[i, j], previous_upper=hi[i, j],
                    hypothetical_exact_value=lower[i, j]))
            for r in city_rows:
                feasibility.append(dict(scenario=label, mode=mode, city=CITIES[r['index']], **r))
            for stem in ('unavoidable', 'anchor', 'surviving'):
                result[stem+'_cities'] = [CITIES[i] for i in result.pop(stem+'_indices')]
            summaries.append(dict(scenario=label, measured_indicators=[NAMES[j] for j in columns],
                                  selected_cells=int(mask.sum()), **result))
    np.testing.assert_array_equal(original, np.stack([lo, hi]))
    pd.DataFrame(lower_rows).to_csv(out/'unavoidable_certificates.csv', index=False)
    pd.DataFrame(witness_cells).to_csv(out/'hypothetical_exact_values.csv', index=False)
    # JSON retains interval arrays and boundary points without CSV string parsing.
    (out/'city_feasibility.json').write_text(json.dumps(feasibility, indent=2)+'\n')
    summary = dict(analysis_kind=KIND, model_version=config['model_version'],
        fixed_alpha=config['fixed_alpha'], alpha_range=config['alpha_range'],
        input_bounds_sha256=hashlib.sha256(original.astype('<f8').tobytes()).hexdigest(),
        main_admitted=False, new_observations=0, scenario_only=True,
        selected_values_shared_across_all_cities_and_alpha=True,
        fixed_score_tolerance=FIXED_TOL, polynomial_tolerance=1e-12,
        formal_interval_arithmetic=False,
        certified_cases=sum(r['joint_minimum_certified'] for r in summaries),
        unresolved_cases=sum(not r['joint_minimum_certified'] for r in summaries),
        interpretation='Conditional on the independent utility-box model and numeric tolerances. '
        'Canonical endpoint assignments are hypothetical feasibility witnesses, not forecasts, '
        'guaranteed real-world data combinations, or a general-purpose optimizer. '
        'Each continuous case fixes all revelations once; different surviving cities may use '
        'different alpha witnesses. Fixed and continuous cases may use different revelations.',
        scenarios=summaries)
    (out/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps([dict(scenario=r['scenario'], mode=r['mode'],
        lower=r['universal_count_lower_bound'], upper=r['attained_count_upper_bound'],
        certified=r['joint_minimum_certified']) for r in summaries], indent=2))
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    run(parser.parse_args().output)
