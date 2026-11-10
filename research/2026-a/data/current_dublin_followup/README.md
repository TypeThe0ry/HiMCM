# Dublin school-resource follow-up

No matched Dublin City secondary pupil / teaching-FTE ratio was found in the two focused searches. No value or bound is proposed for admission.

The [official data.gov.ie catalogue](https://data.gov.ie/en_GB/dataset/schools-in-dublin-region?package_type=dataset) identifies a 2019–20 Dublin-region post-primary school workbook and states that the data can be queried by council area. Its downloaded workbook includes school roll number, local authority, fee-paying status and total enrolment, but its 24 column headings contain no teacher count or teaching FTE. Its enrolment data alone cannot establish a city pupil/teacher ratio or an upper-secondary-only ratio. It is a potential school-location and pupil-data lead, not a matched denominator. Coverage of all providers and its comparability to the current criterion remain unverified.

The [Department's individual-schools collection](https://www.gov.ie/en/department-of-education/collections/data-on-individual-schools/) appeared in search as school-level enrolment data; direct retrieval returned HTTP 403. The search extract is not a captured original and does not establish school-level teacher FTE. The earlier payroll quality report in `../task4_v124_education/README.md` records that school-level FTE is not published in that dataset; this does not prove that no other source exists.

`manifest.json` records the exact two queries, retrieval times, HTTP outcomes, original response hashes and source scope. The successful catalogue HTML and XLSX are unmodified source bytes. The workbook headings were inspected with Python's standard-library ZIP/XML reader. No CSV, population, weights, model, manuscript or registry was modified.
