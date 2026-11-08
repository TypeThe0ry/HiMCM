# V119: conditional 2030 scenarios

Oslo remains the minimax-regret recommendation under all three 10% stress scenarios and both fixed and equal weights. All 16 cities remain possible champions; there is no necessary champion. These scenarios expose recommendation sensitivity, but do not add evidence or resolve missing observations.

| Single-city improvement: PTR, PM2.5 and mean commute duration reduced together | Fixed weights | Equal weights |
|---|---:|---:|
| Zurich | 24.55% | 23.73% |
| Singapore | 39.54% | Not reached within 50% |
| Dublin | Not reached within 50% | Not reached within 50% |

The values locate **ties** with Oslo in minimum maximum regret. A slightly larger reduction yields the competing city's strict minimax recommendation. All other cities and criteria stay at V118. These thresholds describe model response, not feasible policy targets, predicted improvements, or guaranteed quality leadership. Missing commute data remain fully unknown even in an improvement scenario.

## Scenario definitions

The 16-city V118 input is unchanged. The year 2030 labels a conditional future comparison; no 3–5-year panel or growth forecast is available. The 10% parameter is an analyst stress setting, with no probability or estimated trend attached.

- Resource expansion: HE, transport-stop and pool densities multiplied by 1.10, with the supplied population denominator held fixed.
- Living pressure: CLI, PIR and mean commute minutes multiplied by 1.10.
- Balanced improvement: PTR, PM2.5 and mean commute minutes multiplied by 0.90.

Other criteria, both existing weight vectors, anchors, and ideal utility points 0 and 1 remain fixed. The balanced scenario produces decision-rank Kendall tau-b 0.98333 under both weight vectors; the other scenarios preserve decision ranks (tau-b 1). These are rank-agreement statistics, not validation against future outcomes.

## Formulas

For a raw-value multiplier r>0 and existing utility u:

- Benefit utility `u=x/(a+x)` becomes `T_r(u)=r*u/(1-u+r*u)`.
- Cost utility `u=a/(a+x)` becomes `T_r(u)=u/(u+r*(1-u))`.

Both maps are increasing in u, so apply them separately to the lower and upper utility endpoints. Full missingness `[0,1]` remains `[0,1]`. A resource subset lower bound is scaled only under the stated proportional-expansion scenario; this does not imply observed new facilities.

Travel requires a separate rule. The script verifies all 16 V118 travel cells are either `[exp(-mean/30),1]` from a supplied mean or `[0,1]` from missingness. Scaling the mean by r gives `[lower^r,1]`. This is a Jensen bound on mean utility, not an assertion that utility equals the exponential of mean travel time. No empirical individual-duration distribution is invented.

The inherited TOPSIS score remains:

`S(u)=100*sqrt(sum_j w_j*u_j^2) / (sqrt(sum_j w_j*u_j^2)+sqrt(sum_j w_j*(1-u_j)^2))`.

It is increasing in each utility. Therefore city score bounds are `L_i=S(lower_i)`, `U_i=S(upper_i)`. Under the existing independent interval closure, possible champions satisfy `U_i >= max_{k!=i} L_k`; maximum regret is `R_i=max(0,max_{k!=i} U_k-L_i)`. Minimax choices minimize `R_i`. Their decision rank is distinct from a city's possible quality-rank interval.

For each candidate's single-city improvement, the script scans r=1 to 0.5 in 0.001 steps, then bisects the first sign change of `R_candidate(r)-min_{other} R_other(r)`. Candidate regret decreases and other-city regrets cannot decrease as its utility endpoints rise, so the gap is monotone. Numerical ties use tolerance 1e-10 score units; local signs 1e-6 on either side of each reported multiplier are verified. The decimal precision in machine output is numerical precision, not precision of real-world policy requirements.

## Reproduction and checks

Run `python3 scripts/task4_v119_future.py` from `research/2026-a`. Outputs are `ranks.csv`, `utility_bounds.csv`, `threshold_scan.csv`, `thresholds.csv`, and `summary.json`. The summary records input hashes, assumptions, both unchanged weight vectors, possible sets and threshold status.

Checks cover raw-input/admission hashes, identity and inverse transformations, untouched cells, valid endpoints, mean-only travel scope, monotone threshold gaps, and crossing signs. The generated baseline's city order, score endpoints, regrets, decision ranks and possible flags were also checked exactly against the saved V118 `after` results for both weights. No source CSV, main registry, or manuscript is changed.
