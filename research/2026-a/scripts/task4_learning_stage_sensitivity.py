"""Conditional learning-outcome alternative; never rewrites the resource model.

Compare a common grade cutoff with internationally coded upper-secondary stage.
Sampling envelopes are approximate simultaneous intervals for ten proportions;
they do not cover nonresponse, school geography, or age-cohort transport bias.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import kendalltau, norm
from task4_current_model import current_bounds
from task4_v5_model import ROOT, CITIES, NAMES, weights, summarize
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify

DOMAINS = ('grade_ge10', 'isced3')
CITY_SET = {'Bogota', 'Singapore', 'Dubai', 'London', 'Jakarta'}


def learning_bounds(base, records, domain, z):
    lo, hi = (a.copy() for a in base)
    j = NAMES.index('upper_secondary_ptr')
    # Different construct: no resource values may leak into the learning column.
    lo[:, j], hi[:, j] = 0., 1.
    rows = records.loc[records.domain == domain]
    if set(rows.city) != CITY_SET or len(rows) != len(CITY_SET):
        raise ValueError('Expected exactly five identified city domains')
    for row in rows.itertuples():
        if not (np.isfinite([row.mean, row.standard_error]).all()
                and 0 <= row.mean <= 1 and row.standard_error > 0):
            raise ValueError('Invalid learning proportion or uncertainty')
        i = CITIES.index(row.city)
        lo[i, j] = max(0., row.mean - z * row.standard_error)
        hi[i, j] = min(1., row.mean + z * row.standard_error)
    other = np.arange(lo.shape[1]) != j
    for a, b in zip((lo, hi), base):
        np.testing.assert_array_equal(a[:, other], b[:, other])
    unknown = [i for i, c in enumerate(CITIES) if c not in CITY_SET]
    assert np.all(lo[unknown, j] == 0) and np.all(hi[unknown, j] == 1)
    return lo, hi


def main():
    source = ROOT/'data/task4_v87_pisa_cities/outcomes.csv'
    records = pd.read_csv(source)
    # Explicit conditional mapping: Greater London school domain to London candidate.
    records["city"] = records.city.replace({"Greater London": "London"})
    records = records.loc[(records.metric == 'math_level2_fraction') & records.domain.isin(DOMAINS)]
    if len(records) != 10:
        raise ValueError('Expected ten city-domain proportions')
    z = float(norm.ppf(1 - .05 / (2 * len(records))))
    lo, hi, config = current_bounds()
    base = (lo, hi)
    scenarios = [('resource_baseline', base)] + [(d, learning_bounds(base, records, d, z)) for d in DOMAINS]
    frames, reports, bounds, certificates = [], [], [], []
    grade_frame = None
    baseline_frame = None
    for label, (lower, upper) in scenarios:
        f, decision = summarize(lower, upper, weights(config['fixed_alpha']))
        f['scenario'] = label
        frames.append(f)
        cert = certify(lower, upper, *config['alpha_range'])
        for item in cert:
            item.update(scenario=label, city=None if item['winner'] is None else CITIES[item['winner']])
        certificates.extend(cert)
        continuous = [c for i, c in enumerate(CITIES) if feasible_preferences(
            upper[i], lower[np.arange(len(CITIES)) != i], *config['alpha_range'])['possible']]
        report = dict(scenario=label, possible_champions=int(f.possible_champion.sum()),
            continuous_possible_champions=continuous,
            minimax_choices=[CITIES[i] for i in decision['minimax_choices']],
            continuous_recommendation=sorted({c['city'] for c in cert if c['certified']}),
            unresolved_leaves=sum(not c['certified'] for c in cert))
        if label == 'resource_baseline':
            baseline_frame = f
        else:
            report['kendall_tau_vs_resource'] = float(kendalltau(f.decision_rank, baseline_frame.decision_rank).statistic)
            report['changed_ranks_vs_resource'] = int((f.decision_rank != baseline_frame.decision_rank).sum())
        if label == DOMAINS[0]:
            grade_frame = f
        elif label == DOMAINS[1]:
            report['kendall_tau_vs_grade'] = float(kendalltau(f.decision_rank, grade_frame.decision_rank).statistic)
            report['changed_ranks_vs_grade'] = int((f.decision_rank != grade_frame.decision_rank).sum())
        reports.append(report)
        for i, city in enumerate(CITIES):
            for j, criterion in enumerate(NAMES):
                bounds.append(dict(scenario=label, city=city,
                    indicator=('math_level2_fraction' if label != 'resource_baseline' and criterion == 'upper_secondary_ptr' else criterion),
                    lower=lower[i, j], upper=upper[i, j]))
    out = ROOT/'results/task4_v87_learning_stage'
    out.mkdir(parents=True, exist_ok=True)
    combined = pd.concat(frames)
    combined.to_csv(out/'ranks.csv', index=False)
    combined.pivot(index='city', columns='scenario', values='decision_rank').to_csv(out/'rank_comparison.csv')
    pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv', index=False)
    pd.DataFrame(certificates).to_csv(out/'recommendation_certificate.csv', index=False)
    records.assign(simultaneous_lower=np.maximum(0, records['mean'] - z*records.standard_error),
                   simultaneous_upper=np.minimum(1, records['mean'] + z*records.standard_error)).to_csv(out/'learning_intervals.csv', index=False)
    result = dict(main_admitted=False, baseline_model=config['model_version'],
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        source_manifest_sha256=hashlib.sha256((source.parent/'manifest.json').read_bytes()).hexdigest(),
        conditional_geography_mapping={'Greater London': 'London', 'Dubai emirate': 'Dubai', 'DKI Jakarta': 'Jakarta'},
        missing_learning_cities=sorted(set(CITIES)-CITY_SET),
        source=str(source.relative_to(ROOT)), family_size=len(records), normal_critical_value=z,
        interval_scope='Bonferroni normal approximation across ten city-domain proportions; sampling and plausible-value variance only. Missing city learning outcomes remain [0,1].',
        construct='PISA-age sampled pupils in geographically identified school domains; mathematics Level2 fraction, not all14-18 city residents or causal school quality.',
        scenarios=reports)
    (out/'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
