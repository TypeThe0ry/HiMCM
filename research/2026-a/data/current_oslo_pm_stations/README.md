# Oslo 2024 PM2.5: station annual means

Oslo's official table MIL032 provides **12 reported station values and eight missing cells** for 2024. These are station-specific annual means in µg/m³, not a population-weighted city exposure. They do not establish the source of the retained modelled Oslo value of 7.9 and are not substituted into V203.

The [municipal table](https://statistikkbanken.oslo.kommune.no/statbank/pxweb/en/db1/db1__Klima%20og%20milj%C3%B8__Luftkvalitet/OK-MIL032.px/) identifies Bymiljøetaten, Oslo kommune and Statens vegvesen as its providers. The API result was updated on 19 June 2026. Its notes define the geographical units as monitoring stations and explain blank cells as an inactive station, no data, or less than 75% coverage. Missing values remain missing; no city mean or population weights are invented.

`table.html`, `metadata.json` and `annual_2024.json` preserve the successful original responses. `query.json` is the human-readable query and `request_body.json` contains the exact POST body used for the read-only statistical request. The query selects every published location category, year label 2024 and the concentration variable; the JSON-stat result has dimensions `[1,20,1,1]`, including its generated ContentsCode dimension. Values retain the source's reported precision.

`retrievals.json` records requested/final URLs, UTC, actual status, bytes and hashes. Two early endpoint responses are retained separately as `metadata_404.html` and `metadata_400.txt`; they are failed requests, not evidence of missing air measurements. The successful API uses `/statbank/api/v1/no/` with metadata-derived selection codes. Run `python research/2026-a/data/current_oslo_pm_stations/extract.py` to check receipts and print the deterministic selection.

The original CSV, its year and flag, the primary model and manuscript remain unchanged. Primary admissions and actual primary interval-width reduction are zero.
