# V96: grade 11 workbook acquisition remains unresolved

No new Phoenix test records or denominators were obtained. The alternate public `www.azed.gov` URLs for both FY2025 workbooks returned HTTP403 and 4,551-byte HTML responses, matching the earlier CMS access obstacle. They were not saved or treated as Excel files. URLs, response hashes and temporary evidence locations are recorded in [access_checks.json](access_checks.json).

A search-index lead, [Arizona High School Rankings](https://azschoolrankings.com/data-sources), describes a derived FY2025 grade11 export, but its live page failed DNS resolution locally and returned502 through the reader. No export or original workbook was acquired. GitHub filename searches returned only an earlier HiMCM note for the math/ELA file and no science-file result; this limited search does not establish absence of a mirror.

## A newly checked repository does not supply this population

The Education Data Center's [State Assessment Data Repository](https://education-data-tracker.vercel.app/data) has a downloadable original [Version3.1 technical guide](https://education-data-tracker.vercel.app/data_documentation/EDC_technical_documentation_v3.1.pdf), acquired as1,100,602 bytes. Its inclusion section on printed page7 restricts the repository to grades3–8. Although its coverage extends through2024–25, those records cannot fill the missing Phoenix11th-grade counts. The guide also describes count substitutions for some state-years; no such substituted count is introduced into our assessment table.

The acquired document is a provider's guide to its own data coverage, not an ArizonaFY2025 API codebook. It does not resolve the current API brand mapping, suppression meanings or percentage rounding. All existing108-school evidence and unknown-count intervals remain unchanged.

`audit.py` verifies the original PDF hash, page count and inclusion statement. [manifest.json](manifest.json) records its source bytes; [source_checks.json](source_checks.json) separates the unacquired workbook/export leads from the acquired coverage document. No access request, authentication bypass, model edit or manuscript edit occurred.

```sh
python3 research/2026-a/data/task4_v96_phoenix/audit.py
```
