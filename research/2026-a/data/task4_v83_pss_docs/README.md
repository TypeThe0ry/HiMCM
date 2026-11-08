# NCES PSS 2023/24: enrollment, teaching time and coverage definitions

Six official originals support the [Phoenix private-school audit](../task4_v83_phoenix_private/README.md). Download URLs, byte lengths and SHA-256 are in [manifest.json](manifest.json). The [2026 user manual](https://ies.ed.gov/nces/2026/09/nces-2026035-2023-24-private-school-universe-survey-pss-public-use-data-file-users-manual) was retrieved as an original PDF. Questionnaire, layout, codebook, release readme and TABFLAG explanation came from the official PSS data page. `definitions.json` records the relevant mapping.

## Correct interpretation

- Questionnaire Q4 (PDF pages 4–5) asks enrollment around October 1, 2023. Grade 9–12 counts are P270, P280, P290 and P300. Their paired enrollment-presence fields are P265, P275, P285 and P295. Code 1 means students are enrolled; code 2 means none in that grade. A blank count can be converted to a structural zero only after checking the paired field equals 2. The codebook distinguishes these valid skips from nonresponse.
- Q10 (PDF page 9) counts time spent teaching K–12 or comparable ungraded pupils at this school. It includes subject specialists and administrators who regularly teach, but excludes teachers teaching only pre-K, adult or postsecondary classes, aides and short-term substitutes. The counts are not allocated to high-school grades.
- NUMTEACH is an estimated FTE derived from five work-time categories, rather than measured individual hours. User manual PDF page 30 / printed 26 defines `P385 + .875*P390 + .625*P395 + .375*P400 + .125*P405`. Conditional on the categories, a closed outer interval for teaching time uses lower coefficients `(1,.75,.5,.25,0)` and upper coefficients `(1,1,.75,.5,.25)`. These endpoints bound category uncertainty; they do not resolve imputation, high-school allocation or unobserved schools.
- Layout PDF page 4 and questionnaire Q21 (PDF page 15) distinguish mailing PCITY from physical PL_CIT. Coordinates support a boundary check; school-year versus boundary-year differences must remain explicit.
- Manual PDF page 24 / printed 20 defines F_Pxxx flags: 0 original, 4 donor-imputed, 5 analyst-adjusted. Check the component flags when interpreting the derived FTE.

## Population coverage and uncertainty

The release readme identifies 22,510 responding schools only. The user manual describes a list frame plus sampled area frame and nonresponse weighting. Printed page 2 reports an estimated conservative traditional-school coverage rate of 73.14%, and notes Arizona did not supply a state list during the frame update. That national coverage figure cannot be used as Phoenix's local missing fraction.

PFNLWT adjusts for area sampling and school nonresponse. The 88 REPW variables support balanced repeated replication (manual printed pages 3–5). Unweighted records describe observed schools, not a complete city total. Weighted city estimates also need appropriate domain variance and coverage analysis; the presence of weights does not establish complete physical-city enumeration. The PSS target excludes organizations providing home-school support without classroom instruction. The questionnaire includes a virtual/hybrid question, which should be checked separately from physical school coordinates.

TABFLAG describes traditional versus kindergarten-terminal schools; it is not a high-school-stage filter. Use grade counts and offered fields directly, retaining ungraded cases separately.

Run `python3 research/2026-a/data/task4_v83_pss_docs/verify.py` to verify original hashes and the key wording. This package changes no model interval and contains no manuscript edits.
