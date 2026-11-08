# Bogotá V92: home-origin fields remain unavailable

The newly inspected processed **stage module has 110,881 rows and 38 columns**, but no home-origin/home-destination flag or current-grade field. It therefore does not resolve the admission gap in the V91 person/household/trip extract. All model inputs and missing intervals remain unchanged by this audit.

`source_manifest.json` records the pinned source URL, source-byte SHA-256, column inventory and local raw location. The 59,325,906-byte stage file is kept outside Git at `/tmp/bogota92_etapas.csv`; no person records, source identifiers, locations or sensitive attributes are republished here. Its `max_nivel_educativo` and `ocupación_principal` fields retain the V91 distinction between attained education and current grade. The stage field `motivo_viaje` does not identify where the trip began.

## Located implementation evidence

[ESO-Rennes's pinned research code](https://github.com/ESO-Rennes/Distancias_Emisiones_EODH/blob/e6a968153f361faae92fde510592d8e40d226e2f/Distancias_EODH_2023_projection_reseau.Rmd#L159) reads `ANEXO 2_BASE DE DATOS EODH CON FACTORES DE EXPANSIÓN.xlsx` locally. Lines 75–78 identify the sheets, and lines 164–176 join `viajes.d24` to the trip key and `modulo D-E.d7` to the person key. The implementation maps code 1 to home for both variables; destination code 2 maps to another location. This is third-party implementation evidence, **not an acquired official dictionary or raw dataset**.

The repository tree at the pinned commit contains two Rmd files, two HTML files, a README and five maps; it does not supply the named workbook or an enriched trip export. Its home-origin implementation marks only the first trip of a day when the initial-location flag is home. It defaults other origins to another location. That rule should not be copied as a complete home-origin classifier: subsequent trips require their documented origins or validated linkage to preceding trip destinations.

## Access checks on 2026-11-08

- The indexed [official 2023 landing page](https://observatorio.movilidadbogota.gov.co/publicaciones/resultados/encuesta-de-movilidad-2023) lists unprocessed D/E, trip and stage modules plus a dictionary. The [official taxonomy page](https://observatorio.movilidadbogota.gov.co/taxonomy/term/36) also lists the unprocessed-data section. The accessible rendered pages did not expose a usable raw download target.
- Direct official landing-page requests ended with a remote disconnect; web retrieval timed out. Both tested SIMUR route variants returned HTTP 403. The CKAN `package_show` endpoint timed out. These are observed access failures, not evidence that the files do not exist.
- GitHub searches for the exact workbook name and module name found no relevant indexed file. A broad `d7`/`d24`/EODH query returned irrelevant matches and does not establish exhaustive absence.

Next admission step: obtain the original D/E and trip records plus their official dictionary, validate their keys against the processed V91 trip/person records, and verify current school level separately. Shared zones, coordinates and study-trip purposes are not substituted for the home flags.
