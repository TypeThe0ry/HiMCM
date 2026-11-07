# Phoenix V42: full public-school coverage and missing-enrolment follow-up

The previous highest-grade12 query is replaced by a complete Arizona NCES EDGE2024–25 collection: **2,628 unique school records**, fetched in six ID-checked pages. No Arizona geometry is missing. The same archived Phoenix boundary contains **534** schools; **144** operating nonvirtual schools have grades9–12 in their offered range or recorded enrolment. The roster includes 88 exact9–12 schools, 91 schools whose entire offered range lies within9–12, and 53 mixed/other-range schools.

The earlier query omitted Keystone Montessori Charter School (grades1–9). Its grade9 count is actually **0**, and grades10–12 are structurally not applicable; its13 FTE cannot be allocated wholesale to high school. Expanding the query corrects coverage even though this added school's observed high-school enrolment is zero.

## Enrolment bounds

For each school, add nonnegative G09–G12 values. A -2 code becomes structural zero only when that grade lies outside the reported offered range. Other negative codes remain unknown. When target grades are missing and MEMBER is valid, their joint upper bound is MEMBER minus known non-target pupils (PK,KG,G01–G08,G13,UG; adult education excluded consistently with MEMBER). No per-grade upper bounds are summed independently. All original codes remain in the audit.

There are no grade-total/MEMBER contradictions. Known grade9–12 school records total **70,678**. Only **Hope College and Career Readiness Academy**, NCES040386003535, lacks a finite total upper bound: G09–G12 and MEMBER are all-9. Its FTE is4. Therefore the unmodified CCD-only aggregate upper bound remains unknown. Twenty-nine relevant schools have missing/negative FTE.

## New actual Hope observation

ADE's official Student Enrollment API returns FY2025 for entity969999: grade9=19, grade10=33, grade11=86, grade12=1040; sum=ALL total1178. The official NCES ID linkage was already established in V9. This response is archived, hashed and checked; subgroups are not added to the All rows.

API snapshot compatibility with CCD has not yet been demonstrated. The official October1 workbook was located at <https://www.azed.gov/sites/default/files/2025/04/Oct1EnrollmentFY2025.xlsx>, but normal local download returned403 from both www and cms hosts. The web reader recognizes the workbook content type. Do not substitute the1178 automatically. If the same-school and same-snapshot linkage is verified, the conditional total becomes **71,856**. Until then this is an observed alternate-source candidate, not a certified bound.

Scope is school records located within today's Phoenix boundary, not unique resident students; public nonvirtual schools only. Current versus historical locations, cross-school student duplication and private-school coverage remain explicit. No teacher headcount is inferred from FTE and no mixed-school teacher allocation is invented. Main model and manuscript unchanged.

Run `python3 research/2026-a/data/task4_v42_phoenix_coverage/collect.py`; original successful pages are cached. See `manifest.json`, `phoenix_secondary_roster.csv`, and `hope_source_audit.json`.

## Strict known teacher-FTE lower sum

`bound_fte.py` admits FTE only where the entire offered range lies within9–12, every non-target grade field (PK,KG,G01–G08,G13,UG,AE) is zero or structural -2, and FTE is nonnegative. It produces a **67-school known sum of 2,512.97 FTE**, including Hope's4 FTE. Missing FTE contributes no observed amount; it is not imputed as zero. All144 eligibility decisions and the67-school contributing list are saved separately. Mixed-stage teachers never enter this known lower sum.

The lower interpretation assumes comparable, additive school-assigned FTE rather than repeated full counting of shared staff; it is not unique teacher headcount. With Hope's CCD enrolment unresolved, total students still have no finite upper bound, so this teacher sum alone cannot produce a positive city education-utility lower bound. The1178 alternate enrolment remains explicitly conditional on snapshot/coverage compatibility, with no baseline change. Both normal browser/web and local requests for the official October1 workbook were blocked; no further identical retries were made.

Reproduce with `python3 research/2026-a/data/task4_v42_phoenix_coverage/bound_fte.py` after `collect.py`.
