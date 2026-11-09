# V129 education: real school-level ETP, no matched city PTR admitted

Two new official routes establish where the remaining denominator mismatch occurs. Paris now has archived DEPP teacher full-time equivalents and pupil records for the same school/year; the teacher field still lacks the upper-secondary teaching-stage allocation. Madrid's municipal series combines ESO and Bachillerato teachers and labels the unit as a count. Neither supplies the requested city upper-secondary ratio. `observations.json` remains empty and no utility bound is proposed.

## Paris: a valid UAI join does not establish a matched teaching stage

The original DEPP API metadata for `fr-en-indicateurs_personnels_etablissements2d` explicitly measures teachers assigned to institutions in ETP. Its declared providers are public and private schools under contract with the ministry. The dataset's staff fields give institution totals and teacher categories, rather than FTE allocated to upper-secondary classes. Its latest observation is30November2025; the pupil datasets observe the beginning of October2025.

The saved example provides a concrete scope check. Lycée Henri-IV has UAI`0750654D`, teacher ETP153.65 for rentrée2025, and794 pupils in the corresponding general/technological lycée dataset. The official annuaire record with that exact UAI flags `post_bac=1`, cityParis, and an open institution. Its separate collège UAI`0752526N` is not joined into the lycée. Thus this route improves on the earlier mixed-collège source, but the school-level ETP has no published upper-secondary/post-baccalaureate allocation. Dividing794 by153.65 would create an unmatched-stage ratio. The annuaire's current post-bac flag is a scope warning; it is not a recovered2025 teacher workload allocation.

Public/contracted-private coverage also cannot be renamed all-provider city coverage. Under strictly matched schools/year and complete coverage, a whole-institution teacher FTE total can upper-bound the FTE assigned to one teaching stage. Here that inclusion does not extend to **all** Paris upper-secondary teachers: other providers and a complete city denominator envelope are not established. No one-sided city utility bound follows without that further inclusion evidence. The single-school sample is retained as a schema/scope witness, not aggregated into an unverified city estimate.

The first department filter`075` returned zero rows; the teacher dataset uses`75`. The corrected Henri-IV query returns both2024/2025 lycée and collège rows. The annuaire separately uses`075`. These coding differences are recorded and not interpreted as missing teachers. Two attempted pupil projections returnedHTTP400; the successful saved UAI-only query contains2019–2025 rows, with2025 selected locally. Null/suppressed fields are not zeros.

## Madrid: municipality is available, upper-stage FTE is not established

The official municipal series`1902423` distinguishes Municipio de Madrid from the surrounding Comunidad, but its title explicitly combines ESO/Bachillerato and its unit isNúmero. The teacher catalogue classifies nonuniversity teaching by ownership and programme; the inspected metadata did not establish a city upper-only FTE field. The route stopped at that mismatch, without fetching a pupil numerator and forcing a ratio.

Direct original-HTTP attempts at the regional catalogue API and municipal page timed out. `madrid_provider_capture.json` preserves Exa's returned representation of the official pages, including the combined-stage title and unit. It is **not** an archived original HTML or statistical table. No Madrid count from that representation enters the model.

## Files and verification

`sources.json` preserves exact successful/failed URLs, dates, response types, byte counts and hashes. Paris metadata, teacher records, pupil records and the annuaire are original HTTP JSON bytes; API filtering defines the archived slice. `attempts.json` records exactly two routes, years, geography, provider/stage mismatches and nonadmission reasons. The original CSV retains its fixed hash; a registry is allowed to advance between research iterations.

Run `.venv-v120/bin/python research/2026-a/data/task4_v129_education/extract.py`. It verifies archived hashes, exact UAI/year selection, the real ETP field and its schema, the post-bac flag, provider scope, the Madrid representation's title/unit and empty observations. It records live model-file hashes before/after the check and writes only this folder's new `verification.json`. It does not claim to have recovered a city census or revalidated earlier model calculations. The original evidence remains separate from the derived scope audit.
