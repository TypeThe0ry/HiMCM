# NYC four-year diploma outcomes, classes 2024 and 2025

Official citywide data supplies both cohort denominators and diploma counts. Class 2024, measured in August, has 57,353 graduates among 68,882 cohort members. The listed outcome categories leave 34 members with unknown outcomes. Preserving them gives a diploma-outcome fraction of [0.8326268111, 0.8331204088]. Class 2025 has 58,660 graduates among 72,283 members and 49 unknown outcomes, giving [0.8115324488, 0.8122103399]. These intervals concern outcome missingness within the published cohort, not sampling confidence or uncertainty about all city residents.

The source is the NYC Public Schools [graduation results page](https://infohub.nyced.org/reports/academics/graduation-results) and its [citywide workbook](https://infohub.nyced.org/docs/default-source/default-document-library/2025-graduation-rates-public-citywide.xlsx). Original bytes and SHA256 checksums are retained. `extract.py` uses only the `All` sheet's `All Students` rows; it never adds demographic categories or school-level totals. The workbook explicitly says citywide totals include out-of-district placements and will not equal the school-level sum.

The cohort begins with first entry to grade 9. Graduates earn a Local or Regents diploma; June and August outcomes are distinct, with summer graduates included in August. Charter schools are excluded. NYC-paid private placements are part of the wider accountability cohort. Thus this measures the published NYC education-system cohort, not all resident high-school students, and it is not identical to a geographically selected Phoenix school union. Diploma requirements also differ by jurisdiction. Global admission remains false; any model use must retain these scope conditions.

For an August row, let N be total cohort, G diploma graduates and R=N minus the sum of listed outcome categories. Workbook NOTES row 17 explains that the deficit comes from unknown outcomes. Conditional on the published status classification, the bounds are G/N and (G+R)/N. The official administrative graduation rate is G/N. Known non-graduation categories comprise still enrolled, dropout, SACC and TASC/GED; do not count the latter credentials as a Local or Regents diploma.

`graduation_summary.json` contains `scopes["2024"]` and `scopes["2025"]`, each with `lower`, `upper`, `graduates`, `cohort`, `unknown_outcomes`, `reported_rate`, and `june_comparison`. Its `source_notes` locates the scope and missingness definitions in the workbook. `cohort_outcomes.csv` contains the four selected June/August rows. Checks validate all 48 unique `All` rows' reported ratios and diploma components, plus the selected June/August cohort equality.

Run with Python and openpyxl:

```sh
python3 research/2026-a/data/task4_v18_nyc_quality/extract.py
```
