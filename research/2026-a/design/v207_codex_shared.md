# Shared brief for all V207 Codex writers

You are one of four writers revising a HiMCM 2026 Problem A paper (best city for a high schooler) in parallel. Each writer works in its own git worktree on its own branch and edits ONLY its assigned region of `main.tex`. Other writers are editing the other regions at the same time, so touching anything outside your region causes merge conflicts. Never edit the preamble (`\newcommand` definitions) unless your task says so. Do not touch ref.bib, mcmthesis.cls or figures/. When done, `git add main.tex && git commit -m "<short message>"` on your branch. Do not push.

Read first: /data/projects/HiMCM/GUIDELINES.md, /data/projects/HiMCM/docs/guidelines/WRITING.md, /data/projects/HiMCM/docs/guidelines/EVIDENCE.md, /data/projects/HiMCM/research/2026-a/visuals/guidelines/anti-defensive-writing/en/SKILL.md. Then read the current Sections 4 and 5.1-5.2 of main.tex (already revised) so your notation matches (utility u, anchor a, weights w_j, distances D_i^+ and D_i^-, score S_i, utility range [l, h]).

## Writing style (very important)
It must read like a strong student team wrote it, not an AI. Plain, concrete English; short and medium sentences; one idea per sentence. No em-dashes, no "not X but Y" rhetoric, avoid "deliberately/plainly/honestly/crucially/notably/robust/leverage/underscore", no rhythmic triplets, no repeated disclaimers. Lead each paragraph with the finding, then the number, then what it means for a high schooler. Do NOT write "Here x is ... " after every single equation; define symbols once, briefly, where needed. Never write "no data", "missing" cells or question marks as a result: every cell now has a value or a known range.

The advisor's complaints that drove this revision: text too dense, reader cannot see the point; weights looked arbitrary; formulas stacked; results with intervals confusing; figure and table repeating each other; future section full of jargon.

## Data changes in this version (all writers must be consistent with these)
- Zurich homicide: the supplied 0.14 per 100,000 had no verified denominator. We use 0.45 per 100,000: 2 completed homicide offences in 2025 in the Zurich city police crime statistics (cite `zhpks2025`) divided by the 2025 population of 440,935. Zurich stays first unless this rate exceeds 0.69 per 100,000.
- The 11 cells that had no city data now use stated proxy values:
  - Upper-secondary pupils per teacher, national values from Eurostat table educ_uoe_perp04 (ISCED 3, 2024): Helsinki 17.4 (Finland), Amsterdam 16.4 (Netherlands), Dublin 14.2 (Ireland), Paris 11.5 (France), Milan 10.6 (Italy), Madrid 9.6 (Spain). Zurich and London are not covered by Eurostat; they take the median of the other fourteen cities, 13.45.
  - Mean one-way travel time: Vienna 32 min (Vienna Chamber of Labour commuter study), Tokyo 47.5 min (2021 Japanese Survey on Time Use and Leisure Activities: 95 minutes of commuting/school travel per weekday in Tokyo, halved for one way), Warsaw 27 min (the 2022 Warsaw survey school trip already cited as `warsaw2022`). Like the other means, these enter as the range [exp(-t/30), 1].
  - New bib keys are NOT available; cite existing keys where they exist (`warsaw2022`, `zhpks2025`) and otherwise name the source in the text (e.g. "Eurostat table educ\_uoe\_perp04").
- Result: 112 + 11 = 123 cells are single values (or proxy values) and 37 are known ranges; no cell is fully unknown.

## Numbers (all from /data/projects/HiMCM/research/2026-a/results/task4_v207_ahp/; do not invent any)
Files: summary.json, main_ranking.csv (score = representative score at range midpoints; rank; category columns; u_* utilities), withdrawals.csv, controlled_cases.csv, future_2035.csv, catchup_cut.csv. Round scores to 1 decimal.
- Ranking: 1 Zurich 64.5, 2 Madrid 63.3, 3 Singapore 62.5, 4 Milan 61.1, 5 Dublin 60.8, 6 Paris 60.8, 7 Helsinki 58.7, 8 Prague 58.4, 9 Oslo 57.6, 10 London 56.1, 11 Berlin 55.6, 12 Stockholm 55.4, 13 Warsaw 54.5, 14 Vienna 54.4, 15 Tokyo 54.0, 16 Amsterdam 45.2.
- Tiers: top = ranks 1-3 (62.5-64.5), middle = ranks 4-9 (57.6-61.1; 1.4-point gap from Singapore to Milan), bottom = ranks 10-16 (1.5-point gap from Oslo to London; Amsterdam 9 points behind Tokyo).
- Weights: AHP from a high schooler's view, category weights safety & environment 0.340, education 0.340, cost 0.123, mobility 0.123, daily life 0.073; CR 0.0059.
- AHP vs equal weights (the significant revision): equal weights put Zurich, Oslo, Paris, Dublin on top; AHP puts Zurich, Madrid, Singapore, Milan; 12 of 16 cities change rank; Kendall tau 0.517.
- Score ranges (each uncertain cell at its lower or upper end): Zurich 60.5-67.2, Madrid 58.5-66.6, Singapore 59.4-65.1. Minimum maximum regret also picks Zurich (6.1), then Singapore (7.8) and Madrid (8.7). 9 of 16 cities could still be first if every range broke their way.
- Zurich homicide entry removed entirely: Zurich falls to 8th and Madrid becomes first. Amsterdam's homicide utility (0.06) drives its last place; the supplied numerator is not reproduced by official CBS counts; removing it lifts Amsterdam only to 15th.
- Weight perturbation (Dirichlet around AHP weights, 10,000 draws): Zurich first in 56.3% (kappa 20), 82.8% (100), 98.7% (500); Madrid takes most of the rest.
- Preference scenarios (double both education weights, or both mobility weights): Zurich stays first in both (education priority: Zurich 63.3, Madrid 62.1, Singapore 61.3).
- Data withdrawals (AHP weights): Zurich stays first after removing the 13 pre-2020 points; Madrid becomes first after removing the 64 post-2025 points; Milan becomes first after removing the 28 non-ok flagged points or the 95-point union. Under equal weights Zurich stays first except in the union (Milan).
- All 31 controlled source cases from the earlier source audit keep Zurich first.
- VIKOR (v = 0.5, same utilities and AHP weights): Madrid, Zurich, Paris; the acceptable-advantage condition fails and stability holds, so VIKOR does not separate Madrid and Zurich clearly.
- 2035 scenarios (each listed raw value changes 10% by 2035, all cities at once): S1 more facilities (+10% higher-education institutions, stops, pools), S2 higher costs (+10% living cost, housing ratio, travel time), S3 better schools and air (-10% pupils per teacher, PM2.5, travel time). Score changes: S1 +0.1 to +0.3, S2 -0.4 to -0.5, S3 about +1.0 for every city; the top three never change; the only swap is Dublin and Paris (5th/6th) under S3.
- Catch-up: one city alone cuts pupils per teacher, PM2.5 and travel time while all others stay at today's values. Cut needed to reach Zurich's score: Madrid 12%, Singapore 19%, Milan 30%, Paris 32%, Dublin 33%, Helsinki 46.5%, Prague 49.5%, Oslo 53%, London 61.5%, Berlin 68.5%, Warsaw 70%, Stockholm 71%, Tokyo 74%; Vienna and Amsterdam do not reach Zurich even with a 95% cut.

## Figures already in figures/ (final; refer to them, do not edit)
- figures/indicator_compare.pdf (label fig:indicator-compare, already in Section 4.2): heat map of utilities, 16 cities sorted by rank x 10 indicators grouped in five categories; colour 0 worst to 1 best; an asterisk marks a known range shown at its midpoint.
- figures/radar_tiers.pdf: three radar charts of the five category scores (0-1): top ranks 1-3 (Zurich, Madrid, Singapore), middle ranks 7-9 (Helsinki, Prague, Oslo), bottom ranks 14-16 (Vienna, Tokyo, Amsterdam), each against the dashed 16-city mean.
- figures/future_2035.pdf: panel A a table-like heat map of score change by 2035 per city under S1, S2, S3 with today's score, boxed cells where the rank changes; panel B horizontal bars of the cut needed to catch Zurich, sorted, with a note that Vienna and Amsterdam do not reach Zurich.

## Before committing
Compile with `tectonic -X compile main.tex --keep-logs` in your worktree (other writers' regions may still show old text; that is expected). Fix undefined references you caused. Report what you changed and any doubts.
