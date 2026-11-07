# Actual high-school diploma cohorts: conditional V18 comparison

Official NYC records now supply both graduate counts and cohort denominators. Preserving unknown outcomes, the four-year August diploma fraction is 83.2627–83.3120% for class 2024 and 81.1532–81.2210% for class 2025. These are two different entry cohorts and remain separate alternatives. The model does not intersect them or interpret their difference as a causal change in teaching quality.

The V18 calculation adds an explicitly conditional administrative completion dimension to the V16 ten-criterion matrix. NYC excludes charter schools and includes some out-of-district placements. Phoenix retains its geographically selected school-union bounds with unrestricted graduate duplication. Both describe jurisdiction-specific diploma completion, not harmonized learning outcomes or all-resident education quality. Global source admission is unchanged; Toronto is not inserted because matching entry-cohort denominators and coverage remain unresolved.

## Separate changing the criteria from adding evidence

All comparisons below use auxiliary weight alpha=.1. The outcome weight beta is a sensitivity parameter, not estimated from the data. Existing ten weights are multiplied by 1-beta. Other cities' unmeasured outcome utilities stay [0,1].

| Scenario | Outcome weight | NYC decision rank | NYC score width | Mean score width | Possible champions |
| --- | ---: | ---: | ---: | ---: | ---: |
| V16 ten criteria (beta=0) | 0 | 18 | 46.2820 | 37.8657 | 25 |
| Added outcome criterion, all outcome data unknown | .10 | 18 | 49.0575 | 41.2325 | 25 |
| Existing Phoenix evidence only | .10 | 18 | 49.0575 | 41.2287 | 25 |
| Phoenix plus NYC class 2024 | .10 | 4 | 41.5292 | 40.9276 | 25 |
| Phoenix plus NYC class 2025 alternative | .10 | 4 | 41.6283 | 40.9316 | 25 |

Within the fixed eleven-criterion design, NYC class 2024 evidence reduces its score width by about 15.35% and changes its minimax-regret decision rank from 18 to 4. This is an information-driven decision change: measured cities face less worst-case uncertainty. It is not evidence that NYC outperforms all less-measured cities. Phoenix stays 24 and Singapore remains the minimax-regret choice. At beta=.10 the best worst-case regret remains 32.8984 before/after the NYC update.

Adding a mostly missing criterion increases overall uncertainty: mean width 40.9276 after the data update is still larger than V16's 37.8657. Thus this iteration improves an observed cohort's information bounds, but does not improve the overall minimax guarantee or identify a champion. Both negative results are retained.

At beta=.05/.10/.20, NYC's class-2024 conditional decision ranks are 10/4/2. The class-2025 alternative has the same three ranks. These beta values are discrete sensitivity cases; no claim is made about every beta between them. For each beta case, alpha is checked continuously over [.05,.20] using all comparison-polynomial roots. All 25 cities remain possible. `ranks.csv` contains 500 city/scenario/weight rows.

## Mathematical model

For a published cohort with N members, G recorded diploma graduates and R unknown outcomes:

    q in [G/N, (G+R)/N].

For NYC class 2024: N=68,882, G=57,353, R=34. For class 2025: N=72,283, G=58,660, R=49. This is a missing-outcome bound within the published cohort, not a confidence interval or a coverage correction. SACC and GED/TASC do not count as Local/Regents diplomas in this outcome.

Let A10=sum(w_j*(1-u_j)^2), B10=sum(w_j*u_j^2), with w_j=(1-alpha)/8 for eight main criteria and alpha/2 for two auxiliary criteria. Then

    A_beta = (1-beta)*A10 + beta*(1-q)^2
    B_beta = (1-beta)*B10 + beta*q^2
    S_beta = 100*sqrt(B_beta)/(sqrt(A_beta)+sqrt(B_beta)).

Lower/upper scores evaluate lower/upper utilities. Candidate i remains possible when U_i >= max(k!=i)L_k; decision ranks order max(0,max(k!=i)U_k-L_i). Continuous-alpha comparisons use B_i*A_k-B_k*A_i, still a quadratic in alpha at fixed beta. Existing ten-criterion feasibility now delegates its root partition to the same helper; its mathematical rule is unchanged.

## Reproduction, source checks and validation

- [NYC source and extraction](../../data/task4_v18_nyc_quality/README.md): official XLSX and HTML, hashes, 48 cohort-period rows checked, four selected June/August rows, explicit residual outcomes.
- [Toronto method audit](../../data/task4_v18_toronto_quality/cohort_scope_audit.json): official method document describes original Grade 9 board attribution, entry ages 13–15, and tracking movers within Ontario. This is additional scope evidence, not the missing Toronto denominators.
- `summary.json` records actual baseline matrix SHA256 and derived source hashes. The runner asserts all 250 ten-criterion intervals agree with the archived V16 combined matrix.
- Tests verify all five beta=0 scenarios reproduce V16 scores/ranks and continuous champion feasibility, 400 direct affine-term score calculations and 80 collapsed-weight comparisons, exact ties and unchanged other-city utility inputs. The existing continuous solver's own checks also pass.

```sh
python3 research/2026-a/data/task4_v18_nyc_quality/extract.py  # requires openpyxl
python3 research/2026-a/scripts/task4_cohort_outcomes.py
python3 research/2026-a/scripts/test_task4_cohort_outcomes.py
```
