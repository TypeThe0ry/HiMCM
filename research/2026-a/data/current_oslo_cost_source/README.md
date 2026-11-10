# Oslo cost-of-living source check

The intake CSV records Oslo CLI 92.9 and PIR 9.8, both tagged year 2026 and `ok`. The archived Numbeo annual 2026 tables do not reproduce those values: the Cost of Living Index is 90.2 and Price To Income Ratio is 11.6. In the archived comparison, CLI is 92.1 in the 2026 Mid-Year edition and 93.0 in Current; PIR is 11.0 in 2026 Mid-Year and 9.8 in Current. Thus only PIR exactly matches a checked publisher value, and that match is to Current rather than the annual 2026 edition.

The publisher’s definition page says CLI uses New York City as 100 and excludes rent or mortgage housing costs. Its PIR documentation describes a formula based on a 90 m² apartment and assumed family net disposable income of 1.5 times average net salary. These definitions support the indicator names and scale, but do not establish the original CSV extraction path or geographic boundary equivalence. The CSV does not retain a source URL, edition, retrieval date, table cell, or extraction method. Its `2026` label and `ok` flag alone do not identify the Numbeo annual 2026 table.

## Evidence locations

- `cost-of-living_2026.html`: table `t2`, Oslo row at line 497; value 90.2.
- `property-investment_2026.html`: table `t2`, Oslo row at line 1886; Price To Income Ratio 11.6.
- The Mid-Year and Current copies provide the version comparisons listed above. Table column headings are in the same `t2` tables.
- `numbeo_cost_indices_explained.html`, lines 231–236: New York baseline and CLI excluding housing costs.
- `numbeo_property_indicators_explained.html`, lines 235–240: PIR definition and formula assumptions.
- `retrieval.json` records provenance. For the six archived table copies, original request status and exact retrieval time were not retained and are `null`; the access date is recorded separately from the archive provenance. The two explanation pages were fetched on 2026-11-10 and stored byte-for-byte.

The archived table HTML was copied byte-for-byte from `research/2026-a/data/city_matrix_25_audit/sources/`. The retrieval manifest includes sizes and SHA-256 hashes for all saved pages. No intake CSV, model, result, or manuscript was changed.
