# Zurich work-journey source follow-up

No distribution or support is admitted to the retained 39.9-minute input. The baseline interval remains `[exp(-39.9/30), 1]`; the fixed-utility diagnostic does not supply a partial-distribution guarantee. The original CSV and model remain unchanged.

Two new official responses were saved byte-for-byte; `retrievals.json` records the requested and final URL, UTC retrieval time, HTTP status, byte count and SHA-256. Findings:

- `eurostat_ch_country_metadata.html` is the Swiss national Urban Audit metadata linked from the previously archived Eurostat urban metadata. Its last update is 20 November 2012. It describes the general collection and participating institutions, and directs detailed indicator concepts to general metadata. It does not establish the source, survey window, 2024 geography, commuter universe, or distribution underlying CH002C TT1019V. Its old coding description cannot settle the current greater-city label or 2024 data production.
- `zurich_city_commuters.html` is the municipal commuters page. Its 2024 chart is titled commuters by place of residence and place of work; the other identified chart concerns primary transport mode. The page does not give a duration distribution or link its population and time window to Eurostat's 39.9 estimate. It supplies no valid tightening of the retained utility interval.

The previously archived `task4_v184_zurich_commute` Eurostat response identifies TT1019V as average journey-to-work time, gives 39.9 with estimated status for 2024, and labels CH002C Zürich as a greater city. This observation alone does not establish the origin of the retained user input or a city-resident-worker distribution. The `task4_v185_zurich_bins` source documents a different 2023 municipal mean and historical survey-method changes; neither is transferred to this 2024 record.

Next step: obtain from the Swiss Federal Statistical Office the observation-level provenance and geographic composition for the 2024 CH002C TT1019V submission, followed by duration bins or support for that exact weighted population and reference period. Only assess intersection once identity and compatibility are documented; a sample confidence interval is not a deterministic support bound.
