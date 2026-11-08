# Phoenix: direct teacher grade-assignment route

ADE's public SDER-77 reports distinguish secondary, elementary and combined grade assignments, with separate headcount and FTE columns. The October2021 SDER manual defines secondary assignment as grades9–12. This offers a more direct acquisition target than inferring a teacher's assignment from a school's grade range.

[Selected web-reader findings](web_reader_extract.md) record the official URLs, source pages, period and county fields. They are transcribed/paraphrased reader evidence, **not original PDF files**. Direct downloads and subsequent reader reopens returned403; [retry response](retrieval_retry.json) preserves that failure. No failed response is represented as source content.

## What the new route resolves and leaves open

The grade-assignment field exists and public SDER-77 reports are available at least at state/county level. The manual permits itinerant staff to be assigned administratively to one school; the report also includes adult education and administrative-office teachers. Consequently, neither an individual school's grade range nor the report's secondary total alone proves actual classroom allocation to Phoenix high-school students.

The county values are source-discovery observations. They are not a Phoenix teacher pool or an upper/lower bound. Charter coverage, city membership, adult and administrative duties, purchased-service treatment and the reporting period must be matched before admission. No current model interval or manuscript is changed.

## Concrete next acquisition

Obtain the FY2025 SDER-77 for Phoenix Union High School District, official entity4286, and relevant other Phoenix-serving LEAs. Request or retrieve the existing grade-assignment categories and their FTE, then match those records to school/city coverage and relevant teaching roles. Preserve Combined allocation as unknown. Determine whether the published report covers charter staff and intergovernmental arrangements; do not assume a district report is a complete city inventory. No institution has been contacted and no private personnel records have been accessed.

`python3 research/2026-a/data/task4_v78_phoenix/verify.py` checks archive hashes and arithmetic of the selected Maricopa row. It does not validate original PDF bytes, source completeness or city applicability.
