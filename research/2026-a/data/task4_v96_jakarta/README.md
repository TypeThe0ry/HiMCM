# V96: retain unusable questionnaires and the actual Jakarta sampling scope

The thesis's collection table identifies **360 completed SMA/SMK questionnaires: 262 valid and 98 unusable**. Retaining those 98 records with unknown travel utility gives a collection-record envelope of **[0.246928, 0.850371]**, wider than the valid-respondent bound [0.339290, 0.794402]. These are different record sets; the V95 same-valid-sample improvement remains intact. No city indicator is admitted.

## What the original design says

The [ITB thesis](https://digilib.itb.ac.id/gdl/view/74988/stated-preference) is reused byte-for-byte from V95. Chapter3 p36 quotes a 2022 Central Jakarta public-school frame of 24,429 SMP pupils, 9,223 SMA pupils and 11,221 SMK pupils, in 36, 13 and 14 schools respectively. These are school-location counts quoted in the thesis, not a newly acquired resident population register.

Chapter3 p38 says schools were selected to reach the required school-stage sample sizes and proportions. The schools then chose pupils randomly according to the method description. Chapter5 p62 adds geographic representation across the eight Central Jakarta districts. The acquired material gives no school inclusion probabilities, pupil draw probabilities or design-weight file. Matching stage proportions therefore does not establish a self-weighting city sample. Private schools and the rest of DKI Jakarta are outside this school frame; the questionnaire does not establish respondents' residence municipality.

The original collection table (chapter5 p59, visually checked) contains 24 collection rows from **23 distinct schools: 12 SMP, 4 SMA and 7 SMK**. SMK39 appears twice with different collection modes, explaining the extra row. This resolves the journal's contradictory 23-school versus 12+4+6 account: the thesis has seven SMK schools. The table's dated collections run from February10 to March16,2023; this does not date every other research activity.

| Stage | Completed questionnaires | Valid records | Unusable records | Valid/completed |
|---|---:|---:|---:|---:|
| SMP | 390 | 311 | 79 | 79.74% |
| SMA | 124 | 119 | 5 | 95.97% |
| SMK | 236 | 143 | 93 | 60.59% |
| Total | 750 | 573 | 177 | 76.40% |

The published total percentage is76.65%, which disagrees with573/750; individual collection-row percentages agree after rounding. The table provides completed-questionnaire counts, not the denominator of all pupils invited. Reasons for unusable records and person-level deduplication are not established. Consequently these counts must not be called response probabilities or unique-pupil coverage rates. The source's surrounding p57 prose also prints753 usable records, while the table, stage totals and analytic cross-tabs consistently give573; this typo is retained as a source discrepancy rather than used as a second sample.

## Collection-record bounds

For the same school-type target, let [L,V] be V95's bound for262 valid records. Assign every unusable upper-secondary record its full utility range[0,1]:

`L_collection = 262*L/360`

`U_collection = (262*V + 98)/360`.

The result concerns the completed questionnaire record set under the source's additive counts. It does not infer an unobserved pupil's trip or assert that every unusable record is a distinct pupil. The ages and trip outcomes of those98 records remain unknown; no age14–18 extension or population confidence interval is manufactured. Neither these bounds nor a stage calibration factor solve the unknown school-selection and resident-coverage conditions, so Jakarta's city-level travel interval remains[0,1].

## Verification

`audit.py` verifies four reused-source hashes, reconstructs all24 collection rows from the original PDF, checks their counts and displayed percentages, aggregates the three stages, and recomputes the collection envelope from the hashed V95 result. The original school-selection paragraph and collection table were visually checked at final readable rendering. The blank questionnaire on appendix pp149–152 has current school type and age fields, plus home-school distance/time, but no residence municipality field.

```sh
python3 research/2026-a/data/task4_v96_jakarta/audit.py
```

[Summary](summary.json) · [all collection rows](collection_rows.csv) · [reused originals](reused_sources.json). No model, registry, ranking or manuscript was modified.
