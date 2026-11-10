# Zürich official-source follow-up

No compatible observation was identified in two focused searches. V202 retains its existing inputs and uncertainty bounds.

- [City of Zürich, teacher gender proportions](https://www.stadt-zuerich.ch/de/politik-und-verwaltung/statistik-und-daten/daten/bevoelkerung/gleichstellung/bildung-berufswahl/lehrkraefte.html): 2024 employment proportions by sex and school type for city and canton. The page does not supply a matched city secondary-school teaching FTE numerator and pupil denominator; do not admit a ratio.
- [Swiss Federal Statistical Office, commuting mobility](https://dam-api.bfs.admin.ch/hub/api/dam/assets/31525916/master): national 2022 one-way work-commute duration classes, with a 29.6-minute national mean. The geography and observation are not matched to the retained Zürich 39.9-minute mean; do not transfer its distribution.

`manifest.json` records the raw files, URLs, retrieval status and time, SHA-256, scope and admission decisions. These are source assessments, not model inputs. No institution was contacted.

The chart’s linked `teacher_gender_chart.csv` was also retrieved successfully. Its three fields (`stufe,sex,wert`) contain female/male percentages for seven school categories, with no absolute teacher count, teaching FTE or pupil denominator. It does not resolve the missing ratio. The archived values are retained as provided.
