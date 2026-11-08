# Istanbul 2012 household survey: current high-school cohort recovered

The official CKAN report, questionnaire, response metadata and live response datastore became readable through Exa `web_fetch_exa`. Earlier generic-table evidence described completed education; the actual questionnaire **also** asks whether the respondent currently studies and which type of school they attend. The CSV labels are `ogrencimi=EVET`, `okuduguOkulunTuru=LİSE`; these are distinct from `enSonBitirdigiOkul`.

## Evidence and calculation

- Official datastore resource: `a75118db-28c9-4fdf-b367-d5933b7bb810`.
- Live datastore total 49,176 persons agrees exactly with the report introduction's 49,176 people in 16,491 households. The catalog nevertheless reports `datastore_contains_all_records_of_source_file=false`; exact CSV byte equality has not been established.
- All 2,792 explicitly current high-school students were retrieved in six sorted pages. Internal person identifiers were checked only in memory: 2,792 unique persons. Age and person weights matched across separately projected requests. No name, street address or telephone field was requested.
- The known age-14–18 cohort has 2,463 persons, 2,173 households, 39 resident districts and positive person weights totaling 677,016. `kisi_agirlik` is used, not travel-response weight `yol_agirlik`.
- Whole-journey origin/destination and departure/arrival times identify the first actual `EV` (home) to `OKUL` (school) trip. Component vehicle-leg durations are not substituted. Three repeated home-school cases agree between diary order and the 06:00 diary-clock order. No valid case hides an earlier nonhome school arrival.
- Only weekday diaries and positive, unambiguous same-calendar elapsed times in valid questionnaires contribute a measured duration. Missing diaries, no relevant journey, nonpositive/rollover clocks and `EKSİK ANKET` remain unknown. Report section 2 explicitly treats `EKSİK ANKET` as nonresponse and distinguishes it from valid-but-incomplete forms.
- Known-cohort observed: 1,811 persons / weight 499,950. Unknown: 652 / weight 177,066. The weighted measured-duration mean 31.5675 minutes is conditional on observed journeys, not the all-student mean.

With fixed utility `exp(-t/30)`, the known-cohort empirical interval is `[0.3170902972, 0.5786291677]`. `aggregate_results.json` contains the duration-weight histogram, mass accounting, age-group and district diagnostics. Districts with fewer than 20 target respondents are pooled. These are descriptive comparisons with unknown mass retained; they do not establish different age preferences.

## Admission limits

This is **2012 evidence**, not a 2025 measurement. The interval is conditional on the recovered empirical cohort and person weights, not a sampling confidence interval or a forecast. The report describes two-stage clustered sampling with 1,031 primary clusters and earlier five-stratum methods; the full stratum/design mapping and inclusion probabilities have not been reconstructed. A household bootstrap would not automatically recover that design. Strict current-year/population uncertainty therefore remains `[0,1]` until a justified transfer/design rule is supplied.

Optional membership was independently audited in `../task4_v116_ibb_review/`: 13 known-age uncertain student/stage records have weight 3,875. A NULL-first age sort additionally found 21 missing-age records; two could belong to the target cohort, with weight 612. The other missing-age records have known nonstudent or primary/middle-school status. An API equality filter on null had returned zero, so it was explicitly rejected as a missing-age test.

All 15 optional members (weight 4,487) retain utility `[0,1]`. The final historical conditional interval is **`[0.31500258196933106, 0.5814034635501898]`**, with maximum denominator weight **681,503**. Both endpoint extremizers include all optional weight: zero utility for the lower endpoint and one for the upper endpoint. This interval is in `historical_conditional_bounds`; `summary` preserves the narrower known-cohort calculation for audit only. The main evidence registry was not changed.

Age-group marginal intervals including optional membership are `[0.3596131432, 0.5571087967]` for 14–15 and `[0.2934708063, 0.5934561187]` for 16–18. The same missing-age optional weight may belong to either group in its separate marginal bound; it is included only once in the combined-city calculation. The marginal endpoints must not be treated as jointly attainable. District diagnostics remain explicitly conditional on known members and are not complete district-population estimates.

## Reproducibility and privacy

`source_audit.json` records exact projected-query URLs and validation. `provider_*.txt` files are **provider-extracted text, not original PDF/CSV bytes**; their hashes in `provider_text_sha256.json` hash that representation only. SQL aggregate calls returned HTTP 400; minimal nonidentifying fields were projected and aggregated in memory. No individual response rows or person/household IDs were saved in this directory.

`reproduce_aggregate.py` consumes a joined minimal JSON projection on stdin and emits only known-cohort aggregates. It requires the current-status and form-status columns in addition to the travel projection. Input should be streamed from an approved source and never committed. `verify_aggregates.py` runs offline using the published histogram and independently recovered membership controls to verify final endpoints, age marginal accounting and strict current-year `[0,1]`. Clock parser and incomplete-form checks also passed.
