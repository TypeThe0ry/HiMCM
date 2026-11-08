# Independent V113 revision review

`audit.py` checks the source-derived bounds separately from the production extractor: NPA PDF death-victim total 631, Singapore's degree-conferring university status and 2024 actual intake, nonduplication against the prior six institutions, and unchanged population denominators. It recomputes four evidence arms under two fixed weight vectors using the equivalent score-odds expression and direct interval inequalities.

Only Tokyo's conditional homicide utility lower endpoint and Singapore's partial-inventory lower endpoint change. The Tokyo strict arm removes the national-superset constraint. No city-observed homicide count, new school-travel observation, learning-quality measure or survey-derived preference is claimed.

`mc_audit.py` replays V113's 60,000 draws with independently written scoring/ranking calculations. It checks that every sampled-weight hash matches the corresponding V112 run, ensuring the before/after comparison changes evidence only. The source bounds are pinned to the V113 factory rather than a mutable current-model registry. Run after the V113 Monte Carlo output is complete.

From repository root:

```
python3 research/2026-a/results/task4_v113_revision_review/audit.py
python3 research/2026-a/results/task4_v113_revision_review/mc_audit.py
```

`validation.json` reports the source/fixed-weight checks; `mc_validation.json` reports completed Monte Carlo checks. Passing verifies the numerical and conditional source interpretation, not international completeness of recorded crime or an empirical preference distribution.

Additional crosschecks: `alpha_endpoint_check.json` and `alpha_certificate_crosscheck.json` independently check the restricted auxiliary-weight preference family. The numerical certificate has Tokyo as minimum-regret choice on [0.05,0.05531005859375], Singapore on [0.0553169250488281,0.2], and three unresolved leaves near the transition. A 10,001-point independent grid agrees with the certified regions; a grid is not itself a continuous proof. This source revision invalidates the previous claim that Singapore is the single recommendation throughout the old alpha range.

`post_revision_priority.py` recomputes acquisition requirements from the audited V113 saved bounds. A single-cell revelation still cannot exclude any city at either fixed weight reference. Relative to V108, Tokyo under equal weights now requires five hypothetical lower-endpoint cells instead of four; London's inherited-weight minimum remains four but the number of successful minimum bundles changes from one to nine. These are endpoint diagnostics, not admitted observations.
