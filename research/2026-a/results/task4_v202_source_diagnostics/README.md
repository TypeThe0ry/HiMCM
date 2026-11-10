# Isolated V202 commute-source diagnostics

With the retained 26-venue Singapore physical public inventory, the fixed-weight Zurich single-mean tie is **40.06840 minutes**, with Singapore; the retained Zurich mean is 39.9 minutes. The sharp joint 12-mean box radius is **0.42205%**, also binding Singapore. At equal weights, Zurich remains uniquely minimax for every finite nonnegative Zurich mean in the single-mean experiment; the joint radius is **63.44548%**, binding Oslo. V200's corresponding fixed-weight thresholds were 40.52675 minutes and 1.57080%. These are conditional input-sensitivity results, not observed future changes or probabilities.

Each finite mean varies independently by at most a fraction δ in [0, 1], with all other bounds and weights held fixed. Strictly below the joint boundary, Zurich uniquely minimizes regret throughout the box; at the mathematical boundary it remains a minimax choice, with a tie possible at the worst corner; above it an admissible counterexample exists. The root is numerical: rounding the displayed percentage or evaluating within machine precision of it can change the reported tie. The saved signed gaps, nearby probes and full-precision roots support the boundary interpretation. The box is not evidence that all its components can occur together in reality.

With fixed weights, withdrawing Zurich's commute proxy, both Zurich and Dublin proxies, or all 12 means selects Singapore; withdrawing Dublin alone selects Zurich. Equal weights select Zurich in all five evaluated cases, including retained input. Each evaluated case has 16 possible and zero necessary champions; this count is not asserted for the entire mean domain. The independent scalar scoring and self-excluded regret calculation agree with the evaluation entry within 1.43e-14. Two weight settings each test all 4,096 corners at 5% and at their boundary, for 16,384 corner checks. The saved outputs include 160 withdrawal ranking rows, 800 withdrawal bound rows, 202 single-mean probes, 192 joint ranking rows, 1,920 joint bound rows, 144 joint mean rows and 30 pairwise rival comparisons.

The 26 count is a named physical venue inventory, not a count currently open or universally accessible to adolescents. The OCBC Aquatic Centre's multiple basins count as one venue; operating, age and closure conditions remain relevant. Source capture and the 2024 population denominator have different dates. The primary V202 revision separately evaluates the 23-venue old-notices-only and 22-venue all-notices withholding cases; this directory retains the 26-venue input for commute sensitivity. The original CSV, other 159 lower bounds, all upper bounds and weights are unchanged relative to V200. The comparison is conditional on these retained inputs and the Jensen-based lower utility exp(-mean/30), with an upper utility of one; it is not a measured distribution of individual travel times.

Run from the repository root:

```sh
/data/projects/HiMCM/.venv-v120/bin/python research/2026-a/scripts/task4_v202_source_diagnostics.py
```

`summary.json` records inputs, proofs, cases and full-precision thresholds; `comparison.json` compares V200; `input_verification.json` records the 407 source bindings, the changed cell and current paper-resource hash checks. This isolated replay does not activate V202 or alter the current manuscript.
