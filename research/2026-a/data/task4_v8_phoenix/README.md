# Phoenix V8 local household travel evidence audit

Result: **0 new admissible observations**. Phoenix high-school commute utility remains **[0,1]**. This directory changes no model input. No regional adult mean, model-generated travel time, or school district statistic substitutes for a city high-school statistic. Education headcount remains missing; earlier FTE diagnostics are unchanged.

## New local lead: MAG 2017

Official [document directory](https://azmag.gov/Documents/113) links the [2017 MAG Household Travel Survey report](https://azmag.gov/LinkClick.aspx?fileticket=ZIAhg2viL5A%3D&mid=3809&portalid=0&tabid=527), December 2018 update. Web reader verified its 137 pages; direct original download returned HTTP 403. This is a manual source audit, not archived raw survey data.

Report executive summary and sections 2–3 describe 6,073 completed households, GPS for participants aged at least 16, and diaries including children aged 5–15. The expansion analysis uses 5,865 households. Section 3.3.2 aggregates geography into districts; their boundaries approximate municipalities, not exact Phoenix boundaries. The report therefore establishes a promising local survey, not an admissible Phoenix student estimate. Age alone does not establish high-school enrolment. Region-wide weights and mixed recruitment also need examination before estimating city/cohort uncertainty. No student trip records or city-specific duration distribution were acquired.

## Newer local survey

The official [2024 outreach report](https://azmag.gov/LinkClick.aspx?fileticket=_fwsA8dukWE%3D&mid=3809&portalid=0&tabid=527) confirms the regional survey began February 2024 and had over 3,108 household responses by June. Recruitment covered Maricopa, Pinal, and parts of Yavapai/Gila, including random-address invitations and social media. This verifies survey existence, not a released Phoenix high-school result. Direct PDF download returned 403; web-indexed report text was inspected. Search results for a 2023 MAG survey also include Mountainland, Utah; that source is rejected as the wrong agency and geography.

## Arizona add-on, separately from national NHTS

[NLR Arizona add-on landing page](https://www.nlr.gov/transportation/secure-transportation-data/tsdc-2017-nhts-arizona-add-on) reports 2,987 households, 6,081 participants and 19,779 trips. Its non-GPS download control did not yield a file in this audit; direct landing/dictionary requests returned 403. Exact Phoenix geography and grade classification remain unverified. Existence of cleansed data is not proof its public geography identifies the city. No spatial-data application, registration, email or information request was submitted.

## Reproducibility and admission

`manifest.json` records successful original bytes with SHA-256 and failed requests without creating counterfeit PDF/HTML files. Only the MAG open-data portal HTML was successfully archived; it is not survey microdata. `evidence_gaps.csv` records missing requirements and `observations.csv` intentionally contains only a header. Run `python3 audit_sources.py`.

Admission requires verified residence geography, school level (or an explicitly named age-only diagnostic), home-to-school direction and duration, person-day selection, survey weights, missing-response treatment, and adequate sample/uncertainty. A duration histogram with an explicit Phoenix high-school denominator could support the existing interval utility estimator. No denominator or compatible distribution is presently available, so neither a point estimate nor a narrower bound is justified. This is a bounded search result, not a claim that no public dataset exists anywhere.
