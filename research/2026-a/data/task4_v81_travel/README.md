# Barcelona FRESC2025: the current questionnaire omits journey minutes

The official FRESC2025 questionnaire's travel block asks which modes pupils use, followed directly by environmental perceptions. It does not contain the per-mode journey-minute questions listed in the FRESC2021 manual. This changes the next acquisition step: obtain the older survey's actual time records or another survey, rather than assuming that FRESC2025 microdata will supply the old time fields.

## New original sources

The [official manuals page](https://www.aspb.cat/documents/fresc-manuals-questionaris/) links the newly revised 2025 methodology manual (filename dated2026-11-03) and 2025 questionnaire (filename dated2026-01-29). Both PDFs were downloaded successfully; byte lengths, SHA-256 and direct URLs are in [manifest.json](manifest.json). The source year remains2025; filename dates are document-version dates, not survey observation years.

- Questionnaire PDF10 / printed9: B1 lists school-travel modes and allows multiple responses. B2 asks about traffic, noise, vegetation and safety. B3's five-minute reference concerns access to a green space from home, not journey time to school. The page was rendered and visually checked.
- Methodology PDF25 / printed24 describes mode combinations; its variable dictionary contains the mode fields but not the 2021 `peuanar_m`, `bicianar_m`, `tpanar_m`, `cotxeanar_m`, `motoanar_m`, `patinet_anar_m` or `altanar_m` duration fields.
- [V44's archived 2021 manual and mode table](../task4_v44_barcelona/README.md) remain historical sources. Their time-field definitions must not be transferred to2025.

No new student time observations were obtained, and no city interval or ranking is changed. School-based sampling and course coverage still need evaluation if2021 records become available. No institution has been contacted and no data-access request has been submitted.

`verify.py` verifies original hashes, the questionnaire block structure and the year-specific variable-field contrast. Text search is a reproducible check of these identified documents; it does not prove that no other survey or unpublished supplemental data exist.
