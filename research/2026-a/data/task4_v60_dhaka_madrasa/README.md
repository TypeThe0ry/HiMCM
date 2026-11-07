# Dhaka Alim-stage coverage audit — V60

BANBEIS's source-labeled 2025 tables support an **additional Alim (grades11–12) enrollment interval of [0,42393] and teacher interval of [0,1944]** within the reported Dhaka City Corporation madrasa population. These are conservative admissible bounds, not a count estimate or probability distribution. This directory changes no model or manuscript.

## Evidence and correction

Table5.1.10.1 (PDF342/printed309) reports five city institution-type/management cells:

| Institution type | Management | All post-primary students | Girls | Teachers | Alim upper bound |
|---|---|---:|---:|---:|---:|
| Dakhil | Private | 7246 | 3480 | 534 | 1562 |
| Alim | Private | 12332 | 4288 | 572 | 12332 |
| Fazil | Private | 2507 | 775 | 131 | 2507 |
| Kamil | Private | 24945 | 7076 | 657 | 24945 |
| Kamil | Public | 3410 | 0 | 50 | 1047 |
| Total | | 50440 | 15619 | 1944 | 42393 |

**Institution type does not identify students' current stage.** Table5.3.5 (PDF385/printed352, visually checked) explicitly reports1076 grade11 plus486 grade12 students in Dakhil-type institutions nationwide. Table5.3.7 (PDF387/printed354) independently repeats1562 Alim students in Dakhil institutions. Consequently, omitting Dakhil's city students and534 teachers is unsupported. Alim-type institutions also contain lower and higher stages.

For each type/management cell, the city is a subset of the national cell. If city all-stage count is n, national all-stage count N, and national Alim count A, then:

    max(0, n - (N-A)) <= city Alim <= min(n,A).

All city lower bounds remain zero. National totals cap Dhaka Dakhil Alim at1562. National public Kamil Alim is1204, including157 girls; Dhaka's public Kamil cell reports zero girls. Applying the same subset rule separately to girls and other students caps that cell at1204−157=1047. All other city cells retain their entire reported student count as the upper bound. Without the gender restriction the valid, coarser upper bound is42550.

Teacher assignment to grades11–12 is unreported. Keep all1944 reported teacher roles as a possible upper bound and zero as the unresolved lower bound. Do not infer teacher FTE or stage allocation from enrollment proportions. These rectangular outer bounds can contain combinations that are not jointly feasible; they deliberately do not assert a precise student–teacher ratio.

## Scope and unresolved dates

- Geography is the source's **Dhaka City Corporation**, not district or division. Mapping the label to Dhaka North/South boundaries remains unverified.
- Population is enrolled Alim-stage students, not every resident aged14–18. Madrasa addition broadens the general-HSC component but does not complete technical/vocational coverage.
- Tables are labeled2025. The methods text elsewhere in the publication states survey collection20October2024–21November2024; a possible copied date remains unresolved. Do not call the counts a verified2025 census.
- This is an audit of public tables, not a direct city-by-grade microdata extraction. No city Alim-stage teacher or enrollment total was established.
- National totals are used only as subset caps, never as national-share city imputations.

## Next uncovered sector

Table7.3 (PDF422/printed389) reports263578 students and11074 teachers nationally in technical/vocational Higher Secondary, plus a separate mixed Technical School and College category (169462 students,7373 teachers). Neither national aggregate is a Dhaka observation. The chapter's tables provide type/management/level summaries, not an established city-stage allocation. A city institution/EIIN roster plus grade-specific counts is needed before adding this sector; double counting attached technical units must also be checked.

## Reproduction

Run `python3 research/2026-a/data/task4_v60_dhaka_madrasa/extract.py` from the repository root. It checks the reused original PDF SHA256, verifies critical extracted row strings, writes selected-page text, and calculates the bounds in `audit.json`. The original PDF remains unchanged at the path in `raw_reuse_manifest.json`.
