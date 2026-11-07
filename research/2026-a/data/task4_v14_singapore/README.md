# Singapore A-Level exam outcomes: official data, distinct outcome definition

`alevel_timeseries.json` is an official data.gov.sg API response containing130 records across1999–2024. The official metadata HTML and both hashes are archived in manifest.json. `extract_outcomes.py` checks hashes, response completeness, unique record IDs,26 overall-year records, and agreement of candidate numerators/denominators with published rounded percentages. It extracts only the overall series for current analysis; no ethnic composition weighting is introduced.

The SEAB2024 release reports10,889 candidates,10,255 meeting at least3 H2 passes plus GP or KI:94.2%. The SEAB2025 release reports10,977 candidates,10,393 meeting at least3 H2 passes plus GP:94.7%. Candidate counts are structured transcriptions of official web-reader content, not archived release HTML. Exact release URLs and dates are in candidate_outcomes_transcription.json.

These are examination-threshold outcomes, not entry-cohort four-year graduation rates. The certificate-award condition differs (at least one H1/H2 subject at gradeE). The2025 criterion no longer substitutes KI for GP and introduces revised UAS; the change in percentage cannot be treated as an unchanged-outcome trend. Current pre-university enrollment cannot supply the missing entering-cohort denominator or noncandidate outcomes.

The existing Singapore resource observation is a pre-university subset; A-Level outcomes describe related provision but do not complete all-program or city-resident coverage. Formal ISCED mapping was not independently retrieved. Do not replace missing broader upper-secondary outcomes with an age group, O-Level analogy or the A-Level candidate percentage. `main_admitted=false`; no PTR cell or cross-city graduation-rate input changes.

```sh
python3 research/2026-a/data/task4_v14_singapore/extract_outcomes.py
```
