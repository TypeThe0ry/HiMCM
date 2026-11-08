# Mumbai: school-level UDISE+ 2024–25 resource allocation

The mirrored school records identify 280,140 pupils in grades XI–XII, 5,887 teachers recorded as teaching higher secondary only, and 967 teachers recorded as teaching secondary and higher secondary. These are explicit grade/teaching-category fields; they replace the need to infer a stage ratio from whole-school categories.

## Provenance and geography

Files are original downloaded bytes from [OpenCity's Mumbai UDISE+ 2024–25 collection](https://data.opencity.in/dataset/mumbai-udise-2024-25), which attributes the source to `microdata.udiseplus.gov.in`. `manifest.json` records URLs, byte lengths and hashes. `metadata.json` is the serialized API result object, not a byte-for-byte HTTP response. Direct official/mirror byte identity has not been verified.

The mirror calls export 2723 “Mumbai City”, but the actual profile field says **MUMBAI II**, and all 1,750 profiles give **Greater Mumbai Municipal Corporations**. Its blocks include Grant Road, Sion, Ghatkopar, Mulund, Andheri, Malad and Kandivali. These administrative education labels must not be interpreted as a partition of the two civil districts. Export 2722 has 2,343 distinct schools and zero XI–XII pupils or higher-secondary teaching categories. The two pseudocode sets are disjoint. The mirror's “Mumbai Suburban Profile Part 1” resource mistakenly contains the Part 2 schema; it is not used or archived as geography evidence.

[The official Maharashtra Economic Survey](../task4_v78_mumbai/README.md) reports higher-secondary PTR 41 for 2024–25, with its footnote including Mumbai Suburban. The school data give 280140 / (5887 + 967) = 40.872483, numerically consistent with that published integer. This corroborates the aggregate but does not prove mirror byte identity, a rounding rule, or coverage of every possible school system.

## Extraction and checks

`dsp_schema.pdf` defines the fields. Enrolment Part 1 uses `item_group=1`, `item_id=1..4` for General/SC/ST/OBC; other overlapping groups must not be added. Columns `c11_b`, `c11_g`, `c12_b`, `c12_g` supply the numerator; the schema includes transgender counts in the boys field. Independent age-wise Part 2 (`item_group=8`) reproduces each school's four grade/sex totals exactly. The extraction rejects duplicate keys, negative values and missing numeric cells.

Teacher fields `class_taught_hsec_only` and `class_taught_sec_hsec` explicitly identify the teaching level. All nine class-taught categories partition each school's `total_tch` exactly. Teacher and pupil school identities match in both exports. There are 550 schools with nonzero XI–XII enrolment; 31 additional schools have 39 higher-secondary-only and 44 shared teachers despite zero enrolment in those grades.

## Conditional allocation bounds

For resources attributed to the observed enrolled cohort, count 5,848 higher-secondary-only teachers at schools with pupils as the lower resource total. Retain the allocation of 967 shared teachers and 39 higher-secondary-only teachers at zero-enrolment schools as unknown. Thus

\[
N=280140,\qquad T=5848+\theta,\qquad 0\le\theta\le1006,
\]
\[
u_E=\frac{15T}{N+15T}\in[0.2384602838,0.2684684685].
\]

This is a conditional teaching-resource allocation interval, not FTE, instructional hours, a sampling confidence interval or a measure of teaching effectiveness. A convention counting all reported dedicated posts gives lower utility 0.2396694215; the main allocation bound leaves the 39 zero-enrolment-school posts unresolved. All-age XI–XII enrolment is used consistently with the teacher resource; age 14–18 pupils total 275,499 but cannot be assigned all teachers independently.

The numerator differs from V77 DSER's 278,538 by 1,602. No mixed-source ratio is formed and the discrepancy is retained. Source coverage, reporting revisions and geographic administration remain relevant limitations. Do not describe these data as a complete residence-based census of ages 14–18.

Run from repository root:

```sh
python3 research/2026-a/data/task4_v78_mumbai_school/extract.py
```

`extract()` verifies the original hashes, computes the allocation bounds and returns the summary. Running the script writes `summary.json`. No manuscript changes are included.
