# Mumbai: official combined higher-secondary PTR, 2024–25

The Government of Maharashtra reports a pupil–teacher ratio of **41** for higher secondary standards XI–XII in **Mumbai City including Mumbai Suburban**, reference year **2024–25**. This is a directly published stage-specific statistic; it avoids reconstructing a ratio from the unmatched school-category counts identified in [V77](../task4_v77_mumbai/README.md).

## Original and location

The [Finance Department publication page](https://finance.maharashtra.gov.in/en/publication/economic-survey-of-maharashtra-2025-26/) links the archived [Economic Survey of Maharashtra 2025–26 PDF](https://cdnbbsr.s3waas.gov.in/s349d4b2faeb4b7b9e745775793141e2b2/uploads/2026/10/202610151773411968.pdf). Both the landing HTML and PDF are preserved byte-for-byte with retrieval date, size and SHA-256 in `manifest.json`.

On **PDF page 346 / printed page 316**, the district indicators table has a separate Higher Secondary (Std XI–XII) pupil–teacher ratio column, number 24, dated 2024–25. Mumbai City's entry is `41^`; the page footnote says the caret includes Mumbai Suburban. The Suburban row has dashes in the three PTR columns, so its ratio must not be treated as missing and then independently averaged with 41. The header, cell, year and footnote were visually checked on a rendered original page on 2026-11-08.

`extract.py` verifies original hashes and extracts the cell, caret and combined-area footnote from the PDF. It writes `summary.json`; the program verifies the recorded page structure, while visual inspection establishes the header alignment. The directly transformed **published-statistic** utility is `15/(15+41) = 0.26785714285714285`.

## What the statistic identifies

The existing official [UDISE+ 2024–25 original](../task4_v34_education/udise_2024_25.pdf), glossary item 14 on printed page 188, defines PTR using pupils and teachers at the specified education level in a school year. This supports interpreting a stage-labelled PTR as a school-resource measure. The Maharashtra table itself does not give its raw pupil/teacher counts, staff FTEs or a rounding algorithm. Do not reverse-engineer a teacher count by dividing the V77 population by 41: the sources are not proven to share the same underlying count construction.

The source supports using **41 as the observed published statistic**, conditional on the model measuring the reported resource indicator. It does not establish that the underlying unrounded ratio is exactly 41 or provide a confidence interval. If a model uses a one-unit reporting perturbation `[40,42]`, that is an explicit sensitivity assumption, not a source-derived interval. The unknown teacher allocation in the V77 aggregate-pool approach is not solved by this source; the new observation follows a separate direct-statistic route.

Coverage remains the reported higher-secondary school system. This is not an age-specific 14–18 student estimate or a measure of learning outcomes; the source does not establish full coverage of every school outside the reporting system. Annex 10.2 provides Konkan regional counts combining grades IX–XII, which cannot recover the raw Mumbai grades XI–XII denominator.

## Geographic cross-check and download limit

The official MCGM [city profile](https://dm.mcgm.gov.in/assets/pdf/city_profile.pdf) describes Greater Mumbai as Mumbai City plus Mumbai Suburban. Its text was accessible through web search, but a direct original download timed out on 2026-11-08, so no original copy is claimed here. The archived economic survey itself explicitly confirms that the ratio combines these two districts. The combined geography is distinct from the wider Mumbai Metropolitan Region.

Reproduce:

```sh
python3 research/2026-a/data/task4_v78_mumbai/extract.py
```

No model or manuscript files are changed by this source package.
