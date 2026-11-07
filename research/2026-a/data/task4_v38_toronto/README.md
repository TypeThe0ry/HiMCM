# Toronto: new 2024–25 secondary education evidence

Retrieved 2026-11-07 from Ontario Ministry of Education open data. Raw files are unchanged, with URLs and SHA-256 in `manifest.json`. Reproduce extraction using `python3 extract.py`. No citywide model cell is admitted by this package.

## New actual financial statements

`financial_2024_25.csv` is **2024–25 Financial Statements, board submitted**, not estimates/revised budget. It contains same-year school-board enrollment and October/March staffing. `four_boards_secondary_extract.csv` retains all relevant source fields and the four Toronto-serving boards; `key_cells.csv` is a small review table.

| Official field | TDSB | TCDSB | Viamonde | MonAvenir |
|---|---:|---:|---:|---:|
| Total secondary ADE including other pupils (`SC13_00164S`) | 73886.59 | 27595.87 | 2544.49 | 4217.76 |
| October grades 9–12 pupil FTE (`SC13_00140S`) | 73101.25 | 27205.73 | 2559.50 | 4229.27 |
| October total classroom instruction staff FTE, regular secondary (`AP0H_00667S`) | 4762 | 1609.8 | 207.2 | 315.6 |
| October total classroom instruction staff FTE, special education secondary (`AP0H_00670S`) | 146 | 211.3 | 17.8 | 55.5 |

ADE means average daily enrollment; it is not a headcount. The October grades 9–12 FTE cell is NOT all secondary pupils: separate source cells record high-credit pupils, those aged 21+, and visa/other pupils. Staff denominator also has regular/special-education categories plus library/guidance teachers. The extract preserves these distinctions. Do not divide the first available enrollment cell by a conveniently named teacher cell.

## Admission decision

**Retain as board-level evidence, city input missing.** This materially improves on the earlier TDSB-only evidence by providing all four public boards, a common year, and actual staffing. But Viamonde and MonAvenir cover territory outside Toronto; adding their entire totals to the two Toronto English boards is not a city aggregate. Private schools are not covered. A municipal crosswalk and a matching teacher-definition audit remain necessary. Staff FTE must also be harmonized with the model's existing teacher headcount/FTE convention.

A future *publicly funded schools only* analysis could explore coverage bounds: if English-board totals are wholly within Toronto and the two French-board totals contain all its French public schools, unknown city French allocations lie between zero and their full-board totals. Any resulting ratio bound would apply only to that declared public-sector estimand, with matched pupil/staff definitions. Those coverage assumptions and definitions have not been fully checked here; no such bound is admitted or used to narrow the possible-winner set.

## Separate grade enrollment table

`secondary_2024_25.txt` is the Ministry's board-level grade 9–12 enrollment file. Published values are in multiples of five and component sums can differ from the published total (e.g. TDSB component sum 74965, total 74960). Retain original published totals; do not treat rounding discrepancies as extraction errors. It cannot supply teacher counts or resolve French-board geography. No ratio combining this table with financial-statement staffing has been admitted.

Sources: [financial-reports catalogue](https://data.ontario.ca/dataset/school-board-financial-reports-estimates-revised-estimates-and-financial-statements), [education financial accountability](https://www.ontario.ca/page/financial-accountability-education-system). The full original resource URLs are in the manifest.
