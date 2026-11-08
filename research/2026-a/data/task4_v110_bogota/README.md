# Bogotá ECV 2025: repair of the metadata evidence trail

V109's saved capture contained two retrieval errors. It did **not** archive the successful metadata reads seen earlier in the interactive session. V109 README, capture label and audit now state this explicitly. This package preserves new successful rendered responses and checks their substantive contents before accepting them. They are web-tool representations, not original HTML or raw survey files.

## Reverified evidence

- [Education dictionary](https://microdatos.dane.gov.co/index.php/catalog/905/data-dictionary/F24?file_name=Educaci%C3%B3n) opens successfully. Following its displayed links yielded the captures below; directly opening some variable URLs returned errors, so availability is route/tool dependent.
- [P1088 current level](https://microdatos.dane.gov.co/index.php/catalog/905/variable/F24/V2691?name=P1088): Media code4 includes grades10–13. Instructions distinguish current enrollment from approved attainment. The standard upper-secondary grades are10–11;12–13 refer to normal-school teacher training after grade11.
- [P1088s1 current grade](https://microdatos.dane.gov.co/index.php/catalog/905/variable/F24/V2692?name=P1088s1): the same current-grade definition is explicit.
- [P6167 minutes](https://microdatos.dane.gov.co/index.php/catalog/905/variable/F24/V2707?name=P6167): outward travel to the institution, summing time across used modes.
- [P8586 attendance](https://microdatos.dane.gov.co/index.php/catalog/905/variable/F24/V2686?name=P8586): yes1/no2; formal flexible/adult cycles and intended/confirmed enrollment during recess are included.
- [Composition dictionary](https://microdatos.dane.gov.co/index.php/catalog/905/data-dictionary/F9?file_name=Caracteristicas+y+composicion+del+hogar): age P6040, birthdate P6034 and person/household identifiers. Original files therefore belong in ignored local storage.
- [Design dictionary](https://microdatos.dane.gov.co/index.php/catalog/905/data-dictionary/F30?file_name=Variables+dise%C3%B1o+muestral+ENCV+2025): MPIO, SEGMENTO, ESTRATO2020, and calibrated FEX_C. Its description still says2024 despite its2025 heading; that inconsistency is retained.
- [MPIO metadata](https://microdatos.dane.gov.co/index.php/catalog/905/variable/F30/V2833?name=MPIO) includes code11001 with7,415 unweighted cases. This is all-age module metadata, not an extracted student sample, and the displayed code has no municipality-name label. Exact residence mapping and record joins remain to be checked against the acquired originals and codebook.

The [advertised download page](https://microdatos.dane.gov.co/index.php/catalog/905/get-microdata) again renders through the web tool. It names Education, Composition and Design2025 DBF ZIPs dated2026-04-21; catalog creation/modification is2026-07-16. The page heading also carries2024–2025. These are verified catalog statements, not proof of original-record vintage.

## Download scope and remaining limits

The variable page advertises a [JSON export](https://microdatos.dane.gov.co/index.php/metadata/export_variable/905/V2691/json). That export was successfully rendered and contains **variable metadata**, not individual observations or cross-tabulations. The raw-data download controls still appear only as input controls in the rendered page, with no exposed payload link. No advertised alternative supplying the three actual modules was found in these inspected pages. V110 did not repeat the prior shell/browser403 requests, guess hidden endpoints, or bypass access controls.

No microdata was acquired. Current-stage/time definitions are now auditable locally, but city-specific utility still requires the actual linked records, residence validation, missing/nontravel handling and design verification. No model interval or ranking changed.

Run `python3 verify.py` to check capture hashes and expected substantive evidence. The checks reject error-only captures; original V109 error evidence remains labeled as such.

The catalog-advertised [study JSON](https://microdatos.dane.gov.co/index.php/metadata/export/905/json) was also inspected through the web renderer: no `external_resources` match; the ZIP reference found describes internal survey transmission, not a download endpoint. The advertised [DDI](https://microdatos.dane.gov.co/index.php/metadata/export/905/ddi) was unsupported by the web renderer (octet-stream); one normal direct request returned HTTP403 and83 bytes. `download_audit.json` records these distinct outcomes. Full original JSON/DDI was not obtained.
