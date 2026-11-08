# Phoenix: retention-table city needs a physical-school crosswalk

The 2025 ADE retention appendix's school table labels Ridgeview College Preparatory High School as PHOENIX and reports 10 teachers (printed page61). The retained 2024–25 NCES record identifies the same school, NCES040100503720, at 1645 W Skyline Drive, San Tan Valley, Pinal County. Its coordinates also fall outside the current Phoenix boundary in the existing V42 audit. The school's own website, downloaded in this package, gives the same physical address.

This concrete mismatch means the appendix CITY field cannot automatically select Phoenix physical schools. The live NCES directory distinguishes a Phoenix mailing address from the San Tan Valley physical address, suggesting a mailing/administrative explanation for this row; no universal definition of the appendix's CITY field has been established. The main model remains unchanged.

## Evidence

- `crosscheck.json`: selected appendix row transcribed from the web-search returned table, with primary URL and printed page; **not an original PDF or a visually checked page**. Direct PDF retrieval returned403. The 10-teacher value is not admitted.
- [V42 archived NCES original](../task4_v42_phoenix_coverage/arizona_page_2.json): reference year2024–25; original bytes reused and SHA-256 checked rather than duplicated.
- `ridgeview_school.html`: original response from [the school's own website](https://www.ridgeviewcollegeprep.com/), fetched2026-11-08. `download.json` records its URL, bytes and hash.
- [NCES current school directory](https://nces.ed.gov/ccd/schoolsearch/school_detail.asp?ID=040100503720): distinguishes mailing and physical addresses; directory2025–26, membership/staff2024–25. It is a supplementary live lookup, not an archived original here.

For future TIA/retention extraction, join school identities to physical locations and preserve unmatched names. A school-name match alone does not settle teacher duplicate attribution, current grade assignments, FTE, or a complete city pupil denominator. The public workforce guide additionally distinguishes classroom teachers from other educator roles and reports cross-grade teachers in multiple-grade buckets; those definitions do not supply missing filtered counts.

`python3 research/2026-a/data/task4_v81_phoenix/verify.py` validates source integrity and the crosswalk fields. It does not prove the appendix's overall city-field semantics or original PDF authenticity. No new city indicator value or manuscript edit is included.

## Direct dashboard observation

[Visible dashboard transcription](dashboard_observation.json) records page 3, employed year 2025, Phoenix Union High School District, all positions and counties. The independent cohort total is 1,330; the high-school bucket shows 1,311 and multiple grades 25, with middle school and lower elementary one each. These displayed buckets total 1,338, so they cannot be added as a partition of independent teachers. The selected dropped-status count is 163, distinct from the cohort-total cards. This UI observation corroborates a real high-school classification but does not establish a citywide denominator, FTE or exclusive attribution. It is a manual transcription, not a downloaded microdata source.
