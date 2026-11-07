# Bogotá EODH2023: V66 alternate official access audit

Checked 2026-11-08. The official SIMUR landing page was readable and supplies a different 2023 ZIP from the individual archives located in V65. The downloadable ZIP returned HTTP 403 through both web retrieval and a direct HEAD request. No questionnaire, dictionary or microdata original was acquired.

The Bogotá open-data CKAN package_search endpoint timed out in a direct 25-second request; the web tool also could not access it. No catalogue response was obtained, so this is not evidence that the catalogue lacks EODH2023.

## Sources

- Official survey listing: https://www.simur.gov.co/index.php/encuestas-de-movilidad
- Official 2023 aggregate download: https://www.simur.gov.co/sites/www.simur.gov.co/files/2024-05-21/basico/2.PublicacionSIMUR-20240521T211042Z-001.zip
- Public catalogue query: https://datosabiertos.bogota.gov.co/api/3/action/package_search?q=encuesta%20movilidad&rows=100
- Individual official archives and prior results: ../task4_v65_bogota_eodh/access_audit.json

## Eligibility remains unresolved

The official listing identifies questionnaires and a data dictionary but does not reveal question wording or current school grade. We have verified neither presence nor absence of a current upper-secondary enrollment/grade variable. Highest attained education, age alone and general study purpose cannot establish this eligibility. Do not transfer codes from EODH2019 or DANE EM2021.

No observations or model cells change in this audit. Existing missing intervals must remain unchanged. A next useful step is successful ordinary download of one of the already identified official archives, followed by inspection of actual current-attendance/grade question wording and person-trip keys; repeating the same failed requests adds no evidence.
