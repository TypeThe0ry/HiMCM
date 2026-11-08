# Bogotá V93: an additional official archive lead

A downloaded external technical annex identifies a specific SIMUR archive URL on page 13. Its label describes survey technical material (technical sheet, sample coverage and output tables); the archive contents have not been inspected and it cannot yet be called the original D/E–trip workbook. The exact archive request returned HTTP 403 with 3,746 bytes of HTML. The archive remains unacquired.

- [Technical annex](https://www.mas60datosplateados.com/documents/Anexo%20t%C3%A9cnico%20%2B60%20Datos%20Plateados.pdf), page 13: downloaded successfully, 384,452 bytes.
- [Official archive target](https://www.simur.gov.co/sites/www.simur.gov.co/files/2024-05-21/basico/2.PublicacionSIMUR-20240521T211042Z-001.zip): observed HTTP 403.
- [Pinned rendered research](https://github.com/ESO-Rennes/Distancias_Emisiones_EODH/blob/e6a968153f361faae92fde510592d8e40d226e2f/Distancias_EODH_2023_projection_reseau.html): downloaded 5,617,199 bytes. Its three raw-workbook references are local file reads. Inspection found no downloadable raw workbook or embedded interactive data widget. The home-flag code repeats the V92 first-trip-only implementation; it adds no official dictionary or person-level home flags.

The official landing-page request again ended with a remote disconnect; web retrieval returned timeout/502. These access outcomes do not establish that the data are unavailable elsewhere. `source_manifest.json` preserves URLs, hashes and local evidence paths. Downloaded source documents and error HTML remain outside Git; no raw personal records are republished.

No new records enter the model. Bogotá still requires the original home fields, validated joins and current-school-level evidence described in [V92](../task4_v92_bogota/README.md). Its travel interval remains [0,1].
