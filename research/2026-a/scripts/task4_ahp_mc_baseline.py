"""Weight-only TOPSIS sensitivity with unchanged evidence intervals.

Default weights are the inherited policy, NOT elicited AHP judgments. Optional
AHP JSON must document real judgments; this program validates mathematics and
metadata presence, not the truth of provenance. Midpoints are illustrative
completions, never observed values. Dirichlet frequencies are conditional on an
analyst-selected weight distribution, not population preferences/win probabilities.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_current_model import current_bounds, verify_baseline, verify_bounds
from task4_v5_model import ROOT, CITIES, NAMES, weights, score, summarize

RI = {1: 0., 2: 0., 3: .58, 4: .90, 5: 1.12, 6: 1.24,
      7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
TOL = 1e-12


def ahp_weights(document, names):
    """Positive reciprocal full matrix, principal eigenvector, CR < .10."""
    for key in ('source', 'respondents', 'elicitation_date', 'judgment_method'):
        if not isinstance(document.get(key), str) or not document[key].strip():
            raise ValueError('AHP requires nonempty provenance field: '+key)
    if document.get('indicators') != list(names):
        raise ValueError('AHP indicator ordering must exactly match current criteria')
    a = np.asarray(document['matrix'], dtype=float)
    n = len(names)
    if a.shape != (n, n) or not np.isfinite(a).all() or np.any(a <= 0):
        raise ValueError('AHP matrix must be finite, positive, and square')
    if not np.allclose(np.diag(a), 1, atol=1e-10, rtol=0) or not np.allclose(a*a.T, 1, atol=1e-8, rtol=0):
        raise ValueError('AHP matrix must have unit diagonal and reciprocal entries')
    if n not in RI:
        raise ValueError('No configured random index for this matrix dimension')
    values, vectors = np.linalg.eig(a)
    k = int(np.argmax(values.real))
    lam = float(values[k].real)
    v = vectors[:, k].real
    if v.sum() < 0:
        v = -v
    if np.any(v <= 0):
        raise ValueError('Invalid positive principal eigenvector')
    w = v/v.sum()
    ci = max(0., (lam-n)/(n-1)) if n > 1 else 0.
    cr = ci/RI[n] if RI[n] else 0.
    if cr >= .10:
        raise ValueError('AHP consistency ratio must be below 0.10')
    return w, dict(lambda_max=lam, CI=ci, RI=RI[n], CR=cr,
                   provenance={k: document[k] for k in ('source', 'respondents', 'elicitation_date', 'judgment_method')})


def score_many(z, w):
    """Squared distances weighted by w (equivalently sqrt(w) coordinates)."""
    bad = np.sqrt(np.asarray(w) @ (np.asarray(z)**2).T)
    good = np.sqrt(np.asarray(w) @ ((1-np.asarray(z))**2).T)
    return 100*bad/(good+bad)


def rank_metrics(values, descending=True):
    """Average ranks and fractional top-k membership; ties split fairly."""
    x = np.atleast_2d(values)
    delta = x[:, None, :] - x[:, :, None]  # competitor - target
    ahead = np.sum(delta > TOL if descending else delta < -TOL, axis=2)
    tied = np.sum(np.abs(delta) <= TOL, axis=2)
    return (1+ahead+(tied-1)/2,
            np.clip((1-ahead)/tied, 0, 1),
            np.clip((3-ahead)/tied, 0, 1))


def interval_metrics(lower, upper):
    n = lower.shape[1]
    mask = np.eye(n, dtype=bool)[None, :, :]
    other_upper = np.max(np.where(mask, -np.inf, upper[:, None, :]), axis=2)
    other_lower = np.max(np.where(mask, -np.inf, lower[:, None, :]), axis=2)
    regret = np.maximum(0, other_upper-lower)
    possible = upper >= other_lower-TOL
    necessary = lower >= other_upper-TOL
    best = 1+np.sum((lower[:, None, :] > upper[:, :, None]+TOL) & ~mask, axis=2)
    worst = 1+np.sum((upper[:, None, :] > lower[:, :, None]+TOL) & ~mask, axis=2)
    return regret, possible, necessary, best, worst


def run(out, draws=10000, seed=20261108, ahp_path=None):
    if draws < 1:
        raise ValueError('draws must be positive')
    lo, hi, config = current_bounds()
    original_lo, original_hi = lo.copy(), hi.copy()
    old_w = weights(config['fixed_alpha'])
    old, _ = summarize(lo, hi, old_w)
    prior = pd.read_csv(ROOT/config['baseline_ranks'])
    verify_baseline(old, prior[prior.scenario == config['baseline_scenario']].reset_index(drop=True))
    prior_bounds = pd.read_csv(ROOT/config['baseline_bounds'])
    verify_bounds(lo, hi, prior_bounds[prior_bounds.scenario == config['baseline_scenario']].reset_index(drop=True))
    neutral_document = dict(source='Analyst-defined neutral symmetry reference; not empirical judgments',
        respondents='None: symmetry/null assumption only', elicitation_date='Not elicited',
        judgment_method='All criteria equally weighted as a reference, not student preference evidence',
        indicators=NAMES, matrix=np.ones((len(NAMES), len(NAMES))).tolist())
    neutral_w, neutral_ahp = ahp_weights(neutral_document, NAMES)
    neutral_ahp['status'] = 'neutral_symmetry_reference_not_empirical'
    neutral_ahp['matrix'] = neutral_document['matrix']
    neutral_ahp['weights'] = neutral_w.tolist()
    center, ahp = old_w.copy(), None
    if ahp_path:
        center, ahp = ahp_weights(json.loads(ahp_path.read_text()), NAMES)
        ahp['input_sha256'] = hashlib.sha256(ahp_path.read_bytes()).hexdigest()
    mid = (lo+hi)/2
    out.mkdir(parents=True, exist_ok=True)
    baseline_rows, baseline_stats = [], {}
    scenarios = {'inherited_policy': old_w, 'equal_indicator_reference': neutral_w}
    if ahp is not None:
        scenarios['elicited_ahp'] = center
    for name, w in scenarios.items():
        frame, decision = summarize(lo, hi, w)
        mids = score(mid, w)
        ranks, _, _ = rank_metrics(mids)
        frame['scenario'] = name
        frame['illustrative_midpoint_score'] = mids
        frame['illustrative_midpoint_rank'] = ranks[0]
        frame['previous_decision_rank'] = old.decision_rank
        frame['decision_rank_change_positive_improves'] = old.decision_rank-frame.decision_rank
        frame['midpoint_rank_minus_previous_decision_rank'] = ranks[0]-old.decision_rank
        baseline_rows.append(frame)
        baseline_stats[name] = dict(possible_champions=frame.loc[frame.possible_champion, 'city'].tolist(),
            necessary_champions=frame.loc[frame.necessary_champion, 'city'].tolist(),
            minimax_recommendation=[CITIES[i] for i in decision['minimax_choices']],
            kendall_decision_vs_previous=float(kendalltau(old.decision_rank, frame.decision_rank).statistic),
            kendall_midpoint_vs_previous_decision=float(kendalltau(old.decision_rank, ranks[0]).statistic),
            changed_decision_ranks=int((old.decision_rank != frame.decision_rank).sum()))
    pd.concat(baseline_rows, ignore_index=True).to_csv(out/'baseline_comparison.csv', index=False)
    bounds = pd.DataFrame([dict(city=c, indicator=n, lower=lo[i,j], upper=hi[i,j])
        for i,c in enumerate(CITIES) for j,n in enumerate(NAMES)])
    bounds.to_csv(out/'utility_bounds.csv', index=False)
    pd.DataFrame(dict(indicator=NAMES, inherited_weight=old_w, mc_center_weight=center,
        equal_reference_weight=1/len(NAMES))).to_csv(out/'weights.csv', index=False)
    rows, reports, weight_rows = [], {}, []
    mc_centers = {'inherited_policy': old_w, 'neutral_symmetry': neutral_w}
    if ahp is not None:
        mc_centers['elicited_ahp'] = center
    for center_name, concentration in [(name, k) for name in mc_centers for k in (20,100,500)]:
        active_center = mc_centers[center_name]
        rng = np.random.default_rng(np.random.SeedSequence([seed, concentration]))
        sampled = rng.dirichlet(concentration*active_center, size=draws)
        sl, su, sm = (score_many(z, sampled) for z in (lo, hi, mid))
        regret, possible, necessary, best, worst = interval_metrics(sl, su)
        mrank, first, top3 = rank_metrics(sm)
        rrank, recommended, _ = rank_metrics(regret, descending=False)
        mean_rank = mrank.mean(axis=0)
        aggregate_rank = rank_metrics(mean_rank, descending=False)[0][0]
        for i,c in enumerate(CITIES):
            rows.append(dict(center=center_name, concentration=concentration, city=c,
                midpoint_mean_rank=mean_rank[i], midpoint_mean_rank_order=aggregate_rank[i],
                midpoint_first_frequency=first[:,i].mean(), midpoint_top3_frequency=top3[:,i].mean(),
                possible_champion_weight_frequency=possible[:,i].mean(),
                necessary_champion_weight_frequency=necessary[:,i].mean(),
                minimax_recommendation_weight_frequency=recommended[:,i].mean(),
                minimax_mean_decision_rank=rrank[:,i].mean(),
                sampled_best_possible_rank=int(best[:,i].min()), sampled_worst_possible_rank=int(worst[:,i].max()),
                sampled_score_lower_min=float(sl[:,i].min()), sampled_score_upper_max=float(su[:,i].max()),
                previous_decision_rank=int(old.decision_rank.iloc[i])))
        for j,n in enumerate(NAMES):
            weight_rows.append(dict(center_name=center_name, concentration=concentration, indicator=n, center=active_center[j],
                theoretical_sd=np.sqrt(active_center[j]*(1-active_center[j])/(concentration+1)),
                sample_mean=sampled[:,j].mean(), sample_sd=sampled[:,j].std(ddof=0),
                sample_min=sampled[:,j].min(), sample_max=sampled[:,j].max()))
        counts = possible.sum(axis=1)
        reports[center_name+'_'+str(concentration)] = dict(draws=draws,
            observed_possible_champion_count_min=int(counts.min()),
            observed_possible_champion_count_max=int(counts.max()),
            observed_possible_champion_count_mean=float(counts.mean()),
            sampled_possible_champion_union=[c for i,c in enumerate(CITIES) if possible[:,i].any()],
            possible_at_every_sampled_weight=[c for i,c in enumerate(CITIES) if possible[:,i].all()],
            midpoint_mean_rank_leaders=[c for i,c in enumerate(CITIES) if aggregate_rank[i] == aggregate_rank.min()],
            kendall_midpoint_mean_rank_vs_previous_decision=float(kendalltau(mean_rank, old.decision_rank).statistic),
            kendall_midpoint_mean_rank_vs_center_midpoint=float(kendalltau(mean_rank, rank_metrics(score(mid, active_center))[0][0]).statistic),
            max_frequency_standard_error_bound=float(.5/np.sqrt(draws)),
            simplex_valid=bool(np.all(sampled > 0) and np.allclose(sampled.sum(axis=1), 1)),
            sampled_weights_sha256=hashlib.sha256(sampled.astype('<f8').tobytes()).hexdigest())
        assert np.allclose(first.sum(axis=1), 1) and np.allclose(top3.sum(axis=1), 3)
        assert np.allclose(recommended.sum(axis=1), 1)
        assert np.all(sl <= sm+TOL) and np.all(sm <= su+TOL)
    pd.DataFrame(rows).to_csv(out/'monte_carlo_city_summary.csv', index=False)
    pd.DataFrame(weight_rows).to_csv(out/'monte_carlo_weight_summary.csv', index=False)
    assert np.array_equal(lo, original_lo) and np.array_equal(hi, original_hi)
    result = dict(model_version='V112_weight_sensitivity', evidence_model=config['model_version'],
        ahp_status='elicited_matrix_supplied' if ahp else 'neutral_reference_only_no_elicited_judgments', ahp=ahp, neutral_ahp=neutral_ahp,
        mc_centers=list(mc_centers), seed=seed,
        random_generator='numpy.default_rng(SeedSequence([seed, concentration]))',
        numpy_version=np.__version__, concentrations=[20,100,500], draws_per_center_concentration=draws, total_draws=draws*3*len(mc_centers),
        uncertainty='Only weights sampled. Every original evidence interval is retained. Midpoints are illustrative completions.',
        frequency_interpretation='Conditional analyst-selected Dirichlet sensitivity frequencies, not observed student preferences or real winner probabilities.',
        weight_domain='Full positive simplex; this expands beyond the previous restricted auxiliary-weight family. Sample extrema/union are not continuous-domain certificates.',
        topsis_convention='Dplus=sqrt(sum(w*(1-u)^2)); Dminus=sqrt(sum(w*u^2)); score=100*Dminus/(Dplus+Dminus). Fixed ideal points 1 and 0; sqrt(w) coordinates, not squared weights.',
        all_250_cells_unchanged=True, unknown_cells=int(np.sum((lo == 0)&(hi == 1))),
        source_bounds_sha256=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest(),
        baseline_verified=True, baseline=baseline_stats, monte_carlo=reports,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (out/'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'results/task4_v112_ahp_mc')
    parser.add_argument('--draws', type=int, default=10000)
    parser.add_argument('--seed', type=int, default=20261108)
    parser.add_argument('--ahp-json', type=Path)
    args = parser.parse_args()
    run(args.output, args.draws, args.seed, args.ahp_json)
