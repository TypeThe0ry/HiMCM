# Which retained point inputs need source verification first?

Single-cell withdrawal identifies where stronger provenance could change the conservative recommendation. Under V203, withdrawing one point utility changes the minimax choice in **10 of 112 fixed-weight cases** and **35 of 112 equal-weight cases**. The baseline choices are Oslo and Zurich, respectively. Each changed case chooses the other city uniquely. All cases still admit 16 possible champions and no necessary champion.

## Experiment

The 112 point utilities exactly match the values produced from the untouched user CSV. For each point separately, replace its utility range by `[0,1]` in temporary arrays, retain the other 159 cells and the existing weights, and recompute fixed-ideal TOPSIS score intervals and minimax regret. The 48 pre-existing interval cells stay fixed. Two weight references give 224 cases and 3,584 city-result rows.

This is an extreme ignorance stress used to prioritize source review. It does not assert that a retained value is incorrect, estimate its error probability, authorize a correction, or change the primary model. It differs from the common-radius perturbation experiment: one cell loses all information here, while that experiment widens all point utilities by a bounded common radius. The case count is a count of specified deterministic tests, not a probability of changing the recommendation.

## Source-review priorities

For the fixed weights, the ten switches come from eight Oslo points—homicide, PM2.5, cost of living, price/income, pupil/teacher ratio, higher-education density, broadband and pools—and the Zurich cost or price/income point. Withdrawing Oslo's higher-education utility has the largest excess regret for retaining the original Oslo policy among these tests: about **6.822 score points** relative to the new minimax choice. This is a policy comparison after hypothetical withdrawal, not an observed score loss or an improvement from newly collected data.

For equal weights, withdrawing Zurich homicide, higher-education density, broadband or PM2.5 changes the choice to Oslo; 31 other switching cases occur in other cities. Zurich homicide produces the largest original-policy excess regret, about **6.905 score points**. Its submitted `SUSPECT` flag is retained as a source-review cue. Across the 35 switches, 24 inputs carry `ok`, six `MODELLED`, four `STALE` and one `SUSPECT`. A submitted `ok` label is not independent verification, and a flagged value is not proven wrong.

The result directs the next review toward original Oslo higher-education and broadband definitions and the provenance and denominator of Zurich homicide, alongside the already identified missing teacher and travel data. Withdrawal of a competitor's point can also alter the policy because its upper score becomes less constrained; a switch does not identify an erroneous measurement or a causal city effect.

## Files and reproduction

- `cases.csv`: all 224 withdrawals, original values/years/flags, recommendation sets, regret comparisons and interval-width changes.
- `ranks.csv`: all 3,584 city-level score intervals, regret and rank outputs.
- `summary.json`: counts, untouched-source bindings and output hashes.
- `verification.json`: independent scalar TOPSIS and regret checks, plus protected primary and manuscript inputs.

Run `.venv-v120/bin/python research/2026-a/scripts/task4_current_point_withdrawal.py` to intentionally regenerate the diagnostic. The independent auditor is `scripts/audit_current_point_withdrawal.py`; it prints JSON by default, with explicit report output flags for saving. The original CSV, V203 intervals, four manuscript figures and current paper remain unchanged. New primary admissions and actual primary score-width reduction are zero.
