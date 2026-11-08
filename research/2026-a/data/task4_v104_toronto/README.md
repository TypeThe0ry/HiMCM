# Toronto V104: duration measured, city cross-tab still missing

The University of Toronto/CAMH study by Wong et al. (2011), using OSDUHS 2009, measured actual school-trip duration separately for each direction. Its secondary-school analysis contains 2,479 students in grades 9–12, including 256 in the Toronto stratum. Table 1 reports Ontario-wide duration bins and a separate region marginal; Table 2 reports Toronto travel **mode**, not Toronto duration. Those margins cannot be substituted for a city-specific duration distribution. An exact 14–18 age restriction is also unavailable in the published tables. The study covers publicly funded schools and uses survey-weighted percentages, so displayed sample counts divided by totals need not equal those percentages.

`published_aggregates.json` preserves those published Ontario quantities explicitly as Ontario background evidence. It is not a Toronto input. This new source confirms genuine current-secondary time measurement, but contributes no admissible Toronto duration observation. The main utility interval remains [0,1].

## TTS route

The newly checked official **2016 TTS Data Guide**, PDF pages 42 and 106, defines `start_time`. Its trip-variable list supplies no arrival-time or duration variable. Elapsed time between consecutive departures includes activity time. Consequently 2016 does not solve the duration gap already documented for 2022 in V23. The public download page remains https://dmg.utoronto.ca/download-tts-data/ . No restricted-data request or account was created.

Previous relevant work was checked before retrieval: V23 (2022 TTS), V6/V50/V51 (Eglinton/Forest Hill school projects), and V57 (school bus/achievement research). These are not counted as new evidence here. StudentMoveTO measures post-secondary travel and was excluded.

## Reproduce and sources

Run `python3 research/2026-a/data/task4_v104_toronto/extract.py` (BeautifulSoup and `pdftotext`). It verifies both source hashes, parses the published table, and checks that morning duration counts total 2,479. Both downloaded originals are published aggregate documents, with no survey individual records; no new microdata were archived.

- Wong et al., *Mode shifting in school travel mode*, DOI 10.1186/1471-2458-11-618: https://pmc.ncbi.nlm.nih.gov/articles/PMC3199596/ . Open access CC BY 2.0; original article HTML retained.
- University of Toronto DMG 2016 guide: https://dmg.utoronto.ca/wp-content/uploads/2022/06/2016TTS_DataGuide.pdf . Original bytes and SHA256 are recorded in `sources.json`.

Required next source: Toronto-stratum current-secondary home-to-school duration cross-tab, preferably age 14–18, with weights/coverage and nonresponse information. No model, registry, or manuscript files were changed.
