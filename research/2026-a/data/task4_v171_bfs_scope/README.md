# SSP teaching FTE: 2024/25 coverage evidence

The archived national SSP manual establishes a compulsory public/private school census and a direct teaching-workload FTE calculation. It supports the meaning and broad coverage of the actual published V170 teaching FTE totals. This package records methodology evidence; it computes no city PTR or utility and admits no model cell.

The three bounded routes were the national 2024/25 collection manual, Zurich collection documentation, and the official SSP activity profile. Four HTTP 200 originals are retained. One attempted 2024 Zurich manual URL returned 404; its receipt records the failure without an archived response body. The live Zurich help page links a 2026 manual, which was not substituted for 2024 evidence. All successful original bytes, URLs, retrieval UTC times and SHA-256 hashes are in `retrieval.json`.

`source_scope.json` gives exact PDF page pointers. In the 2024/25 manual, pages 6–8 cover private schools, completeness responsibility and disclosure of final collection gaps; pages 9–10 define programmes and census timing; pages 19–20 define FTE as weekly activity workload divided by its full-time basis. Pages 15 and 31 split activities by school, school type and personnel category; page 21 requires separate coding of compulsory and post-compulsory gymnasium years. The statistic counts the defined teaching post/activity workload: during temporary absence, the postholder is recorded rather than a temporary replacement. It is not a classroom-attendance measure or the separate STATENT wage-model estimate.

The scope is useful for a potential broad covering denominator, but the accompanying pupil subset and publication precision still require the parent admission audit. Pure distance learning is excluded. Primary and secondary reference dates are selected by each canton in the first part of the school year; the manual asks that pupil/personnel dates be coordinated as far as possible, rather than asserting that every table has the same date. The private unallocated-stage quantity is included in the published all-stage total and is not a missing-teacher count.

The V170 T8/T10 review found no explicit missing-data marker in the selected published tables. The national manual says final collection gaps should be indicated in basic dissemination. Neither this manual nor the profile supplies an explicit 2024/25 imputation rule or a numerical rounding convention. One-decimal workbook formatting is evidence of display precision, not an automatic outward bound. No individual records are needed merely to understand these aggregate definitions.

Run the offline verification from any directory:

```sh
python /data/projects/HiMCM/research/2026-a/data/task4_v171_bfs_scope/extract.py
```

It checks the saved raw bytes against the receipts, locates key claims by PDF page and writes `verification.json`. The word-search results are not a claim that estimation or rounding never occurred. Existing inputs, results and manuscript files are read-only in this task. The old Zurich city stage split remains an old observation, rather than a newly collected pupil count.
