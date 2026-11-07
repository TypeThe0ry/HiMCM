# Phoenix V39: Arizona add-on dictionary obtained

**No new city high-school commute observation admitted. Existing bounds unchanged.**

Reviewed V6/V7/V8/V27 before searching. The newly accessible official NLR-hosted 2017 dictionary is archived with SHA256. Unlike the earlier failed dictionary request, this round verifies its actual fields. `SCHTYP` distinguishes public/private schooling, home schooling and no schooling; `EDUC` measures attained education, not current grade. Age 14–18 plus these fields does not identify all and only current high-school students. `CITY`, `LATITUDE`, and `LONGITUDE` belong to the location table; their presence in a full dictionary does not establish their release in public non-spatial data. The NLR [spatial-access policy](https://www.nlr.gov/transportation/secure-transportation-data/tsdc-spatial-data) puts coordinates and other redacted fields behind an application and secure environment. No application was submitted and no travel microdata obtained. The web DOWNLOAD control returned the landing page.

The archived [MAG survey contractor announcement](https://etcinstitute.com/maricopa-household-travel-survey/) describes the 2024 survey and says individual responses will not be released. Its original MAG news link now redirects to the news index. This is a statement from the survey contractor, not proof that anonymised aggregates can never be obtained.

NHTS2022 geography limitations were already established in V7 and are not counted as new findings. A defensible next acquisition is an agency-produced aggregate with verified Phoenix residence, current grades 9–12, actual single-direction school-trip duration, respondent denominator and uncertainty. No regional mean or attained-education filter is substituted.

`field_audit.json` records exact workbook sheet/row locations for reproducible checking. `observations.csv` has no data rows. No model or manuscript changed.
