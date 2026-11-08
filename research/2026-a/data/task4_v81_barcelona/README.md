# Barcelona: municipal Batxillerat enrollment and secondary teaching personnel

Official Generalitat CSVs identify 23,149 Batxillerat students and 11,219 secondary teaching personnel in Barcelona in 2025/2026. The corresponding 2024/2025 counts are 23,699 and 11,238. Both public and private establishments are included. Geography is the school municipality (code 08019), rather than student residence or Barcelona province.

| School year | Batxillerat students | Public / private students | Secondary teaching personnel | Public / private personnel |
| --- | ---: | ---: | ---: | ---: |
| 2024/2025 | 23,699 | 9,161 / 14,538 | 11,238 | 5,349 / 5,889 |
| 2025/2026 | 23,149 | 8,865 / 14,284 | 11,219 | 5,488 / 5,731 |

These are separate observed counts with different stage coverage. Secondary personnel cover a broader pool than Batxillerat students. They are not a matched pupil–teacher ratio or an education-quality outcome. The package therefore leaves `main_admitted=false`; it does not narrow the main model's missing interval.

## Sources and reproducibility

The [2025/2026 Batxillerat page](https://educacio.gencat.cat/ca/departament/estadistiques/estadistiques-ensenyament/curs-actual/batxillerat/) and [2025/2026 teaching-personnel page](https://educacio.gencat.cat/ca/departament/estadistiques/estadistiques-ensenyament/curs-actual/personal-docent-de-regim-general/) expose the current files. The [2024/2025 personnel page](https://educacio.gencat.cat/ca/departament/estadistiques/estadistiques-ensenyament/cursos-anteriors/curs-2024-2025/personal-docent-regim-general/) exposes the prior-year files. `manifest.json` records exact download URLs, byte counts, SHA-256 digests and retrieval date for the six original CSVs and six original HTML sources. Current-course URLs can change; the archived CSV `Curs` field identifies the actual year.

Run from the repository root:

```sh
python3 research/2026-a/data/task4_v81_barcelona/extract.py
```

The script requires pandas, verifies every source digest, checks year, municipality and nonnegative counts, and writes `summary.json`. The two teacher tables classify the same pool by specialty and by dedication. Their totals agree independently at municipality district × ownership × sex in both years; these views are compared rather than added. The script sums the published rows without deduplication. Batxillerat enrollment includes both course levels 1 and 2 and all published ages.

## Definition and model admission

The archived [2024/2025 concepts](https://educacio.gencat.cat/ca/departament/estadistiques/estadistiques-ensenyament/cursos-anteriors/curs-2024-2025/metodologia/conceptes-fonamentals/) define teaching personnel through direct contact with students during school hours, excluding staff exclusively teaching extracurricular activities and occasional personnel. The published count measures personnel, not vacant posts. Complete dedication means at least 75% of the normal working week, so the complete/partial split cannot supply teacher FTE. Batxillerat enrollment counts distinct people; vocational enrollment has a different counting rule. Age is referenced to December 31 at the start of the school year. These archived definitions establish the 2024/2025 interpretation; continuity into 2025/2026 has not been independently established from a same-year methodology.

A finite upper bound for all upper-secondary teaching resources needs evidence that the denominator pool contains every teacher relevant to the target. The methodology distinguishes personnel teaching primary, secondary/vocational, both levels, and special education. It also covers foreign curricula and special-regime education. The current evidence does not establish how every mixed-stage or special-regime teacher is allocated to the secondary CSV. The absence of a separately named mixed-stage table does not establish that mixed-stage teachers are omitted. Accordingly, this package establishes actual municipal observations while leaving complete pool coverage and high-school allocation unresolved.

The next admissible improvement requires a stage allocation or a documented complete superset of relevant teachers, together with a consistent student universe. Dividing Batxillerat enrollment by the broader secondary pool would manufacture a point estimate from incompatible stage scopes.
