# Original 16-city CLI/PIR edition comparison

`comparison.csv` reports the 32 original CLI and Price To Income Ratio entries alongside the values and row ranks found in three archived Numbeo `t2` tables. All 96 city-indicator-edition cells are present. Matching uses the exact city and country text, with the single explicit country alias `Prague, Czechia` → `Prague, Czech Republic`. The extractor does not guess across cities. Exact matches list every matching edition because displayed values can repeat; a nonmatch does not establish that an input is wrong.

The 2026 source is Numbeo's annual 2026 edition, not a measurement spanning calendar year 2026. `current` is the Nov 7 archive and is not live current data. Input year and `ok` flags come directly from the original intake CSV; its CLI/PIR source URL, retrieval date, edition, table cells, extraction method, and boundary equivalence are undocumented. `summary.json` records these lineage limits, source hashes, and coverage/match counts. Blanks mean source values are unavailable; none are converted to zero.

The publisher labels CLI “Cost of Living Index” and describes its scale relative to New York City at 100, excluding rent/housing costs. PIR is publisher-defined using a 90 m² apartment and assumed family net disposable income equal to 1.5 times average net salary. These are publisher formula definitions, not evidence of student household costs or equivalent municipal boundaries. See archived definition pages `../current_oslo_cost_source/numbeo_cost_indices_explained.html` and `../current_oslo_cost_source/numbeo_property_indicators_explained.html`.

## Reproduce

From the repository root, run `python research/2026-a/data/current_all16_cost_editions/extract.py` to print CSV to stdout. Add `--write` to regenerate `comparison.csv` and `summary.json`. The script reads the original intake CSV and six existing archived HTML tables; it makes no network requests and does not copy or modify source files.
