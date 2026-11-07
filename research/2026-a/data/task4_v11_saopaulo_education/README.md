# São Paulo upper-secondary education outcomes, 2023

Archived actual IDEB municipal **Ensino Médio Regular** outcomes from a pinned public mirror. `manifest.json` records source URL, size and SHA256. The ODS MD5 matches the companion mirrored checksum list. The alternative XLSX file did not match its listed MD5 and was not adopted as the source. Matching a mirrored checksum establishes consistency within that release package; official INEP byte identity remains unverified because the official ZIP request timed out.

`extract_quality.py` reads ODS numeric attributes rather than rounded display text, identifies columns by the original field-code row, and extracts all four network rows for IBGE3550308. It verifies SHA256, MD5, presence of the digest in the archived checksum list, and the four matching rows. `quality_rows.json` preserves unavailable values as text, rather than zero.

The **Pública** row reports IDEB2023=4.2, approval=89.5%, standardized Saeb mean=4.578743, mathematics=265.86 and Portuguese=277.57. This is an observed public-school network result for schools located in the municipality. It is not an all-school city result, an estimate for city-resident students, a teacher ratio, or a four-year graduation rate. The workbook does not provide the student/examinee denominator needed to resolve private-school coverage or reweight school aggregates.

The four networks report IDEB 4.1 (state), 6.0 (federal), 4.3 (municipal) and 4.2 (public aggregate). Preserve the supplied aggregate; do not average the three network scores or sum overlapping public totals. Do not transfer the Brazilian national assessment scale into a cross-country education-quality utility without a justified common definition. Therefore this package adds real education outcomes while `main_admitted=false`; it does not narrow the current PTR interval or manufacture a city ranking improvement.

Primary methodological reference: https://download.inep.gov.br/ideb/nota_informativa_ideb_2023.pdf. The separate São Paulo 2025 school registration report uses a different year and denominator and is not used to backfill 2023 examinees.

```sh
python3 research/2026-a/data/task4_v11_saopaulo_education/extract_quality.py
```
