# V126: acquisition value for V124's 19 fully missing cells

Dublin and Zurich teacher-resource data have the largest guaranteed decision-information value **if a source completely identifies the missing utility**. Actual source availability is a separate question: the existing teacher routes lack matching city/provider denominators, while official transport inventories and a historical Vienna school-travel table offer more concrete retrieval paths. This diagnosis keeps those two dimensions separate.

The input is the registry's **V124 user16** model: 112 point cells, 29 partial intervals and **19 fully missing cells**. All 141 nonfullymissing cells remain unchanged. The older `task4_v124_priority.py` used V121's 21 missing cells and must not be treated as this baseline. Both current weight references recommend Zurich, retain 16 possible champions and have no necessary champion.

## What the information quantities mean

Let `r0=min_i R_i` be the current minimax regret. For a declared exact resolution `x∈[0,1]` of one currently fully missing utility, keep every other cell fixed and recompute `r(x)=min_i R_i(x)`.

- Conditional guaranteed reduction: `r0−max_x r(x)`.
- Best possible reduction: `r0−min_x r(x)`.

These deterministic bounds use no prior or probabilities. They are measured in TOPSIS score points. “Guaranteed” conditions on obtaining the specified complete information; it does not promise that an available dataset can provide it. A partial stop inventory usually raises only a lower bound, a reported PTR may be an interval, and a travel-time mean gives a Jensen interval rather than an exact mean utility. Those sources cannot automatically claim the exact-resolution guarantee.

## Single-cell results

| Cell | Fixed guaranteed reduction | Fixed best possible reduction | Maximum champion exclusions, fixed/equal |
|---|---:|---:|---:|
| Dublin PTR | 1.066798 | 5.785906 | 1 / 0 |
| Zurich PTR | 0.793974 | 9.316221 | 5 / 1 |
| Helsinki PTR | 0 | 3.990631 | 0 / 0 |
| Madrid PTR | 0 | 3.522989 | 0 / 0 |
| Paris PTR | 0 | 3.418744 | 0 / 0 |
| Vienna travel | 0 | 1.713913 | 1 / 1 |
| Warsaw travel | 0 | 1.645388 | 1 / 0 |
| Prague transport | 0 | 1.219016 | 0 / 0 |
| Berlin transport | 0 | 0.345200 | 0 / 1 |

Under equal weights, Dublin PTR has conditional guaranteed/best reductions 0.044371/0.169330. All other single-cell guaranteed reductions are zero; Zurich's equal-weight best reduction is 8.524018. The full 38 cell/reference rows are in [priority.csv](priority.csv), and all 76 exact low/high endpoints, recommendations, score-width changes and regret reductions are in [endpoint_information.csv](endpoint_information.csv).

For example, fixed-weight current regret is 17.368046. Exact Zurich utility at the low endpoint selects Singapore with regret 16.574072; its high endpoint selects Zurich with regret 8.051825. Exact Dublin utility at the low endpoint retains Zurich with regret 16.301248; its high endpoint selects Dublin with regret 11.582140. These are hypothetical information limits. Utility endpoints may represent limiting raw values, so a best endpoint need not be a finite, physically attainable dataset result.

Zero reduction concerns this specific global minimax-regret objective. It does not imply that a cell has no scientific value: evidence can narrow a city's bounds, change its rank or reveal an adverse city outcome without improving the currently selected action's worst-case regret.

## Champion exclusions and joint acquisition

Zurich's first fixed-weight exclusion, Amsterdam, requires observed lower utility strictly above approximately 0.67088480, equivalent to a PTR upper bound below approximately 7.35853317. Dublin's corresponding utility threshold is approximately 0.97345477, equivalent to PTR below approximately 0.40903638. Recommendation relevance and champion-set exclusion therefore have different thresholds.

For complete same-city missing-cell combinations, the high-endpoint exclusion limits are:

| City / currently missing combination | Fixed | Equal |
|---|---:|---:|
| Zurich PTR | 5 | 1 |
| Vienna transport + travel | 1 | 2 |
| Warsaw transport + travel | 1 | 1 |
| Dublin PTR | 1 | 0 |
| Madrid PTR | 0 | 0 |
| Tokyo transport + travel | 0 | 0 |

Tokyo's two remaining cells can exclude Tokyo itself at unfavorable low endpoints; they no longer have the earlier three-cell high-endpoint ceiling because its pool cell is now a protected partial interval. Madrid's traffic inventory is also protected, so the earlier two-fullymissing-cell Madrid ceiling does not apply. The experiment does not assess improvements to the 29 existing partial intervals.

[joint_priority.csv](joint_priority.csv), [joint_subset_limits.csv](joint_subset_limits.csv) and [joint_endpoint_information.csv](joint_endpoint_information.csv) distinguish high-endpoint exclusions, low-endpoint adverse outcomes and conditional regret reductions. [exclusion_thresholds.csv](exclusion_thresholds.csv) gives all 16 single-cell exclusion thresholds. Strict comparisons use full CSV precision; equality retains a possible tie.

## Source routes with an explicit evidence gate

**High decision value, currently blocked teacher routes.** A useful source must match city schools, upper-secondary stage, provider coverage, pupil denominator and teacher FTE/headcount definition. The [V124 education audit](../../data/task4_v124_education/README.md) establishes why the known alternatives do not qualify: Dublin roll-level FTE is not publicly released and EDA82 has no city dimension; Zurich canton/public-school teacher totals do not match the all-provider city student population; Helsinki adult teaching hours and general personnel are not the required workforce. Paris's collège-inclusive total is also unsuitable. Revisit these cells when a genuinely new matched source or lawful aggregate becomes available, rather than repeating rejected requests or substituting regional totals.

**Prague transport: original operator material is available to inspect.** The [official DPP annual-report page](https://www.dpp.cz/spolecnost/o-spolecnosti/vyrocni-zpravy), checked 2026-11-09, lists 2025 Czech and English reports. A retrieval task should examine original files, establish a named city-boundary station subset and consolidate line appearances/platforms. An operator or regional total alone is insufficient. No count from that page enters this diagnosis.

**London transport: use current download products and stop hierarchy.** The [DfT NaPTAN download service](https://beta-naptan.dft.gov.uk/download) provides national or local-authority CSV/XML access-point data. Its unit is a public-transport access point, so interpreting a row count as city stops requires boundary and source-specific station/stop consolidation. [TfL's official open-data page](https://tfl.gov.uk/info-for/open-data-users/our-open-data) explicitly warns that example feeds are not updated and directs current feeds through its portal. These pages were checked 2026-11-09; no demonstration KML or unprocessed row total is admitted here. A successful lower inventory would improve completeness, although London transport alone has zero exact-resolution regret gain under both current references.

**Vienna school travel: an existing original can support a bounded historical extraction task.** The [archived route audit](../../data/task4_v124_transport/nonadmission_audit.json) locates Statistics Austria's Census2001 pupil/student report, Table10 from printed page118, with residence, school type and actual single-journey duration. The original review copy is already recorded locally; eligibility, denominators and duration bins still require extraction. A usable result would be an explicitly historical conditional proxy with withdrawal, not a 2025/26 observation. The report reserves online redistribution rights; do not put its original PDF in Git. Modeled nearest-school driving times and primary-school-only studies remain unsuitable substitutes.

Tokyo and Warsaw actual high-school travel still need matching resident/stage and one-way-duration evidence. Existing national/metropolitan totals, OD counts without durations and mixed work/university/school results remain rejected. A mean can support `exp(−mean/30)` as a lower bound; missing students, bins and open tails must retain the established rules.

## Reproduction and audit

```sh
python research/2026-a/scripts/task4_v126_priority.py
```

The script resolves the current V124 registry, checks the 19-cell set, and reconciles baseline scores/regrets with saved V124 results. It reuses the existing one-dimensional information optimizer and independently reconstructs its decreasing-focal/increasing-other regret envelope for all 38 cases. Independent vector norms, explicit self-excluded regrets and champion checks cover 2,741 conditioning evaluations, including endpoint and interior probes. Joint ceilings use the existing one-city endpoint argument.

[summary.json](summary.json) records the unchanged evidence and hypotheses; [audit.json](audit.json) records successful optimizer, score, champion, hash and bound checks. No Monte Carlo, new observation, source admission, registry change, CSV edit or manuscript modification occurs. The 141 protected cells and all 160 source bounds remain unchanged.
