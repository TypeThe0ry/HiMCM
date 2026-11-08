# Bogotá EODH 2023: acquired microdata, conditional eligibility

The pinned public mirror supplies actual household, person, and trip records. The extracted Bogotá resident sample contains **3,283 people aged 14–18 in 2,820 households, linked to 5,146 trips**. Of these, 1,952 trips have the reported destination purpose `A Estudiar`. This replaces a download-only inventory with reproducible linked observations. It does not yet identify a citywide high-school home-to-school indicator.

## Source and coverage

Source: [saramirezva/Mobility-Models-Bogota](https://github.com/saramirezva/Mobility-Models-Bogota/tree/b21e3dab606c3a135ee42db29ab1caa5b8c3bcbd/Encuesta%20de%20Movilidad%202023/EODH/CSV), pinned commit `b21e3dab606c3a135ee42db29ab1caa5b8c3bcbd`, accessed 2026-11-08. `source_manifest.json` records exact paths, URLs, byte lengths, SHA-256 hashes, Git blob hashes, and the complete 2023 directory inventory. Acquisition used `git show` of the pinned files; source bytes remain outside this repository.

The mirror's processed modules contain 22,755 households, 67,556 persons, and 100,174 trips. These counts agree with the published survey totals, but agreement in counts does not establish official byte identity. Source classification remains **third-party processed mirror, official byte identity unverified**. The [official survey landing page](https://observatorio.movilidadbogota.gov.co/publicaciones/resultados/encuesta-de-movilidad-2023) is the provenance target, not the source of the downloaded bytes.

The mirror contains five named CSV modules (`hogares`, `personas`, `viajes`, `etapas`, `vehiculos`), six `estrato_*` CSV derivatives, and `num_dis_trips.csv`. The acquisition here uses the first three named modules. Raw questionnaire D/E tables and an official dictionary are absent from the inspected repository tree.

## Resident population and retained fields

Residence is selected by household `cod_mpio_hg == 11001`, whose source label is `Bogotá D.C.`, then linked to persons through `cod_hg == cod_hog`; age is 14–18 inclusive. All selected person municipality labels independently equal `Bogotá`. Person and household identifiers are unique; every source person links to a household and every source trip to a person. Trips use `cod_pers == cod_per`; their household links are also retained.

Derived files replace source identifiers with local sequential identifiers. They contain only anonymous linkage, age, municipality code, reported education/activity, trip order/purpose/duration/mode, and the relevant expansion weights. Coordinates, small-area geography, source IDs, sexual orientation, ethnicity, and victimization fields are excluded.

| File | Role |
|---|---|
| `persons_age14_18.csv` | All 3,283 resident adolescents, including those whose principal activity is not school |
| `households_age14_18.csv` | 2,820 linked households, municipality and household weight |
| `trips_age14_18.csv` | All 5,146 linked trips; purpose and minutes allow explicit cohort checks |
| `education_inventory.csv` | Reported education counts crossed with principal school activity |
| `extraction_summary.json` | Machine-readable coverage, eligibility and quality counts |

All selected person, household, and trip expansion weights are present and positive. European thousands grouping is parsed explicitly: `1.554,6` becomes `1554.6`. The initial parser incorrectly marked 3 person weights and 20 trip weights missing; the corrected extractor restores those observed values. Genuine missing values remain blank. No selected trip duration is missing or nonpositive; durations range from 3 to 243 minutes. These are observations, not automatically valid home-to-school journeys. Person, household and trip weights have different estimands and must not be substituted for each other.

## Eligibility that remains uncertain

`max_nivel_edu` records highest education reached; it is not a direct current-grade field. `ocupacion_principal == Colegio o escuela` identifies principal school activity, which can omit enrolled people whose principal activity is work. There are 2,175 principal-school-activity respondents, including 732 reporting `Media incompleta (10° y 11°)`. The latter group contributes 566 study-destination trips. It is retained as an explicitly **conditional education group**, not certified current grade 10–11 enrolment. All other adolescent records remain available for alternatives and uncertainty analysis.

The processed trip file has no direct home-origin flag. A study destination alone cannot certify a home-to-school trip, and a matching geographic zone would not certify home origin. Consequently this extract is **not admitted to the main model**, and no missing interval is narrowed merely from the 566 conditional trips.

A separate [research implementation](https://github.com/ESO-Rennes/Distancias_Emisiones_EODH/blob/main/Distancias_EODH_2023_projection_reseau.Rmd) identifies actionable missing source fields: raw `ANEXO 2_BASE DE DATOS EODH CON FACTORES DE EXPANSIÓN.xlsx`, sheet `modulo D-E`, `d7` (initial home flag), and sheet `viajes`, `d24` (destination home flag). That external code documents a possible linkage route; its numeric encodings still require the official questionnaire/dictionary before admission. The remaining acquisition target is these raw fields plus a validated current education-stage definition and source verification.

## Reproduce

Requires Python and pandas. Obtain the three pinned source files via Git; keep the full raw files outside the research repository. For example, after cloning the source repository and checking out the pinned commit:

```sh
git show 'b21e3dab606c3a135ee42db29ab1caa5b8c3bcbd:Encuesta de Movilidad 2023/EODH/CSV/Modulo_hogares.csv' > /tmp/bogota91_hogares.csv
git show 'b21e3dab606c3a135ee42db29ab1caa5b8c3bcbd:Encuesta de Movilidad 2023/EODH/CSV/Modulo_personas.csv' > /tmp/bogota91_personas.csv
git show 'b21e3dab606c3a135ee42db29ab1caa5b8c3bcbd:Encuesta de Movilidad 2023/EODH/CSV/Modulo_viajes.csv' > /tmp/bogota91_viajes.csv
```

From the HiMCM root:

```sh
python3 research/2026-a/data/task4_v91_bogota/extract.py --raw-dir /tmp
```

The extractor verifies source SHA-256 and row counts before parsing semicolon-separated Windows-1252 CSVs, validates key coverage, selects municipality and age, and preserves missing numeric values. A second run into a temporary output directory was compared byte-for-byte with the delivered derived files.
