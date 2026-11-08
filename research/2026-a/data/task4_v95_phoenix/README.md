# V95: define the assessment programme without guessing API codes

The official 2024–25 accountability business rules establish that grade 11 uses ACT for ELA/mathematics and AzSCI for science. ACT ELA requires valid English, Reading and Writing components. These facts clarify the state's programme, but do not themselves establish a row-level crosswalk from the public API's legacy `AzMerit`/`type=1` labels. The 319 existing school–subject records retain their original fields and no model interval changes.

## What the source establishes

The [officially linked 2025 business rules](https://docs.google.com/document/d/1ynYRBE9l9Kddb2TImig3Vwl9pGItsFfCNl9ign35PnU/edit) are reused from V91's hashed text export. Relevant locations are lines491–493,802–844 and874–910. The rules distinguish the A–F accountability indicator from a percentage proficient: the former awards weighted performance-level points and uses FAY inclusion, RAEL exclusions and participation adjustments. They also allow a pupil who is FAY at multiple schools to contribute at each school. These accountability conditions cannot simply be imposed on the public `ALL ENROLLED` performance table or used to deduplicate its counts.

The [Arizona ACT cut-score document](https://www.azed.gov/sites/default/files/2022/07/ACT%20Cut%20Scores.pdf), read through the PDF reader, puts ELA and mathematics proficiency at19–24 and high proficiency at25–36. Its date is August2023, with July2022 board approval. These are Arizona accountability thresholds; no international calibration or exact API mapping is established. Original PDF bytes were not obtained.

The same-year business-rules table contains an ACT first-test date of April8,2024 among its2025 entries. This inconsistency is preserved, not silently corrected or used to reconcile the separate performance/participation denominators.

## What remains unresolved

The official current data page links FY2025 ELA/math and science workbooks, but no workbook bytes were obtained. Its linked generic data guide is FY2022, so it cannot identify each FY2025 negative API code or the rounding rule for ordinary integer percentages. The existing ALL ENROLLED definition from V53 and the observed unequal performance/participation counts remain controlling; no enrollment or participation denominator is substituted.

The newly archived current state-page HTML contains an extreme-percentage note nested under contradictory year conditions (outer fiscalYear≥2025, inner fiscalYear<2025). It is not evidence of an operative FY2025 display rule. None of the319 selected records has a published percentage0,1,99 or100, so this note does not alter their descriptors. Negative values remain unknown rather than inferred small counts or zeros.

## Reproduce and audit

`python3 research/2026-a/data/task4_v95_phoenix/audit.py` verifies original/dependency hashes, same-year rule anchors and the319 existing records' year, subgroup, grade and FAY filters. It writes [summary.json](summary.json). [source_checks.json](source_checks.json) distinguishes acquired HTML, reused official text, reader-only evidence and failed workbook acquisition. The current source is archived in `state_reports.html`; [manifest.json](manifest.json) records its original bytes. No original data, prior package, model, registry or manuscript was changed.
