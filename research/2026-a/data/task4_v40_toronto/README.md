# Toronto V40 — school-level high-school achievement and scope audit

## Result

New official 2024–25 school records supply actual Grade 9 mathematics and first-attempt Grade 10 OSSLT results, with named school identifiers and municipal addresses. They improve the education evidence beyond a teacher-ratio proxy. **They do not yet supply a pupil-weighted city achievement rate or city pupil–teacher ratio.** Main-model cells remain missing unless the model explicitly adopts and harmonizes a school-level statistic across cities.

`catalogue.json` is the Ontario Ministry of Education's current resource metadata, identifying the release as **Preliminary 2024–2025**. The downloaded filename/sheet contains “final”; the catalogue's preliminary designation is retained here. The manifest stores URL, SHA-256 and retrieval date. No V38/V39 originals were downloaded again.

## Municipal school roster

`toronto_secondary_roster.csv` contains all 156 records with `Municipality = Toronto, City of` and `School Level = Secondary`; all report grade range9–12. Board counts:

| Board | School records |
|---|---:|
| Toronto DSB | 110 |
| Toronto CDSB | 38 |
| CS Viamonde | 4 |
| CS catholique MonAvenir | 3 |
| Independent Learning Centre/TVOntario | 1 |

The separate TVO record is excluded from the four-board quality summaries: a municipality address is insufficient to establish a local student catchment. Its identifier is992038. The raw roster retains it so the exclusion is reviewable.

This is a named municipal roster, improving on the earlier jurisdiction-only argument. It does not allocate the two French boards' teacher FTE to their seven Toronto schools. No school-level teacher count/FTE field exists in the workbook. School enrollment is rounded and is not examination cohort size.

## Actual secondary achievement evidence

For the155 four-board schools:

- Grade9 mathematics:108 reported school percentages;38 `NA`,7 `N/D`,2 `N/R`; reported-school median55.5%.
- First-attempt Grade10 OSSLT:109 reported school percentages;23 `NA`,9 `N/D`,14 `N/R`; reported-school median84%.

These medians describe **reporting schools with equal school weight**. They are neither student-level pass rates nor estimates for all schools. Missing/suppressed codes remain distinct, and no value is imputed. Different countries' examinations cannot be assumed equivalent. The exact school results are preserved in the CSV for later matched-cohort work.

## Adult day-school audit

`adult_day_scope_cells.csv` extracts five new comparison rows from the existing V38 financial original. Existing V39 `schedule13.txt` explicitly assigns21+ day-school ADE to the adult-day section; `staffing.txt` separately records adult-day/continuing staffing. However, these categories do not provide a student-to-teacher mapping:

| Board | Grade9–12 age21+ October pupil FTE | Adult-day total ADE | Adult/continuing/summer instructional FTE |
|---|---:|---:|---:|
| TDSB |128.31|83.35|51.2|
| TCDSB |1.8|0.9|5|
| Viamonde |2|2|0|
| MonAvenir |1|1|0|

Positive adult pupil enrollment with zero separately recorded adult instructional positions in the French boards shows why removing21+ pupils alone cannot establish a same-population teacher denominator. Possible shared teaching or reporting allocation is unresolved; zero reported staffing is not evidence that these pupils had no teachers. The age21+ distinction also does not isolate ages14–18.

Thus the V39 numerical envelope remains an explicitly conditional diagnostic, not an identified city bound. V40 does not issue another ratio.

## Reproduction and next evidence

Run `python3 extract.py` using the Python standard library. It extracts the XLSX via its XML tables, preserves school identifiers/percentages/missing codes, checks unique school identifiers, and extracts adult-scope financial cells. `summary.json` contains counts and reporting-school medians.

The public school workbook and board financial statement are insufficient for municipal teacher FTE or student-weighted achievement. A school-level staffing allocation and test-cohort denominators would resolve those issues. These two inspected public products do not contain them; this is not a claim that no other public source exists. No main-model ranking, possible-winner set, or manuscript has been changed.
