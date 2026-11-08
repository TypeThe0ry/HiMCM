# V93: Phoenix grade 11 results expanded to 100 schools

Fresh official NCES-ID checks add **38 schools and 112 FY2025 grade 11 subject records** to V92. Combined, the evidence covers **100 schools and 296 school–subject rows**. The newly recovered schools include alternative and charter schools and Sierra Linda High School. The main model remains unchanged: this collection measures published learning outcomes, whereas its existing education column measures teacher resources.

## Acquisition and identity

The existing official search inventory nominates 44 entity IDs: exact normalized names plus five explicitly listed name-change candidates. Names only nominate requests. The official [Arizona Report Cards](https://azreportcards.azed.gov/) `GetEntity` responses must match the complete 12-digit CCD NCES school ID. Forty candidates match previously uncovered roster schools; 38 have selected assessment rows. The two newly matched schools without selected rows are recorded, not replaced by zero scores.

The 84 archived entity/assessment JSON responses have SHA-256 hashes and source URLs in `manifest.json`. All requests succeeded. The independently fetched `GetEntityList?fiscalYear=2025` response contains 3,109 directory entries; it is separately hashed in `directory_source.json`. Both entity endpoints return FY2026 even when FY2025 is requested. This establishes current identifiers, not a historical address. The location frame remains the V42 2024–25 CCD roster inside the current Phoenix boundary.

Four candidates fail the exact uncovered-roster match: a different Genesis Academy; Desiderata with null NCES fields; South Phoenix 7–12 with a different LEA prefix; and Heritage Academy Pinnacle with a different school ID. Similar names or matching last five digits are insufficient. Their entity responses remain archived and no assessment row is admitted through these candidates.

## Coverage of the full roster

| CCD grade 11 category | Roster schools | Verified current identity | Schools with selected grade 11 results |
|---|---:|---:|---:|
| Positive enrollment | 111 | 99 | 99 |
| Zero enrollment | 31 | 9 | 0 |
| Negative source code | 2 | 2 | 1 |
| Total | 144 | 110 | 100 |

`roster_coverage.csv` lists every roster school, including the prior ASDB school whose identity remains unverified. Thus 12 positive-grade-11 schools remain unresolved. The 100 observed schools do not imply a complete city population: the roster also excludes private schools and resident-based catchments. CCD grade enrollment is used only to audit roster coverage, never as a tested-student denominator. Negative enrollment codes are not zero and do not prevent authentic grade 11 test records from being retained.

## Results and missing values

Rows require FY2025, subgroup `All`, grade `11`, assessment `type=1`, and `fayType=ALL ENROLLED`. The source's legacy assessment label is retained; no unverified ACT/AzSCI brand mapping is imposed. Age is not individually observed.

| Subject | Combined rows | Known test-record counts | Unknown-count rows | Published-percentage descriptor interval |
|---|---:|---:|---:|---:|
| ELA | 99 | 14,734 | 10 | 36.134–43.973 |
| Mathematics | 100 | 15,259 | 11 | 27.240–38.905 |
| Science | 97 | 14,315 | 11 | 16.167–34.441 |

For records K with known tested counts n, and their subset P with published percentages p (0–100 units), the descriptor is bounded by:

`L = sum(P: n*p) / sum(K: n)`

`U = L + 100 * sum(K minus P: n) / sum(K: n)`.

The larger collection exposes additional suppressed outcomes, so these descriptor intervals are wider than V92's smaller-subset intervals. They describe different covered subsets; this is not deterioration in student attainment or sampling precision. Counts with negative source codes remain unknown. Unknown-count rows cannot enter a fixed-denominator calculation. The descriptors are not reconstructed pass rates or confidence intervals: percentage rounding, cross-school duplication and citywide coverage remain unresolved. Subjects are not summed as distinct pupils, and no cross-city test calibration has been established.

## Reproduction

`collect.py` reuses cached byte-original responses, fetches absent files, regenerates candidate matches and extracted rows. `audit.py` works offline: it verifies response/dependency hashes, exact identifiers, raw-to-derived row equality, year/filter rules, disjointness from V92, uniqueness and full-roster coverage; it regenerates `summary.json` and `roster_coverage.csv`.

```sh
python3 research/2026-a/data/task4_v93_phoenix/collect.py
python3 research/2026-a/data/task4_v93_phoenix/audit.py
```

`remaining_roster.csv` is the 33-school candidate-acquisition remainder after V92's 71 nominated schools and the 40 new matches. Use the full `roster_coverage.csv` for verified coverage: it additionally counts V92's ASDB identity failure among the 34 unverified schools.
