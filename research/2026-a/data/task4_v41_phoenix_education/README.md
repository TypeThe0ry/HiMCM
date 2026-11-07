# Phoenix V41: actual matched school teacher counts

**New observed teacher data, but no citywide model admission.** The ADE report-card Teacher Qualification API was discovered in the already archived official client. It returns `teacherCount` separately from `teacherAndSchoolLeadersCount`; the client displays the former as total teachers. The distinction prevents principals and other leaders entering the denominator.

We requested FY2025 teacher responses for 34 previously matched schools that NCES2024–25 classifies as pure grades9–12, operating, nonvirtual and located within the current Phoenix boundary. Each candidate's ADE entity NCES identifier now exactly matches its CCD school ID. The entity endpoint returns FY2026 even when FY2025 is requested: identifiers are used for matching only, not for proving historical attributes. Teacher responses themselves return FY2025.

| Matched diagnostic | Value |
|---|---:|
| Candidate schools with exact official ID matches | 34 |
| Schools with one valid teacher response and matching CCD grade counts | 33 |
| Grade9–12 pupils in these same schools | 40,474 |
| ADE reported teacher counts | 1,961 |
| Pupils / reported teacher | 20.639470 |
| CCD FTE in exactly the same 33 schools | 1,999.17 |
| Pupils / CCD FTE | 20.245402 |

Phoenix Educator Preparatory returns an empty teacher list and remains missing. The 33-school ratio is not the V6 64-school ratio: comparisons must hold the school set fixed. `school_teacher_audit.csv` preserves both denominators per school.

## What this improves

The earlier FTE-only evidence now has independently reported, school-ID-matched teacher counts for a documented public-school subset. That is a real new observation, rather than another questionnaire or regional proxy. It does not establish that the ADE count equals our desired all-teacher headcount. In particular the same-set reported teacher count is below the CCD FTE total; individual discrepancies also exist. Snapshot dates, included teaching roles, charter reporting and shared staff require clarification before treating the difference as an FTE-to-headcount correction. The official [report-card explanation](https://azreportcards.azed.gov/state-reports) describes qualification data and charter certification differences but does not resolve this denominator alignment.

## Scope retained

These are schools at their current locations, not Phoenix-resident pupils. Unmatched public schools, missing responses, mixed-stage schools and private schools are not assigned values. Shared teachers or multi-enrolled pupils have not been deduplicated across schools. No coverage percentage or representative-city assumption is invented. The ratio remains a conditional matched-school-record diagnostic, not a city population ratio, and cannot justify narrowing the main missing interval.

Run `python3 research/2026-a/data/task4_v41_phoenix_education/collect.py`. It caches actual successful responses, checks returned teacher year/entity and official NCES identity, and preserves failed/missing cases. Validation completed: 34 unique IDs; 33 valid same-school pupil/teacher pairs; 68 response hashes verified. Input hashes are in `source_hashes.json`. No manuscript or model input changed.
