# V187 independent mathematical review: joint commute-mean box

Zurich's uniform minimax-regret recommendation has an exact robustness boundary under the declared independent box for twelve CSV commute means: **7.1473304991% with fixed weights and 51.4235691502% with equal weights**. Oslo is the first binding rival in both references. These are conditional source-parameter sensitivity thresholds on active V181 user16 bounds; they do not estimate observed source errors, future changes, or probabilities.

## Definition and exact corner proof

Let z denote Zurich, I the twelve cities with finite CSV commute means t_i, and d in [0,1]. The hypothetical means independently satisfy t'_i in [(1-d)t_i,(1+d)t_i]. Their travel lower utilities become exp(-t'_i/30), and their travel upper utilities remain 1. All other bounds, weights and anchors remain fixed. Singapore's historical school-stage travel proxy and the unknown travel intervals for Vienna, Warsaw and Tokyo remain unchanged.

Use the existing fixed-ideal score S(u)=100 A/(A+B), where A=sqrt(sum_j w_j u_j^2) and B=sqrt(sum_j w_j(1-u_j)^2). Weight enters once under each squared distance. Define L_i=S(lower_i), U_i=S(upper_i), C_i=max_{k != i} U_k, and R_i=max(0,C_i-L_i). Self-exclusion matters; including U_i in C_i would change this diagnostic.

All U_i and hence all C_i are fixed. Increasing a travel lower utility increases A and decreases B, so it increases S. Increasing t'_i therefore decreases L_i and increases R_i, leaving every other city's regret unchanged. Define G(t')=R_z(t'_z)-min_{i != z}R_i(t'_i). Every pairwise difference R_z-R_i is maximized simultaneously by setting Zurich's mean to (1+d)t_z and the other eleven finite means to (1-d)t_i. Taking the maximum over rivals proves this same corner is the exact maximum of G over the complete twelve-dimensional box. This is a Cartesian-domain assumption; it is not probabilistic independence. Joint dependence restrictions could produce another boundary.

Along this corner path, R_z strictly increases because its positive mean increases, its travel weight is positive, S is strictly increasing in travel utility, and the regret floor remains inactive. R_z is smallest at d=0: 17.36804635503932 (fixed) and 16.63077901625193 (equal). Every rival regret is nonincreasing or constant. G(d) is consequently continuous and strictly increasing. Opposite endpoint signs give exactly one zero on [0,1].

For d below that zero, Zurich is the unique minimax-regret recommendation for every admissible mean vector. At the zero, Zurich remains a minimax recommendation throughout the box, with an Oslo tie at the corner. Above the zero, this corner supplies a counterexample to a universal Zurich recommendation. This decision property does not establish a necessary realized-score champion.

## Independent scalar verification

The review loaded `task4_user_v181_revision.revised_bounds()` and existing `task4_v5_model.weights(.1)`, then recomputed scores with scalar `math.fsum` and square roots, independently of the runner's evaluation helpers. Equal weights were ten values of 0.1. SciPy Brent solving used xtol=5e-16 and rtol=1e-15. The finite-mean set derived from the input was Zurich, Helsinki, Berlin, London, Amsterdam, Stockholm, Paris, Madrid, Milan, Dublin, Oslo and Prague.

| Quantity | Fixed weights | Equal weights |
| --- | ---: | ---: |
| Critical d | 0.07147330499127809 | 0.5142356915020831 |
| Critical percentage | 7.147330499127809% | 51.423569150208316% |
| First binding rival | Oslo | Oslo |
| Zurich/Oslo regret at boundary | 17.58926782383935 | 17.746081633628535 |
| Gap at d=0 | -0.4862847137381223 | -3.3991441588396683 |
| Gap at d=1 | 7.273772168984998 | 3.467497172303055 |
| Gap at d_star-1e-7 | -7.27724703608601e-7 | -6.9716708139822e-7 |
| Gap at d_star+1e-7 | 7.27724724924883e-7 | 6.971671098199295e-7 |
| Zurich mean at boundary, minutes | 42.751784869152 | 60.41800409093312 |
| Oslo mean at boundary, minutes | 28.78432754527038 | 15.058693563435423 |

The scalar gap returned zero in binary64 at each reported root. These digits describe computational precision, not measurement precision. A rounded root passed to a ranking helper may fall on either side of a numerical tie; apply an explicit tolerance or report the analytical equality.

Independent pairwise root solves identify the earliest rival crossing without relying on the nonsmooth minimum over rivals:

| Rival with a crossing on [0,1] | Fixed d | Equal d |
| --- | ---: | ---: |
| Oslo | 0.07147330499127824 | 0.5142356915020831 |
| Singapore | 0.16764289729997967 | none |
| Stockholm | 0.3712064811598721 | none |
| Prague | 0.3902244872345988 | 0.8486069150592257 |
| Berlin | 0.5385862416978983 | none |
| Dublin | 0.5536982174716625 | none |
| Helsinki | 0.7447536372614889 | none |
| Paris | 0.7521384379046339 | none |
| Madrid | 0.8170393206182731 | none |

Vienna, London, Amsterdam, Milan, Warsaw and Tokyo have no crossing in either reference. “None” follows from monotonic pairwise gaps and negative endpoint signs. Singapore is the closest fixed-weight rival at d=0, although Oslo binds first as d increases.

## Assumptions and edge cases

The proof requires fixed upper bounds, normalization, ideals and weights, plus separable lower-utility updates. Re-estimating weights, moving ideals, changing upper bounds or adding cross-city constraints requires another derivation. A generic zero regret floor can weaken strict monotonicity; positive Zurich regret supplies strictness here.

The domain d in [0,1] keeps all means nonnegative. At d=1, rival means can equal zero, giving a travel interval [1,1] under the declared mapping. Negative means are outside scope. The original CSV values and active V181 bounds stay the baseline; hypothetical means are neither replacement observations nor admissions.

The twelve-mean box differs from V185's one-Zurich-mean perturbation and from independently perturbing utility endpoints. Do not transfer the baseline sixteen possible champions to every parameter vector without recomputing that distinct property. No stochastic error model or time-series prediction enters this analysis.

Review status: exact corner reduction, unique boundary and binding rival independently confirmed. This review changed no manuscript, raw source, model registry or scoring script. The required English anti-defensive-writing skill and repository evidence/writing rules were applied.
