# Point-utility uncertainty: unchanged primary V203

Widening all112 point-utility assumptions independently by±0.05 retains **Oslo under baseline weights and Zurich under equal weights**. This tests the minimax policy for expanded information sets. It does not assert the same recommendation for every exact perturbed dataset, identify a certain champion, or estimate how inaccurate the sources actually are.

## Controlled uncertainty sets

For each originally point-valued utility x, use `[max(0,x-epsilon),min(1,x+epsilon)]`. Leave all48 existing partial/fully unknown intervals unchanged. The160-cell original matrix, CSV, weights, anchors, source flags and primary scores are preserved. Epsilon is additive on the0–1 utility scale; it is not a percentage of the original physical measurement, a confidence level or an error distribution. In particular, the underlying means that induce partial travel intervals are not stressed here.

## Continuous-domain numerical checks

For each city, its lower score decreases and upper score increases as epsilon grows, so its self-excluded maximum regret is nondecreasing. Regrets at the two endpoints therefore enclose that city's regret throughout an epsilon interval. A city is certified on the interval when its padded upper regret is below every rival's padded lower regret. The algorithm bisects otherwise and preserves unresolved leaves; no monotonicity of regret differences is assumed.

The fixed-weight partition has755 leaves:729 positive-gap leaves and26 unresolved leaves. Oslo is certified from0 through0.08135732263326648, Zurich from0.08135734200477601 through0.2. The intervening band is unresolved; the result does not prove a unique crossing inside it. The equal-weight partition has52 positive-gap leaves and no unresolved part on[0,0.2], all recommending Zurich.

The independent audit recomputes all807 endpoint certificates using80-digit Decimal arithmetic, exact binary64 utility inputs and decimal policy weights. It also checks256 city/radius rank rows,2560 bound rows, both strict switch witnesses, complete contiguous coverage, original point masks and the48 unchanged intervals. The1e-9 padding is a numerical margin; this is not a directed-rounding interval-arithmetic proof or a validation of source error rates.

## Selected scenarios

|Utility radius|Fixed-weight recommendation|Equal-weight recommendation|
|---:|---|---|
|0|Oslo|Zurich|
|0.001|Oslo|Zurich|
|0.005|Oslo|Zurich|
|0.01|Oslo|Zurich|
|0.025|Oslo|Zurich|
|0.05|Oslo|Zurich|
|0.1|Zurich|Zurich|
|0.2|Zurich|Zurich|

`leaves.csv` gives the continuous partition, `ranks.csv` the selected scenarios, `bounds.csv` their complete utility ranges, and `switch_witnesses.csv` the two numerical choices outside the unresolved band. `summary.json` binds the calculation; `verification.json` records separate independent validation. All values in these files are declared stress scenarios, not new observations. Primary admission and actual primary interval-width change are both zero.

Run `.venv-v120/bin/python research/2026-a/scripts/task4_current_point_error.py`, then `.venv-v120/bin/python research/2026-a/scripts/audit_current_point_error.py`. The explicit16-city factory is used throughout; the legacy25-city stress entry is not used.

Independent audit commands print JSON to stdout by default. To intentionally update this directory’s verification report, add `--output research/2026-a/results/current_point_error/verification.json --overwrite`. This delivery option does not change the stress calculation.
