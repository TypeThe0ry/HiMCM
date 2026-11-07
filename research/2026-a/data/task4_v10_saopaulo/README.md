# Sao Paulo OD2023 acquisition audit — no observation admitted

Official Metro landing https://www.metro.sp.gov.br/pesquisa-od/ links the 2023 microdata annex. The official indexed resource https://transparencia.metrosp.com.br/dataset/pesquisa-origem-e-destino-2023-anexos/resource/04bd5c3a-1391-4c33-bda7-6feb3d500c16 identifies Site_190225_PesquisaOD2023.zip (189.16 MB, updated 2025-02-20). Its file list contains Banco2023_divulgacao_190225.dbf/.sav, Layout_BD_OD2023_190225.xlsx and municipal/zone spatial files. Prefer this version to the earlier February releases; do not mix layouts.

Access audit 2026-11-07: official portal request HTTP503; web reader timeout. A candidate conventional static-file URL also returned503 and is NOT a verified download address. SciELO mirror metadata request for the older 2017 dataset DOI10.48331/SCIELODATA.UH3OCJ returned403. No ZIP was downloaded or fabricated. A search-indexed official technical review described 147 fields, but its current URL returned404; indexed description is not a substitute for the actual dictionary.

Required extraction gates once the official archive is available:

1. Distinguish municipality of residence from metro-wide and trip destination geography.
2. Verify current high-school enrolment separately from highest educational attainment and age-only filters.
3. Select home-to-school direction, single-trip duration and valid date/day records; document overnight handling and missing codes.
4. Distinguish person, household and trip expansion weights; define one eligible person-day or journey estimand without repeated-person weighting.
5. Preserve nonresponse in utility bounds; record denominators and avoid representing trip-completers as all students.
6. Preserve raw bytes and dictionary hashes; archive only necessary extracts or compressed source parts compatible with GitHub file limits, keeping the full original locally.

No new admissible city cell. Main ranking was not rerun with unchanged inputs. Current formula remains S=100 sqrt(B)/(sqrt(A)+sqrt(B)), B=sum(w*u²), A=sum(w*(1-u)²), u in evidence intervals; main/aux weights (1-alpha)/8 and alpha/2. Last validated main possible-champion set has25 cities. This audit records a concrete official source/version and download failure, not evidence of a rank improvement.

## Acquired microdata and rerun — 2026-11-07

A pinned public research mirror now supplies the actual 143,038-record DBF, its 2025-02-19 layout and municipality code table. `microdata_manifest.json` records exact URLs, commit, sizes and SHA256. The original DBF is archived losslessly as gzip (7.1 MB); decompression reproduces its recorded hash. The official server remains unavailable for byte comparison. This supersedes the earlier “no ZIP/data downloaded” acquisition status; official source identity remains unverified.

`extract_commute.py` selects **ESTUDA=4 (currently attending upper secondary)**, independently of age or educational attainment. Municipality 36 is linked to IBGE 3550308 through the archived code table. Each student contributes FE_PESS once. The first school-destination journey is selected by N_VIAG; only residence-origin (8), education-destination (4), weekday records with positive duration agreeing with the departure/arrival clocks receive measured utility exp(-minutes/30). Other students retain [0,1]. Earlier non-home school journeys cannot be discarded to select a later favorable trip. Zero-travel students remain in the denominator; CD_ENTRE is a household interview field, not the person's travel flag.

| Survey scope | Current HS students | Valid first direct journeys | Utility bounds |
| --- | ---: | ---: | --- |
| Metro | 2,910 | 2,537 | [0.466198, 0.605819] |
| São Paulo municipality | 1,778 | 1,546 | [0.456025, 0.593964] |

These are weighted sample missing-outcome bounds, not sampling-error confidence intervals. Nonresponse among unrepresented households and survey design uncertainty are not estimated. The metro and municipal definitions are separate scenarios; both retain the 2023 vintage. Main admission remains false pending official provenance verification and final city-definition alignment. The aggregate workbook found elsewhere has separate age, attainment and mode-duration tables; those marginal tables were not joined to manufacture a high-school observation.

### Actual comparison

`../../results/task4_v10_saopaulo/` contains fresh baseline and scenario ranks from `../../scripts/task4_saopaulo_conditional.py`. Under the municipal interpretation, the travel interval width falls from 1 to 0.137939 (86.21% reduction), the total score interval width falls from 38.8453 to 33.0936, and the minimax-regret **decision rank** moves from 14 to 6. Nine city decision ranks change. The metro alternative also gives rank 6, with total width 33.1121. These ranks describe decisions under incomplete information, not an identified ordering of true performance.

The possible champion set remains all 25 cities, both at alpha=0.1 and over continuous alpha in [0.05,0.2]. The new evidence materially narrows one city's travel uncertainty but does not establish a unique champion. Baseline main observations are unchanged; Phoenix still lacks an admissible student travel result.

For student weights q_p and known journeys K, the new interval is:

    travel_lower = sum(K, q_p * exp(-t_p/30)) / sum(all students, q_p)
    travel_upper = travel_lower + sum(unknown students, q_p) / sum(all students, q_p)

Current score formula remains S_i=100 sqrt(B_i)/(sqrt(A_i)+sqrt(B_i)), with B_i=sum_j w_j u_ij², A_i=sum_j w_j(1-u_ij)². Main criteria have w=(1-alpha)/8 and auxiliary criteria alpha/2. Score endpoints are L_i=S_i(lower), U_i=S_i(upper); possible champions satisfy U_i >= max(k != i) L_k. Decision ranks minimize max(0,max(k != i) U_k-L_i).

Reproduction (extraction requires dbfread; model uses the project's numpy/pandas/scipy):

```sh
python3 research/2026-a/data/task4_v10_saopaulo/extract_commute.py
python3 research/2026-a/scripts/task4_saopaulo_conditional.py
```

Validation: all three raw hashes and municipality mapping checked; one first-person record per selected student; constant person weight, date and municipality across journeys. A second agent independently reproduced both weighted intervals and verified 273 zero-travel HS students in the metro denominator. Six edge checks covered exact utility, absent journeys, earlier non-home school arrival, inconsistent duration, duplicate order and overnight clocks. No main bounds were overwritten.
