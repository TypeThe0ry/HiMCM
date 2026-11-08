# AHP input provenance and neutral reference

No elicited pairwise judgments applicable to the current ten criteria were found in the team inputs, design files, or model data. Main/auxiliary labels do not supply numerical comparisons. The inherited 90%/10% split is a modeling convention.

The runnable neutral reference uses A_ij = 1 for all criteria: an explicit equal-priority assumption, not a student survey. Its CR = 0 is an algebraic consequence and does not validate preferences. AHP weights are 0.1 each; this intentionally equals the equal-weight comparator. It adds a reproducible input/consistency interface, not new empirical information.

Primary-source rationale: [UNECE 2025 wellbeing guidelines, sections 4.13, 4.17–18 and 4.23](https://w3.unece.org/Stories/2025/09/wellbeing/webpage6.html) discuss transparent equal weighting, sensitivity analysis and opinion-based weights requiring good surveys. [Erbstein, Hartzog and Geraghty youth wellbeing study, section 3.3.3](https://link.springer.com/article/10.1007/s12187-012-9170-6) uses equal weighting within domains; its different domains cannot supply our ten pairwise priorities. Sources consulted 2026-11-08. Neither source supplies the current matrix or the Monte Carlo concentration parameters.

`pairwise_template.csv` contains 45 blank comparisons. A future respondent or documented group should supply positive importance ratios, identity/group description, collection date and reason. Values below one mean the second criterion is preferred. No blanks are interpreted as measured equal importance. The calculation requires a complete positive reciprocal matrix in canonical indicator order and records provenance. A consistency pass checks coherence, not representativeness or truth.

The current Monte Carlo design perturbs weights only, leaving every observed/unknown utility interval unchanged. Dirichlet concentrations are sensitivity assumptions, not estimated student preferences. Midpoint rankings and first/top-three frequencies describe the midpoint scenario; interval possible/necessary champion frequencies describe sampled weights. None is an empirical chance that a city is truly best.
