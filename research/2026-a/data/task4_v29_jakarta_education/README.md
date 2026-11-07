# Jakarta SMA year refresh, V29 supporting evidence

The official BPS indexed table reports 186,461 SMA pupils and 11,983 headmasters and teachers in DKI Jakarta, academic year 2025/2026: PTR 15.560460652591171. This is a same-scope temporal replacement candidate for V6’s 2024/2025 observation (190,143 / 12,114 = 15.696136701337295), not a newly covered city or indicator. Do not intersect the two years as if they constrain the same contemporaneous value.

## Provenance and year

`bps_2025_query_response.json` is the actual serialized web search tool response, containing the complete indexed official BPS table. It is not original HTML/PDF. The indexed body displays update date 24 February 2026, then the selected year **2025**, the six district rows and DKI totals, and Dapodik attribution (odd-semester reports through 30 November). Thus the year is supported by the selected-year content, not solely a dynamic page title. The URL slug says 2019 but its currently indexed selection is 2025. A separate official national BPS indexed table with `?year=2024` independently confirms the old DKI totals; avoid confusing its dynamic 2025/26 title with its actual 2024 selection.

The current table title explicitly includes headmasters and teachers. These are counts of persons (headcount); no FTE conversion is supplied. Rows include both public and private SMA, all six administrative districts of DKI, not Greater Jakarta/Jabodetabek. SMA is general upper secondary; this does not cover SMK vocational or MA religious schools. It is not all-age attainment, school class size, or an educational-outcome measure. Preserve scope-conditional admission and exclusion in strict international comparability checks.

## Files and limitations

`jakarta_sma2025_transcription.csv` manually transcribes the official indexed table. `verify.py` checks every public/private total, all six district sums and presence of year/date/totals in archived indexed evidence. `observations.csv` and `summary.json` hold the candidate observation. No raw original table has been obtained: direct BPS HTML returned HTTP403 (response archived with explicit http403 filename); V6 official PDF URL timed out after35seconds. The 2026 publication entry exists, released27Feb2026, revised23Sep2026, but directopen also403. This is a newer-year indexed-official-source observation, not a completed raw-PDF provenance upgrade. The response archive contains incidental other search results; only the official BPS table supplies admitted values.

Run `python3 research/2026-a/data/task4_v29_jakarta_education/verify.py` from repository root. Checked on2026-11-07: all arithmetic and archived-year checks passed.

Official table: https://jakarta.bps.go.id/id/statistics-table/3/YTFsRmNubEhOWE5ZTUZsdWVHOHhMMFpPWm5VMFp6MDkjMw%3D%3D/number-of-schools--teachers--and-pupils-in-upper-secondary-schools-under-the-ministry-of-education--culture--research--and-technology-by-regency-municipality-in-dki-jakarta-province--2019.html

Publication entry (not used as downloaded evidence): https://jakarta.bps.go.id/id/publication/2026/02/27/6fbb5e306389718511827127/provinsi-dki-jakarta-dalam-angka-2026.html
