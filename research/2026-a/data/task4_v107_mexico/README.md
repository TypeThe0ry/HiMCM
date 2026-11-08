# Mexico City: EIC 2025 actual school travel

The official INEGI Encuesta Intercensal 2025 CDMX microdata provides reported home-to-school travel-time categories, age, attendance and **last approved** education level/grade. Current secondary stage is not directly observed. Two conditional membership rules are compared.

## Source and vintage

The official [program](https://www.inegi.org.mx/programas/eic/2025/), questionnaire, descriptor and sampling-design document are archived and hashed in `manifest.json`. `official_microdata_catalog.json` preserves the public frontend API response linking the CDMX package under `/programas/eic/2025/microdatos/` (identifier 3160704, year 2025). Questionnaire and sampling-design documents identify EIC 2025, published in 2026; archive members are dated 2026-08-28. There is no person-record survey-year variable. The matching official resources establish vintage and availability on 2026-11-08; an exact first-release day is not asserted from locally retained evidence.

The archive has 442,778 persons, all entity code 09, spanning 16 CDMX boroughs. Person expansion factors total 9,165,819 residents of private dwellings. This geography is CDMX, not the wider metropolitan area. The household survey follows residence rather than school-site enrollment.

## Definitions

Question 20 asks time “de aquí a su escuela.” Categories are <=15, 16–30, 31–60, >60–120 and >120 minutes, plus no travel. Conservative continuous closures used for consistency are [0,15], [15,30], [30,60], [60,120], [120,infinity). Utility is exp(-t/30). No travel, unspecified and blank retain [0,1], rather than receiving a perfect score.

For ages 14–18 and attendance code 1:

- `prepa_conditional`: approved levels 4/5/7 and grades 0–2; 9,125 sampled people, expanded weight 187,133. Inclusion remains conditional on progression/current-stage interpretation.
- `boundary3`: approved lower-secondary level 3, grade 3; 7,114 people, weight 145,209. Completed lower-secondary plus attendance does not establish current upper-secondary membership, including around school-year transitions.
- `other_optional`: potentially eligible unspecified stage/grade or attendance; 133 people, weight 2,941. Unspecified age would also remain optional; none occurs here.

Legacy progression includes the first two groups. The revised rule includes only the first and permits boundary3 membership to vary. Both retain other optional observations. Neither is a directly observed current-stage cohort; other atypical progression histories are not fully resolved.

| Rule | Included weight | Optional weight | Utility lower | Utility upper |
|---|---:|---:|---:|---:|
| Legacy progression | 332,342 | 2,941 | 0.2691081603 | 0.5261865661 |
| Boundary 3 optional | 187,133 | 148,150 | 0.2138238687 | 0.5841000315 |

Bounds optimize bin endpoints and optional membership using sorted optional utility masses and all cumulative prefixes. These are conditional sample identification bounds, **not confidence intervals**. FACTOR, ESTRATO and UPM exist; design-based sampling uncertainty is not included. `target_age_missing_field_rows` covers all age-eligible people before attendance filtering, including known nonattenders; it is not selected-cohort missingness.

## Privacy and reproduction

The original ZIP stays in ignored `local_only/`. Person fields contain anonymous join identifiers and FECHA_NAC_M/A; the descriptor defines these dates as the last liveborn child's month/year, not respondent birth dates. No individual records, IDs, detailed geography or family dates are published. `aggregate_bins.json` contains only three-group time-bin counts and expansion-weight sums.

Run `python3 derive_from_aggregates.py` here for offline reconstruction. Its `derive_from_aggregates()` function verifies the aggregate hash and retained source-document hashes, validates count totals, and returns both intervals. `aggregate_manifest.json` records the original ZIP hash. For raw regeneration, obtain the exact ZIP at the manifest URL in `local_only/`, then run `python3 extract.py`. The extractor verifies hashes, entity scope, unique person keys and positive weights and publishes aggregates only.

Main-model admission is controlled by the parent pipeline. Any integration must retain these membership and sampling limitations.

## Model admission after independent review

The V107 registry subsequently selects `boundary3_optional` as a conditional replacement for the older2020 input. The acquisition files do not self-admit data. See `../../results/task4_v107_mexico_revision/README.md` for the four year-by-membership controls, exact rollback and remaining sampling/current-stage limitations.
