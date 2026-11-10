# Zürich school-staff data: official request route

The Zürich Bildungsplanung offers tailored education statistics, providing a route to request a compatible city-level pupil-to-teacher ratio. The three preserved sources do not publish the required city-by-stage teaching full-time equivalents (FTE) and matching pupil count. **No new value is admitted to the model.**

## Evidence

- [`request_page.html`](request_page.html): the [cantonal request page](https://www.zh.ch/de/bildungsdirektion/generalsekretariat-der-bildungsdirektion/bildungsplanung/anfragen-an-die-bildungsplanung.html) offers tailored data about learners, school staff and completions and gives `bista@bi.zh.ch` as the contact.
- [`survey_coverage.html`](survey_coverage.html): the [cantonal SSP survey page](https://www.zh.ch/de/bildung/bildungssystem/studien-in-der-bildung/lehrpersonen-und-schulpersonal.html) describes an annual census of teaching and leadership activities at schools located in the canton, including upper-secondary education. Public and private schools are among its suppliers. The reference date is 15 September, except 1 November for tertiary education. Survey coverage alone does not establish that the requested breakdown is complete or releasable.
- [`ssp_activity_35956351.pdf`](ssp_activity_35956351.pdf): the [Federal Statistical Office SSP profile](https://dam-api.bfs.admin.ch/hub/api/dam/assets/35956351/master), page 1, lists activity identifier, personnel category, contract type, qualification, school identifier, workload (`Pensum`), full-time basis (`Basis Vollzeit`), and school type (`Schulart`) as activity-level characteristics. It describes an annual individual-data census. Page 2 lists cantons as the regionalisation level and ZAS and BUR as linkages. The profile does not define a detailed FTE conversion, prove allocation to city and stage, or publish the desired city aggregate.

[`retrieval.json`](retrieval.json) records URLs, final URLs, UTC retrieval times, statuses, byte counts, SHA-256 hashes and selected response headers. Original response bodies are retained separately. [`scope.json`](scope.json) records the admission decision and request scope.

## Proposed request — not sent

Ask Bildungsplanung for an aggregate for the **same specified school year** and schools physically located in **Stadt Zürich**:

1. Actual **Sekundarstufe II teaching FTE**, summed from teaching activities, excluding leadership and other non-teaching duties; specify the workload-to-FTE calculation, imputation and allocation across institutions and stages.
2. The corresponding pupil count for the same school locations, programmes, provider coverage, study modes and year. Identify the student reference date, age and part-time treatment, and any difference from the staff reference date.
3. All providers combined and public/private breakdowns if available, with included school types and programmes. Identify lower-secondary components in mixed schools and how they are excluded or allocated.
4. Counts or FTE that cannot be assigned to a city location or stage; treatment of multi-site and cross-municipality institutions; missing coverage, suppressed cells, revisions and any remaining numerator–denominator mismatch.

Request aggregate statistics and methodology, not individual records. A school-location pupil count is not a count of Zürich residents: it includes incoming pupils and excludes residents studying outside the city. The agency's response and its actual coverage must be assessed before calculating or admitting a ratio.
