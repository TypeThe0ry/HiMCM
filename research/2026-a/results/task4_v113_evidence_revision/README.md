# V113: actual source additions, unchanged decision rules

Two independently verified source additions narrow two lower utility endpoints. All weights, utility anchors, candidate identities and other 248 cells are unchanged. Neither addition supplies a new high-school travel observation. Original/equal-reference central-weight rankings are unchanged and all 25 cities remain possible champions. The substantive revision is less uncertainty and a corrected preference-stability conclusion, not a forced unique winner.

## New evidence and scope

1. Singapore: official MOE and UAS sources verify one additional independent degree-awarding university, with first 2024 intake and central Singapore address. The incomplete institution inventory increases from 6 to 7, with unchanged 2026 population of 6,208,500. HE utility lower bound .0881251377→.1013244554; upper remains 1. LASALLE/NAFA are not additional counts. Supply is not education quality/access. Source snapshot 2026-11-08 is not relabeled 2025.
2. Tokyo: official NPA 2025 Table 53 gives 631 recorded criminal-death victims nationwide, not cases/attempts. Within that reporting universe, Tokyo intentional criminal deaths are a subset of this deliberately broad national count. With unchanged Tokyo May 2025 population of 14,254,039, rateupper=631/14254039*100000=4.4268154451 and costutilitylower=2/(2+upper)=.3111961153. This is not an observed Tokyo rate and does not bound unreported deaths or resident vital mortality. The strict Tokyo withdrawal arm retains [0,1].

Original sources, SHA256 manifests and verification scripts: ../../data/task4_v113_singapore/ and ../../data/task4_v113_tokyo/. The national-superset assumption is explicit; no unsupported Tokyo-specific allocation is inferred.

## Before/after at inherited fixed weights

| Quantity | Before V108/V112 evidence | After V113 conditional |
|---|---:|---:|
| Tokyo score lower |40.116441|42.350083|
| Tokyo score upper |70.696070|70.696070|
| Tokyo interval width |30.579629|28.345986|
| Singapore score lower |43.457014|43.538541|
| Singapore score upper |71.594641|71.594641|
| Minimum worst-case regret |34.072446|33.990920|
| Changed decision ranks |—|0|
| Possible champions |25|25|

Tokyo's score interval narrows 7.3043%; Singapore's 0.2897%. The improved minimum regret is an information effect, not a measured improvement in city conditions. No ranking accuracy or causal improvement is claimed. Four arms (old, Singaporeonly/strict Tokyo, Tokyo only (conditional), both) under two fixed weight references isolate evidence contributions. Withdrawal of both restores V108 exactly.

## Same random weights, changed evidence

The same two weight centers, three concentrations, seed and 60,000 draws from V112 are reused. Independent audit checks the sampled weight hashes, so changes are attributable to the new bounds, not altered weight assumptions. Singapore's minimum-regret recommendation frequencies:

| Center / perturbation | V112 | V113 |
|---|---:|---:|
| inherited / strong k20 |63.65%|53.87%|
| inherited / medium k100 |88.05%|68.04%|
| inherited / weak k500 |99.60%|86.64%|
| equal / strong k20 |76.85%|71.30%|
| equal / medium k100 |97.92%|94.06%|
| equal / weak k500 |100.00%|99.99%|

The lower Singapore frequency is a material contrary finding: better evidence supports Tokyo more strongly. Frequencies depend on analyst-assumed Dirichlet weights, not actual student preferences or real winner probabilities. All six sampled possible-champion unions still contain 25 cities. See ../task4_v113_ahp_mc/comparison_v112.csv.

Within the ORIGINAL restricted auxiliary-total range [.05,.20], the refreshed numerical certificate recommends Tokyo on [.05,.05531005859] and Singapore on [.05531692505,.20]. Three tiny leaves between these bounds remain unresolved at the configured tolerance/depth. This supersedes the earlier all-range Singapore statement for the conditional Tokyo model. The interval certificate is numerical, not exact interval arithmetic; neither the transition gap nor 100% in a finite Monte Carlo run proves uniqueness over all preferences.

## Which missing data can change the possible set?

The V108 baseline acquisition audit separately investigates exclusion rather than changing the minimum-regret recommendation. At either fixed weight reference, NO single uncertain cell can shrink the25-city possible-champion set: its own upper-score reduction is insufficient, and its maximum lower-score increase cannot exclude another city. This holds for any exact observation within its existing interval by monotonicity. Under inherited weights, Istanbul needs at least 2 hypothetical cells at sufficiently unfavorable values; Lagos/Mumbai/Delhi/Dhaka/Shanghai at least 3, most others 4. These are endpoint information limits, not data to admit or predictions of attainable values. See ../task4_v113_exclusion_priority/README.md. The historical input version is pinned and explicit.

No new qualified Phoenix commute/education data were obtained this round. A Phoenix Speedtest development-host page was inspected but gives inconsistent prose/table date/statistic descriptions and is not admitted as a 2025 city median. No entire-city figure was inferred from individual ISP medians. Official pool search results were not used as a verified complete accessible inventory. Unknown observations remain unknown.

## Reproduce

From research/2026-a:

```sh
python3 data/task4_v113_singapore/extract.py
python3 data/task4_v113_tokyo/extract.py
python3 scripts/task4_v113_evidence_revision.py
python3 scripts/task4_current_model.py
python3 scripts/task4_ahp_mc_baseline.py --output results/task4_v113_ahp_mc
python3 scripts/task4_v113_evidence_revision.py --compare-mc
python3 results/task4_v113_revision_review/audit.py
python3 results/task4_v113_revision_review/mc_audit.py
```

The registry selects the conditional V113 evidence factory, while strict withdrawal remains explicit. Prior acquisition/stress analyses retain their source version labels. No manuscript content was changed.

## Unchanged mathematics

S_i(u,w)=100 sqrt(sum_j w_j u_ij^2)/(sqrt(sum_j w_j u_ij^2)+sqrt(sum_j w_j(1-u_ij)^2)).
L_i=S_i(lower_i,w), U_i=S_i(upper_i,w).
R_i=max(0,max_{h!=i}U_h-L_i); recommend argmin_i R_i.
Possible champion iff U_i>=max_{h!=i}L_h (ties retained).
Monte Carlo w~Dirichlet(kappa*w0), same kappa={20,100,500},10,000 draws for each center/case. No missing utility values are sampled or filled.

Post-revision priority check also finds no single-cell exclusion at either fixed reference. Equal-weight Tokyo now requires at least 5 hypothetical endpoint revelations rather than 4; all other minimum counts remain unchanged. These are lower bounds on information requirements, not predictions of future observations. See `../task4_v113_revision_review/post_revision_priority.json`.
