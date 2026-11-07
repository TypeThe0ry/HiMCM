# Phoenix graduation records: newer guidance and an excess-record sensitivity model

The May2025 ADE Grader provides a more relevant administrative rule than the old dual-graduation exception. Printed pp6–7 instruct concurrent schools to assign a graduation code through one diploma-issuing school and withdraw the other enrollment; p9 schedules validation of FY2024 graduates during May25–July1,2025. The existing report-card application maps fiscalYear2025 to cohort2024. `may2025_guidance.json` preserves page-marked paraphrases, a short quote and exact URLs. Direct PDF downloads failed; the archive is structured web-reader evidence, not original PDF bytes. The FY24 manual's indexed paragraph corroborates the last-school rule, but full-document absence of exceptions has not been verified.

This motivates an **administrative-compliance scenario**, not a claim that API school totals are already deduplicated. The unique graduation-code rule must actually govern the published aggregate counts for the scenario to apply. It does not prove cohort denominators or nongraduate counts are disjoint. Historical geography, state-versus-school outcome status and public-school coverage remain conditions. Any city target constrained by state public cohorts is restricted to that public-school universe; private-school outcomes and city-resident outcomes cannot silently be covered by these bounds.

## Excess records instead of a guessed maximum multiplicity

For school graduate sets A_s with counts G_s, define excess records as sum_s G_s - |union_s A_s|. An individual appearing at three schools contributes two excess records. If this excess is at most D and archived school graduate lower counts are l_s, then a conservative unique-graduate lower bound is:

    g_min(D) = max(max_s l_s, sum_s l_s - D).

There is no evidence-based measured value of D yet. D=0 is the new administrative-compliance hypothesis; progressively larger integer D values test noncompliance or aggregate-linkage errors. With the existing96 school records, sum(l_s)=10,620 and max(l_s)=655. At D>=9,965 the bound recovers the previous unrestricted-overlap result. Suppressed cells remain bounded; no suppressed value is filled in.

Assuming each city's graduates and nongraduates are subsets of the corresponding same-cohort statewide groups, with consistent outcome statuses, use state G=74,261 and F=20,240. Nongraduate overlap remains unrestricted, giving f_min=263. Thus:

    q_lower(D) = g_min(D)/(g_min(D)+20,240)
    q_upper = 74,261/(74,261+263) = 0.9964709355.

This is a conservative result, not a claim of sharpness after all school constraints are considered.

## Recomputed conditional rankings

The 11th outcome component has explicit sensitivity weight beta=.1, while the ten existing criterion weights are multiplied by.9. Other cities' outcome components stay [0,1]. These are rankings within this augmented conditional model, not changes to the ten-criterion main model.

| Allowed excess-record budget | Graduate-rate interval | Phoenix decision rank | Possible champions |
| --- | --- | ---: | ---: |
| 0 | [0.344135,0.996471] | 22 | 25 |
| 230 | [0.339210,0.996471] | 22 | 25 |
| 231 | [0.339188,0.996471] | 23 | 25 |
| 7,885 | [0.119042,0.996471] | 23 | 25 |
| 7,886 | [0.119004,0.996471] | 24 | 25 |
| >=9,965 | [0.031347,0.996471] | 24 | 25 |

The first rank loss at231 excess records shows the rank22 compliance result is sensitive to the unresolved duplication assumption. It does not estimate actual duplicates. No claim that the champion set has narrowed is supported.

All upper score endpoints are constant across D, so rivals' worst regrets are constant; Phoenix's lower score decreases monotonically. Integer binary search finds every crossing with a rival regret and evaluates both neighboring integer budgets. `../../results/task4_v14_duplicate_budget/` contains all25-city ranks, the unknown-quality baseline and summary. The script performs8,192 synthetic membership/lower-count checks and verifies recovery of the previously published unrestricted-overlap interval and rank. An independent agent additionally checked110,592 membership/suppression combinations and verified the count-bound argument.

The score remains S_i=100 sqrt(sum_j w_j u_ij²)/(sqrt(sum_j w_j u_ij²)+sqrt(sum_j w_j(1-u_ij)²)). Use the augmented weight vector (.9*w,.1) only for these outcome scenarios. Possible champions satisfy U_i>=max(k!=i)L_k; decision regret is max(0,max(k!=i)U_k-L_i).

```sh
python3 research/2026-a/scripts/task4_graduate_duplicate_budget.py
```
