# Phoenix public schools: original 2023/24 records align the private-school year

The [official NCES historical layer](https://nces.ed.gov/opengis/rest/services/K12_School_Locations/EDGE_ADMINDATA_PUBLICSCH_2324/MapServer/1) supplies a dated 2023/24 source, instead of the mutable current layer used by V42. All 2,609 Arizona IDs were retrieved in six checked pages. Original layer metadata, ID list and responses are retained with exact request URLs, byte counts and SHA-256 in [manifest](manifest.json).

The existing Phoenix municipal boundary contains 533 public-school records. Among operating nonvirtual schools, 145 records have a grade range overlapping9–12, observed9–12 pupils, or an unresolved range. Explicit9–12 enrollment totals **72,562**, with no unknown enrollment upper endpoint. Another38 records with positive ungraded enrollment extend the potential-stage roster to183. Across this broader roster,106 ungraded pupils remain stage-unknown, giving a conservative student interval **[72,562,72,668]**. These are school-record sums, not unique residents or exact ages14–18. Shared-program enrollment and historical versus current boundary differences remain unresolved.

## Hope is observed in this year, not repaired in the later year

Hope College and Career Readiness Academy, NCES040386003535, has2023/24 grades9–12 counts6,7,19,51: **83** students and **4 FTE**. Its dated physical address is6401 S16th St, Phoenix. This does not replace suppressed2024/25 enrollment or retrospectively apply the2025/26 Tempe directory location. It supplies a usable record for the same year as [PSS2023/24](../task4_v83_phoenix_private/README.md).

## Teacher uncertainty remains

Of91 schools whose range is wholly9–12 and whose other grades are zero or structurally inapplicable,31 have positive known eligible FTE contributions, totaling **2,185.00**. The lower sum only uses schools with positive observed high-school enrollment and no possible non-target grade enrollment. It assumes comparable additive school-assigned instructional FTE, not unique-person headcount. Missing staff is not declared zero.

There are **104 missing-FTE records** in the broader potential-stage roster (all also among the145 grade-eligible records). Thus the sum of known nonnegative all-stage FTE4,238.93 is **not** an upper bound, and no finite teacher upper bound is available from this layer alone. [Missing records](missing_staff_records.csv) preserve original negative codes. The roster also retains all original grade, membership and virtual-status values.

This source closes the public/private **year mismatch** for a2023/24 analysis, but not private nonresponse, stage allocation, modality or complete-city coverage. No city-level main-model interval is changed. The known enrollment and staff figures are dated public-school evidence, not an extrapolation of private responders to the whole city.

## Reproduce

```sh
python3 research/2026-a/data/task4_v85_phoenix_public/extract.py
```

The script checks original hashes, complete ID coverage, unique school identifiers, academic year, finite coordinates, polygon inclusion, structural grade zeros, membership consistency and the Hope row. A negative grade value is only converted to a structural zero when the code is−2 and the grade lies outside the stated range. Unknown grades otherwise retain joint bounds based on valid total membership. Ungraded pupils are separately retained as potentially high-school age/stage. Nonvirtual selection uses the source's explicit `Not Virtual` value; no operational city record has unknown virtual code`N` in this extract.

[Summary](summary.json) · [All city records](city_public_records.csv) · [Potential secondary records](secondary_public_records.csv). `main_admitted=false`; no model or manuscript edits.
