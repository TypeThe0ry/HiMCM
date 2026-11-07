# V5 upper-secondary pupil–teacher observations

Retrieved 2026-11-07. Rebuild offline with `python3 research/2026-a/data/task4_v5_education/extract_education.py` (Python + beautifulsoup4). The extractor validates every successfully archived source against `manifest.json`, checks year/sex/school-type matching, and writes `observations.csv`. Failed requests are retained in the manifest without fabricated files.

| City | 2024 pupils | 2024 teachers | Pupils/teacher | Interpretation |
|---|---:|---:|---:|---|
| Tokyo |302411|19325|15.6486934|Tokyo prefecture national/public/private high schools, full-time and part-time courses; main-duty teacher headcount.|
| Singapore |24382|1979|12.3203638|Matched Government, Government-Aided and Independent pre-university strata, not every upper-secondary programme.|
| Shanghai |224186|22686|9.8821300|Municipality regular senior-secondary schools, excludes vocational education.|

These are genuine upper-secondary/pre-university administrative counts, but are **resource measures**, not measured learning quality. They are headcount ratios, not harmonised international full-time-equivalent ratios. Lower ratios do not demonstrate causal improvement in education. Geographic, programme and teacher-definition differences must remain explicit in uncertainty/scope sensitivity; the three observations do not justify a precise international education-quality ranking.

## Tokyo

Primary source: Tokyo 2024 School Basic Survey Table 7-1 (`gk24qv0711.csv`), row total national/public/private, all Tokyo, 2024. Numerator `生徒数（人）`; denominator `教員数（本務者）（人）`. The high-school subject table and full PDF are retained as crosschecks. This replaces an erroneous junior-high reading with actual high-school data. Correspondence courses and integrated secondary schools are separately tabulated and not included; teachers are main-duty persons, not FTE. Tokyo prefecture is not just the 23 wards.

## Singapore

MOE official data.gov.sg pre-university student and teacher APIs are fully archived (434 and 422 records respectively). For 2024 and sex MF, matched school types yield:

|Type|Pupils|Teachers|
|---|---:|---:|
|Government|12809|969|
|Government-Aided|5653|461|
|Independent|5920|549|

There are another 748 Specialised Independent pupils but no corresponding teacher row. They are **excluded from both matched-scope ratio and all-pre-U claims**, not treated as zero teachers. The naive 25130/1979 calculation is rejected. Pre-U covers JC/CI/Pre-U centres rather than primary/secondary school totals. Teacher reference date is 31 December; student enrolment and teacher dates are not identical within year. Mixed-level institution allocation and excluded programmes remain comparability limitations. The source metadata HTML files are archived. Use only as a scope-conditional observation; do not describe it as universal 14–18 education quality.

## Shanghai

MOE 2024 regular senior-secondary student table: Shanghai enrolment 224186. Teacher table: Shanghai first numeric total 22686. Student HTML is fully archived. Teacher source was visible in the official indexed web table, but direct HTML download repeatedly returned 403/redirect and web reopen timed out. `shanghai_teachers2024_extracted.json` is explicitly a **manual numeric-row transcription**, not an original downloaded table. The source URL and extraction method are preserved and hashed. Offline arithmetic is reproducible; full original teacher-page retrieval is an outstanding provenance limitation. Do not claim all three records have fully downloaded primary source pages.

## Optional pool indicator excluded

The downloaded official ActiveSG pool directory is retained as a lead only. It was not turned into an observation: current directory listings, long-term closures and denominator-year matching were not resolved. Singapore Sports Facilities Census lists private condominium pools too, so counting all swimming-pool rows as public facilities would be wrong. No pool density is invented or silently filled.
