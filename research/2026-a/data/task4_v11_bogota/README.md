# Bogotá 2019 household mobility microdata: cohort audit

Actual public microdata are now archived from a pinned research mirror: `juanfonsecaLS1/encuesta-movilidad-bogota-19@50475bc50005a7622ad2ce356bd7b6a995d8b08d`. `manifest.json` records exact URLs, original byte lengths and SHA256. CSVs are losslessly gzip-compressed; questionnaire PDFs and the original dictionary are preserved. This is the 2019 survey, not the requested newer 2023 release. Official byte identity remains unverified.

The data contain 21,828 households, 66,820 people and 134,497 journeys. Household municipality 11001 identifies 52,174 Bogotá residents; 7,797 report school/college occupation in the main or additional occupation fields. These include 875 whose maximum attainment is incomplete upper secondary, 165 with completed lower secondary, and 108 with completed upper secondary. The latter counts are attainment categories, not validated current-grade cohorts.

The questionnaire's module B question 5 explicitly asks maximum educational attainment. Question 6 reports the preceding week's occupations and distinguishes school attendance from university attendance, but does not establish current grade. Selecting p5=6 would incorrectly equate attainment with current enrollment and can omit entrants whose completed attainment remains lower secondary. No age proxy is substituted. The newly acquired data do not yet justify narrowing the main high-school travel interval.

Trip interpretation also requires care: the dictionary describes `lugar_origen` as the location of the first departure yesterday, not a verified origin type for every later trip. A valid home-school analysis must establish the first trip or verify a return-home chain. Raw clock fields are Excel day fractions; the duration auxiliary file supplies parsed clock times and minutes. Preserve string household IDs such as P01595, person weights separately from trip weights, and students with no eligible journey.

`audit_cohort.py` verifies all archived hashes, household and person identity, household joins, city selection, occupation/attainment counts, and uniqueness of trip/duration composite keys. Both trip tables have zero duplicate keys. It deliberately produces no inferred high-school utility and no fabricated rank change. The current main champion set remains unchanged; this package enables later grade-linkage analysis if evidence becomes available.

```sh
python3 research/2026-a/data/task4_v11_bogota/audit_cohort.py
```

The 2023 official processed EODH ZIP and raw questionnaire sources were attempted again by the acquisition agent; requests failed. A public 2023 analysis repository supplied notebooks but no raw data. No external information request or contact was made.
