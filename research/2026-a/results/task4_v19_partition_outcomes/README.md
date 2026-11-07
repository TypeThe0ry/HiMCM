# V19: what subgroup information actually changes

Using real subgroup counts from the 96 Phoenix school responses yields a tighter conditional outcome interval without assuming the schools have disjoint cohorts. Under stable cross-record ethnicity labels, the unique graduate lower bound rises 655→1,056 and the non-graduate lower bound 263→279. [Data, witnesses and assumptions](../../data/task4_v19_phoenix_partitions/README.md) make the source of the gain explicit.

The decision effect is small. Against V18's Phoenix + NYC2024 conditional model, at outcome weight beta=.10:

| Scenario | Phoenix outcome lower | Phoenix outcome upper | Phoenix score width | Phoenix decision rank | Possible champions |
| --- | ---: | ---: | ---: | ---: | ---: |
| Previous unrestricted labels | .0313472 | .9964709 | 49.08205 | 24 | 25 |
| Stable labels | .0495868 | .9962570 | 49.02338 | 24 | 25 |
| At most 16 excess labels per outcome type | .0488722 | .9964709 | 49.02630 | 24 | 25 |
| At most 100 excess labels per outcome type | .0451028 | .9964709 | 49.03878 | 24 | 25 |
| At most 401 excess labels per outcome type | .0313472 | .9964709 | 49.08205 | 24 | 25 |

Thus the stable-label condition narrows Phoenix's score interval by only 0.05867 points (about 0.12%), with no ranking or champion-set change. Mean score width falls 40.92760→40.92525; the best worst-case regret remains 32.89836. All cities' decision ranks remain unchanged. It would overstate the result to describe the higher count lower bound as a large decision improvement.

The label-change budgets are sensitivity parameters, not measured data. The graduate gain disappears at 401 excess category memberships and the non-graduate gain at 16. Without an empirically supported restriction on inconsistent labels, the previous bound remains the unrestricted conclusion. This explicitly shows the price of the additional classification condition instead of hiding it in a narrower interval.

## Scoring and champion test

For the added administrative completion utility q, the V18 score is unchanged:

    A_beta=(1-beta)*sum(w_j*(1-u_j)^2)+beta*(1-q)^2
    B_beta=(1-beta)*sum(w_j*u_j^2)+beta*q^2
    S_beta=100*sqrt(B_beta)/(sqrt(A_beta)+sqrt(B_beta)).

For each fixed beta in {0,.05,.10,.20}, the auxiliary weight alpha varies continuously over [.05,.20]. Main weights are (1-alpha)/8 and auxiliary weights alpha/2. Candidate i is possible where U_i>=max(k!=i)L_k. Root partitioning checks the continuous range. All 25 remain possible in every reported scenario; beta=0 reproduces the ten-criterion score and ignores the outcome dimension. The beta values are discrete cases, not a continuous-beta guarantee.

## Validation

- An independent agent reproduced all subgroup maxima and witness school IDs from the archived raw responses.
- All 96 school IDs use the same cohort filter as V18; raw-source hashes and All denominators are checked. Known group denominators never exceed each school's All count; incomplete coverage is allowed.
- Tests exhaust all 19,683 assignments of three people across three schools with two possible labels or absence, including label changes. The excess-label correction remains a valid union lower bound in every case.
- A one-person counterexample shows why summing category maxima is invalid without stable labels or an adequate excess-label budget.
- The 401-budget scenario exactly restores V18 utility endpoints. Model runs retain other cities' inputs and keep hypothetical budgets out of observation files.

The county-data search did not produce a usable Maricopa cohort total. The 59 existing NCES crosswalks report Maricopa for the 2024–25 school-directory year; the other 37 schools use current ADE coordinates. None of this substitutes for a matching historical county outcome aggregate, so state upper bounds remain unchanged.

```sh
python3 research/2026-a/data/task4_v19_phoenix_partitions/extract.py
python3 research/2026-a/scripts/task4_partition_outcomes.py
python3 research/2026-a/scripts/test_task4_partition_outcomes.py
```
