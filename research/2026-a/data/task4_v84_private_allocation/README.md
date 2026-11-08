# Phoenix private records: high-school teaching allocation dominates work-time rounding

For the same 6,109 explicitly graded high-school pupils, assigning every reported K–12 teacher hour to high school gives a resource utility of 0.685719. Allowing the actual unknown stage allocation produces the much broader **[0.330722, 0.690707]** outer interval. Seven schools serving only grades 9–12 within the reported K–12/ungraded universe contribute a lower bound of 201.25 teaching-time FTE; the 33 schools with explicit high-school pupils contribute at most 909.50. This is an observed-record diagnostic, not an estimate for all Phoenix schools or an educational-quality outcome.

## Same-cohort comparison

The [V83 original PSS ZIP and municipal overlay](../task4_v83_phoenix_private/README.md) and [official questionnaire/manual](../task4_v83_pss_docs/README.md) are reused with SHA-256 verification. The source covers school year 2023/24, approximately October 1, 2023. No duplicate source files are stored.

| Treatment of the 33 schools | Teaching quantity | Utility for the same N=6,109 |
| --- | ---: | ---: |
| All-stage published midpoint assigned entirely to high school | 888.60 | 0.685719 |
| Work-time categories retained, but all K–12 time still assigned to high school | [867.25, 909.50] | [0.680454, 0.690707] |
| Work-time categories plus unknown high-school allocation | [201.25, 909.50] | [0.330722, 0.690707] |

The first two rows are explicit contrast assumptions, not observed high-school staffing ratios. Accounting for stage allocation increases the interval width from 0.010253 to 0.359985 (35.11 times), exposing uncertainty that the work-time-only calculation omits. It does not demonstrate better predictive accuracy or a smaller city champion set.

For each school, let the five Q10 teacher counts be full time and the four descending fractional-time categories. Closed work-time outer bounds are

\[
t_s^- = n_{1s}+.75n_{2s}+.5n_{3s}+.25n_{4s},\qquad
t_s^+ = n_{1s}+n_{2s}+.75n_{3s}+.5n_{4s}+.25n_{5s}.
\]

Let \(P\) contain the seven reported schools with positive grade 9–12 enrollment, no K–8 or transitional-grade students and no ungraded students. Q10 excludes pre-K-only teaching, so pre-K enrollment is not added to this K–12 allocation universe. Let \(H\) contain the 33 schools with positive explicit grade 9–12 enrollment. Then the explicit-grade diagnostic uses

\[
T_H\in\left[\sum_{s\in P}t_s^-,\sum_{s\in H}t_s^+\right]=[201.25,909.50],\qquad
u_H=\frac{15T_H}{6109+15T_H}.
\]

Other schools' teacher lower contribution is zero because the high-school share is unidentified. The source does not supply grade-specific instructional hours or minimum hours per pupil. These conservative outer bounds do not claim that every endpoint is jointly attainable.

## Ungraded pupils and teaching mode

Four records contain 91 ungraded pupils. Three of these have no explicit high-school enrollment and were outside the earlier 33-school set. Including their potential high-school component gives 36 possible-stage records, student bounds **[6,109, 6,200]**, teacher bounds **[201.25, 974.50]**, and the resource-utility outer interval **[0.327458, 0.705257]**. This is a broader possible-stage population, kept separate from the same-cohort comparison above. Combining separate extrema is a rectangular outer bound: the upper teacher endpoint includes ungraded-only schools while the lower student endpoint excludes their ungraded assignment, so no sharp joint identified-set or endpoint-attainability claim is made.

All 36 schools report in-person classes available (P411=1); six also offer virtual classes (P412=1), and seven offer hybrid classes (P413=1). Twenty-nine offer only in-person classes among these three options. Q11 measures available class types, not each pupil's actual attendance mode. No school is excluded solely because it also offers virtual/hybrid classes, and no onsite student share is inferred. All relevant enrollment, teacher-category and mode flags are zero for these 36 records; the full dataset contains other adjusted fields.

Q4 offered fields P135 through P295 are checked against their paired counts: a missing count is made structural zero only where the offered field is 2. The high-school counts are P270/P280/P290/P300; ungraded is P140; K–8 and transitional counts are P160 through P260 in steps of ten. Q10 measures K–12 and comparable ungraded teaching, not separately grades 9–12. The source does not restrict the pupils to exact ages 14–18.

## Population interpretation and verification

These are unweighted released private-school records within the V83 current-boundary overlay. Nonresponding/unobserved schools, current versus historical boundaries, actual modality shares, and alignment with public-school year 2024/25 remain unresolved. Finite bounds on this subset do not yield finite whole-city bounds on missing students and teacher hours. Therefore Phoenix's main education utility remains **[0,1]** and `main_admitted=false`. Moving this evidence into a city indicator requires a consistent school-year/universe, documented coverage or omission bounds, and appropriate survey-domain uncertainty; national coverage percentages cannot supply Phoenix's local missing fraction.

Run `python3 research/2026-a/data/task4_v84_private_allocation/extract.py`. It checks reused source hashes, ZIP integrity, school IDs, grade/structural-zero logic, time-category arithmetic and relevant flags, then writes [school allocation](school_allocation.csv) and [summary](summary.json). A separate agent independently read the original ZIP with `csv` and reproduced the filters, counts and arithmetic. No main model or manuscript file is modified.
