# V67 Santiago: CASEN 2024 school-stage and commute audit

**New admissible travel observations: 0.** Two new official original PDFs were acquired. CASEN 2024 identifies current secondary school stage, but its recorded commute-time question is for work, not school. London's or other cities' parameters are not substituted. No model, manuscript or Git changes were made.

## Prior-work check

V10 already archived Santiago EOD2012 person/household/trip records and documented unresolved current-school-stage wording; V40 verified journey timing; V48 audited the mixed-source 2025 mobility report. Those are not newly acquired evidence here. A bounded search did not locate a newer official Santiago EOD person/trip release. The official SECTRA regional page and the previously identified MTT library document timed out in the web reader; this is an access outcome, not proof of absent data.

## Newly downloaded official sources

- [CASEN 2024 questionnaire](https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Cuestionario_Casen_2024.pdf), saved as `casen2024_questionnaire.pdf`.
- [CASEN 2024 fieldwork manual](https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Manual_de_trabajo_de_campo_Casen_2024.pdf), saved as `casen2024_manual.pdf`.
- [Official survey catalogue](https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen-2024) lists person microdata, separate comuna/provincia files and codebooks. These large microdata files were not downloaded after the questionnaire failed the school-duration requirement.

All page references below are 1-based PDF pages.

| Requirement | Verified evidence | Consequence |
|---|---|---|
| Current attendance | Questionnaire p13 `e3` asks attendance during school year 2024, including online and adult education. | A general student work-status proxy is unnecessary here. |
| Current secondary stage | Questionnaire p15 `e6a_asiste` explicitly asks the level currently attended; codes 9 and 11 denote general and technical secondary. `e6a_no_asiste` is a separate historical-attainment question. | Current-stage semantics are verified for CASEN, not transferable to EOD2012. |
| Current grade | Questionnaire p16 `e6b_asiste` asks the course currently studied. | Can support a school-stage cohort in a future compatible use. |
| School location | Manual p59 describes `e9com` as school commune. | This is school location, not residence; joining geography still needs the resident microdata/codebook. |
| Observed school commute time | Education module p13–21 has no school travel-duration item. Questionnaire p27 `o28a` measures time from home to principal workplace among employed persons. Manual p84 reinforces the work destination. | Never use `o28a` as school time, even for an employed secondary student. |

The manual p54 has a conflicting printed question header under `e6a_asiste`; the original questionnaire p15 provides the direct current-level wording. This is why the questionnaire, rather than a search snippet or the manual header alone, is the admission reference.

## Decision

CASEN resolves current-stage identification within its own survey but cannot supply the required observed home-to-school duration. Do not statistically match CASEN students to EOD2012 trips as if respondents were linked. No Santiago travel interval is narrowed and no improvement in possible-winner count is claimed. A verified EOD questionnaire or a distinct survey containing the joint current-stage/age/residence/school-duration fields is still needed.

## Verify originals

Run `python3 research/2026-a/data/task4_v67_santiago/audit.py`. It checks SHA-256 and byte counts from `manifest.json` and verifies the key questionnaire wording; dependencies: Python and pypdf.
