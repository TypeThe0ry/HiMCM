"""V207: two-level AHP weights (high-schooler view) on frozen V205 bounds.

Main ranking uses the midpoint representative TOPSIS score; interval bounds,
regret, withdrawals, Dirichlet weights, VIKOR and 2035 scenarios are robustness.
"""
import json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT, NAMES, SPEC, score
from task4_user_v205_revision import revised_bounds, controlled_cases
from task4_user_city_indicators import evaluate
from audit_task4_v203 import raw_map, factors_for

OUT = ROOT / 'results/task4_v207_ahp'
RI = {1: 0, 2: 0, 3: .58, 4: .90, 5: 1.12}
CATEGORIES = [
    ('Safety and environment', ['homicide_rate', 'pm25']),
    ('Cost of living', ['cost_living_index', 'price_income_ratio']),
    ('Education', ['upper_secondary_ptr', 'research_he_density']),
    ('Mobility', ['travel', 'public_transport_density']),
    ('Daily life', ['fixed_broadband_mbps', 'public_pool_density']),
]
# Saaty 1-9 judgements, row compared with column (upper triangle).
CAT_JUDGE = {(0, 1): 3, (0, 2): 1, (0, 3): 3, (0, 4): 4,
             (1, 2): 1/3, (1, 3): 1, (1, 4): 2,
             (2, 3): 3, (2, 4): 4,
             (3, 4): 2}
WITHIN = {'Safety and environment': 2, 'Cost of living': 1, 'Education': 3,
          'Mobility': 2, 'Daily life': 2}
# Zurich homicide: supplied 0.14 has no verified denominator. Modelling value from the
# city police PKS 2025 count of completed homicide offences (2) over the 2025 population.
ZURICH_HOMICIDE = 2 / 440935 * 1e5


# Fills for the 11 cells without city data (modelling assumptions, stated in the paper).
# Upper-secondary pupils per teacher: Eurostat educ_uoe_perp04, ISCED 3, 2024, national.
PTR_FILL = {'Helsinki': 17.4, 'Amsterdam': 16.4, 'Dublin': 14.2, 'Paris': 11.5, 'Milan': 10.6, 'Madrid': 9.6}
PTR_MEDIAN_FILL = ['Zurich', 'London']  # not in Eurostat: median of the other 14 cities
# Mean one-way travel minutes: Vienna AK Wien commuter study (32), Tokyo-to 2021 time-use
# survey commute/school 95 min per day halved (47.5), Warsaw 2022 survey school trip (27).
TRAVEL_FILL = {'Vienna': 32.0, 'Tokyo': 47.5, 'Warsaw': 27.0}


def bounds(override=True, fill=True):
    f, lo, hi = revised_bounds()
    cities = f.city.tolist()
    if override:
        i = cities.index('Zurich')
        lo[i, 0] = hi[i, 0] = 2 / (2 + ZURICH_HOMICIDE)
    if fill:
        j = NAMES.index('upper_secondary_ptr')
        for c, x in PTR_FILL.items():
            i = cities.index(c); assert hi[i, j] - lo[i, j] == 1
            lo[i, j] = hi[i, j] = 15 / (15 + x)
        mid = (lo[:, j] + hi[:, j]) / 2
        known = [k for k, c in enumerate(cities) if c not in PTR_MEDIAN_FILL]
        xs = 15 * (1 - mid[known]) / mid[known]
        med = float(np.median(xs))
        for c in PTR_MEDIAN_FILL:
            i = cities.index(c); assert hi[i, j] - lo[i, j] == 1
            lo[i, j] = hi[i, j] = 15 / (15 + med)
        j = NAMES.index('travel')
        for c, t in TRAVEL_FILL.items():
            i = cities.index(c); assert hi[i, j] - lo[i, j] == 1
            lo[i, j], hi[i, j] = np.exp(-t / 30), 1.0
        assert not np.any(hi - lo >= 1)
        bounds.ptr_median = med
    return f, lo, hi


SCENARIOS_2035 = {
    'resource_expansion': {'research_he_density': .1, 'public_transport_density': .1, 'public_pool_density': .1},
    'living_pressure': {'cost_living_index': .1, 'price_income_ratio': .1, 'travel': .1},
    'balanced_improvement': {'upper_secondary_ptr': -.1, 'pm25': -.1, 'travel': -.1},
}


def matrix(n, judge):
    A = np.ones((n, n))
    for (i, j), v in judge.items():
        A[i, j], A[j, i] = v, 1 / v
    return A


def ahp(A):
    vals, vecs = np.linalg.eig(A)
    k = np.argmax(vals.real)
    w = np.abs(vecs[:, k].real); w /= w.sum()
    n = len(A); lam = vals[k].real
    ci = (lam - n) / (n - 1) if n > 2 else 0.0
    cr = ci / RI[n] if RI[n] else 0.0
    return w, lam, ci, cr


def ahp_weights():
    A = matrix(5, CAT_JUDGE)
    cw, lam, ci, cr = ahp(A)
    w = np.zeros(len(NAMES)); local = {}
    for c, (name, members) in enumerate(CATEGORIES):
        lw, *_ = ahp(matrix(2, {(0, 1): WITHIN[name]}))
        for m, v in zip(members, lw):
            w[NAMES.index(m)] = cw[c] * v; local[m] = v
    assert np.isclose(w.sum(), 1)
    return w, dict(category_matrix=A.round(6).tolist(), category_weights=dict(zip([c for c, _ in CATEGORIES], cw.round(6).tolist())),
                   lambda_max=lam, CI=ci, CR=cr, local_weights=local)


def vikor(z, w, v=.5):
    best, worst = z.max(0), z.min(0)
    span = np.where(best > worst, best - worst, 1)
    d = w * (best - z) / span
    S, R = d.sum(1), d.max(1)
    Q = v * (S - S.min()) / (S.max() - S.min()) + (1 - v) * (R - R.min()) / (R.max() - R.min())
    order = np.argsort(Q)
    adv = Q[order[1]] - Q[order[0]] >= 1 / (len(z) - 1)
    stable = order[0] in (np.argmin(S), np.argmin(R))
    return Q, order, bool(adv), bool(stable)


def table(cities, lo, hi, w):
    t = evaluate(cities, lo, hi, w)
    t['score'] = t.midpoint_illustrative_score
    t['rank'] = t.score.rank(ascending=False, method='min').astype(int)
    return t


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    f, lo, hi = bounds()
    cities = f.city.tolist()
    w, info = ahp_weights()
    filled_means = f.commute_min.to_numpy(dtype=float).copy()
    for c, t in TRAVEL_FILL.items():
        filled_means[cities.index(c)] = t
    eq = np.full(10, .1)
    old = np.array([(.9) / 8 if s[3] else .05 for s in SPEC])
    summary = dict(version='V207 staged', base='V205 bounds + Zurich homicide model value + 11 national/survey fills', ptr_median_fill=bounds.ptr_median, ahp=info,
                   weights=dict(zip(NAMES, w.round(6).tolist())))

    main_t = table(cities, lo, hi, w)
    mid = (lo + hi) / 2
    main_t['category_scores'] = None
    for name, members in CATEGORIES:
        idx = [NAMES.index(m) for m in members]
        main_t[name] = (mid[:, idx] * w[idx]).sum(1) / w[idx].sum()
    for j, n in enumerate(NAMES):
        main_t['u_' + n] = mid[:, j]
    main_t = main_t.drop(columns='category_scores').sort_values('rank')
    main_t.to_csv(OUT / 'main_ranking.csv', index=False)
    comp = {}
    for ref, ww in [('ahp', w), ('equal', eq), ('old_fixed', old)]:
        t = table(cities, lo, hi, ww)
        comp[ref] = dict(midpoint_order=t.sort_values('rank').city.tolist(),
                         midpoint_scores=dict(zip(t.city, t.score.round(2))),
                         regret_choice=t.loc[t.decision_rank.eq(1), 'city'].tolist(),
                         regret_order=t.sort_values('max_regret').city.tolist(),
                         possible_champions=int(t.possible_champion.sum()),
                         necessary_champions=int(t.necessary_champion.sum()),
                         mean_width=float((t.score_upper - t.score_lower).mean()))
        t.to_csv(OUT / f'interval_{ref}.csv', index=False)
    summary['comparison'] = comp

    # Withdrawal of submitted point groups (V143 vintage list), AHP and equal weights.
    points = pd.read_csv(ROOT / 'results/task4_v143_vintage/submitted_points.csv')
    rows = []
    for scen in ['baseline', 'pre2020_points', 'after2025_points', 'non_ok_points', 'union_points']:
        a, b = lo.copy(), hi.copy(); n = 0
        for p in points.itertuples():
            early, late, flag = p.submitted_year < 2020, p.submitted_year > 2025, p.submitted_flag != 'ok'
            rem = dict(baseline=False, pre2020_points=early, after2025_points=late, non_ok_points=flag,
                       union_points=early or late or flag)[scen]
            i, j = cities.index(p.city), NAMES.index(p.indicator)
            if rem and a[i, j] == b[i, j]:
                a[i, j], b[i, j] = 0, 1; n += 1
        for ref, ww in [('ahp', w), ('equal', eq)]:
            t = table(cities, a, b, ww)
            rows.append(dict(scenario=scen, cells=n, weight=ref,
                             midpoint_first=t.loc[t['rank'].eq(1), 'city'].tolist(),
                             midpoint_top3=t.sort_values('rank').city.head(3).tolist(),
                             regret_first=t.loc[t.decision_rank.eq(1), 'city'].tolist(),
                             mean_width=float((t.score_upper - t.score_lower).mean())))
    pd.DataFrame(rows).to_csv(OUT / 'withdrawals.csv', index=False)

    # V205 controlled source cases under AHP.
    _, cases = controlled_cases()
    cr = []
    zi = cities.index('Zurich')
    for label, a, b in cases:
        a, b = a.copy(), b.copy(); a[zi, 0] = b[zi, 0] = lo[zi, 0]
        full = (b - a) >= 1; a[full], b[full] = lo[full], hi[full]
        t = table(cities, a, b, w)
        cr.append(dict(case=label, midpoint_first=t.loc[t['rank'].eq(1), 'city'].tolist(),
                       top3=t.sort_values('rank').city.head(3).tolist(),
                       regret_first=t.loc[t.decision_rank.eq(1), 'city'].tolist()))
    pd.DataFrame(cr).to_csv(OUT / 'controlled_cases.csv', index=False)

    # Dirichlet weight perturbation around AHP weights.
    rng = np.random.default_rng(20261114)
    mc = {}
    for kappa in [20, 100, 500]:
        W = rng.dirichlet(kappa * w, 10000)
        good = np.sqrt((((1 - mid)[None] ** 2) * W[:, None, :]).sum(2))
        bad = np.sqrt(((mid[None] ** 2) * W[:, None, :]).sum(2))
        S = 100 * bad / (good + bad)
        ranks = (-S).argsort(1).argsort(1) + 1
        mc[kappa] = dict(first=dict(zip(cities, (ranks == 1).mean(0).round(4))),
                         top3=dict(zip(cities, (ranks <= 3).mean(0).round(4))),
                         mean_rank=dict(zip(cities, ranks.mean(0).round(3))))
    summary['dirichlet'] = mc

    # VIKOR at the same midpoint utilities.
    vk = {}
    for ref, ww in [('ahp', w), ('equal', eq)]:
        Q, order, adv, stable = vikor(mid, ww)
        vk[ref] = dict(order=[cities[k] for k in order], Q=dict(zip(cities, Q.round(4))), advantage=adv, stability=stable)
    summary['vikor'] = vk

    # 2035 scenarios: each listed raw value changes by 10% by 2035.
    means = filled_means
    fut = []
    for scen, ch in {'today': {}, **SCENARIOS_2035}.items():
        a, b = raw_map(lo, hi, factors_for((16, 10), ch), means)
        t = table(cities, a, b, w)
        for r in t.itertuples():
            fut.append(dict(scenario=scen, city=r.city, score=r.score, rank=r.rank, regret_rank=r.decision_rank))
    fut = pd.DataFrame(fut)
    fut.to_csv(OUT / 'future_2035.csv', index=False)
    summary['future_first'] = {s: g.sort_values('rank').city.head(3).tolist() for s, g in fut.groupby('scenario')}
    from scipy.stats import kendalltau
    pref = {}
    for name, ids in [('education_priority', ['upper_secondary_ptr', 'research_he_density']),
                      ('independent_living', ['travel', 'public_transport_density'])]:
        m = np.ones(10); m[[NAMES.index(i) for i in ids]] = 2; ww = w * m / (w * m).sum()
        t = table(cities, lo, hi, ww).sort_values('rank')
        pref[name] = dict(weights=dict(zip(NAMES, ww.round(4))), top5=list(zip(t.city.head(5), t.score.head(5).round(2))),
                          regret_first=t.loc[t.decision_rank.eq(1), 'city'].tolist())
    summary['preferences'] = pref
    base = table(cities, lo, hi, w).set_index('city'); eqt = table(cities, lo, hi, eq).set_index('city')
    summary['ahp_vs_equal'] = dict(kendall_tau=kendalltau(base.loc[cities, 'rank'], eqt.loc[cities, 'rank']).statistic,
                                   cities_rank_changed=int((base.loc[cities, 'rank'] != eqt.loc[cities, 'rank']).sum()),
                                   equal_order=eqt.sort_values('rank').index.tolist())
    summary['interval_ahp'] = base[['score', 'score_lower', 'score_upper', 'max_regret', 'decision_rank', 'possible_champion']].round(3).reset_index().to_dict('records')
    hw = {}
    for city in ['Amsterdam', 'Zurich']:
        a, b = lo.copy(), hi.copy(); i = cities.index(city); a[i, 0], b[i, 0] = 0, 1
        t = table(cities, a, b, w).set_index('city'); hw[f'withdraw_{city}_homicide'] = dict(rank=int(t.loc[city, 'rank']), first=t['rank'].idxmin())
    summary['homicide_withdrawals'] = hw
    # Zurich homicide rate at which Singapore ties Zurich on the representative score.
    from scipy.optimize import brentq
    def gap(rate):
        a, b = lo.copy(), hi.copy(); a[zi, 0] = b[zi, 0] = 2 / (2 + rate)
        s_ = score((a + b) / 2, w); return s_[zi] - np.delete(s_, zi).max()
    summary['zurich_homicide'] = dict(model_value=ZURICH_HOMICIDE, supplied=0.14, tie_rate=brentq(gap, 0, 20),
                                      rank_with_supplied=None)
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=1, default=float))
    print(json.dumps(dict(ahp=dict(CR=info['CR'], cw=info['category_weights']), weights=summary['weights']), indent=1))
    print(main_t[['rank', 'city', 'score', 'score_lower', 'score_upper', 'decision_rank']].to_string(index=False))
    print(json.dumps(comp, indent=0, default=float)[:3000])


if __name__ == '__main__':
    main()
