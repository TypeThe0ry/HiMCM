"""Independent audit of V122 extensions; never imports their score/decision code."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd
from scipy.stats import kendalltau

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parents[1]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'scripts'))
from task4_user_v121_revision import revised_bounds

NAMES = ['homicide_rate', 'pm25', 'cost_living_index', 'price_income_ratio',
         'upper_secondary_ptr', 'research_he_density', 'public_transport_density',
         'travel', 'fixed_broadband_mbps', 'public_pool_density']
BENEFITS = {5, 6, 8, 9}
WEIGHTS = {'fixed': np.array([.1125]*6+[.05,.1125,.1125,.05]), 'equal': np.ones(10)/10}
CHANGES = {'baseline': {}, 'resource_expansion': {5: .1, 6: .1, 9: .1},
           'living_pressure': {2: .1, 3: .1, 7: .1},
           'balanced_improvement': {4: -.1, 1: -.1, 7: -.1}}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(actual, expected, label='', atol=1e-11):
    np.testing.assert_allclose(actual, expected, atol=atol, rtol=0, err_msg=label)


def score(z, w):
    a = np.linalg.norm(z*np.sqrt(w)[..., None, :], axis=-1)
    b = np.linalg.norm((1-z)*np.sqrt(w)[..., None, :], axis=-1)
    return 100*a/(a+b)


def decisions(lo, hi, w, tol=1e-12, average=False, future_credit=False):
    l, u = score(lo, w), score(hi, w)
    n = l.shape[-1]
    r = np.stack([np.maximum(0, np.max(u[..., [k for k in range(n) if k != i]], axis=-1)-l[..., i])
                  for i in range(n)], axis=-1)
    p = np.stack([u[..., i] >= np.max(l[..., [k for k in range(n) if k != i]], axis=-1)-tol
                  for i in range(n)], axis=-1)
    necessary = np.stack([l[..., i] >= np.max(u[..., [k for k in range(n) if k != i]], axis=-1)-tol
                         for i in range(n)], axis=-1)
    ahead = np.stack([np.sum(r < r[..., i, None]-tol, axis=-1) for i in range(n)], axis=-1)
    tied = np.stack([np.sum(np.abs(r-r[..., i, None]) <= tol, axis=-1) for i in range(n)], axis=-1)
    ranks = 1+ahead+(tied-1)/2 if average else 1+ahead
    if future_credit:
        winners = r <= r.min(axis=-1, keepdims=True)+tol
        credit = winners/winners.sum(axis=-1, keepdims=True)
    else:
        credit = np.clip((1-ahead)/tied, 0, 1)
    top3 = np.clip((3-ahead)/tied, 0, 1)
    return dict(score_lower=l, score_upper=u, max_regret=r, possible_champion=p,
                necessary_champion=necessary, decision_rank=ranks, credit=credit, top3=top3)


def factor(shape, changes, city=None):
    m = np.ones(shape)
    for j, delta in changes.items():
        if city is None:
            m[..., j] = 1+delta
        else:
            m[..., city, j] = 1+delta
    return m


def transformed(lo, hi, multipliers, means):
    """Independent odds inversion plus Jensen/mean-utility power envelopes."""
    a = np.broadcast_to(lo, multipliers.shape).copy()
    b = np.broadcast_to(hi, multipliers.shape).copy()
    for j in range(10):
        r = multipliers[..., j]
        if j == 7:
            a[..., j] = np.minimum(lo[:, j], lo[:, j]**r)
            b[..., j] = np.maximum(hi[:, j], hi[:, j]**r)
            known = np.isfinite(means)
            a[..., known, j] = np.exp(-r[..., known]*means[known]/30)
            b[..., known, j] = 1
        else:
            for source, target in [(lo[:, j], a), (hi[:, j], b)]:
                reciprocal_odds = np.divide(1-source, source,
                    out=np.full_like(source, np.inf), where=source > 0)
                odds_after = reciprocal_odds/r if j in BENEFITS else reciprocal_odds*r
                target[..., j] = 1/(1+odds_after)
    assert np.all(a <= b+1e-14) and np.all(a >= 0) and np.all(b <= 1)
    return a, b


def array_rows(path, cities, names=NAMES, **filters):
    f = pd.read_csv(path)
    for col, value in filters.items():
        f = f[f[col] == value]
    assert len(f) == len(cities)*len(names)
    index = pd.MultiIndex.from_product([cities, names], names=['city', 'indicator'])
    f = f.set_index(['city', 'indicator']).loc[index]
    return f.lower.to_numpy().reshape(len(cities), len(names)), f.upper.to_numpy().reshape(len(cities), len(names))


def city_rows(frame, cities, **filters):
    f = frame
    for col, value in filters.items():
        f = f[f[col] == value]
    assert len(f) == len(cities) and f.city.is_unique
    return f.set_index('city').loc[cities]


def check_static(rows, d, midpoint=None, exact_ranks=True):
    for col in ['score_lower', 'score_upper', 'max_regret', 'possible_champion', 'necessary_champion']:
        close(rows[col], d[col], col)
    if exact_ranks:
        ranks = [1+np.sum(d['max_regret'] < x) for x in d['max_regret']]
        close(rows.decision_rank, ranks, 'static competition rank')
    if midpoint is not None:
        close(rows.midpoint_illustrative_score, midpoint)


def main():
    immutable_paths = [ROOT/'data/task4_v117_team_intake/city_indicators.csv',
        ROOT/'design/task4_user_current_model.json', ROOT/'design/task4_user_v121_admissions.json',
        *[(ROOT/'results/task4_user_v121_revision'/name) for name in
          ['current_ranks.csv', 'utility_bounds.csv', 'all_ranks.csv', 'mc_city_summary.csv', 'summary.json']]]
    protected = {str(p.relative_to(ROOT)): sha(p) for p in immutable_paths}
    for p in immutable_paths:
        original = subprocess.check_output(['git', '-C', str(REPO), 'show', 'deae2f3:'+str(p.relative_to(REPO))])
        assert p.read_bytes() == original, p
    assert protected['data/task4_v117_team_intake/city_indicators.csv'] == '430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
    frame, lo, hi = revised_bounds()
    original_bounds = np.stack([lo, hi]).copy()
    cities, means = frame.city.tolist(), frame.commute_min.to_numpy(dtype=float)
    assert len(cities) == 16 and lo.shape == (16, 10) and frame.country.nunique() == 16
    assert json.loads((ROOT/'design/task4_user_current_model.json').read_text())['version'] == 'V121'
    saved_l, saved_u = array_rows(ROOT/'results/task4_user_v121_revision/utility_bounds.csv', cities, scenario='after_conditional')
    close(saved_l, lo, atol=1e-15); close(saved_u, hi, atol=1e-15)

    # Preferences: construct declared profile weights independently.
    pref = ROOT/'results/task4_v122_preferences'
    pr, pmc = pd.read_csv(pref/'ranks.csv'), pd.read_csv(pref/'mc_city_summary.csv')
    ps = json.loads((pref/'summary.json').read_text())
    pw = pd.read_csv(pref/'weights.csv')
    matrices = json.loads((pref/'scenario_matrices.json').read_text())
    target = {'baseline': [], 'education_priority': [4, 5], 'independent_living_priority': [6, 7]}
    pbase = city_rows(pr, cities, profile='baseline')
    prefs_checked = []
    for name, js in target.items():
        w = WEIGHTS['fixed'].copy(); w[js] *= 2; w /= w.sum()
        weightrows = pw[pw.profile == name].set_index('indicator').loc[NAMES]
        close(weightrows.weight, w, atol=1e-15)
        A = np.asarray(matrices[name]['matrix'])
        assert A.shape == (10, 10) and np.all(A > 0)
        close(A.diagonal(), 1); close(A*A.T, 1); close(A@w, 10*w)
        close(A, w[:, None]/w[None, :])
        assert abs(matrices[name]['diagnostic']['CR']) < 1e-10
        d = decisions(lo, hi, w)
        rows = city_rows(pr, cities, profile=name)
        check_static(rows, d, score((lo+hi)/2, w))
        report = next(x for x in ps['profiles'] if x['profile'] == name)
        close(report['kendall_tau_b_vs_baseline'], kendalltau(pbase.decision_rank, rows.decision_rank).statistic)
        for k in (20, 100, 500):
            sampled = np.random.default_rng(np.random.SeedSequence([20261108, k])).dirichlet(k*w, 10000)
            md = decisions(lo, hi, sampled, average=True)
            rows = city_rows(pmc, cities, profile=name, concentration=k)
            for col, value in [('minimax_recommendation_frequency', md['credit'].mean(0)),
                               ('mean_decision_rank', md['decision_rank'].mean(0)),
                               ('top3_decision_frequency', md['top3'].mean(0)),
                               ('possible_champion_frequency', md['possible_champion'].mean(0)),
                               ('necessary_champion_frequency', md['necessary_champion'].mean(0))]:
                close(rows[col], value, f'pref/{name}/{k}/{col}')
            close(rows.minimax_recommendation_frequency.sum(), 1)
            close(rows.top3_decision_frequency.sum(), 3)
            prefs_checked.append(dict(profile=name, concentration=k))

    # Future scenarios: independent transforms preserve full unknowns.
    future = ROOT/'results/task4_v122_future'
    fs = json.loads((future/'summary.json').read_text())
    fr = pd.read_csv(future/'ranks.csv')
    future_bounds = {}
    for arm in ['conditional', 'withdraw_historical_stage_proxy']:
        l, u = lo.copy(), hi.copy()
        if arm != 'conditional':
            l[cities.index('Singapore'), 7], u[cities.index('Singapore'), 7] = 0, 1
        for name, changes in CHANGES.items():
            a, b = transformed(l, u, factor(l.shape, changes), means)
            future_bounds[(arm, name)] = (a, b)
            al, au = array_rows(future/'utility_bounds.csv', cities, evidence_arm=arm, scenario=name)
            close(al, a, atol=1e-14); close(au, b, atol=1e-14)
            unknown = (l == 0) & (u == 1)
            np.testing.assert_array_equal(a[unknown], 0)
            np.testing.assert_array_equal(b[unknown], 1)
            for ref, w in WEIGHTS.items():
                d = decisions(a, b, w)
                rows = city_rows(fr, cities, evidence_arm=arm, scenario=name, weight_reference=ref)
                check_static(rows, d, score((a+b)/2, w))
                summary = next(x for x in fs['scenarios'] if x['evidence_arm'] == arm and x['scenario'] == name and x['weight_reference'] == ref)
                close(summary['mean_score_interval_width'], np.mean(d['score_upper']-d['score_lower']))

    # Recommendation-switch thresholds: all saved grid points plus root sides.
    threshold_rows = pd.read_csv(future/'thresholds.csv')
    scan = pd.read_csv(future/'threshold_scan.csv')
    threshold_checks = []
    for row in threshold_rows.to_dict('records'):
        i, w = cities.index(row['city']), WEIGHTS[row['weight_reference']]
        other = [k for k in range(16) if k != i]
        def gap(r):
            a, b = transformed(lo, hi, factor(lo.shape, {1: r-1, 4: r-1, 7: r-1}, i), means)
            d = decisions(a, b, w)
            return d['max_regret'][i]-d['max_regret'][other].min()
        recorded = scan[(scan.city == row['city']) & (scan.weight_reference == row['weight_reference'])]
        assert len(recorded) == 101
        for point in recorded.itertuples():
            close(point.regret_gap_to_best_other, gap(point.raw_multiplier))
        close(row['baseline_gap_to_best_other'], gap(1))
        close(row['gap_at_50pct_cost_reduction'], gap(.5))
        if row['status'] == 'crossing_found':
            r = row['threshold_raw_multiplier']
            assert abs(gap(r)) < 1e-8 and gap(r-1e-6) < -1e-10 and gap(r+1e-6) > 1e-10
            close(row['required_cost_reduction_fraction'], 1-r)
        elif row['status'] == 'already_strict_minimax':
            assert gap(1) < -1e-10
        elif row['status'] == 'not_reached':
            assert gap(.5) > 0
        else:
            assert row['status'] == 'tie_only_at_endpoint' and abs(gap(.5)) <= 1e-10
        threshold_checks.append(dict(city=row['city'], weight_reference=row['weight_reference'], status=row['status']))

    # Future shocks: reproduce 10,000 draws, independent transformations and norms.
    fmc = pd.read_csv(future/'future_mc_city_summary.csv')
    rng = np.random.default_rng(20261108122)
    common, local = rng.uniform(0, 1, (10000, 1)), rng.uniform(0, 1, (10000, 16))
    delta = .05*common+.05*local
    for ref, w in WEIGHTS.items():
        l0, u0 = score(lo, w), score(hi, w)
        for name, changes in CHANGES.items():
            if name == 'baseline':
                continue
            m = np.ones((10000, 16, 10))
            for j, change in changes.items():
                m[..., j] = 1+np.sign(change)*delta
            a, b = transformed(lo, hi, m, means)
            md = decisions(a, b, w, tol=1e-10, future_credit=True)
            rows = city_rows(fmc, cities, scenario=name, weight_reference=ref)
            for col, x in [('recommendation_frequency', md['credit'].mean(0)),
                           ('possible_champion_frequency', md['possible_champion'].mean(0)),
                           ('mean_decision_rank', md['decision_rank'].mean(0))]:
                close(rows[col], x, f'shock/{ref}/{name}/{col}')
            for side, baseline in [('lower', l0), ('upper', u0)]:
                for q, suffix in [(.05, 'p05'), (.5, 'p50'), (.95, 'p95')]:
                    close(rows[f'score_{side}_change_{suffix}'], np.quantile(md[f'score_{side}']-baseline, q, axis=0))
            # Scalar norms on fixed draws verify the vectorized audit path too.
            for draw in (0, 1, 9999):
                lower = [100*np.linalg.norm(np.sqrt(w)*x)/(np.linalg.norm(np.sqrt(w)*x)+np.linalg.norm(np.sqrt(w)*(1-x))) for x in a[draw]]
                close(lower, md['score_lower'][draw])

    # Weight-only future sensitivity: same baseline seed as current V121.
    wmc = pd.read_csv(future/'weight_mc_city_summary.csv')
    v121mc = pd.read_csv(ROOT/'results/task4_user_v121_revision/mc_city_summary.csv')
    assert fs['weight_mc']['seed'] == [20261108, 100]
    for ref, w in WEIGHTS.items():
        sampled = np.random.default_rng(np.random.SeedSequence([20261108, 100])).dirichlet(100*w, 10000)
        for name in CHANGES:
            a, b = future_bounds[('conditional', name)]
            md = decisions(a, b, sampled, tol=1e-10, future_credit=True)
            rows = city_rows(wmc, cities, weight_reference=ref, scenario=name)
            for col, x in [('recommendation_frequency', md['credit'].mean(0)),
                           ('mean_decision_rank', md['decision_rank'].mean(0)),
                           ('possible_champion_frequency', md['possible_champion'].mean(0))]:
                close(rows[col], x, f'weight/{ref}/{name}/{col}')
            if name == 'baseline':
                old = city_rows(v121mc, cities, scenario='after_conditional', weight_reference=ref, concentration=100)
                close(rows.recommendation_frequency, old.minimax_recommendation_frequency)
                close(rows.mean_decision_rank, old.mean_decision_rank)
                close(rows.possible_champion_frequency, old.possible_champion_frequency)

    # Same midpoint inputs: independently derive TOPSIS, classic VIKOR and acceptance.
    method = ROOT/'results/task4_v122_method_country'
    ms = json.loads((method/'summary.json').read_text())
    mr = pd.read_csv(method/'method_ranks.csv')
    mi = pd.read_csv(method/'method_utility_inputs.csv')
    method_checks = []
    for version in ['V118', 'V121']:
        a, b = array_rows(method/'method_utility_inputs.csv', cities, evidence_version=version)
        if version == 'V121':
            close(a, lo, atol=1e-15); close(b, hi, atol=1e-15)
        else:
            sl, su = array_rows(ROOT/'results/task4_user_v118_revision/utility_bounds.csv', cities, scenario='after')
            close(a, sl, atol=1e-15); close(b, su, atol=1e-15)
        z = (a+b)/2
        for ref, w in WEIGHTS.items():
            rows = city_rows(mr, cities, evidence_version=version, weight_reference=ref)
            best, worst = z.max(0), z.min(0)
            loss = np.divide(best-z, best-worst, out=np.zeros_like(z), where=(best-worst) > 1e-14)*w
            S, R = loss.sum(1), loss.max(1)
            normalized_s = (S-S.min())/(S.max()-S.min()) if S.max()-S.min() > 1e-14 else np.zeros(16)
            normalized_r = (R-R.min())/(R.max()-R.min()) if R.max()-R.min() > 1e-14 else np.zeros(16)
            Q = .5*(normalized_s+normalized_r)
            t = score(z, w)
            tr, qr = [1+np.sum(t > x) for x in t], [1+np.sum(Q < x) for x in Q]
            for col, x in [('topsis_midpoint_score', t), ('topsis_rank', tr), ('vikor_S', S),
                           ('vikor_R', R), ('vikor_Q', Q), ('vikor_rank', qr)]:
                close(rows[col], x)
            summary = next(x for x in ms['method_cases'] if x['evidence_version'] == version and x['weight_reference'] == ref)
            close(summary['kendall_tau_b'], kendalltau(tr, qr).statistic)
            order = np.argsort(Q, kind='stable'); first, second = order[:2]
            advantage = bool(Q[second]-Q[first] >= 1/15-1e-12)
            stability = bool(S[first] <= S.min()+1e-12 or R[first] <= R.min()+1e-12)
            assert summary['acceptable_advantage'] == advantage and summary['acceptable_stability'] == stability
            assert summary['single_compromise_accepted'] == (advantage and stability and np.sum(Q == Q.min()) == 1)
            method_checks.append(dict(evidence_version=version, weight_reference=ref,
                                      acceptable_advantage=advantage, acceptable_stability=stability))

    # Historical same-country controls remain separate from the main city set.
    coverage = pd.read_csv(method/'user16_country_coverage.csv')
    assert coverage.city.tolist() == cities and coverage.country.nunique() == 16
    pairs = pd.read_csv(method/'country_score_comparison.csv')
    legacy = pd.read_csv(ROOT/'results/task4_v117_city_revision/utility_bounds.csv')
    legacy = legacy[legacy.scenario == 'v117'].set_index(['city', 'indicator'])
    assert len(pairs) == 2 and ms['same_country_pairs_in_main16'] == 0
    assert set(zip(pairs.city_a, pairs.city_b)) == {('Phoenix', 'New York'), ('Mumbai', 'Delhi')}
    country_meta = pd.read_csv(ROOT/'data/city_candidates_team_25.csv').set_index('city')
    country_indicators = pd.read_csv(method/'country_indicator_bounds.csv')
    for row in pairs.to_dict('records'):
        assert row['city_a'] not in cities and row['city_b'] not in cities
        assert country_meta.loc[row['city_a'], 'country'] == country_meta.loc[row['city_b'], 'country'] == row['country']
        intervals = []
        for c in [row['city_a'], row['city_b']]:
            f = legacy.loc[c].loc[NAMES]
            intervals.append((float(score(f.lower.to_numpy()[None], WEIGHTS['fixed'])[0]),
                              float(score(f.upper.to_numpy()[None], WEIGHTS['fixed'])[0])))
        (al, au), (bl, bu) = intervals
        close([row['a_score_lower'], row['a_score_upper'], row['b_score_lower'], row['b_score_upper']], [al, au, bl, bu])
        assert row['a_necessarily_strictly_better'] == (al > bu)
        assert row['b_necessarily_strictly_better'] == (bl > au)
        comparison = country_indicators[(country_indicators.city_a == row['city_a']) &
                                        (country_indicators.city_b == row['city_b'])].set_index('indicator').loc[NAMES]
        for prefix, c in [('a', row['city_a']), ('b', row['city_b'])]:
            for endpoint in ['lower', 'upper']:
                close(comparison[f'{prefix}_{endpoint}'], legacy.loc[c].loc[NAMES, endpoint], atol=1e-15)

    # District aggregation and age proxies are separate supporting cases.
    district = pd.read_csv(method/'shanghai_district_resources.csv')
    s, t = district.students.to_numpy(), district.teachers.to_numpy()
    u, p = 15*t/(s+15*t), s/s.sum()
    close(district.resource_utility, u)
    pooled, local = 15*t.sum()/(s.sum()+15*t.sum()), float(p@u)
    close(ms['equity']['pooled_utility'], pooled)
    close(ms['equity']['student_weighted_district_utility'], local)
    close(ms['equity']['aggregation_gap'], pooled-local)
    remaining, numerator = .2, 0.
    for i in np.argsort(u, kind='stable'):
        take = min(remaining, p[i]); numerator += take*u[i]; remaining -= take
        if remaining <= 1e-14:
            break
    close(ms['equity']['bottom20_student_mass_district_utility'], numerator/.2)
    assert ms['equity']['separate_historical_case'] and not ms['equity']['main_user16_scores_changed']
    age = pd.read_csv(method/'istanbul_historical_age_groups.csv')
    assert age.marginal_utility_lower.max() <= age.marginal_utility_upper.min()
    assert not ms['age_evidence']['age_specific_preferences_observed']
    assert not ms['age_evidence']['exact_age14_vs18_identified']
    sg = pd.read_csv(method/'singapore2020_secondary_exact_age_counts.csv')
    totals = sg.groupby('start_of_year_age').enrolment.sum().to_dict()
    assert totals == ms['age_evidence']['singapore_secondary_age_totals']
    source_receipts = {}
    for label, summary, field in [('preferences', ps, 'source_hashes'),
                                   ('future', fs, 'source_sha256'),
                                   ('method_country', ms, 'input_sha256')]:
        for path, expected in summary[field].items():
            assert sha(ROOT/path) == expected, f'{label}/{path}'
        source_receipts[label] = len(summary[field])
    assert fs['future_mc']['seed'] == 20261108122 and fs['future_mc']['draws'] == 10000
    for path, expected in protected.items():
        assert sha(ROOT/path) == expected, path
    _, final_l, final_u = revised_bounds()
    np.testing.assert_array_equal(original_bounds, np.stack([final_l, final_u]))
    result = dict(status='pass', immutable_baseline_commit='deae2f3',
        main_user16_160_bounds_and_source_CSV_registry_unchanged=True,
        immutable_input_sha256=protected,
        result_source_hash_receipts_verified=source_receipts,
        preferences_deterministic_profiles=3, preferences_independent_MC_settings=prefs_checked,
        preferences_MC_draws_per_setting=10000,
        future_deterministic_scenario_reference_arms=16,
        future_threshold_grid_points_checked=int(len(scan)), future_threshold_cases=threshold_checks,
        future_shock_independent_settings=6, future_shock_draws_per_setting=10000,
        future_shock_scalar_draws=[0, 1, 9999], future_weight_independent_settings=8,
        future_weight_baseline_matches_V121=True, method_independent_cases=method_checks,
        historical_same_country_cases_separate_from_main16=True,
        shanghai_district_aggregation_and_fractional_bottom20=True,
        age_proxies_no_measured_preferences_or_exact14_vs18_claim=True,
        result_sha256={str(p.relative_to(ROOT)): sha(p) for directory in [pref, future, method]
                      for p in sorted(directory.glob('*.csv'))})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print('PASS: independent V122 preferences, future transforms/thresholds/MC, method/country and source protection')


if __name__ == '__main__':
    main()
