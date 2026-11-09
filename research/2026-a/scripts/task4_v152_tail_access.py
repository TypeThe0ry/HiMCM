"""Historical within-cohort lower-tail utility bounds; no current-city admission."""
from pathlib import Path
import csv
import hashlib
import json
import math

R = Path(__file__).resolve().parents[1]
SOURCE = R / 'data/task4_v116_ibb/aggregate_results.json'
OUT = R / 'results/task4_v152_tail_access'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lower_tail(cells, alpha):
    """Fractional weighted lower tail, returning mean and boundary accounting."""
    total = sum(weight for utility, weight in cells)
    target = alpha * total
    remaining = target
    numerator = 0.0
    boundary = None
    for utility, weight in sorted(cells):
        used = min(weight, remaining)
        numerator += used * utility
        remaining -= used
        if remaining <= 1e-8:
            boundary = dict(utility=utility, selected_weight=used,
                            available_weight=weight, fraction=used / weight)
            break
    assert boundary is not None
    return dict(mean=numerator / target, target_weight=target, boundary=boundary)


def main():
    OUT.mkdir(exist_ok=True)
    source = json.loads(SOURCE.read_text())
    s = source['summary']
    cells = [(math.exp(-float(minutes) / 30), row['weight'])
             for minutes, row in source['duration_histogram'].items()]
    observed = sum(w for q, w in cells)
    numerator = sum(q * w for q, w in cells)
    assert observed == s['weight_observed']
    assert math.isclose(numerator, s['utility_known_numerator'], abs_tol=1e-8)
    unknown = s['weight_unknown']
    optional = source['optional_membership']['weight_total']
    denominator = s['weight_total'] + optional
    mean_lower = numerator / denominator
    mean_upper = (numerator + unknown + optional) / denominator
    rows = []
    for alpha in [.1, .2, .3]:
        low = lower_tail(cells + [(0.0, unknown + optional)], alpha)
        high = lower_tail(cells + [(1.0, unknown + optional)], alpha)
        observed_tail = lower_tail(cells, alpha)
        rows.append(dict(tail_fraction=alpha,
                         lower_closure=low['mean'], upper_closure=high['mean'],
                         observed_only_tail=observed_tail['mean'],
                         target_weight=high['target_weight'],
                         upper_boundary_minutes=-30 * math.log(high['boundary']['utility']),
                         upper_boundary_fraction=high['boundary']['fraction'],
                         certified_mean_minus_tail_lower=max(0, mean_lower - high['mean'])))
    with (OUT / 'tail_bounds.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    result = dict(iteration='V152', city='Istanbul', year=2012,
                  population='Recovered conditional current-high-school cohort ages 14–18, with optional membership retained',
                  provider_representation=source['provider'],
                  utility='exp(-minutes/30)', person_weight='kisi_agirlik',
                  known_members=s['n'], observed_members=s['n_observed'],
                  observed_weight=observed, known_unknown_weight=unknown,
                  optional_weight=optional, maximum_denominator_weight=denominator,
                  mean_utility_closure=[mean_lower, mean_upper],
                  lower_tail_rows=rows,
                  endpoint_rule='All unknown utility at 0 or 1 and all optional mass included. Bounds are closure endpoints of the retained aggregate set, not necessarily finite positive trips.',
                  proof='Lower-tail mean is nondecreasing in every utility. Adding a point at 0 cannot increase it; adding a point at 1 cannot decrease it. Thus optional inclusion and unknown endpoint assignment give global lower/upper bounds. Fractional boundary weight is retained.',
                  gap_rule='mean lower minus tail upper is a conservative lower bound on mean-minus-tail in every completion; no joint sharpness claim.',
                  strict_2025_tail_bounds=[0, 1], sampling_confidence_interval=None,
                  primary_data_admissions=0, primary_score_interval_width_reduction=0,
                  source_sha256={str(SOURCE.relative_to(R)): sha(SOURCE)},
                  generator_sha256=sha(Path(__file__)),
                  tail_csv_sha256=sha(OUT / 'tail_bounds.csv'))
    (OUT / 'summary.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
