# V20: reported high-school journeys versus modeled historical routes

Official RHTS 2010–2011 microdata now supplies actual reported school-purpose journeys for directly identified current grade 9–12 students. The earlier NYC travel interval came from the mean of modeled walk/transit routes for ninth graders in 2013–2014. V20 compares these historical alternatives; it does not infer a time trend or claim current 2026 travel has been observed.

The all-age current-high-school cohort has 476 known non-homeschooled NYC members and 127 optional members; 365/37 respectively have a qualifying first direct home-to-school-purpose journey. The age-under-19 alternative has 460 known and 33 optional members. Missing journeys, unknown attendance/stage and unknown age where relevant retain interval or membership uncertainty. [Source, extraction and full scope](../../data/task4_v20_nyc_travel/README.md).

## Results: only the NYC travel cell changes

| Baseline model | NYC travel alternative | NYC decision rank | NYC score width | Mean score width | Possible champions |
| --- | --- | ---: | ---: | ---: | ---: |
| V16, ten criteria | Previous modeled routes | 18 | 46.2820 | 37.8657 | 25 |
| V16, ten criteria | All-age reported trips, sampling envelope | 22 | 44.6116 | 37.7989 | 25 |
| V16, ten criteria | Under-19 reported trips, sampling envelope | 22 | 43.9522 | 37.7725 | 25 |
| V18, outcome weight .10 | Previous modeled routes | 4 | 41.5292 | 40.9276 | 25 |
| V18, outcome weight .10 | All-age reported trips, sampling envelope | 5 | 39.8143 | 40.8590 | 25 |
| V18, outcome weight .10 | Under-19 reported trips, sampling envelope | 5 | 39.2098 | 40.8348 | 25 |

The under-19 alternative reduces NYC score width by about 5.03% in V16 and 5.59% in V18. Its decision rank worsens because the reported-trip lower utility is below the old modeled-route lower bound. More precise evidence need not improve a city's rank. Seven V16 decision ranks and two V18 ranks change; Kendall tau is .96667 and .99333 respectively. Phoenix remains 24. Singapore remains the minimax-regret choice, and the best worst-case regret is unchanged in each model (28.1736 for V16,32.8984 for V18).

Every scenario retains 25 possible champions at alpha=.10 and over the continuous auxiliary weight range [.05,.20]. The outcome weight is fixed at .10 in the V18 comparison; no continuous two-weight claim is made. `ranks.csv` contains all 250 city/model/scenario rows, including known-stage-only and optional-membership intermediate cases.

## What improved, and what remains unknown

The measurement now uses reported diary durations of current high-school students rather than modeled travel routes or an all-age commuting proxy. It handles zero observed school journeys, indirect first school trips, unknown cohort membership, household sampling and age scope explicitly. The main numerical gain is a lower upper bound; the lower bound also falls. Accordingly these alternatives **replace** the old cell and are not presented as nested evidence about one fixed year and target.

The under-19 exploratory utility envelope is [.21398056,.56200752], versus the old [.34993775,1]. Intersecting them would incorrectly retain the old lower bound. The all-age envelope is [.19246098,.60611391]. These envelopes include exploratory household resampling, not official confidence coverage. None removes the age of the source, reporting uncertainty, or school-campus identification limitations.

The source-year limitation remains decisive: this is usable historical evidence, not a current citywide census. A separate official 2024 NYC survey was downloaded and rejected for the minor-high-school target because its weighted diaries cover adults only. No adult-only replacement is used to manufacture recency.

## Formula and checks

Travel utility is E[exp(-T/30)], bounded using person weights, unknown journey endpoints and exact optional-member ratio extrema. In the ten-criterion model:

    A10=sum_j w_j*(1-u_j)^2; B10=sum_j w_j*u_j^2.

For the conditional added graduation outcome q:

    A_beta=(1-beta)*A10+beta*(1-q)^2
    B_beta=(1-beta)*B10+beta*q^2
    S=100*sqrt(B_beta)/(sqrt(A_beta)+sqrt(B_beta)).

Use beta=0 for V16 or .10 for the V18 comparison. Main weights are (1-alpha)/8; auxiliary weights alpha/2. Candidate i is possible where U_i>=max(k!=i)L_k. Continuous-alpha feasibility partitions at all comparison-polynomial roots.

Validation checks include original-source hashes, unique household/person/linked-trip joins, current enrollment and home-school flags, person/household weight precision, duration versus clock equality, missing-journey retention and the exact one-cell model change. Independent raw-data reconstruction and fractional programming matched the membership interval. Another independent reviewer checked 500 random membership cases against 56,652 exhaustive subset ratios, and first-trip selection against original place sequence. Tests retain a reproducible smaller exhaustive regression suite. Model source and baseline-matrix hashes are stored in `summary.json`.

```sh
python3 research/2026-a/scripts/task4_nyc_reported_travel.py
```
