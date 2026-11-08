# Mumbai: reconcile higher-secondary category totals with explicit grades

Mumbai Suburban's Table 8.3 pupil counts match the explicit grades 11–12 counts in Table 8.8, separately for boys and girls in both educational divisions. Mumbai City's tables differ by 14,315 pupils. This adds a concrete internal consistency check to V40; it does not establish the teacher allocation needed for a stage-specific pupil–teacher ratio.

| Reporting area | Table 8.3 pupils | Table 8.8 grades 11–12 | Difference |
| --- | ---: | ---: | ---: |
| Mumbai City / South | 57,525 | 71,840 | 14,315 |
| Mumbai Suburban / West | 131,167 | 131,167 | 0 |
| Mumbai Suburban / North | 75,531 | 75,531 | 0 |
| Mumbai Suburban / Total | 206,698 | 206,698 | 0 |

## Sources and verification

Original official DSER 2025 PDFs remain in [V40](../task4_v40_mumbai/README.md); no duplicate PDFs are added. Reference year is 2024–25. Grade cells were transcribed from the existing PDF text and checked against rendered original pages on 2026-11-08.

- [Mumbai City official PDF](https://cdnbbsr.s3waas.gov.in/s31c87860778df9675a35aa14d3bee8776/uploads/2025/12/2025121642449457.pdf): Table 8.3 PDF page 118 / printed 108; Table 8.8 PDF page 123 / printed 113. Table 8.8 grades 11 and 12 total 18,197 + 17,893 + 17,702 + 18,048 = 71,840. Its source list includes BMC Education and the South education inspector; Table 8.3 cites the South inspector. The difference is observed; its cause is unresolved.
- [Mumbai Suburban official PDF](https://cdnbbsr.s3waas.gov.in/s31c87860778df9675a35aa14d3bee8776/uploads/2025/12/20251216708247665.pdf): Table 8.3 PDF page 104 / printed 94; Table 8.8 PDF page 112 / printed 102. Table 8.8 explicitly labels grades 11 and 12; its footnote specifies educational-division rather than taluka reporting and data supplied through UDISE. BMC's grades 11–12 row is zero. West and North rows individually reconcile by sex with Table 8.3.

`python3 research/2026-a/data/task4_v77_mumbai/verify.py` checks original PDF SHA-256 hashes, arithmetic, sex-specific agreement and division totals. The script verifies the transcription arithmetic; page inspection supplies the semantic identification of the cells.

## Model consequence

The Suburban match supports a grades 11–12 interpretation of its pupil aggregate, without proving a general DSER Table 8.3 mapping. City's mismatch prevents transferring that interpretation mechanically to the entire Mumbai candidate. Neither table identifies the teacher count as teachers assigned exclusively to these grades, an exhaustive pool covering the same students, or FTEs. Thus the current evidence cannot justify either a point PTR or a one-sided allocation bound for the whole-city model. In particular, dividing City's 71,840 pupils by Table 8.3's 1,074 teachers would combine unmatched coverage.

## Broader teacher-pool check

Tables 8.1–8.3 collectively reproduce Table 8.8's all-grade pupil total, separately by sex, in both districts. Their totals are 383,389 for City and 1,324,179 for Suburban. City's 14,315 difference is therefore consistent with different allocations across school categories; there is no aggregate pupil-count gap across the three categories. Numerical agreement alone cannot identify which records account for the difference.

The six teacher totals sum to 54,723. Explicit grades 11–12 pupils across the two districts total 278,538. The accompanying CSV records each category, source page and reference year. Tables 8.1 and 8.2 total pages were also visually checked; all are labelled 2024–25.

If these six totals form a complete pool containing every teacher serving the corresponding grades 11–12 students, then the stage teacher count satisfies `T_stage <= 54723` and the PTR satisfies `PTR >= 278538 / 54723 = 5.08996...`. Duplicate teachers across categories would preserve this upper-pool argument; omitted teachers could invalidate it. This is a conditional derivation, not an admitted bound. The inspected tables call the column number of teachers but do not give the reporting specification needed to establish complete staff coverage, grade allocation or role inclusion. Equal pupil totals provide a useful coverage cross-check, not proof of teacher completeness. The bound also depends on treating the two reporting areas as the model's Mumbai geography.

No main model inputs, uncertainty intervals, rankings or manuscript text are changed. The next useful evidence is a table-specific grade/teacher mapping or an explicit exhaustive staff-pool reporting definition. Generic descriptions of Indian higher-secondary education cannot supply these missing links.
