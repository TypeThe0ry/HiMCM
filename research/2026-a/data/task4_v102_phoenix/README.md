# Phoenix: school-hosted annual financial report provides actual teacher FTE

North Star Charter School's FY2025 Annual Financial Report reports **6 teacher FTE: 3 certified, 3 noncertified and 0 contract** (Page 6, T6:T8). Its school listing names Arizona Preparatory Academy, CTDS078945201, as its sole listed school. These are explicitly reported FTE counts, independently of salary amounts; no salary-ratio inference is used.

The retained V42 NCES2024–25 record independently reports the same **6 FTE**, with **233 pupils in grades9–12** for NCES040030302181 (LEA0400303, state LEAAZ-79701). Thus this new financial original corroborates an existing later-year CCD value; it does not add6 to a previously known total. The workbook gives prior-year average salary but no verified prior-year teacher-FTE cell was found.

The original XLSX was downloaded from [Arizona Preparatory Academy's website](https://www.arizonapreparatoryacademy.com/). `manifest.json` records the file URL, byte count and SHA-256. `extract.json` preserves the cells, teacher definition and name/operator crosswalk to the V85 missing record NCES040030302181. The workbook's Instructions!C34 requires mutually exclusive teacher categories, permits fractional FTE and excludes instructional aides/assistants.

**This source covers FY2025, July2024–June2025, and does not fill the FY2023/24 CCD gap.** The charterwide value is retained as separate evidence. A matching fiscal year and teacher snapshot, grade/campus attribution, and the remaining public/private school coverage are required before it can tighten Phoenix's model interval. No city rank or bound changes follow from this file alone.

The school's separately linked FY2024 candidate download on the ADE budget portal (submissionReferenceId218180) returned403. The source workbook here is the successful school-hosted FY2025 download, not that blocked response. ADE's indexed SAFR definitions describe year-end teacher positions, reinforcing the need to distinguish these from a fall CCD snapshot; that blocked PDF is not used as an archived numeric source.

Run `python3 research/2026-a/data/task4_v102_phoenix/verify.py` from the repository root. It checks original bytes, reported FTE cells, period, school listing, definition and the retained V85 crosswalk, and emits the reproducible extraction. It does not establish equivalence of financial and CCD reporting dates or citywide completeness.
