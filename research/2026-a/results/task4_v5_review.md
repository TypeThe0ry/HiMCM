# Independent V5 review

Reviewed `scripts/task4_v5_model.py` and the interval-decision helper on 2026-11-07. Review is independent of implementation; reviewer did not edit the main script.

## Result

No arithmetic defect found in the reviewed fixed-anchor TOPSIS score, monotone endpoint propagation, independent-box champion calculation, or one-cell perfect-information regret calculation. Current resource lower bounds are correctly admitted as `[u(observed), 1]`, not point observations. This conclusion is conditional on the declared separable box uncertainty model and source scopes; it is not external validation of educational outcomes.

## Focused checks executed

- Imported the actual V5 module: verified exactly eight weights 0.1125 and two weights 0.05, summing to one.
- Generated 25 × 10 ordered utility bounds and checked 100 sampled interior matrices against the score endpoints: all contained.
- Used the actual V5 nonlinear score inside `voi_1d`; compared its best/worst post-information regret with a 501-point grid: passed (worst endpoint/crossing result envelopes grid, best result matches).
- Inspected the helper: possible champion compares own upper bound with all other lower bounds; necessary champion compares own lower bound with all other upper bounds. Tied winners count as champions, as documented. Worst-case regret excludes the city itself and clamps at zero.
- Confirmed that NYC mean-time evidence retains a Jensen interval through the inherited travel file; Singapore retains subgroup envelope; Melbourne is overwritten with the same exploratory bootstrap interval in both comparison arms.
- Confirmed new evidence cannot shrink an interval in the wrong direction under the main nestedness assertion; this makes before/after a controlled evidence comparison within the same ten criteria.

After the core CSV arrived, executed production `build(False)`, `build()`, and `build(strict="strict_scope")`: all 250 utilities finite/ordered/in [0,1]; after nested inside before; travel identical between arms; Singapore university upper utility remained 1; Phoenix/Jakarta broadband remained [0,1]; strict scope expanded all PTR cells to [0,1]; admission audit included three travel records. All passed. Full output generation is owned and executed by the parent agent.

## Issues to address or disclose

1. **RESOLVED during review: added `no_education` and `strict_scope` sensitivity.** The original issue was: scope robustness was narrower than it may sound. `strict` currently controls air only. Tokyo prefecture/headcount, Singapore restricted pre-university strata, and Shanghai manual teacher-table transcription are all admitted as point utilities in every sensitivity arm. Add an education-exclusion/strict-scope sensitivity or explicitly state that education-scope uncertainty was not quantified. Resource headcounts are not observed educational achievement.
2. **RESOLVED during review: three inherited travel audit entries added.** The original issue was: travel provenance missing from admission export. `source_admission.csv` is assembled from new CSV rows; inherited travel and the Melbourne bootstrap replacement are absent. Add audit entries linking these rows to their original source/extraction and identifying the bootstrap as exploratory, not a design-based confidence interval. `utility_bounds.csv` alone does not explain where those bounds came from.
3. **Closed-envelope interpretation.** Missing utility `[0,1]` is a conservative closure; under saturating transforms a benefit utility of 1 may require an infinite raw quantity. Endpoint-only ties need this caveat. Independent boxes also ignore cross-city constraints and correlated missingness. These choices broaden possible champions and should not be presented as exact real-world probabilities.
4. **Perfect information is an acquisition ceiling.** VOI assumes learning an exact utility value for one city/criterion and no change to other cells. It is not expected benefit, cost-adjusted research priority, or the gain from a realistic noisy sample. The report should preserve this distinction, especially for Melbourne's finite-sample travel interval and a lower-bound university inventory.
5. **Before is a within-V5 evidence baseline.** It includes existing housing price/income and travel with the revised ten-criterion frame. It is not the historical V0/V1 or V4 ranking. Its large missingness must remain visible; rank changes measure minimax decision changes, not demonstrated changes in city performance.
6. **Publication-year heterogeneity.** Air observations span markedly different years; broadband is September 2026 rolling-quarter data; education is 2024. Recent-air sensitivity helps, but the conditional score is not a synchronized 2026 census.

## Suggested integration acceptance checks

After core CSV arrives, run the main pipeline once. Check all 250 cells are finite and satisfy `0 <= lower <= upper <= 1`, before/after city order is identical, after intervals nest within before, and every existing travel bound is unchanged between arms. Check Singapore's university density upper utility stays 1, missing broadband in Phoenix/Jakarta stays `[0,1]`, and status `missing*`/`scope_mismatch*` contributes no point value. Check a scope-exclusion arm re-expands PTR evidence rather than replacing it with zero. Confirm source audit now records all three travel observations. These are focused ingestion invariants, not requests for expensive Monte Carlo reruns.

## Final source-year verification

Singapore travel is **Census of Population 2020**, verified directly from the archived official dataset HTML title: `Resident Students Aged 5 Years and Over by Travelling Time to School, Level of Education Attending and Sex (Census of Population 2020)`. Dataset ID `d_e87b21cfebae1a77150eccded58ab116`. The 2020 label in the updated V5 audit is correct; it must not become 2024 or 2026 merely because pre-university PTR or download dates are newer. Secondary and post-secondary non-tertiary strata are not an exact 14–18 age slice.
