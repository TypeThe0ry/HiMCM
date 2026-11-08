# V121 education candidates: Stockholm school-resource ratio; Paris skipped

Stockholm has a directly published city-school pupil/teacher-FTE ratio. Paris's retrieved official booklet does not supply a matching upper-secondary teacher denominator. This directory contains candidates for the parent model review; it changes neither the registered model nor the submitted CSV.

## Stockholm: all providers, schools located in the municipality

[Kolada N17816 metadata](https://api.kolada.se/v3/kpi/N17816) defines pupils per teacher full-time equivalent in upper-secondary schools **located in the municipality**, measured on 15 October, with source Skolverket (Siris). Its operating area is `Gymnasieskola åk 1-3` (upper-secondary school years 1–3), and `auspice=T`. The [official API documentation](https://kolada.se/om-oss/api/) defines T as all activity regardless of provider ownership. [Municipality metadata](https://api.kolada.se/v3/municipality/0180) resolves code 0180 to Stockholm, type K (municipality).

The [period-2025 API response](https://api.kolada.se/v3/data/kpi/N17816/municipality/0180/year/2025) supplies one nondeleted, nonmissing, total-gender value, **16.42091405**. This is a published ratio; this work does not independently reconstruct the city's student and teacher totals. The Skolverket 2025/26 staffing report describes collection from active schools on 15 October or the nearest weekday, and says calculations use unrounded information. The archived Skolverket analysis-table metadata maps year code 2025 to school year 2025/26. The Kolada metadata's next publication date (2027-04-08, reference period 2026) is a future publication schedule, not the year of the already available 2025 observation; the provider's documentation explicitly distinguishes it.

The candidate intentionally reduces the API ratio to one decimal (16.4) and retains a half-last-digit envelope **[16.35,16.45]**, containing the original value. This is an explicit conservative precision convention for the derived input, not a claimed source rounding interval, statistical confidence interval, or independently measured error bound. The unchanged cost utility `15/(15+PTR)` maps it to **[0.4769475358,0.4784688995]**. No interpretation depends on the API's eight decimal places.

This measures the resources of upper-secondary schools in Stockholm, including pupils attending from elsewhere, across provider ownership. It is not a measurement restricted to residents aged 14–18, an annual average teacher workload, or a claim about all education stages. `anpassad gymnasieskola` (adapted upper-secondary schooling) is a separately published school form in Skolverket's staffing tables; the candidate is the published gymnasieskola indicator. These scope conditions belong with any model admission.

## Paris: rejected denominator mismatch

The original [Académie de Paris 2025 booklet](https://www.ac-paris.fr/sites/ac_paris/files/2025-08/chiffres-cl-s-acad-mie-de-paris-44994.pdf) gives 72,476 pre-baccalaureate lycée pupils at the 2024 rentrée, covering public and private schools under contract. Its 15,940 second-degree teachers as of 31 December 2024 cover more than lycée: the second degree also includes collège. The booklet does not split teachers into a denominator matched to those lycée pupils, nor does it establish coverage of private schools outside contract. The ratio `72476/15940` is therefore **not used**. Paris's original fully missing upper-secondary ratio remains unknown.

An early Stockholm city council key-indicator PDF search surfaced a 13.0 pupil/teacher figure, but that table is in the **grundskola** section, not upper-secondary schooling. Its gymnasieskola section has qualification shares rather than a matching ratio. It was not substituted. The city yearbook's upper-secondary student table has no matching teacher denominator and was not used to reconstruct the ratio.

## Reproduce and provenance

Accessed 2026-11-08, Asia/Singapore. `sources.json` records URLs, access date, archive type and SHA256 for each original HTTP response; files retain downloaded bytes. `paris_relevant_pages.txt` is derived using `pdftotext`, not an original source. `skolverket_underlag_metadata.json` supports definitions and year labels, not an independent Stockholm numerical check.

Run `python research/2026-a/data/task4_v121_education/extract.py` from the repository root. The script verifies source hashes, geography, provider scope, indicator definition, missing/deleted flags and year labels, computes the candidate utility envelope, and checks the Paris mismatch against the original PDF. It uses the standard library and Poppler; no package installation or network is required. `observations.json` is a candidate only, and `nonadmission_audit.json` records rejected routes.
