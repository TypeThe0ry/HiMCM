# V97 Phoenix school-travel source audit

No new Phoenix high-school travel-time observation is admitted in this round. The existing missing-data interval and unidentified population mass remain unchanged.

## New source checked

Ross and Kurka, *Predictors of Active Transportation Among Safe Routes to School Participants in Arizona: Impacts of Distance and Income*, Journal of School Health 92(3), 282–292 (2022), DOI [10.1111/josh.13125](https://doi.org/10.1111/josh.13125). The [ASU institutional publication record](https://asu.elsevierpure.com/en/publications/predictors-of-active-transportation-among-safe-routes-to-school-p/) is preserved as `asu_srts_publication.html`; retrieval metadata and SHA-256 are in `source_manifest.json`.

The study uses 11,100 parent surveys across 112 Arizona schools during 2007–2018. Its explicit grade range is 3–8. The reported outcome is active versus inactive school travel, with distance categories. This establishes that the study contains real school-travel observations, but the published population does not cover grades 9–12. Neither a Phoenix-resident high-school denominator nor a corresponding travel-time distribution is supplied by this record. ASU's Phoenix affiliation is not the respondents' residence geography.

The related 2019 report, *The state of school transportation in Arizona: Predictors of walking and biking to school from 2007 to 2018*, was a discovery lead; no figures from its search excerpts were extracted into model inputs. The verified institutional record above supplies the grade-based exclusion.

## Search boundary and prior findings

Read V39, V53 and V54 audits before searching. Targeted public searches covered Phoenix high-school travel surveys, Arizona school-travel research, and GitHub-hosted student-travel data. No qualified released observation was identified by these searches; this is a bounded search result, not a claim that no such data exist.

The search also returned the Maricopa TRP sample student questionnaire. Prior V6, V43 and V60 work already records this route. A blank questionnaire that asks usual one-way minutes does not provide student responses. It is not a new observation. Known restricted MAG/NHTS geography, parent route applications, school transport policies, university travel surveys and adult commuting aggregates were not converted into high-school measurements.

## Consequence for the model

Admitted target observations: **0**. New represented target-population mass: **0**. No ranking or possible-winner change can be attributed to this audit. Any V97 numerical change must come from independently documented inputs or algorithmic revisions.

A future qualifying release must establish Phoenix residence or an explicitly bounded Phoenix subpopulation, current high-school stage, actual home-to-school duration, and the relevant sample/population denominator. Partial coverage must retain the unobserved remainder instead of assigning it the observed subgroup's distribution.

Validation: preserved HTML checked for sample size, school count, grade-range and survey-year terms; source bytes hashed. No model, registry, manuscript or earlier source file was modified.
