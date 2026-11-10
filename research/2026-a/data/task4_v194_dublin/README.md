# V194 Dublin: allocation records do not identify employed teacher FTE

Two new official routes yield four archived HTTP 200 responses and **zero model admissions**. The retained Dublin pupil–teacher utility stays unchanged; actual score-width improvement is zero.

The [NCSE 2024/25 catalog](https://opendata.ncse.ie/en_GB/dataset/2024-2025-school-allocations) links a post-primary allocation CSV: 722 records, including 183 labelled County Dublin. Its columns describe special-education hours/posts and SNA allocations. They give neither total employed teaching workload nor pupil counts. Allocations cannot establish filled posts, and postal areas have not been joined to the retained city boundary. No pupil–teacher bound is inferred.

The [official workforce methodology hub](https://nationaldata.ie/Standards/NationalDataMethodologyHub/DepartmentofEducationandYouth/TeacherWorkforceData/) and linked six-page methodology distinguish payroll from allocations and describe county/national summaries. The hub labels 2015–2023 coverage; the PDF's January 2026 example refers to 2025/26. Neither file supplies the required city/ISCED3 numeric envelope. A browser follow-through to its CSO product link redirected to an empty root page; it supplied no data and was skipped.

`retrievals.json` binds original bytes, URLs, actual UTC timestamps, statuses and SHA-256 hashes. `extract.py` verifies the originals and parses the CSV using cp1252 (UTF-8 fails); embedded header newlines are preserved. `findings.json` records scope decisions. The PDF text is derived, not an original. No raw user input, model, current registry or manuscript was edited.
