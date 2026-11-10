# Acquisition priorities under current V200 evidence

All 48 uncertain entries remain in the diagnostic: 11 fully unknown and37partial intervals, evaluated under baseline and equal weights. `all_uncertain_priority.csv` has96rows; `endpoints.csv` has192cases and `lower_only_refinements.csv` has480cases. The primary16-city matrix, original values, weights and intervals are unchanged.

## Complete exact utility identification

The following baseline-weight reductions are guaranteed only if the selected utility is completely and exactly identified somewhere in its current interval. They are not expected collection yields, source-availability probabilities or guarantees for a newly found count/mean.

| City and indicator | Guaranteed maximum-regret reduction | Best possible reduction | Optimistic champion exclusions |
|---|---:|---:|---:|
| Zurich pupil–teacher ratio | 1.229485 | 9.340177 | 5 |
| Zurich travel utility | 1.229485 | 5.962097 | 0 |
| Dublin pupil–teacher ratio | 1.066798 | 5.356177 | 1 |
| Zurich transport density | 0.450188 | 1.106728 | 0 |
| Dublin travel utility | 0.424075 | 1.066798 | 0 |
| Zurich pool density | 0.342826 | 0.891339 | 0 |

All single-entry guaranteed reductions under equal weights are zero. Endpoint exclusions are optimistic conditional limits, not achieved reductions of the current16possible champions. Zero regret reduction does not by itself mean no information or champion-set value.

Relative to the preceding V199/V197 diagnostic, the only changed input interval is Singapore's pool lower bound, represented by two weight-reference rows. The exact-identification guarantee for Zurich teacher/travel rises from0.364245to1.229485; transport from0.036885to0.450188 and pools from0to0.342826. Singapore's best-possible travel and transport gains also increase; Berlin travel's optimistic exclusion ceiling becomes1rather than0. `previous_comparison.csv` retains the full paired comparison, including unchanged entries and labels.

## Partial evidence and validation

`lower_only_refinements.csv` raises only the selected lower bound in five declared fractions while preserving its upper bound. These conditional scenarios do not promise that a real source attains any fraction. They must not be presented using the exact-identification guarantee above. No new source was admitted and the actual score-width reduction in this diagnostic is0.

`scripts/audit_current_priority.py` independently checks all96envelopes with scalar squared-distance sums, self-excluded regret, endpoint/root candidates and9,696strict interior probes. It verifies192endpoints,480lower-only scenarios and all paired comparisons. `verification.json` records11,187scalar evaluations,407immutable scientific bindings, original CSV, current four registries and the seven current Overleaf source dependencies unchanged during the audit. The paper and Monte Carlo outputs were not rerun or edited.

## Bounded source follow-up

The new Zurich education page offers custom statistics but supplies no matching city/stage teachingFTE. The Swiss Urban Audit country metadata is dated2012; the municipal2024commuter page contains location/count and mode charts, not a matched duration distribution for retained39.9minutes. All three official originals, length/status/hash and scoped text were verified in `source_verification.json`; no new utility interval is admitted. See `data/current_zurich_fte/` and `data/current_zurich_travel/` for the exact records and constraints. No external data request was sent.
