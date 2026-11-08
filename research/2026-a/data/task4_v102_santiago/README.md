# Santiago: real EPJA school-trip observations, separate from the main target

JUNAEB's public data library provides genuine school-trip-duration observations for Santiago residents in **current secondary youth/adult education (EPJA)**. In 2023 there are **84 such respondents**, including 36 in the first secondary level (grades 1–2) and 48 in the second level (grades 3–4). Duration is answered by 81 and missing for 3. These are respondent counts, not population estimates.

| Reported duration | Respondents |
|---|---:|
| Less than 10 minutes | 11 |
| 10–30 minutes | 31 |
| 30–45 minutes | 24 |
| 45–60 minutes | 8 |
| 60–90 minutes | 4 |
| More than 90 minutes | 3 |
| Missing | 3 |

The filter uses current `DS_GRADO` (contains `medio`) and residential `DS_COMUNA_ESTUDIANTE = Santiago`. The source supplies a commune name here, rather than a verified numeric 13101 field. It does not aggregate Greater Santiago. `ULTIMO_ANO_EDUCACION_FORMAL` is prior educational history and is **not** used for current stage. The nationwide file contains 22,673 respondents; 115 reside in Santiago across all EPJA stages.

## Why the main missing interval stays [0, 1]

The same-year questionnaire and manual define travel as time **from the respondent's usual departure point to school**. A home departure is not required. The 2023 public CSV has no age field with which to restrict the sample to ages 14–18. EPJA is a specific youth/adult pathway; these respondents do not cover the city's regular secondary student population. No expansion-weight field was identified. Consequently this package adds real descriptive evidence but makes **no main-model admission, ranking change, or narrowing claim**.

The 2025 EPJA public CSV is archived separately for later verification: it contains age, residential commune, and 40,037 rows, but its coded travel fields lack a matched 2025 dictionary in the inspected library folder. Its current-grade labels also need validation. We do not map 2023 question numbers onto 2025 fields. No 2025 statistics are admitted. The archived **2025 Primero Medio dictionary** contains residence and age, but no actual school-trip-duration field; it does not solve this gap.

## Source and reproducibility

- Official discovery entry: https://bibliotecadatos.sead.junaeb.cl/ and its public `/datos` download page. The site's download implementation directly uses the public `biblioteca-datos` Google Cloud bucket. No login or request for restricted data was made.
- Same-year questionnaire/manual: https://encuestasrpt.junaeb.cl/doc/ . Travel question 14 appears in the questionnaire PDF page 8 and manual PDF page 25.
- `sources.json` records exact download URLs, original byte lengths and SHA-256 hashes. The CSV is kept as lossless gzip under the git-ignored `../local_only_epja/`; it is not distributed in this package. The original uncompressed hash is retained and checked before extraction. Original PDFs and dictionary are unchanged.
- Run `python3 research/2026-a/data/task4_v102_santiago/extract.py` from repository root to regenerate `subgroup_counts.json`, using the standard library only.
- Prior CASEN 2024 absence of school duration was already established in `../task4_v67_santiago`; unresolved EOD 2012 current-stage semantics remain documented in `../task4_v89_santiago_travel`. Neither is counted as new evidence here.

This bounded addition does not modify model code, registry, manuscript, or other agents' files.

## Bounded 2025 follow-up

The full public EPJA directory listing (`epja_public_directory_listing.json`, no pagination token) contains only 2023–2025 CSVs and directory placeholders, with no EPJA questionnaire or dictionary. The public survey site's landing-page assets also supplied no 2025 EPJA questionnaire download. The ministry's indexed 2025 survey announcement (`https://epja.mineduc.cl/encuesta-vulnerabilidad-escolar-2024-para-epja/`) and JUNAEB survey information page timed out during direct retrieval. Search did not identify an accessible official same-year EPJA codebook. These are access findings, not a claim that no codebook exists anywhere.

The local-only `../local_only_epja/epja_desidentificado_2025.csv.gz` preserves the 40,037-row source for a later matched-codebook check. Although an `EDAD` field exists, no age-screened travel estimate is reported: residence, current-grade coding and travel question/category definitions still require a verified 2025 mapping. No 2023 question numbering or bin codes have been copied into 2025. The 2023 descriptive extraction remains unchanged.

## Individual-record handling

A follow-up inspection found identifying content in the supposedly de-identified downloads: one email-like value in 2023's free-text `DIFICULTADES_ADQUIRIR_ALIMENTOS_DETALLE`, and 23,930 email-like values in 2025's `A00B`; 2025 also contains birth dates. Both years contain individual IDs. These fields and all individual records remain local-only. Public outputs contain aggregate counts, source URLs/hashes, and questionnaires/dictionaries. `extract.py` reads the ignored local source, verifies its uncompressed hash, selects only commune/current-grade/travel fields, and writes only aggregate statistics. The source-missing message explains how to restore the local input. No contact values are published here.
