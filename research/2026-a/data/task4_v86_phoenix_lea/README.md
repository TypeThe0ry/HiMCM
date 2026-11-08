# Phoenix 2023/24 LEA teacher coverage audit

The official CCD district staff file covers all **76 LEAs** associated with the **104 missing school-FTE records**, but **73 LEAs still report missing teacher totals**. Those 73 LEAs cover 82 missing schools and 15,506 explicit grade 9–12 pupils. No new physical-high-school FTE bound is admitted by this extraction.

| LEA | Teacher FTE | Known school FTE, all AZ | Missing target schools | Explicit target pupils |
| --- | ---: | ---: | ---: | ---: |
| West-MEC 0400615 | 63.16 | 63.16 | 17 | 122 |
| Maricopa Regional 0403860 | 4.00 | 4.00 | 2 | 0 |
| EVIT 0409731 | 111.56 | 111.56 | 3 | 0 |

The three numerical district totals exactly equal already-reported school FTE. Subtracting the school sum from the district total therefore gives zero. This arithmetic residual is **not an observed zero teacher count at missing schools**. Allocating teachers between central campuses, satellite programs, geography and grade groups requires a consistent assignment definition. Maricopa also reports 3.50 secondary and 0.50 elementary teacher FTE while its known Hope school row has FTE 4 and grade span 09–12, illustrating why district staff categories cannot simply replace school-stage assignments.

The conditional allocation inequality would be

`0 <= sum(missing target school teacher FTE) <= LEA teacher FTE - sum(known school FTE)`.

It requires an exhaustive, additive and mutually exclusive school allocation of the district total; this audit has not established that requirement. The archived zero residuals remain diagnostic values, not model caps. District totals cannot be assigned wholly to Phoenix or to high schools, and missing totals remain missing.

## Sources and reproduction

Original NCES [LEA staff ZIP](https://nces.ed.gov/ccd/Data/zip/ccd_lea_059_2324_l_1a_073124.zip) and [companion workbook](https://nces.ed.gov/ccd/xls/SY_2023-24_LEA_Staff_Companion_2024-252.xlsx) are retained byte-for-byte, with hashes in `manifest.json`. `official_catalogue.json` is the NCES catalogue response selecting nonfiscal district data for 2023/24. Despite the workbook publication identifier containing 2024, its subject year is 2023/24. No 2024/25 totals are used.

`arizona_staff.csv` contains all 14,222 Arizona category rows. `target_lea_staff.csv` preserves all staff categories and flags for the 76 target LEAs. `target_lea_audit.csv` joins their teacher totals to the V85 missing school roster and statewide school records; `summary.json` records counts. The `Teachers` total is marked `Derived` by NCES; individual teacher categories are `Reported` where present. Blank `STAFF_COUNT` with `DMS_FLAG=Missing` remains distinct from reported zero.

Run `python3 research/2026-a/data/task4_v86_phoenix_lea/extract.py` from the research repository root. Validation checks ZIP CRC, the common 2023/24 year and uniqueness of statewide school IDs; arithmetic uses decimal values. Existing V85 source files are inputs and are not changed. No paper files or model parameters are modified.
