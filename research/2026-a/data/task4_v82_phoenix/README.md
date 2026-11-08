# Phoenix Union: matched district enrollment and classroom FTE

The original [NCES district page](https://nces.ed.gov/ccd/districtsearch/district_detail.asp?DistrictID=0406330&ID2=0406330&Search=2&details=1) reports 2024/25 enrollment of 25,800 and classroom teacher FTE of 1,349.60. The displayed ratio is19.12. Directory information refers separately to2025/26. The downloaded HTML is retained byte-for-byte with [manifest](manifest.json).

[Reconciliation](school_crosscheck.csv) uses the existing V42 school originals: 21 school memberships sum to25,800; the20 nonmissing staff values sum to1,349.60. Phoenix Educator Preparatory has zero enrollment and FTE sentinel−1, which is excluded rather than treated as a count or observed zero. The known-staff, nonvirtual subset contains19 schools,25,730 students and1,321.8 FTE. The virtual school contributes70 students and27.8 FTE.

The district-only resource diagnostic is $15T/(N+15T)=0.439666$. It measures staffing resources, not learning quality. This matched pair cannot replace the complete Phoenix city indicator: district boundaries, private coverage, virtual inclusion and exact student ages remain different from the target. `main_admitted=false`.

## Workforce records and next acquisition

The [FY2026 TIA guide](https://www.azed.gov/sites/default/files/2025/07/FY26_TIA-support-guide_Final_7.18.25.pdf), reader text pp25,27,29, specifies assignment-level grade/period entries, multiple position records per educator, reporting long-term substitutes, and retaining exiting/transferring staff through the fiscal year. [Review](tia_reader_review.json) records these findings; original PDF retrieval and screenshot rendering returned403. They motivate person/position deduplication and date filtering, but do not prove the exact cause of V81's category overlap or the FY2025 dashboard's aggregation. A usable TIA extraction needs school identity, anonymous educator key, grades, instructional periods, position status, start/end dates and reference date; it must then align students and physical-school coverage.

Run `python3 research/2026-a/data/task4_v82_phoenix/extract.py`. It checks original and reused hashes, parses the district totals, rejects missing-value arithmetic and reproduces [summary](summary.json). No model or manuscript files changed.
