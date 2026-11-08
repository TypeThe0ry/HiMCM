# V124 education search: no city PTR admitted

Zurich, Helsinki and Dublin retain their existing fully missing upper-secondary pupil/teacher-ratio cells. This bounded follow-up found actual teacher-FTE data, but its published geography does not match the requested cities. It changes no submitted values, weights, utility anchors or existing bounds.

## Zurich: real teaching FTE, canton scope

The canton education authority's current [staffing page](https://www.zh.ch/de/bildung/bildungssystem/zahlen-fakten/entwicklung-des-schulpersonals-an-mittelschulen-und-berufsfachschulen.html) identifies its population as publicly financed middle and vocational schools throughout **Kanton Zürich**. Its embedded chart leads to the public BISTA JSON endpoint archived in `zurich_canton_staff_fte.json`.

The JSON contains school year, school type and teaching full-time equivalents, with a September15 reference date. Its current series spans 2016/17–2025/26, and the metadata's example explicitly says “im Kanton”. There is no municipality or school identifier in its data rows. A canton total for public funding cannot be divided into the existing city student workbook to produce a matched city PTR. This source was rejected, despite successfully obtaining substantive teaching-FTE records.

The city's 2011 statistical yearbook provides a separate historical check. Printed page323 (PDF310), table15.1.19, reports personnel in city-operated kindergarten, primary and lower-secondary schools. Printed pages325–326 (PDF312–313) report canton-operated and private middle-school pupils, including lower-gymnasium groups. The personnel table is not a matched upper-secondary denominator. Full/part-time employee counts are also not an FTE total. No ratio was constructed across these tables.

The earlier city teacher gender-percentage chart and student workbook were reviewed from the V120 failure log rather than downloaded again. Percentages remain insufficient to recover teacher totals.

A further [BFS canton teacher table](https://www.pxweb.bfs.admin.ch/pxweb/de/px-x-1504000000_170/px-x-1504000000_170/px-x-1504000000_170.px/) was checked specifically for a valid teacher superset that might bound the city denominator. Its full title restricts it to **public schools, in persons**. With private-school pupils included in the city workbook, public-school canton teachers do not provide a proven upper bound for all city teachers, and persons do not identify FTE. No one-sided city bound follows from that route.

## Helsinki: student tables remain unmatched to teachers

The [2024 statistical yearbook](https://www.hel.fi/static/kanslia/Kaupunkitieto/24_12_16_Helsingin_tilastollinen_vuosikirja_2024.pdf) includes city education-level student counts in table7.14 (printed page157, PDF158). The adjacent teacher-related material in table7.15 is adult-education teaching **hours**, not upper-secondary teacher FTE or headcounts. It supplies no matching denominator for those upper-secondary pupils. Neither those hours nor all-education personnel are used as teachers.

The previously archived city-operated2024 education report was not downloaded again: its municipal workforce definitions include nonteaching personnel/leave/substitutes and do not establish all-provider city coverage. Individual school reports and student-data catalogues did not establish a complete, matched city teaching workforce during this bounded search. Helsinki's missing ratio stays unknown.

## Dublin: publication policy explains the city denominator gap

The official Department of Education and Youth [Teacher Workforce Data quality report](https://nationaldata.ie/media/NationalDataie/MethodologyDocumentation/Teacher_Workforce_Data_Quality_Report.pdf), reporting period2025–2026, distinguishes real payroll teacher FTE from registration or allocated posts. Section5.2 says FTEs are calculated at school level using roll numbers but are **not published at that level**; DEY annual reports aggregate to county, while PxStat aggregates by school type. Section8.4 gives confidentiality as the reason roll-level records are not published.

The substantive [EDA82 PxStat response](https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/EDA82/JSON-stat/2.0/en) was retrieved and archived. Its dimensions are school type, year and statistic; it has no school, municipality or county dimension. Its nationwide FTE count cannot be joined to Dublin City pupil totals. County Dublin and the Dublin ETB catchments also do not identify the city-boundary population.

This is a stronger source-specific finding than assuming teacher registrations measure employment. It does not prove that no suitable city data exist elsewhere. The older registration/allocated-special-post routes were skipped using the V120 records. A search-only historical lead describing allocated posts was also discarded; it was not treated as actual employed FTE.

## Records and verification

`attempts.json` records the routes, access date, source years, scope, outcome and reasons. `sources.json` records URLs, SHA256 and whether a saved file is original or derived. The official canton page/API and Irish quality report/API retain original downloaded bytes. The rejected multi-megabyte city yearbooks remain in `/data/scratch`; this folder keeps clearly labelled derived scope excerpts, their page locators, original download URLs and original byte hashes. No excerpt is presented as a complete original publication.

Run `python research/2026-a/data/task4_v124_education/extract.py`. It verifies archived hashes, the canton API's lack of a city dimension, the Irish publication restriction and nationwide API dimensions, then verifies `observations.json` is empty. It saves an audit record with the unchanged original CSV hash. The script is a rejection/provenance check, not a new measurement extractor; it makes no network call and edits no model input.

The next useful evidence would be city-school FTE and pupils for matched upper-secondary stages/providers, or a published city PTR with that definition. The current sources do not justify substituting regional totals, staff headcounts, teaching hours or allocated posts.
