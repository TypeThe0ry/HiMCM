# V92: Phoenix grade 11 learning-outcome evidence

Official FY2025 results now cover 62 exactly matched public schools, compared with the three-school V52 example. These are school test records, not a citywide resident estimate. `main_admitted` remains false: this learning-outcome measure cannot silently replace the model's teacher-resource indicator.

## Source and coverage

The collection contains 142 original JSON responses: entity and assessment records for 71 candidates. Candidates comprise the 64 V9 matches plus seven exact NCES-ID matches recovered against the V42 2024–25 CCD current-boundary roster. All three V52 schools remain included. Every response is SHA-256 indexed in `manifest.json`; prior roster and match inputs are hashed in `reused_sources.json`.

The official endpoints are [Arizona Report Cards](https://azreportcards.azed.gov/):

- `/api/Entity/GetEntity?id={entity_id}&fiscalYear=2025`
- `/api/DataApi/Assessment%20DetailsFAY?reportSection=Assessment+DetailsFAY&fiscalYear=2025&educationOrganizationId={entity_id}`

Although FY2025 was requested, entity records return FY2026. They verify current identifiers only; historical school location is not established. Assessment records return FY2025. Selection requires subgroup `All`, grade `11`, assessment family `type=1`, and `fayType=ALL ENROLLED`. The source label `AzMerit` is preserved. Its brand mapping has not been verified, so the collection is not relabeled ACT or AzSCI.

70 of 71 candidates have freshly verified NCES IDs. ASDB–Phoenix Day School for the Deaf (entity 6395) has null current NCES fields: its three result rows are archived but quarantined. Of the 70 matched schools, 62 report grade 11 results; the remaining eight have zero grade 11 enrollment in the source CCD roster. There are 187 selected raw rows and 184 verified school-subject rows. These candidates do not exhaust the V42 roster of 144 public secondary candidates and do not include private-school or resident-catchment coverage.

## What can be calculated

| Subject | Schools with rows | Known tested counts | Sum of known test-record counts | Rows with unknown tested count | Published-percentage descriptor range |
|---|---:|---:|---:|---:|---:|
| ELA | 62 | 56 | 12,832 | 6 | 39.786–41.477 |
| Mathematics | 62 | 56 | 13,239 | 6 | 30.525–34.521 |
| Science | 60 | 54 | 12,479 | 6 | 18.165–28.951 |

The last column describes only the subset with known tested counts. Let K denote those records, P the records in K with published percentages, n the reported tested count and p the published percentage in 0–100 units. Then:

`I_lower = sum(P: n*p) / sum(K: n)`

`I_upper = I_lower + 100 * sum(K minus P: n) / sum(K: n)`

Suppressed percentages retain their full 0–100 range. The corresponding unknown-rate weights are 217, 529 and 1,346 test records. Negative values (`-11`, and one Science percentage `-1`) remain privacy/missing codes, never zero scores. The six unknown-count rows per subject cannot be assigned an arbitrary denominator and are outside this fixed-denominator diagnostic.

This is a bounded descriptor of displayed percentages, not an exact underlying pass rate, inferred pass count, distinct-pupil count, confidence interval, whole-school-set bound, or Phoenix population estimate. Integer-percentage rounding is unverified. Subject counts are not added as unique students, and cross-school duplicate enrollment has not been resolved. V53's official frontend wording describes the performance denominator as enrolled and tested; CCD enrollment and the separate participation API are not substituted into it.

## What improves and what remains unresolved

V92 replaces a three-school illustration with 62 matched schools and exposes which records are missing or withheld. Fresh identity checks also prevent three unverified rows from entering the summary. This improves the breadth and auditability of actual high-school learning evidence. It does not establish citywide coverage, comparable cross-city examinations, or high-school commuting access; it supplies no evidence to narrow those model intervals or the possible-winner set. A ranking change caused solely by forcing this subset into the existing teacher-resource column would be unjustified.

## Files and reproduction

- `responses/`, `manifest.json`: original official responses and URL/hash index.
- `school_audit.csv`: all 71 candidate identities, source years and response coverage.
- `grade11_observations.csv`: all 187 selected rows, including explicit identity flags.
- `verified_grade11_observations.csv`: 184 identity-verified rows, preserving all special values.
- `summary.json`: counts, conditional descriptor bounds, exclusions and scope.
- `collect.py`: public endpoint collection, using cached original responses when present.
- `audit.py`: offline hash, entity, year, selection, uniqueness and row-reconstruction checks; regenerates verified observations and summary.

Run from any working directory with Python and pandas:

```sh
python3 research/2026-a/data/task4_v92_phoenix/audit.py
```

The command shown assumes the repository root. No manuscript or model ranking inputs are changed by this package.
