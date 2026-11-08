# Independent review of EIC2025 CDMX aggregates

The saved2025 questionnaire and microdata descriptor support the selected variables and distinguish completed schooling from current attendance. The extraction reproduces442,778 person rows and weighted private-household population9,165,819, all within residence state09. Person-key uniqueness, source hashes, positive expansion weights and aggregate travel bins were checked without emitting individual values. The raw ZIP is ignored by Git.

An independent fractional-program root calculation reproduces both utility descriptors: legacy progression[0.26910816,0.52618657] and boundary3 optional[0.21382387,0.58410003]. The latter is wider because it relaxes an eligibility assumption. These are conditional, design-weighted partial-identification descriptors, not sampling confidence intervals or directly observed current-high-school city measures.

The questionnaire asks the last year/grade passed. Thus level4/5/7 with completed grades0–2 remains a progression-based stage assumption; making completed secundaria grade3 optional resolves only that particular boundary. Ages14–18 are included; age999 is optional when otherwise eligible. Codes6(no travel),9 and blanks retain[0,1], and reported minute categories are conservatively closed at15/30 rather than pretending exact times. Missing or unspecified schooling/attendance remains in the eligible optional pool under the declared rules.

The official design is stratified cluster sampling. FACTOR supports expansion, while uncertainty estimation must also use ESTRATO andUPM; no design-based confidence interval was computed here. Scope is habitual CDMX residents in private dwellings, with school destinations not restricted to CDMX. Institutionalized residents and unresolved current-stage membership prevent an unconditional city-high-school interpretation.

Run `python3 research/2026-a/data/task4_v107_mexico_review/audit.py` with the local-only raw ZIP present. The script writes only aggregate audit findings and independently checks the saved source-summary hash. No source files or main-model inputs are changed.
