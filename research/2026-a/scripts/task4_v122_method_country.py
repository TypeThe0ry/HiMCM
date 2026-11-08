"""Controlled V118/V121 midpoint method sensitivity and separate historical cases.

No observation, main interval, registry, population or preference weight is changed.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kendalltau

from task4_user_city_indicators import SOURCE, evaluate
from task4_user_v118_revision import revised_bounds as v118_bounds
from task4_user_v121_revision import revised_bounds as v121_bounds
from task4_v119_method_country import vikor
from task4_v5_model import ROOT, NAMES, score, weights

OUT = ROOT / 'results/task4_v122_method_country'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bottom_fraction_mean(values, mass, fraction=.2):
    """Fractional district allocation: homogeneous district means, not persons."""
    values, mass = np.asarray(values, float), np.asarray(mass, float)
    assert values.shape == mass.shape and np.all(mass > 0) and 0 < fraction <= 1
    mass = mass / mass.sum()
    order = np.argsort(values, kind='stable')
    remaining, numerator = fraction, 0.
    for i in order:
        take = min(remaining, mass[i])
        numerator += take * values[i]
        remaining -= take
        if remaining <= 1e-14:
            break
    assert remaining <= 1e-14
    return float(numerator / fraction)


def method_results(frame, lo, hi, version, w, reference):
    cities = frame.city.tolist()
    z = (lo + hi) / 2
    S, R, Q, best, worst = vikor(z, w)
    topsis = score(z, w)
    result = pd.DataFrame(dict(city=cities, topsis_midpoint_score=topsis,
        topsis_rank=pd.Series(topsis).rank(ascending=False, method='min').astype(int),
        vikor_S=S, vikor_R=R, vikor_Q=Q,
        vikor_rank=pd.Series(Q).rank(method='min').astype(int)))
    order = np.argsort(Q, kind='stable')
    a, b = order[:2]
    threshold = 1 / (len(cities) - 1)
    advantage = bool(Q[b] - Q[a] >= threshold - 1e-12)
    stability = bool(S[a] <= S.min() + 1e-12 or R[a] <= R.min() + 1e-12)
    tau = kendalltau(result.topsis_rank, result.vikor_rank, variant='b')
    main = evaluate(cities, lo, hi, w)
    result['main_interval_decision_rank'] = main.decision_rank
    result['evidence_version'], result['weight_reference'] = version, reference
    span = best - worst
    loss = np.divide(best-z, span, out=np.zeros_like(z), where=span > 1e-14) * w
    components = pd.DataFrame([dict(evidence_version=version, weight_reference=reference,
        city=city, indicator=name, midpoint_utility=z[i, j], weight=w[j],
        vikor_weighted_relative_shortfall=loss[i, j],
        sample_best=best[j], sample_worst=worst[j])
        for i, city in enumerate(cities) for j, name in enumerate(NAMES)])
    summary = dict(evidence_version=version, weight_reference=reference,
        topsis_midpoint_winners=result.loc[result.topsis_rank == 1, 'city'].tolist(),
        vikor_q_winners=result.loc[result.vikor_rank == 1, 'city'].tolist(),
        kendall_tau_b=float(tau.statistic), vikor_v=.5,
        acceptable_advantage_threshold=threshold,
        first_second_Q_gap=float(Q[b]-Q[a]), acceptable_advantage=advantage,
        acceptable_stability=stability,
        single_compromise_accepted=bool(advantage and stability and (result.vikor_rank == 1).sum() == 1),
        main_minimax_choices=main.loc[main.decision_rank == 1, 'city'].tolist(),
        main_possible_champion_count=int(main.possible_champion.sum()))
    # VIKOR degeneracy and component identity are meaningful numerical checks.
    for x in [np.ones((3, 10)) * .4, np.tile(z[0], (3, 1))]:
        ds, dr, dq, _, _ = vikor(x, w)
        assert np.all(ds == 0) and np.all(dr == 0) and np.all(dq == 0)
    np.testing.assert_allclose(loss.sum(1), S, rtol=0, atol=1e-14)
    np.testing.assert_allclose(loss.max(1), R, rtol=0, atol=1e-14)
    assert np.all((0 <= Q) & (Q <= 1))
    return result, components, summary


def country_cases():
    path = ROOT / 'results/task4_v117_city_revision/utility_bounds.csv'
    legacy = pd.read_csv(path).query("scenario == 'v117'")
    meta = pd.read_csv(ROOT / 'data/city_candidates_team_25.csv').set_index('city')
    cities = legacy.city.drop_duplicates().tolist()
    assert len(cities) == 25
    lo = legacy.pivot(index='city', columns='indicator', values='lower').loc[cities, NAMES]
    hi = legacy.pivot(index='city', columns='indicator', values='upper').loc[cities, NAMES]
    L, U = pd.Series(score(lo.to_numpy(), weights(.1)), index=cities), pd.Series(score(hi.to_numpy(), weights(.1)), index=cities)
    reports, rows = [], []
    for a, b in [('Phoenix', 'New York'), ('Mumbai', 'Delhi')]:
        country = meta.loc[a, 'country']
        assert country == meta.loc[b, 'country']
        reports.append(dict(country=country, city_a=a, city_b=b,
            evidence_version='legacy25 V117; separate from user16 V121',
            a_score_lower=L[a], a_score_upper=U[a], b_score_lower=L[b], b_score_upper=U[b],
            a_necessarily_strictly_better=bool(L[a] > U[b]),
            b_necessarily_strictly_better=bool(L[b] > U[a]),
            a_possible_pairwise_winner=bool(U[a] >= L[b]),
            b_possible_pairwise_winner=bool(U[b] >= L[a])))
        for name in NAMES:
            al, au, bl, bu = lo.loc[a, name], hi.loc[a, name], lo.loc[b, name], hi.loc[b, name]
            rows.append(dict(country=country, city_a=a, city_b=b, indicator=name,
                a_lower=al, a_upper=au, b_lower=bl, b_upper=bu,
                both_point_identified=bool(al == au and bl == bu),
                both_informative=bool((al > 0 or au < 1) and (bl > 0 or bu < 1)),
                a_necessarily_above=bool(al > bu), b_necessarily_above=bool(bl > au)))
    return pd.DataFrame(reports), pd.DataFrame(rows)


def equity_case():
    source = ROOT / 'data/task4_v32_shanghai'
    data = json.loads((source / 'extracted.json').read_text())
    for m in json.loads((source / 'manifest.json').read_text()):
        assert digest(source / m['file']) == m['sha256']
    sr, tr = data['tables']['students'][1:], data['tables']['teachers'][1:]
    assert len(sr) == len(tr) == 16 and [r['district'] for r in sr] == [r['district'] for r in tr]
    s = np.array([r['values'][2] for r in sr], float)
    t = np.array([r['values'][-1] for r in tr], float)
    assert s.sum() == data['students'] == 235542 and t.sum() == data['teachers'] == 23999
    p, q = s/s.sum(), t/s
    u = 15*q/(1+15*q)
    pooled, local = 15*t.sum()/(s.sum()+15*t.sum()), float(p @ u)
    mu = t.sum()/s.sum()
    identity = 225/(1+15*mu)**2 * (p @ ((q-mu)**2/(1+15*q)))
    np.testing.assert_allclose(pooled-local, identity, rtol=0, atol=1e-14)
    old = json.loads((ROOT / 'results/task4_v33_district_resources/summary.json').read_text())
    np.testing.assert_allclose([pooled, local, pooled-local],
        [old['pooled_utility'], old['student_weighted_district_utility'], old['aggregation_gap']], rtol=0, atol=1e-14)
    lower20 = bottom_fraction_mean(u, s)
    # Fractional cutoff handles a large district without excluding its mass.
    np.testing.assert_allclose(bottom_fraction_mean([.2, .8], [3, 1], 1), .35, rtol=0, atol=1e-14)
    np.testing.assert_allclose(bottom_fraction_mean([.2, .8], [3, 1], .2), .2, rtol=0, atol=1e-14)
    summary = dict(city='Shanghai', year=2025, separate_historical_case=True,
        districts=16, students=int(s.sum()), teacher_headcount=int(t.sum()),
        pooled_utility=float(pooled), student_weighted_district_utility=local,
        aggregation_gap=float(pooled-local), relative_gap_percent=float(100*(pooled-local)/pooled),
        district_utility_min=float(u.min()), district_utility_max=float(u.max()),
        district_ptr_min=float((s/t).min()), district_ptr_max=float((s/t).max()),
        bottom20_student_mass_district_utility=lower20, bottom20_gap_from_student_mean=local-lower20,
        scope='School-location counts for regular senior-secondary pupils and full-time teacher headcount; excludes vocational, not FTE. Fractional bottom20 assumes district-homogeneous exposure, not observed individual experience or resident accessibility.',
        main_user16_scores_changed=False)
    frame = pd.DataFrame(dict(district=[r['district'] for r in sr], students=s.astype(int), teachers=t.astype(int),
        student_weight=p, ptr=s/t, resource_utility=u))
    return frame, summary


def age_cases():
    data = json.loads((ROOT / 'data/task4_v116_ibb/aggregate_results.json').read_text())
    records = []
    for label, group in data['age_groups'].items():
        extra = data['age_groups_optional_membership'][label]
        den = group['weight_total'] + extra['weight_optional_known_age'] + extra['weight_optional_unknown_age']
        lower = group['utility_known_numerator']/den
        upper = (group['utility_known_numerator'] + group['weight_unknown'] + den-group['weight_total'])/den
        np.testing.assert_allclose([lower, upper], [extra['lower'], extra['upper']], rtol=0, atol=1e-14)
        records.append(dict(city='Istanbul', year=2012, age_group=label, n_known=group['n'],
            observed_journey_n=group['n_observed'], observed_journey_weight=group['weight_observed'],
            unknown_duration_weight=group['weight_unknown'],
            conditional_observed_mean_minutes=group['conditional_observed_mean_minutes'],
            marginal_utility_lower=lower, marginal_utility_upper=upper,
            shared_unknown_age_optional_weight=extra['weight_optional_unknown_age']))
    age = pd.DataFrame(records)
    assert age.marginal_utility_lower.max() <= age.marginal_utility_upper.min()
    # Existing exact-age enrolment rows illustrate age/stage overlap, not preferences.
    sg_dir = ROOT / 'data/task4_v71_singapore'
    manifest = json.loads((sg_dir / 'manifest.json').read_text())
    m = next(m for m in manifest if m['file'] == 'moe_level_age_api.json')
    assert digest(sg_dir / m['file']) == m['sha256']
    api = json.loads((sg_dir / m['file']).read_text())
    raw = pd.DataFrame(api['result']['records'])
    assert len(raw) == int(api['result']['total']) == 541
    sg = raw[(raw.YEAR.astype(str) == '2020') & (raw.SEX == 'MF') & raw.AGE.isin(['14 YRS', '18 YRS'])].copy()
    assert not sg.duplicated(['LEVEL', 'AGE']).any()
    sg['enrolment'] = sg.ENROLMENT.astype(int)
    sg = sg.rename(columns={'LEVEL': 'school_level', 'AGE': 'start_of_year_age'})
    sg['within_age_secondary_enrolment_share'] = sg.enrolment / sg.groupby('start_of_year_age').enrolment.transform('sum')
    sg['scope'] = 'MOE2020 secondary enrolment only; all citizenship; start-of-year age; not Census resident school travellers'
    summary = dict(istanbul_year=2012, exact_age14_vs18_identified=False,
        age_groups_available=age.age_group.tolist(), marginal_intervals_overlap=True,
        observed_mean_scope='Only observed home-school journeys; missing-duration and optional members retained in utility bounds',
        joint_attainability_note=data['age_groups_optional_membership_note'],
        singapore_secondary_age_totals=sg.groupby('start_of_year_age').enrolment.sum().to_dict(),
        singapore_age_scope='Age at start of2020; MOE secondary enrolment, no citizenship joint table or Census reference-day/travel coverage match',
        age_specific_preferences_observed=False, no_new_age_weights=True, main_user16_scores_changed=False)
    return age, sg[['school_level', 'start_of_year_age', 'enrolment', 'within_age_secondary_enrolment_share', 'scope']], summary


def main():
    paths = [SOURCE, ROOT/'design/task4_user_current_model.json',
        ROOT/'design/task4_user_v121_admissions.json', ROOT/'results/task4_user_v121_revision/current_ranks.csv',
        ROOT/'results/task4_user_v118_revision/utility_bounds.csv', ROOT/'scripts/task4_v119_method_country.py',
        ROOT/'results/task4_v119_method_country/method_ranks.csv',
        ROOT/'results/task4_v33_district_resources/summary.json',
        ROOT/'results/task4_v117_city_revision/utility_bounds.csv', ROOT/'data/city_candidates_team_25.csv',
        ROOT/'data/task4_v32_shanghai/extracted.json', ROOT/'data/task4_v32_shanghai/manifest.json',
        ROOT/'data/task4_v116_ibb/aggregate_results.json', ROOT/'data/task4_v116_ibb_review/aggregate_controls.json',
        ROOT/'data/task4_v71_singapore/moe_level_age_api.json', ROOT/'data/task4_v71_singapore/manifest.json',
        ROOT/'visuals/cartography/city_map_audit.json']
    protected = {p: digest(p) for p in paths}
    f0, l0, h0 = v118_bounds()
    frame, lo, hi = v121_bounds()
    assert frame.city.tolist() == f0.city.tolist() and lo.shape == hi.shape == (16, 10)
    country_counts = frame.groupby('country').size()
    assert len(country_counts) == 16 and country_counts.max() == 1
    allr, components, method_summary, bound_rows = [], [], [], []
    for version, l, h in [('V118', l0, h0), ('V121', lo, hi)]:
        for reference, w in [('fixed', weights(.1)), ('equal', np.ones(10)/10)]:
            r, c, summary = method_results(frame, l, h, version, w, reference)
            allr.append(r); components.append(c); method_summary.append(summary)
        bound_rows.extend(dict(evidence_version=version, city=city, indicator=name,
            lower=l[i, j], upper=h[i, j], midpoint=(l[i, j]+h[i, j])/2)
            for i, city in enumerate(frame.city) for j, name in enumerate(NAMES))
    ranks = pd.concat(allr, ignore_index=True)
    # Control arm reproduces the historical V119 fixed-weight comparison.
    old = pd.read_csv(ROOT/'results/task4_v119_method_country/method_ranks.csv').set_index('city')
    before = ranks.query("evidence_version == 'V118' and weight_reference == 'fixed'").set_index('city')
    for name in ['topsis_midpoint_score', 'topsis_rank', 'vikor_S', 'vikor_R', 'vikor_Q', 'vikor_rank']:
        np.testing.assert_allclose(before.loc[old.index, name], old[name], rtol=0, atol=1e-12)
    pairs, indicators = country_cases()
    district, equity = equity_case()
    age, sg, age_summary = age_cases()
    OUT.mkdir(parents=True, exist_ok=True)
    ranks.to_csv(OUT/'method_ranks.csv', index=False)
    pd.concat(components, ignore_index=True).to_csv(OUT/'method_components.csv', index=False)
    pd.DataFrame(bound_rows).to_csv(OUT/'method_utility_inputs.csv', index=False)
    pairs.to_csv(OUT/'country_score_comparison.csv', index=False)
    indicators.to_csv(OUT/'country_indicator_bounds.csv', index=False)
    frame[['city', 'country']].to_csv(OUT/'user16_country_coverage.csv', index=False)
    district.to_csv(OUT/'shanghai_district_resources.csv', index=False)
    age.to_csv(OUT/'istanbul_historical_age_groups.csv', index=False)
    sg.to_csv(OUT/'singapore2020_secondary_exact_age_counts.csv', index=False)
    comparisons = []
    for reference in ['fixed', 'equal']:
        a = ranks.query("evidence_version == 'V118' and weight_reference == @reference").set_index('city')
        b = ranks.query("evidence_version == 'V121' and weight_reference == @reference").set_index('city')
        comparisons.append(dict(weight_reference=reference,
            changed_topsis_midpoint_ranks=int((a.topsis_rank != b.topsis_rank).sum()),
            changed_vikor_ranks=int((a.vikor_rank != b.vikor_rank).sum()),
            kendall_topsis_before_after=float(kendalltau(a.topsis_rank, b.topsis_rank).statistic),
            kendall_vikor_before_after=float(kendalltau(a.vikor_rank, b.vikor_rank).statistic)))
    for p, expected in protected.items():
        assert digest(p) == expected, p
    summary = dict(version='V122 extension of user16 V121; no main model change',
        method_cases=method_summary, controlled_V118_V121=comparisons,
        comparison_scope='Same midpoint utilities and weights in each arm; fixed-ideal TOPSIS versus sample-ideal classic VIKOR v=.5. Midpoints are unobserved illustrative scenarios, not imputations or main recommendations.',
        historical_control_reproduces_V119=True,
        same_country_pairs_in_main16=0, country_case_dataset='Separate historical25 V117, inherited fixed weights',
        country_comparability='Common indicator utility definitions/anchors and weights; retain legacy mixed vintages and spatial/stage limits. No harmonized same-year pair dataset or national causal effect.',
        country_pairs=pairs.to_dict('records'), equity=equity, age_evidence=age_summary,
        protected_inputs_unchanged=True,
        input_sha256={str(p.relative_to(ROOT)): h for p, h in protected.items()})
    (OUT/'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


if __name__ == '__main__':
    main()
