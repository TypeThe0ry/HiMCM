# V124 acquisition limits on the current V121 evidence

Zurich education and the joint missing indicators of Madrid and Tokyo have the largest mathematical potential to reduce V121's possible-champion set. A different acquisition objective—changing the conservative recommendation—also makes a matched Dublin teacher denominator relevant. These are conditional limits for selecting evidence searches; they are not newly observed improvements or probabilities of obtaining useful data.

The input is the authoritative **V121 user16** factory. Its 21 fully missing cells are the only acquisition variables. All 139 other cells, including 27 partial intervals, remain unchanged. Baseline fixed/equal mean score widths are 16.18302472/19.08646888; both recommend Zurich and retain 16 possible champions.

## Joint missing-cell potential

| City | Currently fully missing indicators | Maximum exclusions: fixed | Maximum exclusions: equal |
|---|---|---:|---:|
| Zurich | Pupil–teacher resources | 5 | 1 |
| Madrid | Pupil–teacher resources; transport stops | 4 | 3 |
| Tokyo | Transport stops; travel; pools | 2 | 3 |
| Vienna | Transport stops; travel | 1 | 2 |
| Warsaw | Transport stops; travel | 1 | 1 |
| Dublin | Pupil–teacher resources | 1 | 0 |

These six maxima occur at the all-high utility endpoint. Utility 1 for a resource density is generally a limiting value rather than a finite observable density. The endpoints therefore establish optimistic ceilings, not attainable plans. Other combinations can exclude the focal city only when evidence is sufficiently unfavorable; full city/subset/single-cell results are in [joint_priority.csv](joint_priority.csv), [subset_limits.csv](subset_limits.csv) and [single_cell_priority.csv](single_cell_priority.csv).

The older `task4_v121_priority.py` used V120, with 26 fully missing cells. Its Dublin 8/6 and Stockholm 4/5 joint ceilings do not describe this experiment: Stockholm now has no fully missing cells, and Dublin's transport indicator is a retained partial interval. This scope does not assess further improvements to already partial inventories.

For fixed weights, Zurich's education lower utility must exceed approximately 0.67088480—PTR upper below approximately 7.35853317—to exclude the first city, Amsterdam. Dublin's education alone requires utility above approximately 0.97345477, or PTR below approximately 0.409036, for that exclusion. Thus a high endpoint ceiling can conceal an extreme evidence requirement.

Along the common-utility diagonal, the first other-city exclusion is Amsterdam when every selected lower utility strictly exceeds approximately 0.816725 for Madrid's two missing cells, 0.942743 for Tokyo's three, 0.937449 for Vienna's two, or 0.963181 for Warsaw's two. These joint conditions are sufficient, not necessary for unequal evidence combinations. Use the full precision in [exclusion_thresholds.csv](exclusion_thresholds.csv), not the displayed rounding. Equality retains a possible tie.

## Recommendation switches are a separate acquisition objective

An exact, correctly scoped pupil–teacher ratio can change minimax recommendations well before it excludes any possible champion. Holding all other V121 bounds fixed, these are the fixed-weight thresholds at which the focal city's regret ties the best competitor:

| Newly resolved PTR cell | Exact PTR threshold | Result for exact PTR strictly below threshold |
|---|---:|---|
| Dublin | 17.58238478 | Dublin is the strict minimax choice |
| Helsinki | 12.78853203 | Helsinki is the strict minimax choice |
| Paris | 10.44217186 | Paris is the strict minimax choice |
| Madrid | 8.43517454 | Madrid is the strict minimax choice |

For example, an explicitly hypothetical exact Dublin PTR of 15 changes the fixed-weight recommendation to Dublin; it is not an observed ratio. This distinguishes decision relevance from champion-set exclusions. [ptr_recommendation_thresholds.csv](ptr_recommendation_thresholds.csv) includes both weight references, all eight currently missing teacher-resource cells, root checks and the declared PTR=15 scenario.

The acquisition implication is to seek new, matched city/school-stage/provider teacher records where a result could cross a decision boundary. Dublin's previously rejected registration/allocation routes and Paris's collège-inclusive teacher total remain unsuitable. Madrid's combined teacher and city transport evidence, and Tokyo's school travel plus facility evidence, address joint uncertainty. The limits do not establish source availability or justify replacing pupils/FTE with an unmatched national or regional denominator.

## Zurich PTR: exact observations and intervals

Under fixed weights, the exact-cell switch is

`u*=0.078807617916563`, corresponding to `PTR*=175.336929303981` through `u=15/(15+PTR)`.

- Exact PTR below the threshold retains Zurich.
- Exact PTR above the threshold recommends Singapore.
- Equality gives the Zurich–Singapore tie.

This changes only Zurich's previously fully missing teacher-resource cell. It leaves the other 159 cells unchanged. Resolving a cell can reduce Zurich's upper score and thereby reduce competitors' regrets; observing it is not equivalent to merely improving Zurich's lower score. The observed interval `[PTR_lower,PTR_upper]` must therefore be propagated through **both** endpoints.

PTR upper strictly below the stated threshold is sufficient for a strict Zurich recommendation; PTR lower strictly above it is sufficient for Singapore. A straddling PTR interval needs the full two-bound calculation. The original `[0,1]` utility interval itself recommends Zurich, even though an exact utility near zero recommends Singapore. [zurich_ptr_interval_boundary.csv](zurich_ptr_interval_boundary.csv) gives five nondegenerate two-bound tie examples; [zurich_ptr_exact_grid.csv](zurich_ptr_exact_grid.csv) gives 201 exact utility resolutions per reference.

With equal weights, Zurich stays the strict minimax choice for every allowed exact PTR and every PTR interval. The proof uses the monotonic regret gap: Zurich's regret decreases as its utility lower endpoint increases, and every other city's regret is nondecreasing as Zurich's upper endpoint increases. The maximum gap occurs at the all-low exact resolution and is already negative. Piecewise-linear competitor checks identify Singapore as the best non-Zurich alternative under fixed weights, and Oslo under equal weights, throughout the allowable upper-score range.

As another declared scenario, exact Zurich PTR=15 retains Zurich and 16 possible champions under both references. Fixed-weight Zurich regret becomes 12.12788, compared with 17.36805 before resolution. This is a hypothetical information effect, not an empirical improvement.

## Reproduction and independent checks

```sh
python research/2026-a/scripts/task4_v124_priority.py
```

The script calls `task4_user_v121_revision.revised_bounds()` directly and reconciles baseline scores/regrets with the V121 `after_conditional` output. Joint and single-cell maxima follow the one-city endpoint argument: excluding the focal city cannot coincide with excluding another baseline-possible city; the all-low/all-high corners maximize those two possibilities respectively. Random interior probes test the bound without drawing or imputing measurements.

Independent vector norms and explicit self-excluded regrets check 3,571 acquisition evaluations, 996 Zurich PTR evaluations and 396 teacher-threshold evaluations. Roots are checked on both sides; the Zurich nonfocal competitor audit checks every piecewise-linear knot. [audit.json](audit.json) records the checks, and [summary.json](summary.json) records the fixed V121 sources, baseline, hypotheses and hashes. The source CSV, registry during execution, saved V121 ranks and all protected nonmissing bounds remain unchanged. No old priority results, model registry, raw input or manuscript file was edited.

## Read-only Madrid candidate check

A separate read-only review of the [Madrid candidate archive](../../data/task4_v124_madrid/observations.json) reproduced 293 unique source records, 242 municipality-28079 records, omission of two unnamed/no-line entries, and consolidation of 240 named records into 191 network complexes. There were 193 distinct names, no same-name/different-complex duplicates, and no exactly coincident coordinates across different complex codes. Noviciado/Plaza de España and Acacias/Embajadores are each conservatively counted as one linked complex. All selected records have past start dates and no recorded end date; these fields do not prove real-time opening status. This supports the declared 2026 registered-metro-inventory subset, with unchanged 2025 population, rather than an operational or all-provider census. The candidate is **not incorporated into this V121 priority baseline**. Admission and its controlled before/after comparison belong to a separate evidence revision; V122/V123 results remain frozen on V121.
