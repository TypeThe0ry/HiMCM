"""Independent shared-completion replay using long-double quadratics.

No project scoring, feasibility, or acquisition functions are imported.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

P = Path(__file__).resolve().parent
D = np.longdouble
MAIN, AUX = [0, 1, 2, 3, 4, 5, 7, 8], [6, 9]


def score(x, alpha):
    x = np.asarray(x, dtype=D); alpha = D(str(alpha))
    w = np.full(10, (1-alpha)/8, dtype=D); w[AUX] = alpha/2
    pos = np.sqrt(np.sum(w*x*x, axis=-1))
    neg = np.sqrt(np.sum(w*(1-x)**2, axis=-1))
    return 100*pos/(pos+neg)


def polynomial(x, y):
    def terms(z):
        z = np.asarray(z, dtype=D)
        p0, p1 = np.mean(z[MAIN]**2), np.mean(z[AUX]**2)
        q0, q1 = np.mean((1-z[MAIN])**2), np.mean((1-z[AUX])**2)
        return p0, p1-p0, q0, q1-q0
    p0, p1, q0, q1 = terms(x); a0, a1, b0, b1 = terms(y)
    return (p0*b0-a0*q0, p0*b1+p1*b0-a0*q1-a1*q0, p1*b1-a1*q1)


def feasible(x, rivals, amin, amax):
    polys = [polynomial(x, y) for y in rivals]
    cuts = {D(str(amin)), D(str(amax))}
    for c, b, a in polys:
        roots = []
        if a == 0:
            if b != 0: roots = [-c/b]
        else:
            disc = b*b-4*a*c
            if disc >= 0:
                q = -(b+np.copysign(np.sqrt(disc), b))/2
                roots = [q/a, c/q] if q != 0 else [-b/(2*a)]
        cuts.update(r for r in roots if amin < r < amax)
    cuts = sorted(cuts)
    points = cuts+[(a+b)/2 for a, b in zip(cuts[:-1], cuts[1:])]
    return any(all(c+t*b+t*t*a >= -D('1e-12') for c, b, a in polys) for t in points)


def main():
    s = json.loads((P/'summary.json').read_text())
    base = pd.read_csv(P/'baseline/utility_bounds.csv', float_precision='round_trip')
    cities, names = base.city.drop_duplicates().tolist(), base.indicator.drop_duplicates().tolist()
    assert len(cities) == 25 and len(names) == 10 and len(base) == 250
    lo, hi = (base[k].to_numpy().reshape(25, 10) for k in ('lower', 'upper'))
    assert hashlib.sha256(np.stack([lo, hi]).astype('<f8').tobytes()).hexdigest() == s['input_bounds_sha256']
    assert s['model_version'] == 'V102' and s['scenario_only'] and not s['main_admitted']
    v102 = pd.read_csv(P.parent/'task4_v102_copenhagen_revision/utility_bounds.csv', float_precision='round_trip')
    v102 = v102[v102.scenario.eq('v102_copenhagen_resources')].drop(columns=['scenario']).reset_index(drop=True)
    pd.testing.assert_frame_equal(base, v102)
    assert names == ['homicide_rate','pm25','cost_living_index','price_income_ratio','upper_secondary_ptr','research_he_density','public_transport_density','travel','fixed_broadband_mbps','public_pool_density']
    source_cert = pd.read_csv(P/'unavoidable_certificates.csv', float_precision='round_trip')
    exact = pd.read_csv(P/'hypothetical_exact_values.csv', float_precision='round_trip')
    city_results = json.loads((P/'city_feasibility.json').read_text())
    assert len(source_cert) == 300 and len(city_results) == 600 and len(s['scenarios']) == 24
    assert not exact.duplicated(['scenario', 'mode', 'city', 'indicator']).any()
    alpha, (amin, amax) = s['fixed_alpha'], s['alpha_range']
    errors, checked_lower, checked_joint, positive_witnesses = [], set(), 0, 0
    summaries = []
    for case in s['scenarios']:
        label, mode = case['scenario'], case['mode']
        mask = np.zeros((25, 10), bool)
        js = [names.index(j) for j in case['measured_indicators']]
        if label == 'phoenix_education_and_travel': mask[cities.index('Phoenix'), js] = True
        else: mask[:, js] = True
        worst_upper, best_lower = np.where(mask, lo, hi), np.where(mask, hi, lo)
        cert_rows = source_cert[source_cert.scenario.eq(label)]
        required = []
        for row in cert_rows.itertuples():
            i = cities.index(row.city); others = np.arange(25) != i
            if label not in checked_lower:
                margin = score(worst_upper[i], alpha)-max(score(best_lower[others], alpha))
                errors.append(abs(margin-D(str(row.worst_fixed_margin))))
                assert (margin >= -D('1e-10')) == row.fixed_unavoidable
                yes = feasible(worst_upper[i], best_lower[others], amin, amax)
                assert yes == row.continuous_unavoidable
                if yes:
                    assert amin <= row.witness_alpha <= amax
                    assert score(worst_upper[i], row.witness_alpha) >= max(score(best_lower[others], row.witness_alpha))-D('1e-8')
            if getattr(row, mode+'_unavoidable'): required.append(row.city)
        checked_lower.add(label)
        assert required == case['unavoidable_cities']
        l, h = lo.copy(), hi.copy()
        cells = exact[exact.scenario.eq(label) & exact['mode'].eq(mode)]
        assert len(cells) == mask.sum() == case['selected_cells']
        for row in cells.itertuples():
            i, j = cities.index(row.city), names.index(row.indicator)
            assert mask[i, j] and row.previous_lower == lo[i, j] and row.previous_upper == hi[i, j]
            value = row.hypothetical_exact_value
            assert lo[i, j] <= value <= hi[i, j]
            expected = hi[i, j] if row.city in case['anchor_cities'] else lo[i, j]
            assert value == expected
            l[i, j] = h[i, j] = value
        np.testing.assert_array_equal(l[~mask], lo[~mask]); np.testing.assert_array_equal(h[~mask], hi[~mask])
        rows = [r for r in city_results if r['scenario'] == label and r['mode'] == mode]
        assert [r['city'] for r in rows] == cities
        survivors = []
        for row in rows:
            i = cities.index(row['city']); others = np.arange(25) != i
            margin = score(h[i], alpha)-max(score(l[others], alpha))
            errors.append(abs(margin-D(str(row['fixed_score_margin']))))
            yes = bool(margin >= -D('1e-10')) if mode == 'fixed' else feasible(h[i], l[others], amin, amax)
            assert yes == row['possible']
            if yes:
                survivors.append(row['city']); witness = row['witness_alpha']
                assert amin <= witness <= amax
                assert score(h[i], witness) >= max(score(l[others], witness))-D('1e-8')
                positive_witnesses += 1
            checked_joint += 1
        assert survivors == case['surviving_cities'] and set(required) <= set(survivors)
        lower, upper = max(1, len(required)), len(survivors)
        assert lower == case['universal_count_lower_bound'] and upper == case['attained_count_upper_bound']
        assert (lower == upper) == case['joint_minimum_certified']
        assert case['certified_minimum'] == (lower if lower == upper else None)
        summaries.append(dict(scenario=label, mode=mode, lower=lower, upper=upper))
    assert max(errors) < D('1e-11')
    unresolved = [r for r in summaries if r['lower'] != r['upper']]
    assert unresolved == [dict(scenario='both_plus_homicide_rate',mode='continuous',lower=3,upper=5)]
    assert s['certified_cases']==23 and s['unresolved_cases']==1
    assert len(exact)==1404

    result = dict(passed=True, model_version=s['model_version'], input_hash_verified=True, baseline_matches_admitted_v102=True, unresolved_cases=unresolved,
        lower_certificates_checked=len(checked_lower)*25, shared_completion_city_checks=checked_joint,
        hypothetical_selected_cell_values_checked=len(exact), positive_joint_witnesses=positive_witnesses,
        maximum_fixed_margin_discrepancy=float(max(errors)),
        minimum_count_matches=sum(r['lower'] == r['upper'] for r in summaries),
        method='Independent long-double scores, direct quadratic coefficients and stable analytical roots; no project helpers.',
        scenario_only=True, main_admitted=False, formal_interval_arithmetic=False,
        input_file_sha256={f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['summary.json','hypothetical_exact_values.csv','city_feasibility.json','unavoidable_certificates.csv','baseline/utility_bounds.csv']})
    (P/'audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
