# V128: method sensitivity on the fixed V127 snapshot

V127's additional Prague and Vienna transport lower bounds change four fixed-weight and six equal-weight VIKOR ranks relative to V125's V124-input results. The method winners remain unchanged: midpoint TOPSIS selects Zurich, fixed-weight VIKOR accepts Dublin, and equal-weight VIKOR gives Oslo the smallest Q without satisfying either acceptance condition. These are illustrative midpoint comparisons, separate from the primary interval decision.

| Evidence / extension | Fixed TOPSIS–VIKOR tau-b | Equal TOPSIS–VIKOR tau-b |
|---|---:|---:|
| V121 control / frozen V122 | 0.483333 | 0.766667 |
| V124 / frozen V125 | 0.500000 | 0.750000 |
| V127 / current V128 | 0.500000 | 0.666667 |

The same fixed-weight tau does not mean that the rank vector is unchanged. Relative to V125, four fixed-weight VIKOR ranks change; equal weights change six. Midpoint TOPSIS ranks remain unchanged under both references. The primary interval ranks change for two fixed-weight cities and no equal-weight cities, consistent with the saved V127 primary output.

For current fixed weights, the first/second Q gap is 0.21320297, above `1/15`, and Dublin satisfies stability. With equal weights the gap is 0.03969924, below `1/15`, and Oslo is neither S-minimal nor R-minimal. Lowest Q alone is therefore not an accepted unique compromise under equal weights.

## Controlled evidence and method conventions

The main method CSVs contain V121 control and current V127 arms. Their criteria, weights, utility anchors and midpoint construction are identical. TOPSIS retains fixed 0/1 ideals; classic VIKOR uses sample best/worst utilities, total and maximum weighted shortfalls, and `v=0.5`. Midpoints are chosen utility scenarios, not measured replacements for missing values or the primary minimax rule.

The V121 control reproduces all earlier V122 score/rank columns. [v125_v128_rank_comparison.csv](v125_v128_rank_comparison.csv) separately compares actual frozen V125/V124 results with recomputed V128/V127 results. [summary.json](summary.json) retains `method_cases`, `controlled_V121_V127` and `controlled_V125_V128`, including rank-change counts, Q gaps, acceptance conditions and maximum score/Q changes.

V121→V127 contains four new lower bounds: Madrid transport, Tokyo pools, Prague transport and Vienna transport. The V125→V128 comparison isolates the latter two additions. It does not re-label previous V124 results as current calculations.

## Historical cases remain byte-frozen

The main 16 cities still represent 16 countries, so within-country pairs remain outside the primary ranking. Six case/coverage CSVs are copied byte-for-byte from the earlier V122 archive and independently regenerated to verify numeric equality:

- United States/India pairs use separate legacy 25-city V117 utility bounds and fixed weights.
- Shanghai retains its 2025 district school-resource aggregation and fractional bottom-20% pupil-mass example.
- Istanbul retains its 2012 broad-age marginal travel-utility bounds and shared unknown-age qualification.
- Singapore retains 2020 start-of-year secondary-enrolment ages, not current resident travel or measured preferences.

Original labels and source scopes are retained verbatim; none of these data enters V127's 16-city cells. The separate Vienna 2001 historical review is not introduced as a new primary observation or paper case by this migration. File hashes and original case summaries are in `frozen_case_sha256`, `country_pairs`, `equity` and `age_evidence`.

## Reproduce and audit

```sh
python research/2026-a/scripts/task4_v128_method_country.py
```

The fixed input receipt is `design/task4_user_v127_snapshot.json`, SHA256 `8f754bb3b666fdea8030bacf0551dea8a455bb0fc22df56c1860d4f4e747e45d`. The receipt and all nine referenced primary files are checked before and after execution. Independent vector norms, direct VIKOR shortfalls and acceptance-condition calculations verify all four method arms; current main ranks reconcile with V127. [audit.json](audit.json) records these checks and six-file byte/numeric preservation. Original CSV, registry, snapshot, primary outputs and old extension files remain unchanged. No manuscript file was edited.
