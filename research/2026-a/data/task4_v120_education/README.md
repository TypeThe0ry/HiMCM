# V120 education: three missing cells, no numerical admission

Only missing Zurich/Dublin/Helsinki school-ratio cells were researched. Existing user CSV values were neither checked nor changed. All three retain [0,1]; no teacher denominator was invented.

## Zurich
Official city workbook `zurich_students2024.xlsx` supplies 2008–2024 students by school, ownership and lower/upper-secondary stage (sheets T_1–T_6). The official city teacher page links chart32a.csv, archived here: its `wert` column is gender percentage, with each level summing to 100; it supplies no headcounts/FTE. Canton teacher totals are not city totals. Thus no matched denominator or justified ratio bound follows.
Student page: https://www.stadt-zuerich.ch/de/politik-und-verwaltung/statistik-und-daten/daten/bildung/mittelschulen-berufsbildung.html
Teacher page: https://www.stadt-zuerich.ch/de/politik-und-verwaltung/statistik-und-daten/daten/bevoelkerung/gleichstellung/bildung-berufswahl/lehrkraefte.html

## Helsinki
Official 2024 education annual report is archived. PDF page40 gives city-operated Finnish general-upper-secondary pupils 9,374 and Swedish 1,377. PDF page33 personnel definitions include leave, substitutes, trainees/apprentices and exclude secondary-job hourly teachers. The workforce rows are not a complete citywide teaching-only denominator; city-operated schools also do not exhaust all providers. Relevant pages16,33,40 extracted for scope review. Do not divide student counts by total staff or describe the municipal subset as all-city coverage.

## Dublin
Official paths found concern registration (not actual employment) or allocated special-education posts (not complete teachers), so no ratio admitted:
https://data.gov.ie/dataset?_theme_limit=0&organization=the-teaching-council&theme-=
https://www.ncse.ie/ncse/data-and-statistics/set-hours-special-class-teachers-and-sna-allocations/

Manifest contains original download URLs and SHA256 hashes. Sources are substantive public data, not failure screenshots. Needed next: teacher count/FTE for the same city, providers, stage, and year as student counts, or a defensible complete-coverage upper/lower denominator bound.

## Prague follow-up: candidate found

Official ČSÚ 2024/25 report Table3.1.3 (PDF183 / printed182) gives the same city-school scope for students and teachers: 80,073 pupils including8,748 in compulsory schooling;6,877.1 teacher FTE including737.8 in lower gymnasium. Removing those lower-stage groups gives71,325 pupils and6,139.3 teacher FTE. Table6.1.18 independently decomposes total and lower-stage FTE into qualified/unqualified, reproducing those denominators. Conservative rounding difference interval[6139.2,6139.4] yields the utility in prague_candidate.json. This is an all-study-mode school-resource measure including non-daytime/adult pupils, not a14–18 cohort or resident measure. Conservatoires are separately reported and excluded. No main model edits; parent must decide scope compatibility.

Additional bounded routes: Amsterdam returns the already rejected DUO headquarters geography; no reuse as city-school point. Madrid official education portal offers region tables but no immediately retrieved city-stage matching denominator, so skipped.

Alignment confirmation: PDF74 explicitly identifies pupils fulfilling compulsory schooling within secondary schools as lower multi-year gymnasium pupils. Table3.1.3 footnote2 gives the matching lower-gymnasium teacher years. Conservatoires are separately tabulated (chapter4; separate columns in6.1.18) and excluded from both sides. observations.json now contains only Prague conditional FTE admission; the three original nonadmissions are retained in nonadmission_audit.json.
