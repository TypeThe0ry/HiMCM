# V95: Warsaw upper-secondary school flows, with suppressed cells retained as unknown

Official 2024–25 school-flow workbooks identify **1,502 Warsaw-resident upper-secondary pupils studying in another municipality**, and **27,956 nonresident pupils studying in Warsaw**. The totals make the residence/school-location distinction concrete; they supply no trip duration and do not narrow Warsaw's travel utility [0,1].

The [GUS publication](https://publikacje.new.stat.gov.pl/portal-publikacje/dojazdy-uczniow-do-szkol-podstawowych-i-ponadpodstawowych-w-roku-szkolnym-20242025) links three acquired originals: a PDF, tables and a flow workbook. They refer to school year 2024/25, September 30. The landing-page body instead repeats 2023/24 values; the downloaded originals govern this extraction. Warsaw's TERYT code is 1465011. Flows concern different residence and school municipalities, not observed diary trips.

| Upper-secondary direction | Official aggregate | Published OD cells | Published-cell sum | Unallocated aggregate residual |
|---|---:|---:|---:|---:|
| Warsaw residents leaving | 1,502 | 51 | 1,426 | 76 |
| Other residents entering Warsaw | 27,956 | 145 | 27,642 | 314 |

The workbook omits OD cells below 3 pupils. Residuals remain unallocated; omitted pairs are not zero and no suppressed pair count is reconstructed. `warsaw_published_flows.csv` preserves only published pairs and their direction. Primary-school flows are separately extracted as a cross-check.

## Interpretation and verification

These are youth-school administrative flows. No individual age, within-municipality student denominator, mode or duration is available. Distances or minutes cannot be invented from municipal pairs. Consequently this evidence cannot supply an average high-school commute, a share of all Warsaw high-school pupils commuting, or a city utility bound. It demonstrates why school-location education results cannot automatically describe resident students.

`audit.py` verifies original hashes and XLSX integrity, extracts tables by their actual sheet names, checks unique origin–destination pairs and the published-cell threshold, compares primary-plus-upper-secondary Warsaw totals with the separate official tables, and verifies national upper-secondary inbound/outbound aggregates both equal 754,290. The published matrix has 10,583 upper-secondary OD rows nationally. Original bytes, URLs and hashes are in `manifest.json`.

```sh
python3 research/2026-a/data/task4_v95_warsaw/collect.py
python3 research/2026-a/data/task4_v95_warsaw/audit.py
```

Separate WBR access checks found no usable original report/presentation: the 2015 PDF target returned zero bytes; the 2025 presentation returned HTTP 202 with zero bytes; the 2024 survey page returned HTTP 403 through the reader. These outcomes do not establish absence of suitable microdata. No contact request or access-control bypass was attempted.

Source attribution: **Źródło danych GUS. Opracowanie własne na podstawie danych GUS.** No model, ranking or manuscript was modified. [Summary](summary.json) · [access checks](access_checks.json) · [WBR2025 request](wbr_access.json).
