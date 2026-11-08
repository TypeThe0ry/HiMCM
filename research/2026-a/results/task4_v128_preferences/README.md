# V128: preference analysis on frozen V127 evidence

The V127 evidence recommends Zurich under baseline priorities, Oslo under education priorities, and Zurich under independent-living priorities. All sixteen cities remain possible champions in each deterministic profile; none is a necessary champion. The new Vienna and Prague transport lower bounds change rankings and conditional recommendation frequencies even though these three conservative choices remain the same.

The original ten criteria, anchors and weights are retained. Relative to V121, four utility lower bounds differ: Madrid transport, Tokyo pools, Vienna transport and Prague transport. Relative to V124 (the frozen V125 preference analysis), two lower bounds differ: Vienna and Prague transport. All upper bounds and the141 V124 cells already containing information are preserved. This migration adds no observations or changes to the primary model.

## Direct comparison with V125 using V124 evidence

| Analyst profile | Conservative choice | Decision ranks changed | Tau-b across evidence versions | Tau-b versus its own current baseline | Mean score-width before → after |
|---|---|---:|---:|---:|---:|
| Baseline | Zurich | 2 | 0.983333 | 1.000000 | 16.15002092 → 16.10728557 |
| Education priority | Oslo | 0 | 1.000000 | 0.716667 | 17.06299872 → 17.02422688 |
| Independent-living priority | Zurich | 2 | 0.983333 | 0.883333 | 22.21785283 → 22.15756818 |

Vienna moves12th→11th in the baseline and13th→12th under independent-living priorities; Warsaw moves down one place in each. Education-profile ranks are unchanged. Its tau-b against the baseline changes0.700000→0.716667 because the baseline ordering changes. The independent-living tau-b against its baseline stays0.883333. These within-evidence comparisons differ from the across-evidence tau-b column above.

## Same Monte Carlo samples, changed results

Each of three profiles uses10000 weight draws at each concentration20/100/500, resetting `default_rng(SeedSequence([20261108,k]))` per profile and concentration. No missing utility is sampled. Frequencies describe recommendations under this declared weight distribution, not actual winning probabilities or measured population preferences.

At concentration100:

| Profile | City | Recommendation frequency before → after | Mean decision rank before → after |
|---|---|---:|---:|
| Baseline | Zurich | 43.34% → 43.33% | 2.2305 → 2.2536 |
| Baseline | Oslo | 28.00% → 27.92% | 2.1071 → 2.1092 |
| Baseline | Singapore | 28.23% → 28.23% | 2.5770 → 2.6026 |
| Baseline | Prague | 0.02% → 0.11% | 5.1848 → 4.8062 |
| Education priority | Oslo | 45.62% → 42.95% | 1.7046 → 1.7646 |
| Education priority | Prague | 5.34% → 8.71% | 3.0658 → 2.8552 |
| Education priority | Singapore | 42.11% → 41.43% | 2.3242 → 2.3735 |
| Independent-living priority | Zurich | 58.99% → 58.99% | 1.6522 → 1.6641 |
| Independent-living priority | Prague | 0.00% → 0.00% | 6.2035 → 5.5307 |

At this concentration, baseline Oslo has mean decision rank2.1092 and top-three frequency99.47%; Zurich has2.2536 and81.79%. These sensitivity summaries optimize different quantities from the deterministic minimum-maximum-regret rule.

Across all concentrations,45/48 baseline,43/48 education and47/48 independent-living city-setting rows change in at least one saved MC metric. The largest recommendation-frequency changes are Prague gains of0.89 percentage points at concentration20 under baseline priorities,3.37 points at concentration100 under education priorities, and0.53 points at concentration20 under independent-living priorities. The largest absolute mean-rank changes in those profiles are0.3786 (Prague,k100),0.2566 (Vienna,k20) and0.6728 (Prague,k100). These paired differences use identical weight samples; they arise from changed evidence bounds.

## Preference definitions and verification

Education priority multiplies the pupil/teacher-resource and higher-education-density weights by2; independent-living priority multiplies travel and transport-stop weights by2. Each profile renormalizes all ten weights. The matrices remain `A_ij=w_i/w_j`, with CR0 checking algebraic consistency. These are analyst scenarios, not an AHP survey, expert elicitation or measured age preferences.

The new script reuses V125's `calculate()` and V122's profile and independent-decision functions. A freshly computed V121 control exactly reproduces frozen V122 ranks, weights, all144 MC rows,160 bounds, matrices and profile summaries. The actual V125 comparison reads frozen outputs, verifies their160 bounds against the V124 factory, then joins all48 city/profile rank pairs and144 city/profile/concentration/draw MC pairs one-to-one. Weights and scenario matrices are exactly unchanged across all three evidence versions.

Both computed arms receive independent weighted-norm, self-excluded-regret, possible/necessary-champion and per-draw tie-credit/rank/top-three checks:18 MC settings,10000 draws each. Three synthetic tie cases check fractional first-place and top-three credit. V127 baseline ranks and all three baseline MC settings exactly match the primary V127 saved results. The immutable V127 snapshot and all source hashes, original CSV, prior scripts/results and141 protected cells are checked before/after; all160 V127 bounds remain unchanged. `audit.json` records these checks.

`ranks.csv`, `weights.csv`, `mc_city_summary.csv`, `utility_bounds.csv`, `summary.json` and the scenario matrices retain the earlier output structure. `v125_rank_comparison.csv` and `v125_mc_comparison.csv` use `_v124` and `_v127` suffixes and signed new-minus-old changes. The separate `v122_*comparison.csv` files retain the older V121 control comparison. Frequencies are fractions in CSVs; multiply their changes by100 for percentage points. Negative mean-rank changes indicate better average ranks.

Run from the repository root:

```sh
.venv-v120/bin/python research/2026-a/scripts/task4_v128_preferences.py
```

This extension retains the primary evidence's mixed years, conditional inventory subsets and withdrawable historical school-stage travel proxy. It writes the new V128 result directory; it does not modify the CSV, registries, older results or Overleaf.
