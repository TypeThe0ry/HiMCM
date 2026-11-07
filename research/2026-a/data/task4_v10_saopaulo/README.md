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
