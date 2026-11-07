"""Approximate stratified-PSU Taylor inference for GHS bounded mean utilities.

All sampled PSUs in domain-relevant strata, including zero-domain PSUs, enter
variance estimation. Public calibrated weights are treated as fixed; no FPC,
replicate weights or calibration residual adjustment is available here.
"""
import json
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd
from scipy.stats import t

HERE = Path(__file__).resolve().parent


def endpoint_envelope(frame, domain, lo, hi):
    """Return point bounds and approximate joint 95% endpoint envelope.

    Arguments are frame-length aligned arrays; utilities must be finite on the
    domain and within [0,1]. Frame must retain the complete design of the geographic analysis scope,
    including strata with no sampled target members, not just domain records. Off-domain values may be missing.
    """
    domain = np.asarray(domain, dtype=bool)
    lo, hi = np.asarray(lo, dtype=float), np.asarray(hi, dtype=float)
    if any(len(a) != len(frame) for a in (domain, lo, hi)):
        raise ValueError('Domain and endpoints must align with frame')
    if not domain.any():
        raise ValueError('Empty target domain')
    if (not np.isfinite(lo[domain]).all() or not np.isfinite(hi[domain]).all()
            or (lo[domain] < 0).any() or (hi[domain] > 1).any()
            or (lo[domain] > hi[domain]).any()):
        raise ValueError('Invalid bounded utility endpoints')
    w = frame['person_wgt'].to_numpy(dtype=float)
    if not np.isfinite(w).all() or (w <= 0).any():
        raise ValueError('Weights must be finite and positive')
    relevant = np.ones(len(frame), dtype=bool)
    design = frame.loc[relevant, ['stratum', 'psu']].copy()
    counts = design.drop_duplicates().groupby('stratum').size()
    if (counts < 2).any():
        raise ValueError('Singleton stratum: explicit variance policy required')
    df = int(counts.sum() - len(counts))
    critical = float(t.ppf(0.9875, df))
    denominator = float(w[domain].sum())
    estimates, standard_errors = [], []
    for endpoint in (lo, hi):
        estimate = float(np.dot(w[domain], endpoint[domain]) / denominator)
        residual = np.zeros(len(frame))
        residual[domain] = w[domain] * (endpoint[domain] - estimate) / denominator
        design['residual'] = residual[np.asarray(relevant)]
        totals = design.groupby(['stratum', 'psu'])['residual'].sum()
        variance = 0.0
        for _, values in totals.groupby(level='stratum'):
            m = len(values)
            variance += m / (m - 1) * float(((values - values.mean()) ** 2).sum())
        estimates.append(estimate)
        standard_errors.append(float(np.sqrt(variance)))
    endpoint_intervals = [[max(0.0, est-critical*se), min(1.0, est+critical*se)]
                          for est, se in zip(estimates, standard_errors)]
    return {
        'n': int(domain.sum()), 'weighted_population': denominator,
        'point_bounds': estimates, 'endpoint_standard_errors': standard_errors,
        'endpoint_97_5_percent_intervals': endpoint_intervals,
        'joint_95_percent_approximate_envelope': [endpoint_intervals[0][0], endpoint_intervals[1][1]],
        'psus_all_relevant_strata': int(counts.sum()), 'strata': int(len(counts)),
        'domain_psus': int(frame.loc[domain, ['stratum', 'psu']].drop_duplicates().shape[0]),
        'degrees_of_freedom': df, 'critical_value': critical,
        'method': 'Stratified ultimate-cluster Taylor ratio linearization; Bonferroni two endpoint intervals',
        'finite_population_correction': None,
        'calibrated_weights_treated_as_fixed': True,
        'limitations': 'Approximate design-based sampling envelope, not an exact confidence set. Omits calibration estimation and FPC; conditional on recorded eligibility and survey coverage. Does not cover out-of-frame students or transportability to other years.'
    }


def main():
    with ZipFile(HERE / 'GHS2023.zip') as archive:
        with archive.open('GHS2023PERSON.csv') as source:
            frame = pd.read_csv(source)
    frame = frame.loc[frame.metro_code == 2].reset_index(drop=True)
    domain = ((frame.metro_code == 2) & (frame.edu_attend == 1)
              & (frame.edu_edui == 2) & (frame.edu_corr == 2)
              & frame.edu_grde.isin([10, 11, 12]))
    edges = {1: (0, 15), 2: (15, 30), 3: (30, 60), 4: (60, 90), 5: (90, np.inf)}
    lo = frame.edu_time.map({k: np.exp(-b/30) for k, (_, b) in edges.items()}).fillna(0)
    hi = frame.edu_time.map({k: np.exp(-a/30) for k, (a, _) in edges.items()}).fillna(1)
    summary = {name: endpoint_envelope(frame, mask, lo, hi) for name, mask in {
        'all_age': domain, 'age14_18': domain & frame.age.between(14, 18)
    }.items()}
    summary['utility'] = 'exp(-one_way_minutes/30); conservative closures [0,15], [15,30], [30,60], [60,90], [90,infinity); source labels 31-60 and 61-90 widened to avoid minute-rounding assumptions'
    summary['unknown_time_rule'] = 'Unknown times within confirmed domain receive utility bounds [0,1]'
    (HERE / 'inference_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
