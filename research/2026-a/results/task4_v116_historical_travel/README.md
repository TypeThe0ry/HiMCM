# V116: historical Istanbul high-school travel comparison

Using the recovered 2012 survey narrows Istanbul's score interval in an isolated historical scenario, but **does not reduce the 25-city possible-champion set**. The current V114 registry and its Istanbul travel interval `[0,1]` are unchanged.

| Fixed weights | V114 Istanbul decision rank | 2012 optional-membership rank | Score interval width, before → after | Kendall tau-b |
|---|---:|---:|---:|---:|
| Inherited `weights(.1)` | 7 | 4 | 20.2348 → 14.4610 | 0.9800 |
| Equal | 4 | 3 | 23.0984 → 18.3045 | 0.9933 |

Decision rank orders maximum regret, not identified city quality. Both weight references retain 25 possible champions. The improvement is reduced uncertainty about one city's historical student journeys; the remaining indicators still allow every city to be a champion.

Four scenarios are included: `current_v114`, `2012_known_cohort`, `2012_optional_membership`, and `withdrawal`. The known-cohort arm is diagnostic because it omits possible target members. The optional-membership arm includes 2,463 known members plus 15 possible members, retaining unknown utility `[0,1]`. It uses the independently verified historical interval `[0.31500258196933106, 0.5814034635501898]`. Withdrawal restores every baseline input and every city output exactly.

These are **2012 conditional empirical scenarios**, not replacement 2025 measurements or sampling confidence intervals. Only Istanbul's travel cell changes; all other 249 city-indicator cells, transformations and weights remain fixed. The inherited vector has 0.1125 on each of eight main indicators and 0.05 on each of the two facility indicators. The equal vector has 0.1 on every indicator.

`istanbul_age_groups.csv` reports actual age-group aggregates: observed-journey mean 29.44 minutes for ages 14–15 and 32.72 for ages 16–18, with missing observations retained in the utility bounds. Their optional-membership intervals overlap. Missing-age optional members enter each group's separate marginal bounds, but only once in the combined-city denominator. No age-specific preferences or rankings for the other cities are inferred.

Reproduce with `python3 scripts/task4_v116_historical_travel.py` from `research/2026-a`. The script verifies the aggregate duration histogram against independent membership controls, asserts all other cells unchanged, and verifies exact withdrawal. `ranks.csv` contains all cities' score bounds, possible/necessary champion flags, decision ranks and changes for both weight vectors. `utility_bounds.csv` contains the four input matrices; `summary.json` records champion sets, Kendall comparisons, fixed weights and input hashes.
