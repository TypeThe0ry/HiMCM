# A smaller complete certificate for the historical lower-tail gap

The retained Istanbul2012 fractional-mass uncertainty set needs **51 threshold evaluations per error budget**, rather than the1227 thresholds in the frozen V162 implementation. An endpoint argument removes all1176 pair-cost crossings from the minimisation. The seven existing results remain unchanged: in particular, the sharp gaps at0%,5%,20% editable observed mass are0.226685527,0.200134245,0.129090818. This is a simplification and independent check of the existing fairness calculation, not a new city-scoring model or a claim of algorithmic novelty.

## Endpoint certificate

Aggregate identical utilities first. Let the resulting distinct observed utilities be `q_i∈[0,1]`, positive group masses `w_i`, `W=Σw_i>0`, and tail fraction `0<α<1`. Keep the original unknown mass and optional-membership rules. The retained case permits all optional mass to be included, with total `N_max=W+U+B`. Editing at most `δW` observed mass, `0≤δ≤1`, has the fractional retained-mass polytope

`K_δ={k:0≤k_i≤w_i, Σk_i=(1−δ)W}`.

For a completed utility distribution of total mass `N`, its mean minus its lowest-α weighted mean equals the minimum over `z∈[0,1]` of `N⁻¹` times the sum of nonnegative contributions

`φ(q,z)=(q−z)+(z−q)_+/α`.

Every originally unknown or edited utility may be set to `z`, where its contribution is zero. Nonnegative costs permit the full edit budget to be used. The resulting minimum numerator is

`g_δ(z)=min_{k∈K_δ} Σk_i φ(q_i,z)`.

Between two consecutive observed utility values, each `φ(q_i,z)` is affine in `z`. The feasible set `K_δ` does not depend on `z`, so `g_δ` is the pointwise infimum of affine functions and is **concave on that interval**. Its minimum on the closed interval occurs at an endpoint. Applying this to every interval shows that the global minimum occurs in `{0,1,q_1,…,q_n}`. Pairwise cost-order changes can produce interior kinks or maxima, but no strictly lower interior minimum is needed. This is joint minimisation, with no exchange of a minimum and a maximum.

Originally unknown and optional mass contribute zero at the selected `z`. Since the remaining numerator is nonnegative and independent of optional mass, including all optional members minimises the ratio. Thus the sharp gap is `min_z g_δ(z)/N_max`. The retained allocation and common free utility construct an attaining completion. With49 distinct observed utilities, the stated certificate has51 endpoints.

The case `δ=0` recovers the joint missing-data result. At `δ=1`, no observed mass must be retained and a constant finite utility attains zero. More generally, zero becomes attainable at `δ=1−max_i(w_i)/W`, because retained positive mass must be concentrated at one utility for every contribution to vanish. Without pre-aggregated equal utilities, the formula is `1−max_v Σ_{i:q_i=v}w_i/W`. The retained data give the exact fraction recorded in `summary.json` (approximately0.784246425). This argument assumes `α<1`; if `α=1`, the gap is identically zero. The actual seven witnesses all select observed utilities with finite durations45,45,40,40,30,30,30minutes.

## Computation and verification

`task4_current_tail_endpoints.py` evaluates the51 endpoints with80-digit Decimal arithmetic and fractional mass budgets. At fixed `z`, it retains the lowest-cost mass, with a fractional boundary group. `endpoint_values.csv` records all357 objectives; `witnesses.csv` records343 observed-bin allocations; `summary.json` records seven minima and their completed means/tails. All source weights and original unknown/membership rules remain fixed.

A separate HiGHS mass-selection LP at each endpoint checks the sorting calculation. A lower-tail mass LP checks each newly generated witness, rather than assuming the chosen threshold is the witness's quantile. The bounded independent review separately ran357 endpoint LPs and7 frozen-witness tail LPs; it found a maximum357-objective difference of4.44×10⁻¹⁶ against the Decimal calculation. The portable audit records its own checks and numerical tolerances. Decimal arithmetic here is not a directed-rounding proof or a measurement-accuracy interval. The mathematical endpoint argument supplies the continuous-domain certificate; the finite numerical checks validate its implementation on the retained case.

Reproduce into a new external directory:

```bash
PYTHONDONTWRITEBYTECODE=1 /data/scratch/himcm-current-check-env/bin/python research/2026-a/scripts/task4_current_tail_endpoints.py --output-dir /data/scratch/himcm-tail-endpoints-new
```

The read-only audit defaults to stdout:

```bash
PYTHONDONTWRITEBYTECODE=1 /data/scratch/himcm-current-check-env/bin/python research/2026-a/scripts/audit_current_tail_endpoints.py
```

## Scientific and delivery scope

The evidence remains the saved official-portal projection of a2012 survey, not original CSV bytes. The proof concerns the retained conditional empirical set, with fixed cohort/weights and divisible observed mass. Edit budgets are declared stress parameters, not measured error rates or fractions of whole students. No source validation, sampling confidence, current-year population inference or actual facility access follows from this certificate.

Frozen V158/V162 results, current V203 bounds, weights,160indicator cells and manuscript/PDF remain unchanged. There is no MC or TeX replay, primary-data admission or actual primary score-width improvement. The51-versus1227 comparison counts thresholds; it is not an end-to-end runtime benchmark. The supporting proof can inform later specifically authorised manuscript revision.
