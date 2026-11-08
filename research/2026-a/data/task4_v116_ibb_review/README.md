# Independent review of Istanbul 2012 student travel evidence

The IBB catalogue, metadata and blank questionnaire in `../task4_v116_ibb/provider_catalog_and_schema.txt` distinguish current enrollment from educational attainment. `ogrencimi` asks whether the respondent is a student; `okuduguOkulunTuru` asks current students their school type. `enSonBitirdigiOkul` separately asks the last school completed. Thus current LİSE enrollment can be identified without substituting attainment or age alone.

The source defines `kisi_agirlik` as the weight for total persons, `yol_agirlik` as the weight for persons whose journey information was obtained, and `tam_agirlik` as the weight for complete questionnaires. For the student-roster estimand, use the first weight for both observed and unknown journeys. Substituting the journey-information weight changes the denominator and cannot silently be used as the same estimand.

The blank questionnaire includes nontravelers. The official report introduction independently states 16,491 households and 49,176 people. The acquisition agent reports the datastore exact total as 49,176, agreeing with this published control. The catalogue nevertheless has `datastore_contains_all_records_of_source_file=false`; matching the total is a useful coverage check, not a byte-for-byte comparison with the 115 MB CSV. No original CSV acquisition is claimed in this review.

## Admission requirements

1. Restrict known membership to resident Istanbul students aged 14–18 in current LİSE. The household district field must supply residence, rather than school destination. Audit unknown age, student status and current stage separately; possible members must not be silently excluded.
2. Use one first school-directed journey per person. Require its origin to be home and consistent departure/arrival clocks. An earlier nonhome school journey cannot be discarded simply to select a later home–school journey. Do not sum return trips or intermediate modes as independent students. Check all exposed journey slots against the reported journey count.
3. Retain nontravel, missing school journeys, incomplete interviews and invalid durations with utility [0,1]. Publish weekday/weekend handling explicitly, without silently changing the roster denominator to travelers or weekday attenders.
4. For known members K and optional members O, with positive person weights w and per-person endpoints l,h, compute L=min_z(sum_K wl+sum_O zwl)/(sum_K w+sum_O zw) and U=max_z(sum_K wh+sum_O zwh)/(sum_K w+sum_O zw), z∈{0,1}. Observed utility is exp(−t/30); unknown utility is [0,1]. Missing/invalid weights require separate resolution, not zero replacement.
5. A positive weighted cohort size and a narrow missingness interval do not quantify survey sampling uncertainty. If household clustering/design cannot be reproduced, label the result as a sample-weighted identification interval, not a confidence interval. Avoid an individual bootstrap that ignores household clustering.

## Historical comparison

The observations are from 2012. Catalogue publication/update dates do not update the journeys. The existing NYC comparison uses 2010–2011 data as a historical conditional scenario, includes unknown-stage optional members, and reports an exploratory household bootstrap. Its under-19 group is not an exact 14–18 cohort because its age categories are coarser. Istanbul should receive the same explicit historical treatment, with a withdrawal scenario restoring [0,1] rather than a fabricated temporal correction or arbitrary narrow time penalty. A current-year main-population claim remains unsupported by this historical survey alone.

This audit verifies measurement definitions and lays out admission checks. It does not alter the evidence registry, scores, weights or missingness rules. Acquisition-agent counts are not an independent recalculation of person records. The aggregate extraction review must establish remaining membership and trip-coverage checks before numerical admission.

Sources: [IBB catalogue API](https://data.ibb.gov.tr/api/3/action/package_show?id=71fc2b91-a3a5-44aa-a514-a12f6ab63595); [2012 metadata](https://data.ibb.gov.tr/dataset/71fc2b91-a3a5-44aa-a514-a12f6ab63595/resource/221390e6-73c1-4245-9048-ff76e1ad70eb/download/2012-ulam-ana-plan-hanehalk-anket-yantlar-metadata-.pdf); [2012 blank questionnaire](https://data.ibb.gov.tr/dataset/71fc2b91-a3a5-44aa-a514-a12f6ab63595/resource/48d0eb92-b4eb-4ca4-85a5-478cb31e2473/download/2012-yl-ulam-ana-plan-hanehalk-anketi.pdf). Read from provider text captures; no visual PDF inspection claimed.

## Independent roster controls and NULL correction

Independent four-field projections for each age14–18 returned complete pages totaling4,320 people. The known LİSE cohort has2,463 people and weight677,016. Thirteen known-age people have uncertain enrollment/stage (5unknown student status,3Other school,5Disability school), totalweight3,875. Disability school does not establish the education stage.

A first `filters={yasi:null}` request returnedzero, which was not evidence that missing ages were absent: SQL equality does not match NULL. The corrected `sort=yasi desc` query returned21leading null-age records followed by979nonnull records, completing the NULL prefix in one1000rowpage. Two null-age people remain possible members (unknownstudent1/weight302; currentstudent with unknownschool1/weight310). The other19 have known nonstudent status or primary/middle stage. The final optional membership is15people, weight4,487; known-plus-optional weight681,503. These optional members retain utility[0,1]. Only aggregate controls are saved.
