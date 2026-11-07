# Rival evidence can eliminate candidates: an acquisition diagnostic

The V17 diagnostic expands evidence planning to measurements of a competing city. V16 only asked how low exact outcomes for a candidate's own indicators could exclude it. V17 also asks how high exact outcomes for a rival could certify exclusion. Actual evidence is unchanged: all 25 cities remain possible champions, Singapore remains the minimax-regret choice, São Paulo ranks 6, Mexico City 20 and Phoenix 24. `current_ranks.csv` is recomputed from the V16 matrix.

## Computed potential, conditional on favorable outcomes

| At most this many exact measurements in one rival city | Maximum candidates excluded by that single rival across all allowed weights | Representative source city |
| --- | ---: | --- |
| 1 | 0 | No certificate |
| 2 | 1 | Singapore |
| 3 | 1 | Singapore |
| 4 | 2 | Singapore |
| 5 | 14 | Melbourne |
| 6 | 24 | Copenhagen |

These are optimistic information potentials, not forecasts or changes to the observed champion set. For two measurements, the representative Singapore bundle is research-university density and public-pool density, with Istanbul excluded. For four measurements, the example additionally uses public-transport density and school-travel utility, excluding Lagos and Istanbul. `budget_profiles.csv` gives each source city's exact-budget profile and the number of tied best bundles, with one representative bundle. `summary.json` maximizes over budgets up to the stated limit; ties across source cities are resolved by the existing city order, not a collection-cost ranking.

The candidate-specific result for Phoenix requires six measurements in a single rival to create this type of certificate, versus four measurements in Phoenix itself under V16's different best-case strategy. This does not establish a globally optimal plan. Multiple rivals can exclude a candidate at different weights, and combined candidate/rival measurements can be more efficient. These alternatives are outside this certificate class.

The large six-measurement potential is driven partly by unbounded missing resource indicators with utility upper bound 1. Such bounds may be closure limits rather than attainable finite observations; no claim is made that these endpoint outcomes will occur jointly. Strict inequalities also hold in a sufficiently small neighborhood of the endpoint, but real-world joint feasibility remains unverified. The calculation measures what the current uncertainty permits, not what the city can realistically achieve. No hypothetical endpoint is written into the observation files.

## Formula and exact continuous comparison

Let the current utility interval be [l_k,h_k]. For subset B of a source city k, define a hypothetical new lower vector v by setting v_j=h_kj for j in B, and v_j=l_kj otherwise. Its upper vector stays h_k. For every candidate i other than k, use

    A(u,alpha) = sum_j w_j(alpha) (1-u_j)^2
    B(u,alpha) = sum_j w_j(alpha) u_j^2
    S(u,alpha) = 100 sqrt(B)/(sqrt(A)+sqrt(B))
    G_ki(alpha) = B(v,alpha) A(h_i,alpha) - B(h_i,alpha) A(v,alpha).

The single-rival certificate holds when min over alpha in [.05,.2] of G_ki(alpha) > 1e-12. This proves S(v)>S(h_i) at every allowed weight and hence excludes i. The source city never counts as excluded by itself. Main-criterion weights are (1-alpha)/8 and auxiliary weights alpha/2.

G is quadratic because A and B are affine in alpha. Its minimum is evaluated at both boundaries and, for a convex quadratic, the stationary point when it lies inside the interval. This avoids a sampled weight grid. Every subset of uncertain indicators is enumerated. The minimum in `target_certificates.csv` is the minimum **within the single-rival certificate class**; it is not a necessary count for exclusion in the full model. Empty minima mean that this class supplies no certificate.

## Validation and data access

Three focused tests cover polynomial edge cases including exact ties, 120 randomized comparisons against the separate root-partition solver, all 365 displayed real-data exclusion witnesses, budget monotonicity, every smaller subset for reported target minima, and unchanged input matrices. The result summary records the complete input matrix SHA256.

Phoenix retrieval identified the official Arizona 2017 add-on and a restricted spatial-data access route. Current Phoenix-city high-school records were not obtained; its school-travel interval remains [0,1]. An official indexed reference to a 2025 MAG survey also leaves the relation to the previously found 2024 recruitment wave unresolved. See `../../data/task4_v17_phoenix/source_access_audit.json`.

Istanbul retrieval recovered exact official report URLs from archived catalogue metadata, but the official downloads still failed. An indexed report table describes last completed school, which cannot be used alone to identify currently enrolled high-school students. No observation was added. See `../../data/task4_v17_istanbul/source_audit.json`.

```sh
python3 research/2026-a/scripts/task4_rival_acquisition.py
python3 research/2026-a/scripts/test_task4_rival_acquisition.py
```
