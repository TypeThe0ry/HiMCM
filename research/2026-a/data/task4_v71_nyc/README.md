# V71: New NYC source checks (2026-11-08)

**No new admissible high-school journey-duration observation was found in this bounded search.** Preserve the existing V20/V21/V26 NYC RHTS 2010–11 actual reported trip-chain evidence and its missing-data intervals. The historical NYU 2013–14 estimate is a modeled home-to-school route time, not an observed trip; it is not the current replacement target.

## New primary originals

URLs, retrieval date, byte counts and SHA-256 are in `manifest.json`.

- `nymtc_designation.pdf`: official NYSDOT Contract C004307 designation dated August 11, 2025, naming Westat as tentative prime consultant for a regional household travel survey and long-term data collection program. This is procurement evidence, not completed survey observations. Linked from https://www.nymtc.org/current-rfps .
- `student_survey2026.pdf`: official 2026 NYC student survey sample/proof form, seven pages and questions 1–61. Full instrument reviewed. Page 5, question 43 measures perceived safety traveling between home and school (four ordered safety responses); it does not measure elapsed journey time. No duration item was found in this instrument. A blank questionnaire provides no student counts or duration estimate.
- `survey_revisions2026.pdf`: official two-page explanation of the redesigned 2026 instrument. Page 2 explicitly requires a new baseline for 2025–26 and discourages comparisons with prior cycles for revised items. Favorability changes cannot automatically be interpreted as improvements in actual educational or travel conditions.
- `school_survey_catalogue.html`: official NYC Schools catalogue connecting the 2026 questionnaire, revisions and result files. No duration estimate is derived from this page.
- `ornl_nys_rural2024.pdf`: ORNL/SPR-2024/3216, July 2024, *Travel Patterns and Characteristics of Population in Rural Areas of New York State*. Printed page 3 describes the 2017 NYSDOT NHTS add-on; printed page 4, Table 1-1 explicitly defines NYC as Bronx, Kings, New York, Queens and Richmond counties for 2009/2017 analyses. This establishes a promising geographically correct analytical source, not public access to its detailed microdata or a high-school duration statistic. Its broad-population summaries are not substituted for high-school journeys.

The current NJTPA household-survey webpage states that an update to the 2010/11 RHTS is planned to start in 2026: https://njtpa.org/household-travel-survey/ . The web reader retrieved this statement, but direct raw download returned HTTP 403; the failed request is retained in the manifest and no local HTML is claimed. A plan is not a completed dataset. These checks do not establish that no newer dataset exists anywhere.

## Bounded 2017 NHTS follow-up

The public codebook already archived in `../task4_v7_phoenix/nhts2017_codebook.xlsx` was inspected, so it is not duplicated. Its `HH_CBSA=35620` identifies the New York–Newark–Jersey City NY–NJ–PA metropolitan area, not NYC's five counties. `SCHTYP` distinguishes public/private school from home schooling; it does **not** identify high-school enrollment. `R_AGE` and `TRVLCMIN` provide age and trip duration, but age is not a substitute for current high-school enrollment, nor is metro geography a substitute for the city. No public five-county add-on person/trip release resolving both issues was located in this bounded search. The ORNL report is therefore a follow-up lead; no city value or tighter interval is computed from it.

## Decision and verification

New accepted numeric model cells: **0**. No model, score, ranking, uncertainty interval or manuscript changed. No claim of champion-set reduction is supported by these sources. Run `python3 research/2026-a/data/task4_v71_nyc/audit.py` from the repository root (requires the existing `pdftotext` executable). The audit verifies archived bytes and selected source anchors; the no-duration conclusion additionally rests on the full manual instrument review. Page 5 was visually checked to confirm question 43 and its safety response categories.
