"""Migrate the V122 method comparison to V124; freeze historical case outputs."""
import hashlib
import json

import numpy as np
import pandas as pd
from scipy.stats import kendalltau

from task4_user_city_indicators import SOURCE
from task4_user_v121_revision import revised_bounds as previous_bounds
from task4_user_v124_revision import MANIFEST, revised_bounds
from task4_v122_method_country import method_results, country_cases, equity_case, age_cases
from task4_v5_model import ROOT, NAMES, weights

OUT = ROOT/'results/task4_v125_method_country'
OLD = ROOT/'results/task4_v122_method_country'
CASE_FILES = ['country_score_comparison.csv', 'country_indicator_bounds.csv',
              'user16_country_coverage.csv', 'shanghai_district_resources.csv',
              'istanbul_historical_age_groups.csv', 'singapore2020_secondary_exact_age_counts.csv']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def independent_method_check(result, summary, lo, hi, w):
    """Direct norms and relative-shortfall equations, without VIKOR helper."""
    z = (lo+hi)/2
    a, b = np.linalg.norm(z*np.sqrt(w), axis=1), np.linalg.norm((1-z)*np.sqrt(w), axis=1)
    topsis = 100*a/(a+b)
    best, worst = z.max(0), z.min(0)
    loss = np.divide(best-z, best-worst, out=np.zeros_like(z), where=(best-worst) > 1e-14)*w
    S, R = loss.sum(1), loss.max(1)
    sn = (S-S.min())/(S.max()-S.min()) if S.max()-S.min() > 1e-14 else np.zeros(len(S))
    rn = (R-R.min())/(R.max()-R.min()) if R.max()-R.min() > 1e-14 else np.zeros(len(R))
    Q = (sn+rn)/2
    tr = np.array([1+np.sum(topsis > x) for x in topsis])
    qr = np.array([1+np.sum(Q < x) for x in Q])
    for column, value in [('topsis_midpoint_score', topsis), ('topsis_rank', tr),
                          ('vikor_S', S), ('vikor_R', R), ('vikor_Q', Q), ('vikor_rank', qr)]:
        np.testing.assert_allclose(result[column], value, atol=1e-12, rtol=0)
    np.testing.assert_allclose(summary['kendall_tau_b'], kendalltau(tr, qr).statistic, atol=1e-14, rtol=0)
    order = np.argsort(Q, kind='stable'); first, second = order[:2]
    advantage = bool(Q[second]-Q[first] >= 1/15-1e-12)
    stability = bool(S[first] <= S.min()+1e-12 or R[first] <= R.min()+1e-12)
    assert summary['acceptable_advantage'] == advantage
    assert summary['acceptable_stability'] == stability
    assert summary['single_compromise_accepted'] == (advantage and stability and np.sum(qr == 1) == 1)


def main():
    protected_paths = [SOURCE, MANIFEST, ROOT/'design/task4_user_current_model.json',
        ROOT/'design/task4_user_v121_admissions.json', ROOT/'scripts/task4_user_v124_revision.py',
        ROOT/'scripts/task4_v122_method_country.py', ROOT/'scripts/task4_v119_method_country.py',
        *[p for p in sorted(OLD.iterdir()) if p.is_file()],
        *[(ROOT/f'results/task4_user_{v}_revision'/name) for v in ['v121', 'v124']
          for name in ['current_ranks.csv', 'utility_bounds.csv', 'summary.json']]]
    protected = {str(p.relative_to(ROOT)): digest(p) for p in protected_paths}
    previous, l0, h0 = previous_bounds()
    frame, lo, hi = revised_bounds()
    original = np.stack([lo, hi]).copy()
    cities = frame.city.tolist()
    assert cities == previous.city.tolist() and lo.shape == hi.shape == (16, 10)
    assert frame.country.nunique() == 16
    allr, components, method_summary, bound_rows = [], [], [], []
    for version, l, h in [('V121', l0, h0), ('V124', lo, hi)]:
        for reference, w in [('fixed', weights(.1)), ('equal', np.ones(10)/10)]:
            result, component, summary = method_results(frame, l, h, version, w, reference)
            independent_method_check(result, summary, l, h, w)
            allr.append(result); components.append(component); method_summary.append(summary)
        bound_rows.extend(dict(evidence_version=version, city=city, indicator=name,
            lower=l[i, j], upper=h[i, j], midpoint=(l[i, j]+h[i, j])/2)
            for i, city in enumerate(cities) for j, name in enumerate(NAMES))
    ranks = pd.concat(allr, ignore_index=True)
    old_ranks = pd.read_csv(OLD/'method_ranks.csv')
    check_columns = ['topsis_midpoint_score', 'topsis_rank', 'vikor_S', 'vikor_R', 'vikor_Q',
                     'vikor_rank', 'main_interval_decision_rank']
    for reference in ['fixed', 'equal']:
        before = ranks.query("evidence_version == 'V121' and weight_reference == @reference").set_index('city').loc[cities]
        old = old_ranks.query("evidence_version == 'V121' and weight_reference == @reference").set_index('city').loc[cities]
        np.testing.assert_allclose(before[check_columns], old[check_columns], atol=1e-12, rtol=0)

    # Pure legacy-case calculations still reproduce their frozen V122 files.
    country, country_indicators = country_cases()
    district, equity = equity_case()
    age, sg, age_summary = age_cases()
    regenerated = {'country_score_comparison.csv': country,
        'country_indicator_bounds.csv': country_indicators,
        'shanghai_district_resources.csv': district,
        'istanbul_historical_age_groups.csv': age,
        'singapore2020_secondary_exact_age_counts.csv': sg,
        'user16_country_coverage.csv': frame[['city', 'country']]}
    old_summary = json.loads((OLD/'summary.json').read_text())
    assert equity == old_summary['equity'] and age_summary == old_summary['age_evidence']
    OUT.mkdir(parents=True, exist_ok=True)
    frozen = {}
    for name in CASE_FILES:
        pd.testing.assert_frame_equal(regenerated[name].reset_index(drop=True), pd.read_csv(OLD/name),
                                      check_dtype=False, check_exact=False, atol=1e-14, rtol=0)
        (OUT/name).write_bytes((OLD/name).read_bytes())
        assert (OUT/name).read_bytes() == (OLD/name).read_bytes()
        frozen[name] = digest(OUT/name)
    ranks.to_csv(OUT/'method_ranks.csv', index=False)
    pd.concat(components, ignore_index=True).to_csv(OUT/'method_components.csv', index=False)
    pd.DataFrame(bound_rows).to_csv(OUT/'method_utility_inputs.csv', index=False)
    comparisons = []
    for reference in ['fixed', 'equal']:
        a = ranks.query("evidence_version == 'V121' and weight_reference == @reference").set_index('city')
        b = ranks.query("evidence_version == 'V124' and weight_reference == @reference").set_index('city')
        comparisons.append(dict(weight_reference=reference,
            changed_topsis_midpoint_ranks=int((a.topsis_rank != b.topsis_rank).sum()),
            changed_vikor_ranks=int((a.vikor_rank != b.vikor_rank).sum()),
            kendall_topsis_before_after=float(kendalltau(a.topsis_rank, b.topsis_rank).statistic),
            kendall_vikor_before_after=float(kendalltau(a.vikor_rank, b.vikor_rank).statistic)))
    for path, expected in protected.items():
        assert digest(ROOT/path) == expected, path
    _, final_l, final_u = revised_bounds()
    np.testing.assert_array_equal(original, np.stack([final_l, final_u]))
    summary = dict(version='V125 extension of user16 V124; no main model change',
        method_cases=method_summary, controlled_V121_V124=comparisons,
        comparison_scope='Same midpoint utilities and weights in each evidence arm; fixed-ideal TOPSIS versus sample-ideal classic VIKOR v=.5. Illustrative midpoint scenarios, not imputation or main recommendation.',
        historical_control_reproduces_V122_V121=True, same_country_pairs_in_main16=0,
        country_case_dataset='Byte-frozen V122 cases: separate historical25 V117, inherited fixed weights',
        country_comparability=old_summary['country_comparability'],
        country_pairs=old_summary['country_pairs'], equity=old_summary['equity'],
        age_evidence=old_summary['age_evidence'], frozen_case_sha256=frozen,
        frozen_case_scope='Original case labels, years and source scope retained verbatim; none is inserted into V124 user16. Shanghai2025, Istanbul2012 and Singapore2020 remain independent cases.',
        protected_inputs_unchanged=True, input_sha256=protected)
    (OUT/'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
    (OUT/'audit.json').write_text(json.dumps(dict(status='pass',
        V121_control_matches_V122_numeric=True, independent_norm_VIKOR_and_acceptance_cases=4,
        frozen_case_files_byte_and_numeric_equal=len(CASE_FILES), frozen_case_sha256=frozen,
        main_user16_country_count=16, main_user16_bounds_exactly_unchanged=True,
        source_CSV_registry_old_results_and_source_hashes_unchanged=True), indent=2)+'\n')
    print(json.dumps(dict(method_cases=method_summary, controlled_V121_V124=comparisons), indent=2))


if __name__ == '__main__':
    main()
