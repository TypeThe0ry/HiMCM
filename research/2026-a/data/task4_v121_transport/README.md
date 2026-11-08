# V121 transport: three city-scoped inventory candidates

The new observations address only originally missing stop-density cells. They keep the user CSV, population denominators, utility anchor50 and interval rule unchanged. Every inventory is a supply subset: `d=count*100000/population`, `utility=[d/(50+d),1]`. The upper bound remains1. Admission into the main model is the parent analysis's decision.

| City | Retained inventory | Source scope and date |
|---|---:|---|
| Stockholm | 13 metro stations | Original city/police2025 report, PDFp11/printed10:8 in Bromma and5 in Hässelby-Vällingby. Previous page explicitly locates both districts inside Stockholm municipality. The police district also includes Ekerö, but none of these13 is assigned there. Other city districts/modes remain uncounted. |
| Paris | 244 metro stations | Apur March2022 Atlas, PDFp37/printed37, explicitly Paris intra-muros. Underlying source is RATP2021 and Apur BDÉquipement2022.58 interchange stations are included; the separate332 line stop-points are not substituted. No RER addition, since overlap has not been deduplicated. |
| Dublin | 19 named existing tram stops | City Centre Transport Plan2023 technical note, issued2024, PDFp23/printed20, Figure3-7. A manual named subset inside its red city-centre study boundary; other plotted stops and regional totals omitted. The figure says existing infrastructure. Planned bus/MetroLink2030 changes are excluded. |

Paris and Dublin are **historical inventory proxies**, combined transparently with unchanged attachment populations (Paris2023; Dublin2022). They do not identify complete2025/2026 supply. Preserve a withdrawal arm restoring their cells to[0,1] if the intended claim requires contemporaneous inventories. Stockholm2025 uses the unchanged attachment's2025 population. Counts measure facility supply, not access, frequency, teenage usage or travel duration.

## Original sources and extraction

- [Stockholm city/police2025 report](https://meetingspublic.stockholm.se/welcome-sv/namnder-styrelser/hasselby-vallingby-stadsdelsnamnd/mote-2025-12-18/agenda/6-lagesbild-2025-samverkansoverenskommelse-mellan-hasselby-vallingby-sdf-och-lokalpolisomrade-vallingbypdf?downloadMode=open): original `stockholm_vallingby_2025.pdf`; PDFpage11 is rendered in `stockholm_vallingby_page11.png`. District counts are image content, so the record explicitly uses manual reading, not a fabricated text extraction.
- [Apur Atlas](https://www.apur.org/sites/default/files/atlas_activites_paris_immobilier.pdf): original `paris_apur_atlas.pdf`,45836500bytes. A slow direct download was incomplete and discarded; byte-range downloads assembled the complete original, then Poppler parsed its pages. Cover and provenance confirm March2022, not the misleading2025 date attached to a search result. `extract.py` verifies the count, intra-muros definition, distinction from332 stop-points, source years and SHA256. Its SHA256 is `877ca2d1926f90665c5d013f3053b8a2e1712270fb43f782ab0f3bc1c39cbf3e`.
- [Dublin official technical note](https://www.dublincity.ie/sites/default/files/2024-04/06-dublin-city-centre-transport-plan-public-transport-technical-note.pdf): original `dublin_public_transport_2023.pdf`. `dublin_luas_page23.png` preserves the checked map. `manual_figure_readings.json` lists every retained name, scope evidence and exclusions; names are counted once, not once per platform or serving route. The source report's existing-infrastructure label is checked by code; selected map-marker membership is a manual visual check.

Access date:2026-11-08, Asia/Singapore. `manifest.json` records original-file and derived-file hashes plus source URLs. Source-page images are extraction evidence, not new paper figures. No manuscript or Overleaf files were edited.

Run from the repository root:

```sh
.venv-v120/bin/python research/2026-a/data/task4_v121_transport/extract.py
```

The script needs only the Python standard library and Poppler `pdftotext`. It verifies the authoritative input hash and unchanged population denominators, validates source-file hashes and text-layer assertions, validates the explicit manual reading records, and regenerates `observations.json`/`manifest.json`. It does not claim to automate the visual judgment of image-only source figures.

## Bounded failed and nonadmitted routes

`nonadmission_audit.json` records the routes below. Failure did not lead to invented values.

- Dublin NaPTAN catalogue was retrieved, but both original StopAreas/StopPoints downloads returned403. Neither stop-points nor regional stops are used. The catalogue is archived as `naptan_catalogue.json`; a catalogue listing alone supplies no count.
- The older Paris data.gouv station dataset's download endpoint returned404. It is not used.
- Stockholm2026 statistical yearbook transport table14.18 gives county rolling-stock/journey statistics, not municipal unique stops. No county figure is admitted. The unrelated full yearbook is held only in scratch after the bounded review.
- Stockholm regional metro network has100 stations. A nonofficial source gave82 inside the municipality, but no official municipal82 count was verified, so neither100 nor82 is admitted. The defensible city/police subset13 is used instead.
- Dublin regional67-stop total and future infrastructure are not numerical inputs. Stops with ambiguous labels or near the study boundary are excluded, making19 a lower bound rather than a census.
