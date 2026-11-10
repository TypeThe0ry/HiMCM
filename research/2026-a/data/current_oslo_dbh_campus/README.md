# Oslo DBH campus and public enrolment records

The public DBH API supplies municipality-coded campus and enrolment records beyond the earlier ROR city labels. In each examined semester, 25 institution codes have a positive public enrolment value in any teaching mode, while 23 have a positive value in mode1 or mode4. Campus registration alone lists26/26/26/27institution codes from2025spring through2026autumn. These are counts of visible reported codes under explicit filters, not a complete Oslo higher-education inventory or proof of the submitted25's original source.

| Period | Campus registry rows | Registry institution codes | Enrolment rows returned | Codes with positive value, any mode | Codes with positive value, modes1/4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2025 spring |35|26|46|25|23|
| 2025 autumn |36|26|46|25|23|
| 2026 spring |37|26|56|25|23|
| 2026 autumn |38|27|55|25|23|

## Source and extraction

Four requested DBH documentation/client pages returned403. Their error HTML bodies are retained with status403; they are not successful metadata downloads and were not retried. The separately documented public data endpoint succeeded for three bulk reference tables:002field metadata(1206rows),211institution metadata(293rows), and662campus registrations(3698rows). Table124was queried through a public, unauthenticated POST with2025/2026, semesters1/3 and campus municipality0301filters. Its203returned rows are preserved in the original BOM/semicolon CSV. `retrieval.json` records each URL, request UTC, status, final URL, content type, size and SHA256; the POST payload is `enrolment_query.json`. No authentication tokens, SSO access, bulk student microdata or external messages were used.

The source is [HK-dir's DBH public API](https://dbh.hkdir.no/dbhapiklient/), using its linked `dbh-data.dataporten-api.no/Tabeller/` endpoint. The API's institution/campus variable names and code labels are retained as returned. `Antall` has GDPRflag1 in table002; the precise privacy transformation of this response is unverified. Public numeric values are not asserted to be exact unrounded student counts, and zero/missing records are not treated as proof of no provision. Institution code0217has a registeredOslo campus but no returned row in each period. In2026autumn,26institution codes have returned rows,25have positive values. No zero is filled in for omitted data.

Mode1is labeled `Undervisning ved institusjonen`, mode4`Undervisning ved studiested (ny)`; both are retained in the narrow institution/study-site screen. Two2026rows still use code1. Other returned modes include decentralized teaching, online teaching, online with gatherings, and entirely online. The1/4screen does not exhaust physical activity: mode5explicitly includes gatherings. The registry itself also contains names such as Nettstudier, Online and Uplassert; label flags are diagnostics rather than exclusions. A stable code count does not imply an unchanged provider composition or a trend in provision.

`extract_campus.py` preserves146selected source rows and joins institution metadata by exact code, retaining all metadata candidates as JSON. The293institution codes are unique in this extract; none of the selected keys are duplicated. `extract_enrolment.py` preserves and classifies203rows, joins the exact year/semester/institution/campus keys to table662and saves period-specific code lists. It does not substitute institution headquarters addresses for campus municipalities, collapse institutions by similar name, interpret institution validity fields, or infer accreditation from activity.

The controlled count-definition comparison is documented separately at `../../results/current_oslo_dbh_review/README.md`. It changes one Oslo HE point in temporary copies; it does not admit a new primary value. Accreditation, reporting coverage, provider/campus rules, in-person availability, historical scope and the original25-entity lineage still need compatible evidence.
