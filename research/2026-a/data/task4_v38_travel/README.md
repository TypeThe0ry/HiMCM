# Copenhagen: verified current-school-stage extraction route (2026-11-07)

**No observed city commute value obtained. Preserve the existing missing interval.**

DTU TU0625v1 covers May 2006–December 2025. Its official variable catalogue, archived here, distinguishes current upper-secondary pupils: `RespPrimOcc=116` (printed p.22; HHX/HTX/STX/HF). `RespEduLevel` instead describes highest completed education (p.23), and is unsuitable for identifying current pupils. Home municipality is `HomeAdrMunCode`; Copenhagen is code 101. Trip duration is `tur.SumMin` (p.113), rather than the whole-day duration in the session table.

Next extraction must verify actual home-to-education journeys, residence geography, school-day selection, survey weights and respondent sample size. Restrict to current upper-secondary pupils, retain uncertainty, and report a respondent-based estimand rather than inadvertently weighting frequent travellers more heavily. Diary duration should not be divided by two.

Official free self-service dashboard: <https://transportvaner.dk/> (PowerBI). Its usable filters and downloadable observations remain unverified: the browser provider was unavailable in this audit. No regional microdata or point estimate was acquired, and no contact request was sent.

Documentation index: <https://www.man.dtu.dk/Myndighedsbetjening/Transportvaneundersoegelsen-TU-/Data-og-Dokumentation/Dokumentation>.

Earlier Tokyo 2021 value (87 minutes) was already audited in `task4_v6_commute`: daily combined work/school travel among actors, not a one-way school commute. It remains excluded. This round adds an actionable, stage-specific data route; it does not justify narrowing any interval or changing ranks.
