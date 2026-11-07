# Phoenix V43: same-year LEA membership tested against the original file

**The LEA route does not provide a finite Hope enrolment upper bound.** This conclusion now comes from the successfully downloaded official CCD2024–25 LEA membership file, not a failed website request.

The archive contains a649,957,451-byte CSV. We streamed all **3,822,460 rows** and extracted **227** matching NCES LEA0403860 / Arizona AZ-4234, Maricopa County Regional School District. Every extracted row has an empty STUDENT_COUNT and DMS_FLAG=Suppressed. This includes the education-unit total, the total excluding adult education, all four grade9–12 subtotals and demographic detail. Suppression is not interpreted as zero, nor as an assumed small-cell upper limit.

The already archived school-level file explicitly links Hope NCES040386003535 to this LEA in2024–25. Its other listed school, Southwest Key Transitional Learning Center, has zero membership. Subtracting a known zero from an unknown district total does not resolve Hope. `school_lea_crosswalk.csv` preserves the same-year affiliation and relevant counts.

The official [CCD2024–25 summary](https://nces.ed.gov/ccd/tables/202425_summary_1.asp), note11, defines membership as October1 enrolment excluding adult education. The matching long-file derived-total category explicitly excludes adult education. Thus the requested vintage and denominator route were correct; the required number is not published in this release.

## Sources and reproduction

Original: <https://nces.ed.gov/ccd/Data/zip/ccd_lea_052_2425_l_1a_073025.zip>. The downloaded ZIP was 68,497,561 bytes; its SHA256 and extraction provenance are retained in `membership_source.json`. Its complete original CSV member is stored here as `ccd_lea_052_2425.csv.xz` (17,910,372 bytes), a lossless recompression rather than the original ZIP. `csv_archive.json` records both the compressed hash and the 649,957,451 original CSV bytes' hash. No rows or fields were removed from this archive. `maricopa_lea_membership_rows.csv` is the separate value-preserving 227-row extract.

From the repository root, reproduce offline with:

```sh
python3 research/2026-a/data/task4_v43_phoenix_lea/extract.py
```

Alternatively append `--archive PATH_TO_OFFICIAL_ZIP`. Both routes validate archive size and SHA256, stream the complete CSV with bounded memory, check its byte count and SHA256, and reproduce the same extracted files. The original ZIP extraction also read through EOF to validate its CRC. Original download provenance is preserved unchanged.

The official EDGE district-characteristics polygon query returns no matching feature; this means no feature, not zero students. The office-location layer confirms the LEA and2024–25 vintage but contains no membership count. Both responses and their metadata are archived with hashes.

A separate staff caution remains: the official NCES district-search index displays4 total FTE split into0.67 elementary and3.33 secondary. This is a reason to review school-level grade-allocation assumptions, not proof that3.33 is exactly high-school FTE. No staff allocation or prior results were overwritten.

This evidence supplies no finite population upper bound and makes no model or manuscript change. V42's ADE1178 remains a distinct observed alternate-source figure with unresolved snapshot compatibility.
