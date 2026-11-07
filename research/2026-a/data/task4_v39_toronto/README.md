# Toronto V39 — independent public day-school FTE diagnostic

**Decision: retain missing in the main city model.** This package establishes jurisdiction and improves the matching of two administrative measures. It computes a conditional diagnostic envelope, not a city observation, teacher-headcount PTR, 14–18 resident ratio, or education-quality score.

## New evidence

The City of Toronto's `jurisdiction.html` explicitly identifies Toronto as the jurisdiction of TDSB and TCDSB and states that Viamonde/MonAvenir boundaries extend beyond Toronto. `four_boards.html` and `ward_reference.pdf` identify the four publicly funded systems serving Toronto. This establishes jurisdictional containment, not the residence of every enrolled student or the physical location of every board-operated program. The four systems also do not encompass private schools, separate hospital school authorities, or provincial schools.

Official 2024–25 EFIS staffing instructions (`staffing.html`) establish actual October 31 position FTE, prorated regular/special-program allocations, and separate ECPP staff. The teacher total includes instructional time of principals/vice-principals and resource teachers; it excludes library/guidance staff reported elsewhere. It is therefore described here as *classroom instructional FTE*, not all teacher headcount.

Official 2024–25 enrollment register instructions (`register_instructions.pdf`, printed p.40; extracted text lines 2183–2188) exclude ECPP/hospital/provincial-program attendance from the regular register. Accordingly, ECPP instructional FTE is subtracted from the denominator. This avoids charging ordinary day-school pupils for staff serving excluded programs. The Ontario.ca PDF endpoint returned403; the identical-titled Ministry EFIS-hosted PDF downloaded successfully. `pdftotext` completed with two PDF name-token warnings; the relevant passage is legible.

## Computation and limits

Run `python3 derive.py`. It reads the unchanged V38 financial-statements CSV and saves its SHA-256, every source-cell identifier, four board subtotals, and a diagnostic result. All enrollment components are October pupil FTE; neither ADE nor rounded grade headcounts are mixed in. Separate high-credit, age21+, and other-pupil components are included once. The other-pupil aggregate rows are deliberately not added again.

Let E denote the two English boards, F the two full French boards, S student FTE, and T regular plus special classroom instructional FTE minus ECPP. Derived totals:

| Component | E | F |
|---|---:|---:|
| October secondary pupil FTE | 102286.05 | 6798.02 |
| Non-ECPP classroom instructional FTE | 6656.1 | 594.9 |

For unknown Toronto French allocations satisfying `0 <= s <= S_F` and `0 <= t <= T_F`, the conditional ratio is `(S_E+s)/(T_E+t)`. Its conservative outer envelope is:

`S_E/(T_E+T_F) <= R <= (S_E+S_F)/T_E`, or **[14.106475, 16.388586] pupil FTE per instructional FTE**.

No proportional French allocation is assumed. The endpoints are outer bounds, not evidence that a real combination of schools attains them. The central whole-four-board ratio is not a Toronto measurement.

**Unresolved matching condition:** the enrollment extract includes a small age21+ category, while Appendix H separately reports adult-day/continuing programs. We have not established that every pupil FTE in the nine chosen cells maps to the exact non-ECPP secondary instructional cells, rather than part of adult-day staffing. Nor does jurisdiction prove that every included service is physically inside the municipality. These conditions prevent treating the envelope as a verified municipal PTR. It is usable only as a separately labelled diagnostic of the explicitly stated coverage assumptions; it must not shrink the main model's missing interval or possible-winner set.

## Artifacts

- `manifest.json`: official document URLs, raw-byte hashes, retrieval date.
- `source_cells.csv`: exact 12 source rows (nine pupils, three staffing).
- `board_fte.csv`: board subtotal calculation.
- `conditional_diagnostic.json`: assumptions and outer envelope.
- `derive.py`: reproducible extraction; positive denominator checks.

Next decisive evidence: a school/program roster matching pupil FTE to staffing, including adult-day classification and municipality. Residence-based analysis additionally needs pupil residential geography; school-board jurisdictions cannot substitute for it.
