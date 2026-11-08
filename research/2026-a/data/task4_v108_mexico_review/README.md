# Independent review of EIC2025 design moments

Independent replay of the local-only raw person file verifies442,778 rows,49 strata and3433 observed PSUs. All586 PSUs with zero target-vector contribution remain included; there are no singleton strata and the reported degrees of freedom are3384. All24 weighted totals reproduce exactly.

The centered crossproduct was independently reconstructed using second moments rather than the source's row-wise centering loop. Its maximum absolute difference is9.45e-8 at aggregate-total scale, within the declared tolerance. All36 candidate ratios and Taylor standard errors also reproduce. The raw ZIP and local PSU table are Git-ignored; no personal or PSU identifiers are published by this review.

The official design is single-stage stratified cluster SRS without replacement. The published sufficient moments instead support an explicitly labeled **fixed-final-weight, with-replacement ultimate-cluster approximation without FPC**. Nonresponse-adjusted final factors are not independently established as calibrated weights. Natural inclusion probabilities, stratum population PSU totals and wholly nonresponding sampled PSUs have not been reconstructed.

The verified calculation is therefore useful for conditional sensitivity analysis, not a claim to reproduce the full official survey variance. Selecting one minimum/maximum candidate's standard error does not establish simultaneous confidence coverage. Current high-school membership remains inferred from completed schooling under the V107 progression assumptions.

Run `python3 research/2026-a/data/task4_v108_mexico_review/audit.py` with local raw data present. Output contains aggregate findings only; source files and the main model are unchanged.
