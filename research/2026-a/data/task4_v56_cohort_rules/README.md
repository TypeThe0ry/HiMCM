# V56 — Arizona cohort responsibility audit

## Finding

The FY24 ADE technical manual provides more than the previously archived single-graduation-code rule: it defines both the outcome date and last-school/LEA responsibility. This supports a conditional district-to-school reconciliation, but does not establish that the archived district API is an independently deduplicated extract or that all excluded historical provision has been identified.

The manual was accessible through indexed official-source text; direct PDF retrieval returned HTTP 403. `official_rule_extract.json` is a short paraphrase, not an original PDF archive. No new student records or transfer counts were obtained.

## Reconciliation conditions

Let D be the unique cohort2024 persons assigned to PXU, O the persons assigned to excluded provision, and T the target physical Phoenix school population. District subtraction requires that D minus O is contained in T. A current address roster alone does not establish this: the manual retains responsibility for students no longer enrolled in their graduation year. Also establish consistent cohort/outcome cutoff and the same final correction snapshot.

Existing official API observations are PXU N=6285/G=4813/F=1472 and Digital Academy N=485/G=286/F=199. These come from `../task4_v55_phoenix_outcomes/pxu_graduation_fy2025.json` and `../task4_v9_phoenix/spatial_responses/875776.json`. Both use fiscalYear=2025 and studentGroupDescription=All. These exact files have compatible field names; do not confuse them with other school-export schemas. F=N−G is derived, not an explicit dropout count.

If uniqueness, complete exclusion coverage, and status-specific compatibility hold, the target lower counts are G>=4527 and F>=1273. These need not be exact city counts. If only a valid upper cap of 485 excluded unique persons is established, without status-specific compatibility, conservative lower counts are G>=4328 and F>=987. Without complete exclusion coverage even these latter counts cannot enter the evidence bound. Multiple subtraction scenarios are not new observations.

The report-card frontend labels FY2025 as cohort2024, consistent with the manual. Its display logic does not perform or document person-level deduplication. `noofRecords=1`, equal male/female sum checks, and matching rounded percentages cannot establish unique persons, cross-entity membership, transfer reconciliation, or same correction snapshot. Transfer numbers cannot be reconstructed from these aggregates.

## Decision

Retain the existing evidence interval pending historical responsibility coverage and verified aggregate membership. Treat district subtraction as a clearly conditional sensitivity scenario only. No city model input was modified in this audit.
