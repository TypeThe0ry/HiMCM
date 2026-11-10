# Broadband statistic-definition sensitivity on user16 V203

All sixteen supplied broadband values have an exact numerical match in one archived Ookla snapshot: fifteen match named-city **fixed download medians**, while Singapore's 667.71 Mbps matches the **country fixed download mean**. Singapore's fixed median is 476.02 Mbps. City mean rows are unavailable for the other cities; national means are not substituted for them. This classifies publisher fields, not the original CSV extraction route or municipal geography.

A controlled alternative replaces only Singapore's broadband utility in temporary V203 arrays, using 476.02/(100+476.02) instead of 667.71/(100+667.71). All other 159 lower/upper cells, weights, anchors and fixed ideal points remain identical. The primary CSV and results remain unchanged.

| Weight reference | Retained Singapore score interval | Median alternative | Singapore decision rank | Conservative choice, both cases |
| --- | --- | --- | --- | --- |
| Fixed | 55.23172–63.53485 | 54.88014–63.22937 | 3 | Oslo |
| Equal | 54.38530–66.13833 | 54.06416–65.88253 | 3 | Zurich |

All sixteen decision ranks are unchanged under each weight set. Both scenarios still have sixteen possible and zero necessary champions. The median alternative increases mean score-interval width by 0.00288119 fixed-weight score points and 0.00408349 equal-weight points. A different point statistic changes nonlinear endpoint responses; harmonization is not automatically an uncertainty reduction. Actual primary admissions and primary width reduction are zero.

The source label is September 2026. Embedded records for all sixteen selected matches give month `2026-09`, `global_index_date` 2026-09-01, `aggregate_date` 2026-07-01 00:00:00 and `time_period_type` rolling_quarter. These raw field labels do not by themselves prove exact start/end dates, a calendar-year average, student access or city-proper boundary equivalence. Singapore is retained explicitly as a national city-state fallback and the original NATIONAL flag is preserved.

The source classifier uses regex extraction of HTML; the independent auditor decodes the embedded JSON, matching country codes and an explicit Zurich/Zürich alias. It checks all available four-field comparisons, 320 utility-bound rows and 64 city/scenario/weight cases, with separate scalar squared-distance and regret calculations. The audit protects the original 548 scientific bindings, 77 supplementary bindings, ten withdrawal entries, 24 edition entries, both seven-file paper copies and the current PDF. It does not replay Monte Carlo simulations or update the manuscript.

Files `bounds.csv`, `ranks.csv`, `summary.json` and `verification.json` contain the full comparison and source hashes. The generator intentionally writes this diagnostic; the auditor prints JSON by default and requires explicit output flags to save a report. This is a single-field source-definition check, not an additional ranking model, primary correction or general robustness claim.
