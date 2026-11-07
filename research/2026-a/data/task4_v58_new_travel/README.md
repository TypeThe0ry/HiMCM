# V58 — Current-stage travel source checks

No city travel interval changes. This audit obtained the original Mexico EOD2017 questionnaire and checked a new Jakarta2023 source, identifying why neither supplies the required city-wide current-upper-secondary duration distribution.

## Mexico City: EOD2017

The original [INEGI questionnaire](eod2017_questionnaire.pdf), printed page3 Q3.6, records the highest year or grade passed. Printed page4 Q3.7 uses a single activity code, asking about work and job search before student status. Hence student code4 cannot identify all working students, and education code06 cannot be interpreted as the current upper-secondary programme. The journey diary records actual departure/arrival times, but those times do not resolve student-stage membership. This older survey does not replace or intersect the existing2020 Mexico interval.

The primary www host returned403; the indexed official English host supplied the original985955-byte PDF. Its hash is retained in `manifest.json`. The offline audit checks the original instrument definitions, rather than relying on a translated secondary summary.

## Jakarta: Komuter2023

The [official BPS publication](https://www.bps.go.id/en/publication/2024/03/28/33b6bef825944e576e7ea3ba/commuter-statistics-of-jabodetabek-results-of-jabodetabek-commuter-surveys-2023.html) has a genuinely current-stage table: Table55, printed pp95–97, separates SMA/MA/equivalent by residence and sex. Table20, printed p37, reports journey-duration bands for all commuters by residence, rather than a joint high-school-stage/duration table. The report defines commuters as people crossing a regency/city administrative boundary, leaving same-boundary students outside that commuter population. Neither margin alone identifies the model's student travel distribution.

The report was read through the official PDF web reader. The attempted local PDF download timed out; the publication and microdata pages returned403 locally. `jakarta_reader_audit.json` is a labelled paraphrase, not an original PDF. The official microdata catalogue lists a paid full-data product; no purchase, application or external contact was made. No numeric high-school travel value was inferred from the all-commuter table.

Validation: `python3 research/2026-a/data/task4_v58_new_travel/audit.py`. Source population, school-stage ambiguity, and missing joint distribution remain explicit. No manuscript or model input changed.
