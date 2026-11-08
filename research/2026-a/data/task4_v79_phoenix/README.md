# Phoenix Union: actual 2025 report, staffing positions include vacancies

The district's official FY2025 Annual Comprehensive Financial Report supplies average daily membership 25,502 and teaching-staff FTE 1,635, yielding a published ratio 15.6. Its table explicitly includes both filled and vacant teaching positions. These numbers cannot be substituted for actual citywide high-school teachers and enrolled-student headcounts.

## Original evidence

The [district finance catalogue](https://www.pxu.org/documents/departments/finance-division/financial-reports/comprehensive-annual-financial-reports/24270626) exposes the [2025 report](https://files-backend.assets.thrillshare.com/documents/asset/uploaded_file/4844/Pxu/5276ce83-8c11-477b-b3a8-fcb72f200319/Phoenix_UHS_ACFR_25.pdf). Both original files are archived with hashes and retrieval URLs in `manifest.json`.

PDF page140 / printed133, Operating Statistics, FY2025 row:

| Field | Published value |
| --- | ---: |
| Average Daily Membership | 25,502 |
| Teaching Staff | 1,635 |
| Pupil–Teacher Ratio | 15.6 |

The footnote defines Teaching Staff as FTE positions, filled and vacant. PDF pages138–139 / printed131–132 separately report 1,635 instruction FTE positions as of June30,2025, again explicitly including vacancies. The operating table and footnote were visually checked against the original PDF. The teaching-staff values in earlier-year rows do not all equal the instruction-position series, so equality in2025 does not establish general identity across years.

## Consequence for model intake

This is new source content, not a repeated failure log. It explains why an apparently direct district PTR cannot resolve the current Phoenix indicator: ADM differs from a pupil headcount snapshot, positions include vacancies, the staff table is not split by current teaching grade, and the district is only part of Phoenix's public/charter/private school landscape. An FTE capacity count is not an observed teacher headcount. No Phoenix bound changes.

The SDER-77 district endpoint for entity4286 remained inaccessible in this check. Its reporting route remains documented in [V78](../task4_v78_phoenix/README.md); the Maricopa county totals were already recorded in [V13](../task4_v13_scope_audit/README.md), and are not new observations here. The next useful staff source must identify filled positions or actual teacher records with secondary/combined assignment and city coverage.

`python3 research/2026-a/data/task4_v79_phoenix/extract.py` verifies original hashes, FY2025 row values, the vacancy footnote, and arithmetic. This verifies the published statistic and definition; it does not certify school coverage or turn a statistical appendix into an audited staffing census.
