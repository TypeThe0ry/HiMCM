# Delhi: school-level teaching allocation and zero-enrolment posts

The 2024–25 school files reproduce the existing official totals exactly: 603,437 XI–XII pupils, 26,766 teachers recorded as teaching higher secondary only, and 3,420 recorded as teaching secondary and higher secondary. The new school-level information identifies 18 schools with no XI–XII pupils but 105 higher-secondary-only and 14 shared teachers. These posts cannot simply be assigned to the observed enrolled cohort.

## Source and coverage

The five downloaded files come from [OpenCity's Delhi UDISE+ 2024–25 collection](https://data.opencity.in/dataset/delhi-udise-2024-25), which attributes its source to `microdata.udiseplus.gov.in`. [The manifest](manifest.json) records source URLs, retrieval date, byte lengths and SHA-256. Original downloaded bytes are preserved. `metadata.json` is the serialized CKAN API result, not the raw HTTP response. Official/mirror byte identity has not been verified.

All 5,556 school profiles report state DELHI. This is Delhi NCT, not just New Delhi district or the wider NCR. The files reproduce all three corresponding [official UDISE+ publication](../task4_v34_education/README.md) totals: 5,556 schools, 4,491,032 pupils and 161,958 teachers. The official PDF remains in V34; `extract()` verifies its original hash and re-extracts the aggregate and stage rows without modifying it. Agreement corroborates coverage and counts; it does not establish byte identity or coverage outside the reporting system.

## Reconciliation

The numerator uses enrolment Part 1 `item_group=1`, social groups 1–4 (General, SC, ST, OBC). Other overlapping categories are excluded. Its school-by-grade-by-sex cells match the independent age-wise Part 2 exactly for **every reported grade**, not only XI–XII. The schema places transgender counts in the boys columns.

Teacher and pupil school keys match the profile keys. All nine class-taught categories sum to each school's teacher total; regular, contract and part-time categories also sum to the total. Duplicate keys, missing numeric cells and negative counts are rejected. The 1,874 schools with XI–XII pupils all report offering grade XII. The age 14–18 XI–XII pupil subset is 597,603; it is recorded separately and is not assigned the entire teaching pool.

## Allocation convention and formula

For the nominal teaching-resource convention used in V78 Mumbai, count higher-secondary-only teachers at schools with enrolled XI–XII pupils in the lower resource total. Leave shared teachers and the zero-enrolment-school dedicated posts unallocated:

\[
N=603437,\qquad T=26661+\theta,\qquad0\le\theta\le3525,
\]
\[
u_E=\frac{15T}{N+15T}\in[0.3985789633,0.4286862578].
\]

The 3,525 unresolved positions comprise 3,420 shared teachers and 105 dedicated teachers at zero-enrolment schools. The 14 shared teachers at those schools are already included in 3,420 and must not be added again.

This is a **conditional nominal resource-allocation convention**. It is not an identified FTE or instructional-hours interval, a sampling confidence interval, or a claim that a shared teacher provides no high-school instruction. If the indicator instead counts every person who teaches XI–XII, the official participating-teacher headcount of 30,186 and its point utility 0.4286862578 remain the corresponding reported statistic. Applying the allocation convention consistently changes the modeled resource definition; the school-level data additionally identify which dedicated posts should remain unresolved.

The new lower endpoint is slightly below the dedicated-only aggregate endpoint 0.3995215573 because the latter includes all 105 zero-enrolment-school posts. Data describe school-located resources and all-age XI–XII enrolment, not a residence-based census of ages 14–18 or educational effectiveness.

## Reproduce

```sh
python3 research/2026-a/data/task4_v79_delhi/extract.py
```

`extract()` returns the verified summary; script execution writes [summary.json](summary.json). This package does not edit the model registry or manuscript.
