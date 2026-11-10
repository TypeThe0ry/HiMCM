# Oslo pupil–teacher ratio: bounded source check

**Result.** Statistics Norway (SSB) table 12609 reports **12.5 pupils per contracted teacher man-year** for Oslo municipality in 2025; the supplied CSV records **18.2**, year 2025, flag `ok`. The values do not match. This check does not identify the original source or establish the input’s full lineage. The user-supplied value remains unchanged; the SSB cell is not a replacement.

## Source and scope

The [SSB API table 12609](https://data.ssb.no/api/v0/en/table/12609/) identifies upper secondary education, Oslo region code `0300`, metric `KOSelevperlarsv0000`, and year 2025. The saved JSON-stat response, `ssb_12609_response.json`, indexes 2024 and 2025 as 10.9 and 12.5 respectively and gives the metric reference period as `31.12`. `ssb_12609_query.json` records the exact POST selection; `ssb_12609_metadata.json` contains the table dimensions. It is a teacher full-time-equivalent measure, not a teacher headcount.

The [SSB historical indicator definition for table 06942](https://www.ssb.no/343185/videregaende-opplaering-nokkeltall-f-tabell-06942), under **Elever per lærerårsverk**, describes county-run upper secondary schools, including vocational college students in those schools; the denominator is contracted teacher man-years excluding long absences and leadership/inspector positions. Pupils are assigned by school county and counted on 1 October; pupils and personnel are matched at county level, not by individual school. It excludes other providers from its stated coverage. This older definition provides a relevant scope warning, but its exact continuity with the current table 12609 is unverified. The API reference period of 31 December is not proof that both numerator and denominator were observed on that date; the exact current denominator date remains unverified.

## Match assessment

- **Value:** no match (12.5 versus 18.2).
- **Metadata:** year and Oslo administrative selection match; full stage, geography, provider, denominator, and observation-date equivalence with the CSV cannot be established because the input does not specify them. The historical definition includes vocational college students, so it is not a pure upper-secondary numerator.
- **Lineage:** unverified; no document connects the CSV cell to this SSB series or to another original observation.

`receipts.json` records each direct HTTP retrieval with timestamp, status, final URL, byte count and SHA-256. `ssb_12186_metadata.json` is retained as an exploratory leadership-table response and contains no pupil ratio. Web search discovery is not represented as a captured original request. No model, source input, registry or manuscript was modified.
