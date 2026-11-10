# Helsinki and Dublin transit acquisition ceiling

Improving these two transit lower bounds cannot resolve the current champion set or change the conservative recommendation on its own. Under the retained V204 inputs and either registered weight vector, even the relaxed endpoint where both transit utility lower bounds reach 1 retains **Oslo under fixed weights, Zurich under equal weights, 16 possible champions and zero necessary champions**.

The certificate covers the entire rectangle between the retained lower bounds and 1. With upper scores fixed, city i's maximum regret is `max(0, max(U_k for k != i) - L_i)`. Increasing either target's lower bound decreases its own regret while leaving every other city's regret fixed. Both targets still have larger regret than the retained choice at their highest lower bounds. The endpoint also retains every possible champion and no necessary champion; decreasing lower bounds cannot remove a possible champion or create a necessary champion. These monotonicity arguments extend the endpoint checks to all intermediate values, without a grid approximation.

The two-coordinate endpoint reduces the hypothetical 16-city mean score width from 15.7767827274 to 15.3016525108 under fixed weights, and from 18.3021208336 to 17.3676383514 under equal weights. These are **relaxed ceilings on the improvement available from these two lower bounds**, not actual improvements: utility 1 is not obtained from any finite stop count under `density/(50+density)`. No new observation is admitted and actual primary width reduction is zero. Full ranking stability, other cells, other weights and later joint acquisitions are outside this certificate.

`city_cases.csv` contains four endpoint configurations × two weight vectors × sixteen cities (128 rows). `verification.json` binds the implementation and source files, records independent scalar formula checks against the model implementation, and preserves the retained CSV and utility arrays. `peer_review.json`, when present, records the separate reviewer’s checks. Reproduce in a scratch copy or move the existing output aside in a scratch checkout; the script refuses to overwrite this frozen output:

```bash
PYTHONDONTWRITEBYTECODE=1 /data/scratch/himcm-current-check-env/bin/python research/2026-a/scripts/task4_current_two_city_transit_ceiling.py
```

This result supports a bounded source-feasibility check rather than a large new traffic-data integration. Matched Zurich teacher/student and travel-distribution evidence remains more directly relevant to reducing decision ambiguity in the current acquisition diagnostics.
