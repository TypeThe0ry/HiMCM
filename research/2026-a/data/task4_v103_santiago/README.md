# Santiago V103: 2025 codes do not identify school-trip duration

Inspection of the actual 2025 CSV confirms that `E14` has only three values: `1` (10,668 records), `2` (24,291), and `88` (5,078). It does not carry the six duration labels found in the 2023 questionnaire. This rules out copying the 2023 question-number interpretation onto this field. The recorded values are **raw codes with unknown semantics**, not short/long travel categories.

The source has 40,037 records and an `EDAD` field, but the matched 2025 travel-question definition remains unverified. `DS_GRADO` also needs reconciliation with teaching-type codes: its supplied labels cannot automatically be treated as a clean age/current-stage crosswalk. No age-14–18 travel estimate or main-model narrowing is made. The same-year codebook is the next specific prerequisite; the EPJA population, usual-departure-point versus home-origin issue, and expansion/coverage questions would still remain afterward.

## Checks completed on 2026-11-08

- Rechecked actual CSV values rather than assuming every code required an external label. The inspected travel-candidate fields are numeric codes, without duration text labels. `coded_field_diagnostic.json` contains only national counts for a fixed whitelist of numeric fields.
- The official library's complete public EPJA directory contains CSVs for 2023–2025 and placeholders, but no matched questionnaire/dictionary (listing retained in V102).
- The public survey landing page and its publicly linked JavaScript asset provided no 2025 EPJA questionnaire/schema download. Authenticated survey-answer routes were not requested.
- Searches for official 2025 EPJA questionnaire/instructions, and a GitHub-indexed EPJA/JUNAEB mirror, did not identify an accessible matching codebook. The MINEDUC indexed 2025 announcement timed out again. This bounded check does not establish that no such document exists elsewhere.

Entry points: https://bibliotecadatos.sead.junaeb.cl/ ; https://sistemaencuestas.sead.junaeb.cl/ ; https://epja.mineduc.cl/encuesta-vulnerabilidad-escolar-2024-para-epja/ . Exact source CSV URL and SHA256 are in `../task4_v102_santiago/sources.json`.

## Source handling correction

The public files contain identifying data despite their de-identified filenames. Only field/count findings are reported: 2023 has one email-like value in a free-text field; 2025's `A00B` has 23,930 email-like values and `FECHA_NACIMIENTO` is populated in 40,037 rows. Both contain individual IDs. The parent agent moved the raw CSVs to ignored local storage. The V102 extraction now checks the original hash, reads that local file, selects only required analytic fields and publishes aggregate counts. No personal values or individual records are included in V103.
