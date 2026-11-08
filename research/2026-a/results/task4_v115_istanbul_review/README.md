# V115 Istanbul source review: no new model admission

The evidence model remains V114. Fresh execution of the selected model reproduces all 250 utility intervals, all 25 city decision ranks, travel evidence and the numerical recommendation certificate exactly. Istanbul remains decision rank 7 under the default weights, its travel interval remains [0,1], and all 25 cities remain possible champions. No weighting, transformation or missing-data rule changed. Monte Carlo was not repeated because its inputs are unchanged; the V114 results remain applicable.

## What the new evidence establishes

- The complete 126-page scan of the 2011 Istanbul high-school report goes beyond V114’s limited chapter check. The study selected grades 9 and 11, excluded grade 12, and analyzed 2,035 questionnaires. Transport spending priorities and living arrangements are not travel durations. Seven OCR pages were empty or poorly recognized, so the result is that no usable duration field was verified, not a claim that every possible field is absent.
- The original University of Twente 2010 thesis covers four districts and 91 schools. It models access to the nearest school at an assumed walking speed; the author states that student travel behavior was not captured. Its age-specific demand is estimated from broader age bands. Neither quantity is an observed journey to the actual attended school or an observed district-by-age access rate.
- An original article published in 2021 studies 180 pupils in grades 10/11 at one Istanbul school. Publication year is not an established fieldwork year. Its questionnaire does not provide the required commute variable or a 14-year-old comparison group. Time use does not supply elicited AHP preferences.
- New official parliamentary document routes identify the 2025 school-transport question and grouped reply, but the specific reply body remains unread. Failed downloads are recorded as failures, with no invented PDF or numerical result.

Source packages: ../../data/task4_v115_istanbul_survey/, ../../data/task4_v115_istanbul_age/, ../../data/task4_v115_istanbul_reply/. These are acquisition and scope findings, not additions to the scoring matrix.

## Consequence for fairness and age analysis

A count of facilities does not identify which students can use them. An age band in a convenience sample does not identify population differences between ages 14 and 18. The next admissible inputs need current enrollment stage, student age, residence geography, actual outbound school duration, survey weights and missing-person coverage. District resource access additionally needs locations, opening times, fees and eligibility. No such missing inputs are filled by a nearest-school walking estimate, a broad all-age commute average, or an assumed equal split of age bands.

The V114 bundle audit remains the actionable priority: holding other cities fixed, every remaining minimal hypothetical exclusion bundle for Istanbul contains travel. Replacing [0,1] requires verified evidence; no artificial narrowing is performed to obtain a smaller champion set.

## Reproduce

From research/2026-a:

```sh
python3 data/task4_v115_istanbul_survey/verify.py
python3 data/task4_v115_istanbul_age/audit.py
python3 scripts/task4_current_model.py --output results/task4_v115_istanbul_review/reproduced
python3 results/task4_v115_istanbul_review/verify.py
```

The full OCR scan has its own reproduction script in the survey package. Numerical model and formulas are unchanged from V114. No Overleaf manuscript was edited.
