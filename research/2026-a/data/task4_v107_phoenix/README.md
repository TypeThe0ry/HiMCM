# Official report-card UI clarifies the All Enrolled population

The archived Arizona Department of Education report-card page defines **All Enrolled as students who were both tested and enrolled at the school**. It is not a count of every enrolled student regardless of testing. The same tooltip distinguishes part-year and majority-of-year enrollment among tested students.

The official frontend's `assessment-results` component uses this template, requests `Assessment DetailsFAY` forFY2021 onward, and filters returned `fayType`. This directly connects the published explanation to the endpoint family used by V92–V94. The FY2025 rendering also treats `numberTested=-11` as suppressed. The original page and script are retained with URL, date, bytes and SHA256; `verify.py` reproduces the checked assertions and `definitions.json`.

This resolves a specific population-label ambiguity. It does not establish the legacy `type=1`/`AzMerit` brand mapping to ACT, the corresponding science test, the exact FAY dates, valid-score inclusion rules, or unique-pupil deduplication. No new interpretation of319 school–subject records or revised city quality statistic is asserted. In particular, statewide federal-accountability proficiency formulas cannot automatically supply the denominator for this public All Enrolled display.

Targeted official-source searches also located FY2025 accountability business rules and assessment overview pages, which name ACT/AzSCI generally. Those general programme names are not an API-field crosswalk and were not adopted as one. The previously blocked assessment workbook was not retried. No observations, model inputs, rankings or manuscript sections are changed.

Run `python3 research/2026-a/data/task4_v107_phoenix/verify.py`. This is a source-definition package; it contains no student-level response data.
