# Bogotá: newly verified ECV 2025 acquisition route

Prior V11/V33/V41/V65/V66/V91–93 packages were checked first. This route is **DANE ECV 2025**, a different survey from the previously investigated EM2021 and EODH2019/2023. It resolves the metadata question of whether current stage and actual travel minutes are collected together. No new person records have been acquired or admitted.

The official [catalog 905 download page](https://microdatos.dane.gov.co/index.php/catalog/905/get-microdata) lists education, household-composition and sample-design DBF ZIPs, dated 2026-04-21. Catalog creation is 2026-07-16. These names identify download targets, not acquired files:

- `DBF-ECV-Educacion-2025.zip`
- `DBF-ECV-Caracteristicas_composicion_hogar-2025.zip`
- `DBF-ECV-Variables_diseno_muestral-2025.zip`

## Verified fields and the distinction from earlier sources

The [education dictionary](https://microdatos.dane.gov.co/index.php/catalog/905/data-dictionary/F24) lists 221,043 records and these questions:

| Field | Confirmed meaning | Required handling |
|---|---|---|
| P8586 | Current formal attendance; yes=1 | Includes school-break enrollment/intention and formal flexible/adult cycles |
| P1088 | Current enrolled stage; Media=4 | Direct current-stage variable, unlike EODH attained education |
| P1088S1 | Current grade | Restrict 10–11; Media also codes normal-school post-grade-11 cycles as 12–13 |
| P6167 | Outbound travel minutes to the attended institution | Interviewer instructions sum times across modes; preserve missing values and verify code handling before extraction |
| P3336 and subitems | In-person/virtual/alternating study modality | Retain nontravel/virtual students, not automatic utility=1 |

[P1088 metadata](https://microdatos.dane.gov.co/index.php/catalog/905/variable/F24/V2691?name=P1088) explicitly distinguishes current grade from the separate highest-approved question. [P6167 metadata](https://microdatos.dane.gov.co/index.php/catalog/905/variable/F24/V2707?name=P6167) establishes a reported outward journey, rather than a modelled accessibility proxy. National variable frequencies are not Bogotá estimates.

The [composition dictionary](https://microdatos.dane.gov.co/index.php/catalog/905/data-dictionary/F9) provides age P6040 and person linkage fields. It also lists birth date P6034 and sensitive attributes: full originals must stay ignored locally, with only necessary aggregate outputs published. The [design module](https://microdatos.dane.gov.co/index.php/catalog/905/data-dictionary/F30) supplies resident MPIO, SEGMENTO, ESTRATO2020, expansion factors and calibrated FEX_C. MPIO=11001 should be verified against its code labels in actual records; school destination P3514S2 must not replace residence. Joins and weights remain untested.

## Remaining blockers

Direct command-line requests and the ordinary Chrome download-page visit both returned a JSON `403 Forbidden` response. The web retrieval tool could render metadata and download names but not activate the download controls or supply their payload. No login, restricted-data request or access-control bypass was attempted. `web_metadata_capture.json` contains only **two unsuccessful Internal Error responses**, not substantive metadata. Earlier interactive reads supported the findings, but the V109 archive did not preserve them. V110 corrects this gap with checked successful rendered captures in `../task4_v110_bogota/`; these are still not original HTML or survey bytes.

Next bounded step is acquiring the three named public modules through a functioning official download interface, then checking join uniqueness, age 14–18, current grades 10–11, residence 11001, time values/special codes, modality and positive expansion factors. Survey uncertainty requires separate design verification. The catalog has legacy metadata text (design table description says ENCV2024; export document title mentions 2023) despite its 2025 title, dates and file names; raw vintage must therefore be checked when acquired.

Separately, the [EM main page](https://www.dane.gov.co/index.php/estadisticas-por-tema/pobreza-y-condiciones-de-vida/encuesta-multiproposito) now announces EM2025 tables dated 2026-10-28, but its anonymized-microdata link still leads to catalog743/EM2021. That link is not evidence of EM2025 microdata. The new person-annex URL returned a forbidden response to local download, not an XLSX file.

No interval is narrowed, no citywide estimate is fabricated, and no main-model file was changed.
