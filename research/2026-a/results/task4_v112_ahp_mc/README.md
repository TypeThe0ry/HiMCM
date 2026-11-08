# V112: neutral AHP reference and interval-preserving weight sensitivity

## Result

The neutral AHP reference and inherited policy both recommend Singapore by minimum worst-case regret and retain 25 possible champions. Equal weighting exchanges only Mexico City (24 to 23) and Mumbai (23 to 24) in the decision ranking; Kendall tau versus the prior decision ranking is 0.993333. The inherited arm exactly reproduces V108. This is a preference sensitivity extension, not new observations or improved predictive accuracy. The selected evidence registry remains V108/latest evidence review V111.

No applicable elicited AHP matrix exists in the inspected inputs. The neutral reference A_ij=1 explicitly assumes equal priority, yielding w_j=0.1 and CR=0. This is an analyst reference, not a survey; consistency is automatic, not evidence that students agree. See ../../design/task4_ahp_elicitation/README.md for the provenance audit and primary-source rationale. Genuine documented judgments can be passed through --ahp-json; metadata presence does not authenticate their truth.

## Controlled comparison

All 250 current utility intervals are unchanged, including 132 fully unknown [0,1] cells. No raw observation, source year, geography, normalization anchor or ideal point changed. The midpoint is an illustrative completion, never an imputed observation. At the inherited central weights its leader is Copenhagen; at neutral equal weights its leader is Singapore. Both interval decisions still prefer Singapore. A point leaderboard and a worst-case decision leaderboard answer different questions.

For each of two centers, draw 10,000 weights at each concentration kappa=20,100,500, totaling 60,000. Lower concentration means stronger perturbation. Seed 20261108, NumPy SeedSequence([seed,kappa]); weights are sampled, utility values are not. These analyst-chosen distributions span individual-criterion preferences beyond the old auxiliary-total [0.05,0.20] family. They are not estimated student preference distributions.

| Center | Strong kappa=20 | Medium kappa=100 | Weak kappa=500 |
|---|---:|---:|---:|
| Inherited: Singapore minimum-regret recommendation frequency | 63.65% | 88.05% | 99.60% |
| Neutral: Singapore minimum-regret recommendation frequency | 76.85% | 97.92% | 100.00% |

Under inherited weights, Copenhagen leads midpoint average ranks at all three concentrations. Under neutral weights, Copenhagen leads at 20, Singapore at 100 and 500. In the neutral strong-perturbation run Singapore has the higher midpoint first frequency (60.28% versus 28.46%), but Copenhagen has the better mean rank (2.1059 versus 2.4074). Thus first frequency and average rank need not select the same city; aggregation choice should be declared before viewing results.

All six sampled possible-champion unions contain all 25 cities. Some strong-perturbation draws admit only 17 possible champions, but this conditional exclusion does not establish evidence-driven narrowing. Neither fixed central weights identify a necessary champion. Sampled extrema are not continuous-domain certificates. The old restricted-weight certificate is not contradicted by a broader preference domain.

The practical improvement is detection of previously hidden preference dependence, explicit separation of illustrative point rankings from evidence-supported possibilities, and a reproducible AHP input check. No claim is made that the winner became more accurate or that missing data were resolved. Real learning-quality data and missing student travel observations remain the substantive next evidence needs.

## Formulas

A w = lambda_max w; sum_j w_j=1;
CI=(lambda_max-N)/(N-1); CR=CI/RI, with RI_10=1.49.

D_i^+(u,w)=sqrt(sum_j w_j(1-u_ij)^2),
D_i^-(u,w)=sqrt(sum_j w_j u_ij^2),
S_i=100 D_i^-/(D_i^++D_i^-).

This uses sqrt(w) coordinates and fixed ideal points 0/1, matching the previous model. It does not multiply coordinates by w and then inadvertently square importance weights.

For rectangular evidence intervals, monotonicity gives L_i=S_i(lower_i,w), U_i=S_i(upper_i,w).
R_i=max(0,max_{h!=i} U_h-L_i); recommend argmin_i R_i.
Possible champion: U_i>=max_{h!=i} L_h. Necessary champion: L_i>=max_{h!=i} U_h (ties allowed).

w^(b)~Dirichlet(kappa*w0); midpoint rank r_i^(b) uses (lower+upper)/2 only as an illustrative scenario; mean rank=(1/B)sum_b r_i^(b). First/top-three boundary ties are split fractionally. Possible-champion frequency averages the above interval condition across sampled weights. It is not a probability over missing observations or a real-world winning probability. Frequency Monte Carlo standard error is at most 0.005 at B=10,000, excluding assumption uncertainty.

## Reproduce and inspect

From research/2026-a:

```sh
python3 scripts/task4_ahp_mc_baseline.py --output results/task4_v112_ahp_mc
python3 -m unittest discover -s scripts -p test_task4_ahp_mc_baseline.py
```

- baseline_comparison.csv: prior and neutral decision ranks, midpoint ranks, score intervals and possible/necessary status.
- monte_carlo_city_summary.csv: average midpoint ranks, first/top-three frequencies, interval possibility and minimax frequencies, sampled rank bounds.
- monte_carlo_weight_summary.csv: stated centers and theoretical/empirical dispersion.
- utility_bounds.csv and weights.csv: exact input interpretation.
- summary.json: seed, version, source-bound and script hashes, validation and six-run summaries.
- ../task4_v112_ahp_mc_review/: independent replay audit.

No manuscript files were changed. This directory is a research result, not a replacement for the team's Overleaf prose.
