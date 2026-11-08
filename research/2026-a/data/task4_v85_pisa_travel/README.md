# PISA2018: framework proposals do not supply journey-time observations

The final PISA2018 well-being questionnaire and public-use codebook do not identify an actual school-journey duration field. This closes a new acquisition lead before downloading the much larger student microdata. No city indicator is changed.

The [2018 well-being framework](https://www.oecd.org/en/publications/pisa-2018-assessment-and-analytical-framework_b25efab8-en/full-report/component-9.html) discusses collecting commute hours. The final 28-page instrument linked from the [official database](https://www.oecd.org/en/data/datasets/pisa-2018-database.html) instead contains well-being, relationships, activity and recent-experience questions. The framework discussion must not be treated as proof that the proposed measurement is present in the released data.

## Original evidence and field audit

`wellbeing2018.pdf` and `codebook2018.xlsx` are original OECD downloads, with URLs, byte lengths and SHA-256 in [manifest](manifest.json). The codebook student-questionnaire sheet contains1118 variable labels. It provides derived current-grade information (`ST001D01T`) but the transport-related fields found concern parental barriers or school-choice preferences. The four `EC158/EC159` hours/minutes fields measure study before or after school, not travel. Cognitive items titled Transport and their test-response times also measure a different activity.

`verify.py` checks original integrity, reads the XLSX XML directly without extra Excel dependencies, and checks the identified field patterns and final questionnaire text. [Summary](summary.json) records the relevant variable names. The negative keyword checks support this bounded instrument audit; they do not prove that every national supplement or other PISA-family survey lacks duration measurements. PISA for Development has different instruments and populations and must be evaluated separately.

Run `python3 research/2026-a/data/task4_v85_pisa_travel/verify.py`. No student microdata were downloaded and no ranking, main-model or manuscript file was edited.
