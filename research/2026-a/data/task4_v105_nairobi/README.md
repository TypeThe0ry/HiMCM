# Nairobi V105: newest national workbook does not supply city staffing

The newly downloaded official **KNBS Economic Survey 2026** education workbook reports provisional **2025** national secondary enrolment of **3,338.818 thousand** (Table 15.8, AH9) and **131,501** teachers in **public secondary schools and teacher training colleges combined** (Table 15.11, Y8). These are different coverage definitions and are not a matched Nairobi pair. The teacher table measures persons by qualification/sex, not verified FTE, and excludes teachers on unpaid study leave and those with disciplinary cases.

The workbook contains 32 tables. Secondary enrolment and relevant teacher tables are national; Nairobi-name rows in other tables concern university/adult education and cannot provide a secondary numerator or denominator. The 2025 Form 1 cells in Table 15.8 are blank while Forms 2–4 sum to the displayed total. The blank is recorded explicitly and not converted to an observed zero or interpreted as a policy effect without further documentation.

No positive Nairobi teacher lower bound follows from this national total. Nor is it a complete upper bound on all city teachers: the public/TSC scope leaves other teacher categories unresolved. Therefore the main education utility interval remains **[0,1]**, without combining the new national figure with older city enrolment.

V35, V45, V61 and V98 were checked before retrieval. Their TSC/BOM/private and common-reference-date gaps remain. The Nairobi County website still yielded the May 2024 notice announcing development of a county statistical abstract, rather than a retrieved final county table. No duplicate failure responses are included in this package.

## Source and verification

- [Official 2026 release page](https://www.knbs.or.ke/reports/2026-economic-survey/)
- [Original education workbook](https://www.knbs.or.ke/wp-content/uploads/2026/10/Chapter-15-Education-and-Training.xlsx)
- [County abstract development notice](https://nairobi.go.ke/nairobi-county-commences-development-of-county-statistical-abstract-2024)

`manifest.json` records original bytes and SHA256. Run `python3 research/2026-a/data/task4_v105_nairobi/extract.py` with the Python standard library. It validates the original hash, same-year headers, teacher qualification sums, enrolment subtotal, and explicit blank Form 1 cell; `summary.json` distinguishes national background evidence from city admission. No microdata, model, registry, or manuscript changes are involved.
