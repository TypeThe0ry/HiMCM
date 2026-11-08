# V120 acquisition limits on unchanged V118 evidence

No single missing cell offers a strong realistic route to a much smaller possible-champion set. With the fixed weights, perfect knowledge of Singapore travel at its optimistic endpoint could reduce the set from 16 to 13. However, the required travel utility is extremely high. Equal weights permit at most one exclusion from any one-cell perfect resolution.

| Singapore lower travel utility exceeds | City excluded, fixed weights | Sufficient mean duration below, via Jensen |
|---:|---|---:|
| 0.871331 | Amsterdam | 4.132 minutes |
| 0.963079 | Vienna | 1.129 minutes |
| 0.977595 | Tokyo | 0.680 minutes |

These are feasibility limits within the model, not expected survey results or acquisition success probabilities. The mean-duration conditions are sufficient, not necessary, and apply only to the required student travel population. A new travel distribution may identify a different lower bound. Keeping the upper bound at 1 does not prevent these particular other-city exclusions if the required lower bound is established.

Low-utility perfect resolution could exclude the measured city itself. For Amsterdam PTR, the fixed-weight condition requires a certified PTR lower bound greater than 42.4073; under equal weights it would require greater than 1137.9045. The equal-weight Amsterdam transport condition requires a certified density upper bound below 0.6591 stops per 100,000. Partial facility lists only give lower bounds and cannot establish this exclusion. Vienna, Warsaw and Tokyo travel could also exclude themselves under sufficiently small upper utility bounds, but mean duration alone supplies only a Jensen lower bound and cannot establish those upper bounds.

The numerical priority therefore should be combined with source availability. Do not pursue Singapore on an expectation of three exclusions, or select evidence to hit a favorable threshold. Useful data can reduce uncertainty or change a decision even when the possible-champion count does not change. Multiple missing cells in one city may need joint resolution; this audit does not evaluate combinations.

## Method and reproduction

Run `python3 scripts/task4_v120_priority.py` from `research/2026-a`. The script reads V118 user16 bounds without changes, and evaluates all 48 non-point cells under both inherited fixed weights and equal weights. Each cell is hypothetically resolved to its current lower or upper endpoint, leaving all other 159 cells unchanged. Partial intervals are included alongside full missingness. This is perfect-information analysis, not newly collected evidence.

For score intervals `[L_i,U_i]`, a city remains possible when `U_i >= max_{k!=i} L_k`. A resolved utility changes only its city's endpoints monotonically. Since all 16 cities are initially possible, a focal city cannot be excluded while its lower score excludes any other city: if `U_i(x) < max_other L`, then `L_i(x) <= U_i(x) < max_other L <= every other U`. Other-city exclusions increase with x; focal exclusion decreases with x. Hence the best possible count over all one-cell resolutions occurs at one of the endpoints. Endpoint sufficiency is also checked on 21 interior probes per cell, and exclusion thresholds are solved by bisection. Ties remain possible, so the numerical thresholds require strict inequality.

`priority.csv` ranks optimistic exclusion potential, then strongest attainable lower score and baseline upper score; it is not a city quality ranking. `endpoint_limits.csv` lists every endpoint case and affected cities. `exclusion_thresholds.csv` gives both other-city lower-bound thresholds and focal-city upper-bound thresholds. `summary.json` records unchanged input hashes and scope. No scenario outcomes are inserted into the evidence registry, weights, or supplied CSV.
