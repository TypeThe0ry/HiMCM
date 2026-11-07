# Lagos V60: teacher and school universe audit

The archived DNEMIS tables support a public senior-secondary dashboard ratio of **30.1 learners per teacher**. They do not identify a complete Lagos high-school population. This round changes **zero model cells** and retains the existing missing-data interval.

## New checks

- Lagos `MD: Total teachers` and `ASC-GEN Teachers` both equal 131,636. Across the national/state/LGA table they agree in 765 of 770 comparable units. Five disagree: the Nigeria aggregate, Kogi State, and three Kogi LGAs. Numeric agreement therefore cannot establish that the two fields are interchangeable or that either covers all registered schools.
- The SSS school-type row has 268,413 learners, 8,920 teachers and an official `ASC-GEN Learner-teacher ratio` of 30.1. The arithmetic ratio is 30.0911. This strengthens the interpretation as an official dashboard statistic for the public SSS school-type category, but supplies no school-level proof that teacher and student records have identical reporters.
- Public SSS missing reports can be located: one each in Lagos Mainland, Ojo, Ikeja and Lagos Island (329 reports of 333 expected). Their student or teacher counts remain unidentified.
- `MD: Total schools` is 14,582; public plus private counts total 14,622. The 20 LGA `MD: Total schools` values sum to 14,581. The portal's expected-report universe and the master-data school count must not silently be treated as one complete registry.
- The public organization-unit table contains one national unit, 37 state/FCT units and 774 LGAs, with no school records. It cannot identify which four public SSS schools are missing or recover their enrollment/capacity.

## What bounds can be justified?

For an explicitly hypothetical matched-reporter population, let N=413,720 reported SSS learners, T_pub=8,920 public SSS teachers and T_private be private teachers serving SSS. If the private all-stage pool of 104,805 contains every relevant private SSS teacher and counts are compatible, then 0 <= T_private <= 104,805 and N/(8,920+104,805) <= N/(8,920+T_private) <= N/8,920. These are **conditional diagnostic bounds**, not an admitted city interval: matching reporter populations and the allocation of mixed-stage teachers remain unverified. The upper endpoint also permits zero private SSS teachers and is not a claim about actual staffing.

For the full population, even assuming the observed counts are matched, write R=(N+N_missing)/(T+T_missing). The count of missing schools provides neither an enrollment cap nor a teacher cap. With unknown nonnegative N_missing and T_missing, no informative positive lower or finite upper ratio follows from reporting counts alone. School-report completeness (329/333) is not student coverage. Consequently the normalized full-population indicator retains [0,1]. Lagos State versus metropolitan-city geography remains a separate unresolved condition.

## Reproduction and provenance

Run `PYTHONPATH=/tmp/himcm_v59_arrow python3 research/2026-a/data/task4_v60_lagos_universe/audit_universe.py` from the repository root, or use an environment containing pandas and pyarrow. The script checks SHA-256 against the unchanged V59 manifest and writes `universe_audit.json`, `lagos_lga_universe.csv` and `teacher_field_disagreements.csv`.

Original public source: https://emis.education.gov.ng/portal/asc/state-H2ZhSMudlMI/ ; original tables and query SQL remain in `../task4_v59_secondary_sources/`. Source period: 2024; displayed school year: 2024/2025; geography: Lagos State, all 20 LGAs. This audit was performed 2026-11-07. The archived public metadata provides indicator labels and aggregate query filters, not a school-level inclusion rule for the teacher fields.

Next useful evidence is a school-level SSS enrollment/teacher extract with reporting flags, or a documented all-registered-school coverage rule plus missing-school student/teacher bounds. Another aggregate enrollment ratio does not resolve this gap.
