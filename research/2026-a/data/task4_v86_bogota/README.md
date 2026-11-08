# Bogotá: PISA 2022 current-grade-specific learning outcomes

This package extracts the Bogotá public-use microdata and estimates learning outcomes separately for all PISA grades and current grades 10–11. It contains public and private schools. The grade restriction is a genuine improvement in population matching over the published all-grade regional mean, but does not cover all high-school ages.

## Observed results

The subset has 1,986 Bogotá records from 56 schools. Of these, 1,399 students in 55 schools report grade 10 or 11 (1,124 and 275 respectively). They represent 67.69% of the weighted Bogotá PISA cohort. The other 587 records are in grades 7–9. Both domains have observed AGE values from 15.33 to 16.33 years and no missing AGE. These actual public-file ages are retained; no extra age-window filter was imposed from a generic description of PISA eligibility.

| Subject | All PISA grades: mean (SE) | Grades 10–11: mean (SE) | Paired difference (95% interval) |
| --- | ---: | ---: | ---: |
| Mathematics | 422.67 (4.95) | 439.12 (4.77) | +16.45 [11.24, 21.65] |
| Reading | 462.15 (5.82) | 482.07 (5.44) | +19.92 [13.38, 26.45] |
| Science | 459.16 (5.45) | 477.60 (5.00) | +18.44 [12.28, 24.60] |

The all-grade reconstruction matches all three original OECD published means and standard errors to floating-point precision (largest absolute discrepancy below 2×10⁻¹³). This independently checks geography, weighting, plausible values and replication against the published aggregates.

The practical gain is a directly computed grade-10/11 estimate with defensible sampling and measurement uncertainty. Previously, the only available city mean included lower grades. Removing those records changes the estimated target-population mean by 16–20 points; it does not demonstrate a better school system, a policy effect, or an improved cross-city rank. Public-school and private-school strata are both retained. Reported weighted population totals are survey expansion totals for these sample domains, not a count of every high-school student in Bogotá.

## Sources and reproducibility

- Original [OECD student SPSS ZIP](https://webfs.oecd.org/pisa2022/STU_QQQ_SPSS.zip), linked from the [official download page](https://webfs.oecd.org/pisa2022/index.html).
- [OECD analysis guide](https://www.oecd.org/en/about/programmes/pisa/how-to-prepare-and-analyse-the-pisa-database.html): plausible values and replicate-weight inference.
- The previously archived V85 Annex B2 workbook supplies the independent published Bogotá mean/SE checks. Its original bytes and provenance remain in `../task4_v85_pisa_city/`.

The 682,364,259-byte original ZIP and its 2,096,666,903-byte SAV member stay outside Git. `manifest.json` records source URL, original SHA-256 hashes, member CRC, selection criteria, variable labels, and the derived subset hash. Before analysis, SHA-256 checks verify the subset and the V85 published summary, workbook and provenance manifest. The checked-in CSV is explicitly a derived row/column subset; it is not presented as original source bytes.

Reproduce extraction with Python, pandas and pyreadstat:

```sh
python extract_subset.py /path/to/STU_QQQ_SPSS.zip /path/to/scratch
python analyse.py
```

`analyse.py` can run directly on the included small CSV without downloading the international archive. It requires numpy and pandas. `extract_subset.py` verifies full member CRC, selects all records where country is Colombia and REGION is 17001, and checks equality with the COL01–COL03 stratum selection. All 10 plausible values for each of mathematics, reading and science, the final student weight and all 80 replicate weights are retained.

## Estimator

For domain D (all Bogotá PISA records, or current grades 10–11), plausible value m and replicate r:

\[
\hat\mu_{Dm}=\frac{\sum_{i\in D}w_i y_{im}}{\sum_{i\in D}w_i},\qquad
\hat\mu_{Dmr}=\frac{\sum_{i\in D}w_{ir} y_{im}}{\sum_{i\in D}w_{ir}}.
\]

With M=10 plausible values, R=80 replicates, and Fay coefficient 0.5:

\[
\hat\mu_D=\frac1{10}\sum_m\hat\mu_{Dm},\qquad
V_{s,D}=\frac1{10}\sum_m\frac4{80}\sum_r(\hat\mu_{Dmr}-\hat\mu_{Dm})^2,
\]
\[
B_D=\frac1{9}\sum_m(\hat\mu_{Dm}-\hat\mu_D)^2,\qquad
SE_D=\sqrt{V_{s,D}+1.1 B_D}.
\]

For the high-school-minus-all-grade difference, subtraction occurs within each plausible value and replicate before computing these variance components. This retains covariance between the overlapping populations. Adding the two independent squared standard errors would be incorrect.

`plausible_value_replicate_estimates.csv` exposes all intermediate domain estimates for an independent statistical audit. Reported 95% intervals use mean ±1.96 SE; they describe uncertainty of each population mean or paired contrast, not individual score ranges or jointly simultaneous coverage.

## Interpretation boundaries

The high-school domain covers PISA-eligible students attending Bogotá schools who report current grade 10 or 11. PISA's age-based sampling means it does not represent every 14–18-year-old or every student in these grades. Geography is school/sample region rather than a separately verified residence boundary. Conditioning on grade also selects progression and retention histories; the difference from all grades is a population-composition comparison, not a causal estimate of teaching quality or an improvement over time.

These estimates are supporting evidence, with `main_admitted=false`. Direct substitution into the cross-city model would require compatible age/grade definitions and learning measures for other cities. No missing indicator interval or possible-champion set is narrowed by this package alone.
