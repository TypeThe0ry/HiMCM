# Current Swiss source definitions: separate from the retained Zurich observation

The FSO's September2026 variable list explicitly defines `TT1019V_zb` as mean one-way work-journey time for incoming and internal commuters, excluding education commuters. Its source is the Structural Survey (SE), a sample of permanent residents aged15+ in private households, with stated exclusions. This supplies current source-method detail, but does **not** establish an observation-level link to Eurostat's `TT1019V`, CH002C,39.9minutes in2024. The suffix, geography and observation must be reconciled; codes that look similar are not a provenance chain.

The current FSO topic page states a one-year reference-label shift for Eurostat variables sourced from STATPOP, BDS, SE and STATENT: Swiss31December observations are labelled with the following reference year in Eurostat. This general rule does not independently prove the exact survey input used for the39.9 estimate. The old Swiss national Eurostat metadata page, already captured in `data/current_zurich_travel/`, was last updated in2012; it cannot settle2024 production.

## Selected current observations

The newly linked `DF_CITYSTAT_1` version1.0.1 response gives the following incoming/internal work-journey means, in minutes, with Swiss period labels:

| Official geography code and label | 2023 | 2024 |
| --- | ---: | ---: |
|261901 Zurich: core city|41.0244504880|41.0491469489|
|261910 Zurich: other agglomeration municipalities|32.0986553841|32.3977983553|
|261920 Zurich: agglomeration|36.5967153593|36.7440821538|

This asset uses the2020 Swiss agglomeration version. These territorial groups are not automatically Eurostat greater city CH002C or its functional urban area. None of the selected means is transferred to the original39.9-minute cell. CI-operation values are preserved in the response without interpreting their unit or confidence level; sampling intervals are not deterministic travel-duration support or bins. No duration distribution was obtained for the retained observation.

## Provenance and reproduction

`retrievals.json` records the exact request/final URLs, actual HTTP status, UTC, bytes, SHA-256 and selected response headers. `fso_city_portal.html`, `data_asset.html`, `variable_list.xlsx`, `current_structure.xml` and `zurich_worktime.xml` preserve original bodies. The SDMX data request uses the linked1.0.1 flow, observed geography codes and `TT1019V_zb` from the downloaded variable list. The two operation codes are OBS and CI; period filters are2023–2024. FSO assets state OPEN-BY attribution requirements; source: Federal Statistical Office.

Run `python research/2026-a/data/current_zurich_source2026/extract.py` for byte checks and deterministic XLSX/XML extraction. Three derived JSON files retain the selected source descriptions, code labels and observations. No workbook or original input is edited; no person-level data is present. PrimaryV203, source CSV, weights, interval rules and manuscript remain unchanged, with zero admissions and zero score-width reduction.
