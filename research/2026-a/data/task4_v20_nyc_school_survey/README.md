# NYC 2024 school-travel coverage audit

The official 2024 Citywide Mobility Survey (CMS) has a direct current-high-school field, but its weighted travel diaries cover adults. The public person file contains 365 current-high-school roster members; only 35 participants aged 18–24 have positive person weights and own trip records. All 286 high-school minors have zero person weights and no own diaries. Thus this newer release cannot replace the model's all-high-school school-travel input without a separate coverage model. No travel utility was admitted.

| Current high-school roster group | Persons | Positive person weights | People with own trip records |
| --- | ---: | ---: | ---: |
| Ages 5–15, nonparticipant | 113 | 0 | 0 |
| Ages 16–17, nonparticipant | 173 | 0 | 0 |
| Ages 18–24, nonparticipant | 44 | 0 | 0 |
| Ages 18–24, participant | 35 | 35 | 35 |

The 35 adult participants have 1,234 recorded trips of all purposes, not 1,234 school journeys. No school-trip mean is calculated here. The released adult-trip table also has household-companion flags; these do not by themselves identify each accompanying child's school destination or supply a representative child diary.

## Sources and direct variable definitions

The [NYC DOT CMS page](https://www.nyc.gov/html/dot/html/about/citywide-mobility-survey.shtml) identifies collection from May 6 to June 22, 2024. The official [Person 2024 dataset](https://data.cityofnewyork.us/Transportation/Citywide-Mobility-Survey-Person-2024/i2im-iqtt) and [Trip 2024 dataset](https://data.cityofnewyork.us/Transportation/Citywide-Mobility-Survey-Trip-2024/wgnh-qwsg) were released in 2026. Release year is not observation year.

The original attached dictionary `cms_dictionary_2024.xlsx`, sheet `Column Information`, defines:

- `school_type=7`: currently attending high school, public/private/charter. Questionnaire section 2.17 asks current school enrollment, distinct from highest completed education.
- `age=2/3/4`: 5–15 / 16–17 / 18–24.
- `is_participant=1`: active survey participant aged 18+.
- `person_weight_citywide`: expansion to adult city residents, not minors.

The original user guide, weighting section and reminders, confirms that person and trip weighted targets are adults and exclude child trips. The dated guide contains some reused survey-year wording; data-year identification follows the official catalogue and questionnaire. No minor weights are invented or borrowed from adult records.

Direct DOT questionnaire/guide PDF downloads returned HTTP403, but official NYC Open Data attached copies downloaded successfully. Original PDF/XLSX bytes, person and trip metadata, and public CSV exports are retained with SHA256 in `manifest.json`. The 77,353,399-byte trip CSV is stored as a lossless gzip (5,432,424 bytes), with both compressed and original hashes retained. The analysis uses only publicly released redacted data; no restricted spatial file was requested.

## NYC School Survey questionnaires

The separate official 2024 and 2025 NYC School Survey student instruments were also downloaded. They ask about school-bus satisfaction and perceived safety traveling between home and school. They do not provide a school-journey duration question. Those attitudes are not travel-time observations and are not substituted into the commute utility. The original instruments are `student_questionnaire_2024.pdf` and `student_questionnaire_2025.pdf`.

Run `python3 research/2026-a/data/task4_v20_nyc_school_survey/audit.py`. It checks all source hashes, 8,569 unique person records, 115,920 unique trip records, all trip-to-person joins, current-school-type membership and diary/weight coverage. Results are in `coverage_audit.json`.
