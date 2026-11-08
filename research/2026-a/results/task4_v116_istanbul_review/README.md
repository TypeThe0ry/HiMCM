# V116: actual high-school journeys recovered; current-year gap retained

The official Istanbul 2012 household travel datastore yields 2,463 identified current high-school students aged 14–18, including 1,811 valid observed school journeys. An independent roster audit retains 15 possible additional members. This replaces a previously inaccessible source with reproducible historical evidence. The current V114 evidence registry remains unchanged.

## Result and interpretation

Holding all other 249 city-indicator cells, utility transformations and weights fixed, substituting the historical empirical travel interval [0.31500258196933106, 0.5814034635501898] changes Istanbul's inherited-weight minimax-regret decision rank from 7 to 4. Its score bounds move from [35.10706405, 55.34182975] to [37.33439159, 51.79539939]. This is a narrower score interval and a better conservative decision position, not evidence of an improvement in the city over time. All 25 candidates remain possible champions, and Singapore remains the minimax recommendation. Under equal weights the decision rank changes from 4 to 3, also with all 25 possible champions.

The historical substitution is an explicitly mixed-vintage diagnostic, not a 2012 cross-city ranking or a 2025 measurement. The interval retains missing journeys and uncertain cohort membership. It is conditional on the recovered sample and person weights; the survey design has not been reconstructed sufficiently to claim a population confidence interval. Withdrawing the historical input restores travel [0,1] and the current baseline exactly. The main registry and existing current-model Monte Carlo inputs stay unchanged.

## What the data add to age and fairness analysis

The age-group table in ../task4_v116_historical_travel/ uses the observed 2012 enrollment and ages. Optional-member marginal utility bounds overlap: ages 14–15 [0.35961314, 0.55710880], ages 16–18 [0.29347081, 0.59345612]. Their observed-duration means are 29.44 and 32.72 minutes, respectively, but missing coverage differs. These observations do not identify age preferences or prove older students face worse population-level conditions. The unknown-age members can enter either marginal group, but must not be counted twice in the city total.

District aggregates describe known-member travel samples, with small districts pooled. They do not yet measure equitable access to parks, pools or other facilities. That extension requires student-weighted residence coverage and usable facilities, including fees, opening hours and eligibility. No facility-count penalty or age-specific preference weight was invented.

## Source findings

- ../../data/task4_v116_ibb/: official questionnaire, API metadata, projected-query provenance, duration-weight histogram and aggregate-only reproduction. The original response CSV was not archived; provider-extracted source text is explicitly labeled. The API roster count matches the report, while the catalog's incomplete-source flag remains disclosed.
- ../../data/task4_v116_ibb_review/: independent cohort/NULL-age controls and scope review. The final optional mass is 4,487, not the earlier incomplete 3,875.
- ../../data/task4_v116_tbmm_review/: the previously unread 2025 parliamentary reply is now extracted. Its school-bus/public-transport shares concern all students, and its 60-minute statement is planning context, not a measured high-school duration distribution. Neither is substituted into travel.
- ../../data/task4_v116_tuik_access/: an original 2025 research report describes the national 2022 child-survey microdata's geographic limitation. Ordinary access cannot be assumed to identify Istanbul; confidential linkage or a provider-produced table remains an unverified option.

The additional official SKUp source check identifies a 2024 household survey of 70,000 people. Its published bus share does not supply high-school duration, and the survey extends beyond Istanbul to Kocaeli and Tekirdağ. This is the next acquisition priority; see `../../data/task4_v116_tuik_access/ibb_2024_route_audit.json`. The older 23.3-minute all-stage school statistic is dated 2012, while 15 minutes is a 2040 target.

## Unchanged model

For utility vector u in [0,1]^10 and fixed nonnegative weights summing to one:

    S(u) = 100 sqrt(sum_j w_j u_j^2) /
           (sqrt(sum_j w_j u_j^2) + sqrt(sum_j w_j (1-u_j)^2))
    L_i = S(lo_i); U_i = S(hi_i)
    R_i = max(0, max_{k != i} U_k - L_i)
    recommendation = argmin_i R_i
    possible champion i iff U_i >= max_{k != i} L_k

Default weights are 0.1125 for each of eight main indicators and 0.05 for each of two auxiliary indicators. Historical travel utility is exp(-t/30), evaluated per student before weighting. If N is the observed weighted utility sum, W the known-member weight, M unknown-journey weight and O optional-member weight, its empirical bounds are [N/(W+O), (N+M+O)/(W+O)]. Here N=214675.20461984503, W=677016, M=177066 and O=4487. This preserves the existing missing-value rule.

## Reproduce

From the repository root:

```sh
python3 research/2026-a/data/task4_v116_ibb/verify_aggregates.py
python3 research/2026-a/data/task4_v116_ibb_review/verify.py
python3 research/2026-a/data/task4_v116_tbmm_review/verify.py
python3 research/2026-a/scripts/task4_v116_historical_travel.py
```

The remaining decision-relevant gap is evidence that supports present-period Istanbul high-school travel and its population coverage. No authored manuscript or Overleaf file was edited.
