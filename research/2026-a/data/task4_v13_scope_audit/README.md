# New scope evidence and a corrected admission rule

ADE's FY2024–25 SDER77 supplies both teacher Count and FTE. Its Maricopa Secondary row has Count9,565 and FTE9,618.50; female and male subtotals independently sum to those totals. This is a concrete counterexample to the assumed universal inequality FTE<=headcount. The report includes adult education and teachers working from administrative offices. Neither these county totals nor Phoenix's existing complete-school FTE subset establishes a Phoenix all-high-school headcount ratio. Keep Phoenix PTR [0,1]. `sder77_counterexample.json` records the exact official URL and indexed transcription; direct PDF download failed and no PDF original is claimed.

Tokyo2018 official PT classification and report were downloaded and hashed. The public occupation category combines children, pupils and students, with age bins such as15–19; home-to-school purpose is available but current upper-secondary stage is not separately identified. Age15–19 cannot replace current high-school enrollment. These files do not provide a new admissible Tokyo HS duration, so its interval remains unchanged. Only the source files supporting this finding are archived; no repeated archive of unrelated historical handbooks was added.

## Actual code defect fixed

V5 previously admitted any finite observation whose status did not begin with missing or scope_mismatch. A diagnostic subset with a finite FTE ratio would therefore be accepted if placed in a baseline observations file. V6 accepted any observed_ status with a unit containing the substring headcount, including a misleading not_headcount unit or an unreviewed mixed-grade subset. These permissive checks contradicted the headcount target and the existing evidence policy.

V5 now admits reviewed statuses per source package and requires the exact headcount unit for the teacher ratio. V6 admits only reviewed status/unit pairs, preserving the separately documented headmaster-inclusive condition. New status labels require review rather than automatic admission. This is a metadata consistency gate, not proof that a source is true or that its scope is complete.

Six regression checks reject diagnostic FTE rows, FTE units under an approved status, unknown observed statuses, headcount substrings and mismatched teacher definitions; the sixth verifies all250 existing admitted utility endpoints against archived V7 values. Fresh rankings in `../../results/task4_v13_admission/` confirm zero changed input cells and ranks and25 possible champions. The fix prevents erroneous future tightening; it does not claim new data or current ranking improvement.

The score remains S_i=100 sqrt(sum_j w_j u_ij²)/(sqrt(sum_j w_j u_ij²)+sqrt(sum_j w_j(1-u_ij)²)), with u_ij in reviewed evidence intervals. Main weights are (1-alpha)/8, auxiliary alpha/2; current alpha=.1. Score endpoints L_i and U_i yield possible champions U_i>=max(k!=i)L_k and decision regret max(0,max(k!=i)U_k-L_i).

```sh
python3 research/2026-a/scripts/test_task4_headcount_admission.py
```
