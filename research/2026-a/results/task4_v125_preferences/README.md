# V125: migrate preference analysis to V124 without changing preferences

The V124 evidence still recommends **Zurich under baseline priorities, Oslo under education priority, and Zurich under independent-living priority**. All 16 cities remain possible champions in each deterministic profile, with no necessary champion. The three independent-living decision ranks that change show why migrating the evidence requires a fresh calculation even when the preferred city stays the same.

This extension changes the evidence input from V121 to V124. The only new utility information is Madrid's metro-inventory lower bound and Tokyo's five-venue swimming-inventory lower bound. The ten criteria, utility anchors, original CSV, three preference profiles and random streams remain fixed. The main registry and older outputs are not modified by this extension.

## Deterministic decisions

| Analyst priority profile | Conservative recommendation | Kendall tau-b versus current baseline | Mean score-interval width: V121 to V124 | Changed decision ranks across evidence |
|---|---|---:|---:|---:|
| Baseline | Zurich | 1.000000 | 16.18302472 to 16.15002092 | 0 |
| Education priority | Oslo | 0.700000 | 17.08782332 to 17.06299872 | 0 |
| Independent-living priority | Zurich | 0.883333 | 22.26139862 to 22.21785283 | 3 |

In the independent-living profile, Madrid moves from 10th to 8th, Helsinki from 8th to 9th, and Paris from 9th to 10th. Its Kendall tau-b across the old and new evidence is0.966667. The older profile's tau-b relative to its own baseline was0.916667; the new profile's corresponding value is0.883333. These are different comparisons and neither should be silently reused as the other.

`ranks.csv` preserves the V122 output schema, including decision ranks, score endpoints and illustrative midpoint columns. Midpoints do not replace the retained evidence ranges. `v122_rank_comparison.csv` gives all 48 old/new city-profile pairs. Narrowing a conditional score range is an information change, not an observed improvement in the city itself.

## Same declared AHP preferences

The baseline retains eight main weights of 0.1125 and auxiliary transport/pool weights of 0.05. Education priority multiplies the pupil/teacher-resource and higher-education-density weights by 2; independent-living priority multiplies travel and transport-stop weights by 2. Each profile then renormalizes all ten weights.

The exact-ratio matrices remain `A_ij=w_i/w_j`. The existing V122 `profile()` function constructs them and checks positivity, unit diagonal, reciprocity, principal-eigenvector recovery, rank 1, multiplicative transitivity and consistency ratio near0. This is algebraic consistency of analyst-designed priorities, not a student survey, expert elicitation, age-preference estimate or validation of representative opinions. The 3 matrices and all 30 weight rows are exactly unchanged from V122; see `weights.csv`, `scenario_matrices.json` and the three `*_matrix.csv` files.

## Monte Carlo: unchanged streams, measurable rank changes

For each profile, concentrations 20/100/500 use 10, 000 draws from `Dirichlet(k*profile_weights)`. Every profile/concentration resets `default_rng(SeedSequence([20261108,k]))`. Only weights are sampled; unknown utility values are not randomly filled. Tied recommendations share one slot, and tied top-three membership shares three slots.

At concentration 100, the Zurich/Oslo/Singapore recommendation frequencies happen to remain unchanged in all three profiles. Other summaries change even within that concentration:

| Profile | City | Recommendation frequency: old/new | Mean decision rank: old to new |
|---|---|---:|---:|
| Baseline | Zurich | 43.34% /43.34% | 2.2305 to 2.2305 |
| Baseline | Oslo | 28.00% /28.00% | 2.1062 to 2.1071 |
| Baseline | Singapore | 28.23% /28.23% | 2.5760 to 2.5770 |
| Baseline | Madrid | 0.00% /0.00% | 9.6782 to 9.1815 |
| Education | Oslo | 45.62% /45.62% | 1.7046 to 1.7046 |
| Education | Singapore | 42.11% /42.11% | 2.3242 to 2.3242 |
| Education | Madrid | 0.00% /0.00% | 12.2109 to 12.1116 |
| Independent living | Zurich | 58.99% /58.99% | 1.6522 to 1.6522 |
| Independent living | Madrid | 0.00% /0.00% | 8.8271 to 8.0204 |

Across all concentrations, 42 of 48 baseline city-setting rows, 37 of 48 education rows and41 of 48 independent-living rows change in at least one saved MC metric. At concentration 20, independent-living Madrid gains0.14 percentage points in recommendation frequency; the largest baseline-profile change is Madrid's0.04 percentage-point increase. Education-profile recommendation frequencies are unchanged at every concentration, while its mean ranks and other membership metrics can change. At concentration 500, independent-living Madrid's mean decision rank improves by 1.1408.

The current concentration 100 baseline gives Oslo mean decision rank 2.1071 and top-three frequency99.49%, compared with Zurich 2.2305 and82.69%. These sensitivity summaries answer different questions from the deterministic maximum-regret rule, which continues to recommend Zurich. All simulation frequencies depend on the declared weight distribution; they are neither real winning probabilities nor population preference shares.

`mc_city_summary.csv` contains all 144 current city-setting rows and changes against the current same-concentration baseline. `v122_mc_comparison.csv` pairs all 144 rows with their V121-evidence controls and reports signed new-minus-old changes. Recommendation and membership frequencies in the files are fractions; multiply by 100 for percentage-point changes. A negative mean-rank change is an improvement in average decision rank.

## Exact control and independent checks

The script calculates a V121 control before the V124 analysis, using the original V122 pure profile and independent-score functions. Reading frozen CSVs with round-trip float parsing permits exact, not rounded, comparisons. The control exactly matches the saved V122 ranks, all 30 weights, all 144 MC rows across 9 settings, all 160 utility bounds, scenario matrices and profile summaries. `control_v121_ranks.csv` and `control_v121_mc_city_summary.csv` retain that control explicitly.

For both evidence arms, independent weighted norms and explicit exclusion of each focal city reproduce scores, regret and possible/necessary champion flags. Per-city independent tie-credit calculations check every simulated recommendation, mean rank and top-three frequency across 18 settings. Three synthetic tied-regret cases additionally check first-place ties, complete ties and a tie crossing the top-three cutoff. The V124 baseline also exactly matches the saved main V124 ranks and all three baseline MC settings.

`audit.json` records the checks. `summary.json` preserves the original compatible profile/parameter fields and adds the controlled-evidence comparison and source hashes. Original CSV, registry, both evidence factories, V124 admissions and main outputs, the reused V122 code and every existing V122 preference output are hashed before calculation and checked unchanged afterward. All 160 current V124 bounds are exactly unchanged.

Run from the repository root:

```sh
python research/2026-a/scripts/task4_v125_preferences.py
```

The current evidence retains V124's mixed-year school-resource and facility-inventory conditions, including the historical Singapore school-stage travel proxy. This migration adds no new empirical source, future trend or age label. It writes only the new V125 script's result directory and does not update Overleaf.
