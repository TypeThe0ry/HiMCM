# V65 London LTDS: public-data admission audit

**Result: 0 new admissible high-school commute observations.** The downloaded official LTDS workbook covers London through 2024/25, including 2022/23 and 2023/24, but cannot identify the joint population London resident × age 14–18 × current secondary/sixth-form education × observed journey to school. Keep London's existing missingness bounds unchanged. This is new London-specific evidence, not a reuse of V52's England NTS estimate.

## Archived official evidence

All four original files were retrieved on 2026-11-08 with HTTP 200; byte counts and SHA-256 values are in `manifest.json`.

- [TfL survey overview](https://tfl.gov.uk/corporate/about-tfl/how-we-work/planning-for-the-future/consultations-and-surveys): `survey_page.html`.
- [Public workbook](https://content.tfl.gov.uk/ltds-0525-acc.ods): `ltds2024_25.ods`, titled 2005/06–2024/25, first published January 2026.
- [Survey design](https://content.tfl.gov.uk/london-travel-demand-survey-sampling-and-design-acc.pdf): `sampling_design.pdf`.
- [FOI-2692-2627 response, 15 October 2026](https://tfl.gov.uk/corporate/transparency/freedom-of-information/foi-request-detail?referenceId=FOI-2692-2627): `foi2026.html`.

## What can actually be identified?

| Requirement | Public workbook finding | Admission decision |
|---|---|---|
| London resident | Greater/inner/outer London residence groups are available. | Correct city geography. |
| Age 14–18 | Age tables use broad bands including 5–16 and 17–24. | Cannot isolate target ages. |
| Current high-school stage | Employment tables include Student; no school/sixth-form/college-stage cross-tab was found. | Student alone does not establish secondary education. |
| Actual to-school duration | `Time_travelled` gives all-purpose minutes per person/day and per trip. Purpose tables are separate. | Cannot isolate outbound school travel. |
| Joint sample and uncertainty | Workbook has aggregate tables, not linked person-trip records. | Cannot estimate the desired mean or survey interval. |

`Stages_by_*` refers to **journey stages**, not education stages. Neither the aggregate Student category nor a journey with education purpose identifies the requested current school stage. Separate marginal tables cannot be multiplied or joined as if they described the same respondents.

`workbook_inventory.json` records every nonempty workbook row and sheet name without inventing a record-level dataset. `audit.py` regenerates it from the archived ODS and verifies all four original hashes.

## Microdata lead and unresolved fields

The October 2026 FOI confirms TfL holds requested household/person/trip extracts, but supplied them to that requester using a separately emailed Asite link. The public response itself contains no downloadable microdata or Access dictionary attachment. Its described join keys are `hhid` (household) and `phid` (person). It names grouped `page` (age), `pwkstat` (work status), `topurpi`/`tdpurpi`/`tjpurpi` (purposes), and `tdbmmode` (main mode). The exact age categories, school-stage fields, duration field definitions, label tables and survey weights remain unverified in a usable extract. This finding does not establish that no suitable LTDS extract exists elsewhere.

Before using a future extract: inspect exact age and current-education labels; distinguish secondary/sixth-form from further/higher education; select actual home-to-school trips and retain person/household linkage; check term-time and weekday weights; report eligible unweighted persons and trips separately. The design document specifies population expansion weights and additional weekday/term-time weights. It also advises caution below 500 persons/households and avoiding estimates below 100; a small eligible sample is not cured by counting multiple trips as independent students.

No access request was submitted, no private Asite link was used, and no model/score/manuscript file was changed. This evidence cannot justify narrowing London's missingness interval or claiming a smaller possible-winner set.

## Reproduce

From repository root:

```sh
python3 research/2026-a/data/task4_v65_london_ltds/audit.py
```

Expected: four hashes verified and 30 workbook sheets inventoried. Python standard library only.
