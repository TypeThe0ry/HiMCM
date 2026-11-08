# Vienna2001: independently checked historical school-travel evidence

The Statistics Austria source supports a reproducible **2001 resident school-stage audit**. Its three selected upper-secondary school types contain 42,774 resident students, of whom 40,604 have published daily outward-time bins. The other 2,170 retain unknown utility. The source also discloses official reconstruction/imputation of missing times, without identifying its amount or error quality in these aggregates.

**Admission status: `historical_case_only_not_current16`; primary admissions: 0.** The parent review excludes this source from the current model because no2001-to2025/26 transfer evidence or source-editing error calibration exists. `observations.json` is empty. This review does not run the city ranking or Monte Carlo and adds no current city observation.

## Original source and geographic eligibility

Source: Statistics Austria, *Volkszählung2001: Schüler und Studenten*, census date15 May2001, publication2005. The [original publication URL](https://www.statistik.at/fileadmin/publications/Volkszaehlung_2001__Schueler_und_Studenten.pdf) is recorded with SHA256 `ac650df634fea8e0f5b4bfceae84065f61f9ec69d9af2e2e33fd7d6d2760a814`.

The original is a locally held review copy and is not redistributed. This directory contains selected factual derived counts, mathematical results, scripts and paraphrased source definitions. It contains no PDF, source-page image or complete extracted source text.

Table10 is organized by **residence**, not school location. Its `9Wien` aggregate is the2001 city/state territory; it is not a greater metropolitan region. Definitions note that Vienna districts are treated like municipalities for commuter classification. Summing all23 resident districts901–923 reproduces every field of the selected city rows exactly, so interdistrict classification is not mistaken for exclusion from the city.

Relevant locators:

| Material | Physical PDF page | Printed page |
|---|---:|---:|
| Full Vienna student denominators, Table1 | 47 | 48 |
| City daily duration bins, Table10 | 183 | 184 |
| City changing/non-daily columns, Table10 companion | 184 | 185 |
| Reference date, student employment and school-type definitions | 28 | 29 |
| Daily outward time, editing and commuter definitions | 30 | 31 |
| All23 districts used for reconciliation | 183,185,187,189,191 | 184,186,188,190,192 |

The three types are BMS (vocational middle school), AHS upper stage and BHS (vocational higher school). Lower AHS is separately published and excluded. The selection also excludes primary/lower-secondary, polytechnic preparatory school, special-school, Kolleg, tertiary and other-training rows. It is a selected school-type proxy, not every secondary setting or an exact age14–18 population. Ages cannot be joined to duration bins from marginal age totals alone.

## Coverage and unknown mass

The definition of students includes employed students, but employed students were directed to answer work-travel questions and classified as work commuters. Their school-travel durations are therefore not recoverable from Table10. Table1 provides fuller resident school-type totals; every difference is retained as unrepresented duration mass rather than silently dropping these students.

| Selected school type | Table1 full residents | Table10 total | Daily bins | Changing destination | Non-daily | Not in Table10 | Total unknown duration |
|---|---:|---:|---:|---:|---:|---:|---:|
| BMS | 6,929 | 6,680 | 6,479 | 7 | 194 | 249 | 450 |
| AHS upper | 19,373 | 18,930 | 18,604 | 0 | 326 | 443 | 769 |
| BHS | 16,472 | 15,865 | 15,521 | 1 | 343 | 607 | 951 |
| Sum | 42,774 | 41,475 | 40,604 | 8 | 863 | 1,299 | 2,170 |

For each row, daily bins plus changing destination plus non-daily equal Table10 total. Adding the Table1/Table10 residual gives the full resident denominator. The residual is labelled unrepresented mass; it is not assumed to measure only one exclusion mechanism. Non-daily and changing-destination students receive `[0,1]`, not zero duration or zero travel utility. The walking transport category also is not confused with “no school journey.”

## Conditional historical moment bounds

The measured item is the reported average duration of the **daily outward journey**, not a round trip or a modeled nearest-school car route. Published duration classes are1–5,6–10,11–15,16–30,31–45,46–60 and61+ minutes.

The default conservative continuous closure uses `[0,5]`, `[5,10]`, `[10,15]`, `[15,30]`, `[30,45]`, `[45,60]`, `[60,infinity)`. It contains the published integer classes while avoiding unsupported gaps; the exact literal integer-class convention is separately reported. Both integrate `q(t)=exp(−t/30)` at endpoints, retain a zero lower utility for the unbounded tail and use no bin midpoint or finite tail cap.

For stage denominatorN, bin countsc, bin endpointsa/b and unknown massm:

`lower=sum(c*exp(−b/30))/N; upper=(sum(c*exp(−a/30))+m)/N`.

| Historical conditional output | Lower | Upper |
|---|---:|---:|
| BMS | 0.282808 | 0.504197 |
| AHS upper | 0.414279 | 0.622144 |
| BHS | 0.286741 | 0.504129 |
| Pooled with Table1's all-age school-type weights | 0.343868 | 0.557591 |
| Unknown mixture of the three school types | 0.282808 | 0.622144 |

The pooled arm and convex hull answer different mixture questions; neither identifies exact ages. Full precision, literal-class sensitivity and denominators are in `historical_bounds.json`.

These are bounds **conditional on the official edited cells**. The source explicitly reconstructs/imputes missing reported times; these edits cannot be isolated as an additional known mass from the published aggregate. The2,170 unknown students cover identifiable denominator exclusions, not all possible editing error. No sampling confidence, unedited-response accuracy or current-year transfer is claimed. Without accepting the edited cells or a historical-to-current link, the corresponding current utility remains `[0,1]`.

## Reproduction and verification

Keep the private original outside Git and run:

```sh
.venv-v120/bin/python research/2026-a/data/task4_v127_vienna_travel/extract.py \
  --source-pdf /data/scratch/himcm-austria2001-pupils-students.pdf
.venv-v120/bin/python research/2026-a/data/task4_v127_vienna_travel/audit.py
```

Extraction verifies the original SHA, source definitions, manually/visually checked city counts, full denominators and all23 district sums. The independent scalar audit rechecks the manual count vectors, both endpoint conventions, pooled/hull formulas and file hashes. `audit.json` records success. The original user CSV and current model registry remain unchanged; zero primary admissions are asserted in both scripts.
