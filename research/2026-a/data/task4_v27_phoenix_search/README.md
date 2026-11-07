# Phoenix: new district evidence, unchanged city bounds

No new city-level observations are admitted. Phoenix high-school commute and education missing-data bounds remain unchanged. This bounded search checked prior V7/V8 travel and V9/V14/V24/V25 graduation audits before looking for additional official district reports.

The archived [FY2025 district spending report](pxu_fy2025_spending.pdf), produced by the Arizona Auditor General and hosted by PXU, reports 18.3 students per certified teacher for FY2025 (PDF p11), 18.0 for FY2024 (p14), and a rounded 77% graduation rate labelled 2024 (p1). The ratio includes specialist teachers; headcount versus FTE is not established by this document. These are genuine high-school-district observations, but district coverage does not establish Phoenix city coverage. No city ratio is inferred. `diagnostic_observations.csv` preserves the limited observations and page references.

The [2009 performance audit](pxu_2009_performance.pdf), PDF p32 / printed p21, says the district had not established and monitored transportation performance measures, including ride times. It supplies no usable commute-duration distribution and cannot describe present-day performance. Current spending-report transportation cost measures are N/A, not zero.

Feasible integration: retain these district observations in the evidence appendix. To admit a city teacher ratio, obtain compatible school-level student and teacher counts, establish headcount/FTE semantics and historical city coverage, and preserve missing-school bounds. To admit commute utility, obtain an observed home-to-school duration distribution with a Phoenix high-school denominator and survey design. Procurement time limits are service targets, not observed journeys.

`manifest.json` contains exact URLs, successful HTTP status, original-file byte sizes and SHA-256 values. PDFs are byte-preserved; text files are pdftotext derivatives. Checked the reported values against extracted PDF text. `observations.csv` intentionally has no data rows. No existing inputs, scripts, or rankings were edited.
