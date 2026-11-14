You are continuing a revision of a HiMCM 2026 Problem A paper (best city for a high schooler). Work ONLY in /data/projects/HiMCM-Overleaf on git branch `advisor-rev`, editing `main.tex` only. Do not commit or push. Do not touch ref.bib, mcmthesis.cls or anything in figures/ (the figures are final and supplied by the figure author).

A previous run already rewrote Section 4 (indicator construction and city selection) and Sections 5.1-5.2 (AHP weights, TOPSIS steps). Read them first so your text matches their notation. Also read: /data/projects/HiMCM/GUIDELINES.md, /data/projects/HiMCM/docs/guidelines/WRITING.md, /data/projects/HiMCM/docs/guidelines/EVIDENCE.md, and /data/projects/HiMCM/research/2026-a/visuals/guidelines/anti-defensive-writing/en/SKILL.md.

## Writing style (very important)
Must read like a strong student team, not an AI. Plain concrete English, short and medium sentences, one idea per sentence. No em-dashes, no "not X but Y" rhetoric, no "deliberately/plainly/honestly/crucially/notably/robust/leverage", no rhythmic triplets, no repeated disclaimers. Lead each paragraph with the finding, then the number, then what it means for a high schooler. The advisor complained that the old results, intervals and future sections were dense, full of jargon, and that figure and table repeated each other. Fix exactly that.

## All numbers come from these files (do not invent any)
/data/projects/HiMCM/research/2026-a/results/task4_v207_ahp/: summary.json (keys: weights, ahp, comparison, interval_ahp, dirichlet, vikor, preferences, ahp_vs_equal, homicide_withdrawals, future_first), main_ranking.csv (score = representative score, rank, category columns), withdrawals.csv, controlled_cases.csv, future_2035.csv, catchup_cut.csv. Round scores to 1 decimal in prose and tables.

Key facts (verify against the files):
- Zurich homicide input changed. The supplied team value 0.14 per 100,000 has no verified denominator. The model now uses 0.45 per 100,000: the Zurich city police crime statistics (cite zhpks2025) list 2 completed homicide offences in 2025, divided by Zurich's 2025 population of 440,935. State in Section 4.3 (data handling) in one or two sentences that this is a modelling value derived this way (offences counted, not victims), replacing the supplied 0.14. Fix any sentence in Section 4 that still says the 0.14 entry is retained. Zurich stays first unless its rate exceeds 0.70 per 100,000 (summary.json zurich_homicide.tie_rate).
- Representative-score ranking (AHP weights): 1 Zurich 63.8, 2 Singapore 62.5, 3 Madrid 60.5, 4 Dublin 60.4, 5 Helsinki 59.7, 6 Milan 59.1, 7 Paris 59.1, 8 Prague 58.4, 9 Oslo 57.6, 10 Berlin 55.6, 11 Stockholm 55.4, 12 London 55.4, 13 Tokyo 53.2, 14 Vienna 53.0, 15 Warsaw 52.9, 16 Amsterdam 45.7.
- Tiers: top = ranks 1-2 (Singapore leads Madrid by 2.0 points), middle = 3-9 (57.6-60.5), bottom = 10-16 (1.9-point gap from Oslo to Berlin; Amsterdam far behind).
- Why: Zurich combines good safety (homicide utility 0.82), strong higher education (0.84), transit and pools; Singapore has the best safety (0.97) and broadband (0.87) but the weakest housing (0.31) and travel (0.41). Middle-tier cities trade strengths (Madrid safety 0.80; Prague and Oslo strong transit and pools and known teacher ratios). Amsterdam's last place comes mostly from its homicide utility 0.06; Section 4 notes that official CBS counts do not reproduce the supplied numerator; withdrawing it moves Amsterdam to rank 13.
- If Zurich's homicide entry is withdrawn entirely (treated as unknown), Zurich drops to rank 9 and Singapore becomes first. Say this in robustness and the conclusion.
- Score ranges and worst case: with each uncertain cell at its lower or upper end, Zurich's score range is 48.9-76.4 (wide: no teacher data, partly known transit and travel) and Singapore's 59.4-65.1. Minimum maximum regret picks Singapore (16.9), then Prague (21.7), Oslo (22.0), Zurich (24.8). 12 of 16 cities could still be first.
- Weight perturbation (Dirichlet around AHP weights, 10,000 draws each): Zurich first in 62.8% (kappa 20), 89.8% (kappa 100), 99.9% (kappa 500); Singapore takes nearly all the rest.
- Preference scenarios (double both education weights, or double both mobility weights, then renormalise): Zurich first and Singapore second in both.
- Data withdrawals (withdrawals.csv, AHP weights): Zurich stays first after removing the 13 pre-2020 points; Singapore becomes first after removing the 64 post-2025 points, the 28 non-ok flagged points, or the 95-point union. Under equal weights Zurich stays first in all but the union (Milan).
- All 31 controlled source cases from the earlier audit keep Zurich first on the representative score.
- VIKOR at the same utilities and AHP weights: order Zurich, Singapore, Prague; the acceptable-advantage condition fails, stability holds.
- AHP vs equal weights (the significant revision): equal weights give Zurich, Oslo, Dublin on top; AHP gives Zurich, Singapore, Madrid; 14 of 16 cities change rank; Kendall tau 0.583.
- 2035: each scenario changes the listed raw values by 10% by 2035 for every city at once: S1 more facilities (+10% higher-education institutions, stops, pools), S2 higher costs (+10% living cost, housing ratio, travel time), S3 better schools and air (-10% pupils per teacher, PM2.5, travel time). Score changes stay below 1.1 points; the only rank change is Stockholm and London swapping 11th and 12th under S1. Second analysis: one city alone cuts pupils per teacher, PM2.5 and travel time while the others stay at today's values; the cut needed to reach Zurich's score (catchup_cut.csv): Singapore 12.5%, Prague 44.5%, Oslo 48.5%, Berlin 63.5%, Stockholm 66.5%, Madrid 68%, Milan 72.5%, Warsaw 73.5%, Tokyo 75%, Paris 83%, Dublin 84%; Helsinki, London, Vienna and Amsterdam do not reach Zurich even with a 95% cut.

## What to write

1. **Results (`\subsection{Scoring results and interpretation}`).** Replace the old regret table and the interval figure (remove the float that includes figures/score_intervals.pdf and the table tab:baseline) with:
   - one compact table: Rank | City | Score | Tier, in two side-by-side halves (ranks 1-8 and 9-16) like the old table layout; bold the first-ranked row. Label tab:baseline (keep the label).
   - three short paragraphs: Top tier, Middle tier, Bottom tier, each explaining why with 2-3 concrete utilities.
   - the radar figure:
```
\begin{figure}[!ht]\centering
\includegraphics[width=\linewidth]{figures/radar_tiers.pdf}
\caption{CAPTION}\label{fig:radar}
\end{figure}
```
   It shows category scores (0-1, weighted mean of representative utilities in each category) for Zurich and Singapore (top), Madrid, Oslo and Prague (middle), Tokyo and Amsterdam (bottom), against the dashed 16-city mean. Do not repeat the table in the text.
   - delete the VIKOR paragraph and the `\MethodComparison` use here (VIKOR moves to robustness).

2. **Significant revision.** Replace the subsection "A significant revision: retaining uncertain evidence" with "A significant revision: from equal weights to AHP weights": why equal weights do not reflect a high schooler's priorities, what changed, the same-input comparison numbers above, and what it means. Keep one short paragraph saying that the score ranges are handled in the robustness section.

3. **Robustness (`\subsection{Sensitivity to the accepted input information}\label{sec:sourcepolicy}`).** Rename to "Robustness of the recommendation", keep the label, and rewrite as a compact set of checks, each a short paragraph with a bold lead-in: (a) score ranges and worst-case regret, with the regret formula as two numbered steps (one equation each; keep label eq:regret on the regret equation) and a plain-language reading; (b) the homicide-source dependence of Zurich (and Amsterdam); (c) data withdrawals as a small table (Withdrawn group | Cells | First under AHP | First under equal weights), label tab:vintage; (d) weight perturbation and preference scenarios in two or three sentences; (e) VIKOR as a method check, written in numbered steps with one formula per equation (group utility S_i, individual regret R_i, compromise index Q_i with v=0.5) and its result. Delete everything else that was in the old sensitivity subsection (bus subsets, Prague/Vienna witness details, commute radii, critical radii) since those numbers belong to the old weights.

4. **Section 6 "Model revision and extension".**
   - `\subsection{Considering future changes}`: rewrite in plain language: why look at 2035, what each scenario changes and why that is plausible for a city (one sentence each), how the change enters the model (raw value times r, then the same utility formulas; keep at most one short numbered equation), the result, and the catch-up analysis. Delete the Jensen/moment-bound equation eq:moment and the macros \FutureDeterministic, \FutureThresholds, \EvidenceThresholdCheck, \FutureMonteCarlo, \ProxyWithdrawalMC from the text (remove their uses; you may delete their \newcommand definitions if unused elsewhere). Insert:
```
\begin{figure}[!ht]\centering
\includegraphics[width=\linewidth]{figures/future_2035.pdf}
\caption{CAPTION}\label{fig:future}
\end{figure}
```
   Panel A: change in 2035 score per city under S1, S2, S3 (rank label shown only where the rank changes). Panel B: the cut needed for one city alone to reach Zurich's score; "not reached" means no cut up to 95% is enough.
   - `\subsection{Considering different preferences and development situations}` and `\subsection{Perturbing weights and point assumptions}`: their results are now summarised in robustness (d). Replace both with nothing, or at most a two-sentence pointer; remove the old Dirichlet table, Hoeffding paragraph, point-padding and per-point withdrawal paragraphs and their macros' uses (\PreferenceResults, \PreferenceEvidenceChange).
   - Leave `\subsection{Within-city fairness and growth stages}` and Section 7 (country comparison) unchanged.

5. **Everything that states the old headline.** The old paper recommended Oslo by minimum regret with fixed weights. Update to the new result (Zurich first on the representative score, Singapore the safest choice under worst-case data, Zurich's lead resting on its supplied homicide rate) in: the summary sheet (abstract), Section 1 where it describes method and result, the Assumptions section only if it mentions fixed weights, the Conclusion, the news article ("A city choice built around a student's day" and its subsections), and any \newcommand macros in the preamble that carry old numbers (\MethodComparison, \LatestEvidenceChange, \TotalWidthReduction, \CurrentMeanWidth, etc.: remove the ones no longer used; fix any still used). Keep the rest of those sections' wording as it is; change only sentences that state outdated methods or numbers. Do NOT edit the subsection "City selection" / "Why these sixteen cities" (a teammate's text) or the AI-use report.

## Checks before finishing
- Compile: `cd /data/projects/HiMCM-Overleaf && tectonic -X compile main.tex --keep-logs`. No undefined references or citations. `grep -n "Oslo" main.tex` and confirm no remaining claim that Oslo is the recommendation.
- Page budget: everything before the "Report on Use of AI Tools" must fit in 25 pages (the AI report does not count). Report the page number where the AI report starts. If over budget, shorten your own new text first, then condense `Within-city fairness` only as a last resort and tell me what you cut.
- `git diff --stat`; report per section what changed and anything you were unsure of.
