# V94: same-year NCES identifiers resolve the remaining 12 schools

The official **2024–25 NCES directory** resolves all 12 previously unmatched schools with positive grade 11 enrollment. Eight supply 23 FY2025 grade 11 subject records, including three ASDB records previously quarantined. Combined with V92–V93, the collection now covers **108 schools and 319 school–subject records**. Among the 111 positive-grade-11 schools in the existing Phoenix roster, all 111 have an identified entity and 107 have selected results; four identified career-and-technical schools return empty assessment responses.

This is an evidence-linkage improvement. No city indicator enters the model: published examination outcomes still differ from its teacher-resource indicator, and citywide tested populations and comparable international examination scales are unresolved.

## Same-year bridge and source

The [official NCES download catalog](https://nces.ed.gov/ccd/files.asp) supplies the [2024–25 Directory ZIP](https://nces.ed.gov/ccd/Data/zip/ccd_sch_029_2425_w_1a_073025.zip). Its CSV contains 102,178 unique school records. The catalog labels the overall collection v.2a, while this Directory component is named `1a_073025`; both source labels are preserved. The original ZIP, catalog API response, controller script and every acquired endpoint response are byte-original and SHA-256 indexed in `manifest.json`.

For an exact NCES school ID, the directory records `ST_SCHID=AZ-{LEA entity}-{school entity}`. Its school-entity component is joined to the assessment response's `educationOrganizationId`, requiring FY2025. All 100 previously covered schools independently agree with this same-year mapping; there are no control mismatches. Names only helped locate candidate requests and do not determine the final join.

| School | NCES ID | Verified 2024–25 state school ID | Selected grade 11 subject rows |
|---|---|---|---:|
| Midtown High School | 040039103074 | AZ-79907-80385 | 2 |
| Precision Academy | 040039402323 | AZ-79929-80006 | 3 |
| AMCS at Anthem dba Caurus Academy | 040041502414 | AZ-85749-85750 | 3 |
| ASDB – Phoenix Day School for the Deaf | 040046302884 | AZ-6393-6395 | 3 |
| West-MEC – Sandra Day O'Connor High School | 040061502519 | AZ-80923-87322 | 0 |
| West-MEC – Sierra Linda High School | 040061503372 | AZ-80923-92189 | 0 |
| Northeast Campus | 040061503528 | AZ-80923-93018 | 0 |
| West-MEC Gateway Community College | 040061503595 | AZ-80923-1000083 | 0 |
| Arizona Collegiate High School | 040082103226 | AZ-90536-90907 | 3 |
| ASU Preparatory Academy – South Phoenix High School | 040094603375 | AZ-346763-92248 | 3 |
| Desiderata Program | 040633001429 | AZ-4286-6250 | 3 |
| Heritage Academy Pointe | 040974703852 | AZ-1002101-1002105 | 3 |

The historical directory resolves missing or changed current identifiers. In particular, Heritage's entity is **1002105**, not the earlier rejected name candidate 1002102. ASDB and Desiderata have null NCES fields in the current ADE response, but the official same-year directory supplies the complete identifier bridge. ASU's historical LEA differs from its current one; its FY2025 school record is linked through the historical state school ID, not the current LEA prefix.

Live NCES school pages now mix 2025–26 directory information with 2024–25 enrollment details; six requested pages returned generic search forms. These supplemental responses are retained as access evidence and are not used to establish historical identity. The ZIP is the historical authority.

## Results and unresolved scope

Selection retains subgroup `All`, grade `11`, assessment family `type=1`, and `fayType=ALL ENROLLED`, with FY2025 and the exact verified entity ID. Legacy assessment labels are unchanged; brand mapping and individual pupil age are not inferred. The new rows' displayed percentages are suppressed; negative codes remain unknown, never zero. ASDB's three rows match its previously quarantined records and are included exactly once in the combined collection.

| Subject | Combined school–subject rows | Known test-record counts | Unknown-count rows | Published-percentage descriptor interval |
|---|---:|---:|---:|---:|
| ELA | 107 | 14,854 | 12 | 35.842–44.426 |
| Mathematics | 108 | 15,401 | 13 | 26.989–39.468 |
| Science | 104 | 14,456 | 12 | 16.009–35.081 |

For records K with known tested counts n, and their subset P with published percentages p in 0–100 units, `L=sum(P:n*p)/sum(K:n)` and `U=L+100*sum(K minus P:n)/sum(K:n)`. Unknown-count rows remain outside this fixed-denominator descriptor. Published percentages have unverified rounding; these are neither reconstructed pass rates nor confidence intervals. Expanding coverage adds unknown outcomes and widens descriptors relative to V93; the covered school sets differ, so this is not a time trend or a same-population precision comparison.

The four empty assessment responses correspond to schools classified by NCES as `Career and Technical School`; current ADE responses also mark them `isJTED=true` and `CTED`. Their empty responses establish no tested-score observation, not zero proficiency. Whether their pupils also appear at primary high schools has not been resolved. School counts and subject counts must not be summed as unique pupils. The roster does not cover all private schools or resident catchments, and full citywide outcome coverage is not claimed.

## Files and verification

- `identity_bridge.csv`: all 12 exact historical mappings, current-identity comparison and assessment availability.
- `directory_target_extract.csv`: complete original CSV rows for those schools.
- `grade11_observations.csv`: 23 selected new/admitted subject records, with their linkage rule.
- `summary.json`: combined coverage and missing-value descriptors.
- `collect.py`: cached acquisition of explicitly listed official sources.
- `audit.py`: offline hashes, ZIP integrity, unique historical records, 100 known controls, all 12 joins, FY2025 filters, uniqueness, ASDB one-time readmission, and descriptor reconstruction.

```sh
python3 research/2026-a/data/task4_v94_phoenix/collect.py
python3 research/2026-a/data/task4_v94_phoenix/audit.py
```

All main-model missing intervals are preserved. No manuscript, model registry or ranking output is changed by this package.
