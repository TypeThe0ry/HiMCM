# Cape Town: GHS 2023 exact schema, acquisition unresolved

Access date: 2026-11-07. No observed Cape Town commute distribution was obtained, so no numeric observation is admitted. All files in this folder are metadata, access-response evidence, or derived extraction instructions. Raw responses retain their original bytes; SHA256 and source URLs are in `manifest.json`.

## Strongest route: General Household Survey 2023

The archived complete [World Bank metadata](https://microdata.worldbank.org/metadata/export/7839/json), produced by Statistics South Africa and distributed via DataFirst, contains all required fields in `ghs-2023-person-v1` (F3):

| Purpose | Variable | Verified coding |
|---|---|---|
| Resident municipality | `metro_code` | 2 = WC – City of Cape Town |
| Current grade | `edu_grde` | 10, 11, 12 = Grade 10, Grade 11, Grade 12/Matric |
| Broader secondary sensitivity | `edu_grde` | 8–12; keep separate from upper secondary |
| Actual journey duration category | `edu_time` | 1 <15; 2 15–30; 3 31–60; 4 61–90; 5 >90 minutes |
| Unresolved time | `edu_time` | 6 do not know; 9 unspecified; 8 not applicable |
| Survey weight | `person_wgt` | Person weight, not household weight |
| Optional age restriction | `age` | Age, not a replacement for current grade |

The official [GHS metadata PDF](https://isibaloweb.statssa.gov.za/metadata/GHS/2023/General%20Household%20Survey%202023%20metadata.pdf), page 33, was verified through its web search index: EDU8 explicitly asks time to the attended educational institution for **one direction**, using all usual transport means. The original PDF was not archived. Travel is inapplicable to correspondence/distance education; handle this eligibility separately from unknown time. `extraction_spec.json` records the planned bin and missingness treatment; `ghs_selected_schema.json` is a selection from the archived complete metadata, not observed student data.

[World Bank data access](https://microdata.worldbank.org/catalog/7839/get-microdata) directs users to [DataFirst catalogue 961](https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/961/get-microdata), whose inspected page requires login. No accounts were created. The [Stats SA public download landing page](https://isibaloweb.statssa.gov.za/pages/surveys/pss/ghs/2023/ghs2023.php) advertises CSV, SPSS and STATA in the search index, but both web access and direct HTTP retrieval failed to expose its links: the archived HTTP-200 response is an Incapsula rejection page, not the dataset. No protection bypass was attempted.

## NHTS 2020: weaker population definition

The archived [complete NHTS metadata](https://microdata.worldbank.org/metadata/export/4553/json) has 566 variables across geographic, household and person files. `Uqno` links person to geography; `Metro_code` is the metropolitan municipality field. Person fields include age, attendance, `Eduinst`, `Education`, `Q33NeedTrav`, `Tot_time_travel_edu` and person `Weight`.

`Eduinst=2` combines formal-school Grades R–12. `Education` is highest educational attainment, **not current grade**. Thus NHTS age-filtered school attendance is not an exact upper-secondary cohort and is not admitted as such. `Tot_time_travel_edu=999` is unspecified; the category list does not establish a Cape Town sample count or a Cape Town distribution. No actual microdata were obtained.

[DataFirst catalogue 886](https://www.datafirst.uct.ac.za/Dataportal/index.php/catalog/886/get-microdata) requires login. The [Stats SA NHTS landing page](https://isibaloweb.statssa.gov.za/pages/surveys/pss/nhts/2020/nhts2020.php) and metadata PDF returned HTML challenge/rejection responses. They are explicitly named and recorded as HTML, not PDF/data. World Bank metadata also contains conflicting survey-design descriptions relative to indexed Stats SA documentation; obtain the original technical report before claiming design-correct uncertainty.

## Admission decision and remaining work

GHS 2023 is structurally suitable for exact Cape Town upper-secondary commute bins. It needs actual permitted microdata acquisition, sample/weight and eligibility validation, and missingness-aware interval calculations before admission. Grade-specific city sampling uncertainty remains unmeasured. Exact attendance mask: `edu_attend=1` and `edu_edui=2`; in-person eligibility is `edu_corr=2` (No distance learning). Audit ambiguous eligibility codes 3/8/9 separately. `psu` and `stratum` are available for design-aware estimation. No fabricated records, age-to-grade imputation, national-to-city substitution, or point estimates were produced. A 2006 Cape Town report found through a third-party mirror was not used: its education-duration plot combines institutions, while separate school accessibility figures require distinguishing actual attendance from facility access.

Verification: complete metadata JSON parsed successfully; grade, city, time, weight labels inspected; downloaded bodies inspected to distinguish data from HTTP-200 protection pages. The manifest can be checked with Python `hashlib.sha256` over each archived source. No model files or manuscripts were edited.

FAO follow-up: checked [catalogue3072](https://microdata.fao.org/index.php/catalog/3072/get-microdata). Its Get Microdata page redirects users to World Bank catalogue7839; it does not provide an independent microdata download. This closes the FAO mirror lead for this round.
