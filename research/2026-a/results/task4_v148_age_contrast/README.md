# V148: joint historical age-group travel contrast

The retained Istanbul 2012 aggregate uncertainty set permits both age-group orderings even when the shared unknown-age mass is allocated once. The closure of younger-minus-older mean travel utility is **[-0.233304860844, 0.263249542848]**. Two separate finite-duration completions give **+0.238421822664** and **-0.208477140660**. These are feasibility statements for broad groups 14–15 and 16–18, not measured age effects, exact ages 14 and 18, representative preferences, current-year estimates or confidence intervals. Istanbul is a separate historical case; no primary city is added.

## Retained inputs and contrast

The sole numerical input is the unchanged `data/task4_v116_ibb/aggregate_results.json`. No raw respondent records are requested or reconstructed. The V122/V137 historical marginal outputs remain frozen. Travel utility remains q=exp(-t/30).

For younger and older groups respectively, the known weighted denominators are 217085 and 459931, known utility numerators are 78805.26459099671 and 135869.94002884784, and known-cohort unknown-duration weights are 41225 and 135841. Optional known-age weights are 1442 and 2433. Two optional unknown-age people have total weight T=612 shared between groups. This pool cannot be included in both groups in the same completion.

Let A=218527 and B=462364 include each group's optional known-age mass; N_A,N_B are the known utility numerators, U_A=42667 and U_B=138274 are each group's unknown-duration plus optional known-age mass. Set x as shared mass allocated to the younger group and T-x to the older group. In the declared interval model, including optional mass at the favourable utility endpoint improves the respective contrast; discarding it cannot improve either extremum. The lower and upper contrast functions are

- f(x)=N_A/(A+x) − (N_B+U_B+T−x)/(B+T−x);
- g(x)=(N_A+U_A+x)/(A+x) − N_B/(B+T−x), for 0≤x≤T.

Writing C_A=A−N_A−U_A>0 and C_B=B−N_B−U_B>0, f is strictly convex and g strictly concave. At x=T, f'=-7.60591397e-7<0 and g'=1.38549325e-6>0. Therefore f decreases and g increases throughout the interval: both extrema allocate all 612 shared weight to the younger group, once. The unconstrained stationary points are outside [0,T]. The continuous allocation relaxation attains both extrema at this vertex, which does not split either unknown-age person between groups.

Naively subtracting separate marginal intervals gives [-0.233842975523,0.263637990334], using shared mass in both denominators. Coupling tightens the contrast width by 0.000926562165; it does not identify a direction. Utility zero is a closure limit as t tends to infinity, so endpoints are infimum/supremum statements, not finite observed journeys. The two ordering witnesses instead assign unknown utilities 0.05/0.95 (about 89.872/1.539 minutes), retain all known numerators and weights, and include optional known-age members in their own groups. They satisfy the retained aggregate set, not an independently reconstructed set of all raw-record or physical constraints.

## Verification and scope

Run `task4_v148_age_contrast.py`, then `audit_task4_v148_age_contrast.py` with the existing `.venv-v120/bin/python` from the research repository. The producer evaluates closed-form stationary points. The independent verifier instead uses derivative signs, enumerates 5,151 allocations including unused shared mass, checks both finite witnesses and utility-duration inversion, and protects 139 frozen scientific files. The grid is a diagnostic; the convexity/concavity and endpoint signs establish the global bounds. Neither witnesses nor grid points are sampling draws or probabilities.

No data are admitted. Primary V136, V137 preference/future/model-comparison results, the original CSV, weights, anchors and score intervals remain unchanged; primary score-width reduction is zero. The owned paper's Section 6.4 gains a compact joint-feasibility result. Its documentation revision is V148; other six owned sections, previous numerical assets and team content retain their bytes. Selected summary, verification and witnesses accompany the paragraph in Overleaf; full code and derivation remain in research.
