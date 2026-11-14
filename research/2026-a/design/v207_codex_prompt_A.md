You are revising a HiMCM 2026 Problem A paper (best city for a high schooler). Work ONLY in /data/projects/HiMCM-Overleaf on the already-checked-out git branch `advisor-rev`. Edit `main.tex` only. Do not commit, do not push, do not touch ref.bib, mcmthesis.cls or figures/.

Read first: /data/projects/HiMCM/GUIDELINES.md, /data/projects/HiMCM/docs/guidelines/WRITING.md, /data/projects/HiMCM/docs/guidelines/EVIDENCE.md, and the English anti-defensive writing skill at /data/projects/HiMCM/research/2026-a/visuals/guidelines/anti-defensive-writing/en/SKILL.md.

## Why this revision
The team advisor read the paper and found Chapters 4-5 hard to follow: too dense, the reader cannot tell what each indicator means, the weights look arbitrary, and the TOPSIS formulas are stacked three per equation with heavy notation. Your job in THIS run is Chapter 4 and the first two subsections of Chapter 5 (weights and the TOPSIS method). A later run will rewrite the results, robustness, future and conclusion sections, so leave everything from `\subsection{Scoring results and interpretation}` onward untouched, and leave Sections 1-3 untouched except the Notation table.

## Writing style (very important)
The prose must read like a strong student team wrote it, not like an AI. Plain, concrete English. Mix short and medium sentences. One idea per sentence. Avoid: em-dashes, "not X but Y" / "rather than" contrasts used as rhetoric, words like "deliberately", "plainly", "honestly", "crucially", "robust", "leverage", "notably", triplet lists for rhythm, repeated disclaimers ("these are not confidence intervals" etc. — say it once where it matters). State what is measured, how, and why it matters for a high schooler. Keep numbers that the reader needs; drop audit trivia.

## Target structure

### Section 4 retitled: `\section{Indicator construction and city selection}`
**4.1 City selection.** The subsection `\subsection{Why these sixteen cities}\label{sec:citychoice}` and its table `tab:cityset` were written by a teammate (Marc) today. Keep his text, rules R1-R4, his table and his paragraph "What the set is not" VERBATIM. You may only (a) rename the heading to `\subsection{City selection}` keeping the label, and (b) add at most two sentences at its start that name the sixteen cities. Fix nothing else in it.

**4.2 Indicator system.** Group the ten indicators into five categories, two indicators each (these groups are also the AHP hierarchy):
- Safety and environment: homicide rate (deaths per 100,000, cost, anchor 2); PM2.5 (ug/m3, cost, anchor 15)
- Cost of living: living-cost index (cost, anchor 100); housing price-to-income ratio (cost, anchor 10)
- Education: upper-secondary pupils per teacher (cost, anchor 15); higher-education institutions per 100,000 (benefit, anchor 1)
- Mobility: mean travel/commute time in minutes (utility exp(-t/30)); public-transport stops per 100,000 (benefit, anchor 50)
- Daily life: fixed broadband Mbps (benefit, anchor 100); public swimming pools per 100,000 (benefit, anchor 1)
Replace the current indicator table with one clear table: Category | Indicator | Unit | Better when (higher/lower) | Why it matters for a high schooler (a few words). Indicators that need a real calculation get their own numbered equations, written one formula per equation, each followed by one sentence saying what the symbols are:
1. utility of a benefit indicator u = x/(a+x) and of a cost indicator u = a/(a+x) (two separate numbered equations), with the anchor a explained as a reference level at which utility is 0.5;
2. facility density d = 100000 c / P (stops and pools);
3. upper-secondary pupil-teacher ratio = pupils / teacher FTE, matched to the same school stage (Prague's example: 71,325 pupils and about 6,139 FTE);
4. travel utility q = exp(-t/30), and why only the mean is known gives the range [exp(-mean/30), 1].
Use simple symbols (x, a, u, c, P, t). Then reference a new figure that I (the figure author) will supply: `figures/indicator_compare.pdf`, label `fig:indicator-compare`. Insert this float:
```
\begin{figure}[!ht]\centering
\includegraphics[width=\linewidth]{figures/indicator_compare.pdf}
\caption{CAPTION}\label{fig:indicator-compare}
\end{figure}
```
The figure is a heat map: rows are the 16 cities sorted by final score, columns the 10 indicators grouped by the five categories, cell colour is utility from 0 (worst) to 1 (best); cells with a known range show the range midpoint with a small dot, cells with no data are hatched grey and labelled "no data" in the legend. Write a short caption and 2-3 sentences of text pointing at real differences visible in the data (use the utilities in /data/projects/HiMCM/research/2026-a/results/task4_v207_ahp/main_ranking.csv columns u_*; e.g. Singapore and Zurich lead on homicide, Amsterdam is lowest on homicide, upper-secondary teacher ratios are missing for 8 cities). Remove the old figure float `fig:identification-matrix` (identification_matrix.pdf) and its text references.

**4.3 Data sources and missing values.** Condense the current subsections "A traceable city--indicator matrix" and "Collection problems and their resolution" (about 2.5 pages) into about two thirds of a page. Keep: the team table is the starting matrix and supplied values are kept; official statistical, operator and municipal sources fill empty cells; three counting rules in one short sentence each with one example each (count stations once, not platforms; match school stage before forming ratios; keep incompatible units out instead of converting); the outcome: of 160 cells, 112 are single values, 37 are known ranges and 11 have no data (8 teacher ratios, 3 travel); how a range enters the model (a utility range [lower, upper], and no data means [0,1]). Keep citations for the facts you keep; you may drop citations of facts you remove (do not delete bib entries). Where a sentence you keep was reworded by Marc today (Tveten bru exclusion; Tokyo machine-readable flags), keep his wording. Preserve `\label{sec:sourcepolicy}` (it is in a later section, do not move it) and any label still referenced elsewhere; run a check that every \ref and \cite resolves.

### Section 5
**5.1 Determining indicator weights (AHP).** Replace the current text (fixed 0.1125/0.05 weights and the exact-ratio AHP) with a two-level AHP from a high schooler's point of view. Write it in steps:
- Step 1 hierarchy: goal, five categories, ten indicators.
- Step 2 pairwise comparison of the five categories on Saaty's 1-9 scale. Give the 5x5 matrix as a table. Rows/cols order: Safety & environment, Cost of living, Education, Mobility, Daily life. Upper triangle: S-C 3, S-E 1, S-M 3, S-D 4, C-E 1/3, C-M 1, C-D 2, E-M 3, E-D 4, M-D 2 (lower triangle reciprocals). Justify briefly in a student's terms: a teenager's safety and schooling come first and are equally important; cost matters through the family budget and equals daily mobility; broadband and pools are nice to have.
- Step 3 weights from the principal eigenvector, consistency CI=(lambda_max-n)/(n-1), CR=CI/RI with RI=1.12 for n=5; report lambda_max, CI and CR=0.0059 < 0.1.
- Step 4 within each category a 2x2 comparison: homicide 2x PM2.5; living cost 1x housing; teacher ratio 3x higher education; travel time 2x stops; broadband 2x pools.
- One table of final weights (category weight, local weight, global weight). Exact values are in /data/projects/HiMCM/research/2026-a/results/task4_v207_ahp/summary.json (keys ahp, weights). Round to 3 decimals; make sure they sum to 1.
- One sentence: equal weights (0.1 each) are kept only as a comparison in the robustness section.
Each formula one per numbered equation.

**5.2 TOPSIS scoring.** Rewrite as numbered steps, one formula per numbered equation, simple symbols:
- Step 1: the utility matrix u_ij in [0,1] from Section 4.2 (no extra normalisation needed because utilities already share a 0-1 scale; the ideal is 1 and the worst is 0).
- Step 2: distance to the ideal D_i^+ = sqrt(sum_j w_j (1-u_ij)^2).
- Step 3: distance to the worst D_i^- = sqrt(sum_j w_j u_ij^2).
- Step 4: score S_i = 100 D_i^-/(D_i^+ + D_i^-).
- Step 5 (short): when a cell is a range, the city's score is also a range [S(lower), S(upper)] because S rises with every utility. For the main ranking we use one representative score, computed at the middle of each range; the full range is used only in the robustness section. Do not introduce regret, possible-champion sets, Jensen bounds or other machinery here; those belong to the robustness section the next run will write. You may delete the equations eq:regret and the possible-champion set from here; if a later section still references eq:regret, keep a copy of that equation (with its label) at the start of the subsection "A significant revision: retaining uncertain evidence" so the build does not break.

**Notation table (Section 3).** Update to match: x, a, u, c, P, t, w_j, D^+, D^-, S, lower/upper score. Remove symbols no longer used in Sections 4-5 only if no later section uses them.

## Checks before finishing
- Compile: `cd /data/projects/HiMCM-Overleaf && tectonic -X compile main.tex --keep-logs` (a missing figures/indicator_compare.pdf is expected; if it blocks the build, temporarily test with a copy of figures/score_intervals.pdf in /tmp, never commit or leave a placeholder in figures/). Fix all undefined references.
- `git diff --stat` and make sure nothing outside the allowed regions changed.
- Report: what you changed per subsection, page count of the build, anything you were unsure about.
