# Phoenix: comparable public-school coverage across two years

Applying the same V85 rules to archived official NCES2024–25 records reduces missing teacher-FTE rows from104 to29. Among158 school IDs eligible in both years,74 move from missing to reported FTE and one moves in the opposite direction. This improves observed public-school coverage, but does not complete the city denominator.

| Same-rule public-school measure | 2023–24 | 2024–25 |
| --- | ---: | ---: |
| Arizona source records | 2609 | 2628 |
| Schools inside fixed current Phoenix boundary | 533 | 534 |
| Operational, nonvirtual, possibly high-school records, including UG-only | 183 | 168 |
| Explicit high-school grade eligibility | 145 | 144 |
| Strict high-school-only records | 91 | 91 |
| Known grades9–12 pupils | 72562 | 70678 |
| Grades9–12 upper bound | 72562 | unknown |
| Reported ungraded pupils, allocation unknown | 106 | 81 |
| Missing teacher-FTE records | 104 | 29 |
| Missing teacher FTE among strict high-school records | 60 | 24 |
| Positive known teacher-FTE lower contributors | 31 | 66 |
| Conditional known strict teacher-FTE lower sum | 2185.00 | 2508.97 |

The2024–25 pupil upper bound remains unknown because Hope College and Career Readiness Academy, NCES040386003535, has suppressed grade and membership counts. V42's separate ADE1178 observation is not substituted without snapshot compatibility. Its4 FTE also does not enter this V85-compatible lower sum: the rule requires positive observed high-school enrolment. This explains the difference from V42's67-school2512.97 sum. No prior-year Hope enrolment is carried forward.

The broader roster retains24 UG-only records in2024–25, compared with38 in2023–24. The81/106 ungraded pupils remain possibly high-school pupils. Mixed-stage teacher FTE is not assigned wholesale to high school. Missing staff remains unknown, so neither year's total teacher upper bound is finite. V86's2023–24 LEA totals and zero arithmetic residuals are not used to fill2024–25 school rows.

The proposed control is **public-only, identical definitions and fixed boundary**, with year-specific source rows. It measures source coverage changes, not a measured improvement in education quality. Twenty-five eligible IDs occur only in2023–24 and ten only in2024–25; changes therefore cannot all be interpreted as changes at stable schools. Private PSS2023–24 data is excluded. The school-located population is not unique Phoenix-resident students, and school-assigned FTE additivity remains an explicit assumption.

`reused_sources.json` records original source URLs, byte counts and SHA256 for both years and the fixed boundary, without duplicating original files. The V42 current-layer responses are archived snapshots whose actual SURVYEAR is verified, not a claim that the live current layer remains unchanged. `extract.py` verifies IDs/page completeness, original bytes, years, geometry, grade rules and unresolved fields; it emits both rosters, missing-staff lists, matched-school comparison and `summary.json`.

Run `python3 research/2026-a/data/task4_v105_phoenix/extract.py`. No main-model observation, interval, ranking, or manuscript changes are included.
