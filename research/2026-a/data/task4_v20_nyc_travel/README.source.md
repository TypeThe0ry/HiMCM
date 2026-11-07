# Official 2010/2011 NYC-area travel microdata

The NYMTC/NJTPA official public-use release was downloaded from the [NYMTC catalogue](https://www.nymtc.org/20102011-regional-household-travel-survey). `CSV.zip` is the untouched 34,043,273-byte archive; `public_data_manual.pdf` and `source_page.html` preserve its documentation and source. Hashes and original URLs are in `download_manifest.json`. ZIP CRC verification passed. Keep the archive compressed: several individual members exceed 50 MB. CSV text uses Windows-1252 encoding.

This is historical 2010–2011 data, not a 2023/2024 survey release. The current catalogue provides a 2023 request-for-information summary, while the downloadable release found here remains 2010/2011. A recent web-page date is not a survey observation year.

The public person file directly identifies current Grade 9–12 enrollment. Filter its decoded `STUDE` labels for full- or part-time students and `SCHOL` for Grade 9 to 12. Join households by `SAMPN` and identify NYC residence using numeric `CTFIP` values 36005, 36047, 36061, 36081 and 36085. The person `HFIPS` field contains decoded county names, not numbers. `SLOC=Yes` means home schooling; `SLOC=No` means outside-home schooling. No adult educational-attainment proxy is needed.

Linked trips provide recorded departure/arrival components and `TRPDUR` in minutes. `DTPURP` values 12/13 identify class/study or other school activities; `ORIG_HOME=1` identifies a home origin. `DOW` is Monday=1 through Friday=5. Do not use `TRPDUR_HN` (modeled highway-network time) or `TTTSS` (asked for bicycle school mode only). Duration comparisons require floating tolerance because minute fields have tiny representation errors.

The actual linked-trip key includes `TOUR_ID`: `(SAMPN,PERNO,TOUR_ID,LTRIPNO)` is unique, as is `PLSAM`. The manual's shorter three-field key is not unique in the CSV. `LTRIPNO` restarts within tours; first-school selection must use chronology relative to the 03:00 diary-day boundary or a verified place sequence.

For a one-student statistic use person-file `HH_WHT2` once per sampled person. `WHT_FAC3` is a trip-frequency weight including `TOURFAC`, and should not silently multiply the representation of students with several trips. Person and household weights agree to relative 1e-7 but are formatted at different precision. The released household-weight sum differs slightly from the manual's printed control total; this is recorded rather than silently rescaled.

Independent checks found 18,965 households, 43,558 persons, 143,925 linked trips and 479 current Grade 9–12 NYC residents, of whom 476 report outside-home schooling. Among the latter, 365 have a first school-directed linked trip directly from home with positive duration matching elapsed clocks. This is a sample count, not a city population count. Missing journeys, ambiguous membership, non-home origins, sampling uncertainty and historical scope still require explicit analysis. `source_schema_audit.json` records field/page locators and independent counts. Derived commute estimates are produced separately by the main extraction workflow.

The official public-use manual retains copyright, credits and its noncommercial-use disclaimer. No private or restricted individual-level location data was requested.
