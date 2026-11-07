# V42 read-only audit of Toronto V41

**No numerical or cohort-matching bug found in the reported V41 conditional ranges.** This audit does not change V41 files, the main matrix, or a manuscript. It uses existing downloaded originals only.

`python3 audit.py` independently reads EQAO ZIP members and verifies all108 Grade9 and109 OSSLT reportable school records:

- Grade9 successful count equals Levels3+4; all achievement outcome counts sum to fully participating; registered students equal participating plus no-data students.
- OSSLT records are first-time eligible (`Eligibility=1`), annual `Overall`; successful plus not-successful equals fully participating. Eligible count equals participating plus absent/deferred/OSSLC/insufficient-evidence counts, without adding separately reported exempt records.
- Every school satisfies `0 <= Y <= P <= E`. Fractions are calculated independently of floating-point V41 outputs.
- Every possible aggregate missing-success count from0 through `E-P` is checked:1498 completions for Grade9 and1425 for OSSLT. All lie within the saved range, with endpoints attained by all missing outcomes0 or all1. Observed participant rates lie inside these ranges.

The bounds are completion scenarios for a defined but unobserved binary result under the same assessment, with observed outcomes held fixed. They are not identified causal effects of compelling attendance, actual official rates, predictions, or a claim that a feasible intervention would leave participant scores unchanged. V41 already states these conditions and keeps main-model admission false. No corrective code change is needed.

## New evidence about unmatched schools

The same official2024–25 OSSLT archive also contains the **previously eligible** cohort. Exact school-ID checks find:

| Missing V41 assessment | Unmatched roster schools | Present in same-year previously eligible data |
|---|---:|---:|
| Grade9 |38|33|
| First-time-eligible OSSLT |23|18|

Of the33 Grade9-unmatched schools,8 have reportable previously eligible records,14 nonparticipation records,11 privacy-suppressed records. Of the18 first-time-unmatched schools,2 have reportable previously eligible records,10 nonparticipation records,6 privacy-suppressed records.

`unmatched_other_cohort.csv` records every matched identifier and source status. These are records of the same schools in a different same-year assessment cohort; absence from Grade9/first-time results cannot justify classifying them as closed or assigning zero scores. Previously eligible results cannot fill first-time or Grade9 cells. For the remaining5 schools in either unmatched list, these inspected products do not determine the reason for absence. No institution closure, renaming, or replacement-year inference is made.

Outputs: `audit.json` (exact-fraction checks and coverage), `source_hashes.json` (audited versions), and the cross-cohort evidence CSV. All checks passed.
