# São Paulo: direct travel-scale reevaluation of the V48 cohort

Recalculates exp(-travel_minutes/tau) from the existing OD2023 records for tau=15,20,30,45,60. It uses the **V48 age14–18 cohort**, not the older all-age cohort. Municipality36 is verified against IBGE3550308. ESTUDA4 means current upper-secondary attendance; age is directly observed. Original mirror provenance and unverified official byte identity remain unchanged.

The same 1,690 students and unresolved cases are retained. The first study-purpose journey must have a confirmed home origin, consistent positive duration and clocks, and verified weekday. Unresolved/no-journey students retain [0,1]. No new observations or tighter missingness assumptions were introduced.

## Paired recalculation

`extract.py` checks original decompressed DBF SHA256, municipality mapping and cohort consistency. It reuses V48's validated journey classification. For each scale it computes weighted lower/upper household contributions, then uses exactly V48's zone-stratified household bootstrap: all21,917 municipal households, including zero-eligible households; seed20261107;2,000 replicates; fixed final person weights; identical draws across all five scales. The reported envelope is min(point lower, bootstrap2.5% lower) to max(point upper, bootstrap97.5% upper). It remains exploratory, not an official design-valid confidence interval.

| tau minutes | Direct envelope | Width | Jensen transported width |
|---:|---|---:|---:|
|15|[0.268465204,0.433377771]|0.164913|0.411952|
|20|[0.339806172,0.505445759]|0.165640|0.313484|
|30|[0.441794965,0.607135087]|0.165340|0.165340|
|45|[0.536539154,0.699520991]|0.162982|0.275212|
|60|[0.596043172,0.756811343]|0.160768|0.337394|

At tau30, both point and sampling endpoints match the current V48 values within1e-12 (sampling endpoints match exactly in this run). Away from30, using the actual travel distribution avoids the broad mean-only Jensen transport. For p=30/tau, mean-only bounds are [L^p,U] if p>=1 and [L,U^p] otherwise. These comparisons transport the existing exploratory envelope; they do not upgrade its confidence interpretation. Results cover **five discrete scenarios**, not every continuous tau or a jointly calibrated confidence band.

## Public outputs and reproduction

`aggregate.json` contains city-level counts, a weighted observed-duration histogram, unresolved weight and weighted endpoint totals. `bootstrap_endpoints.json` contains only city-level replicate ratios; it has no person, household or zone identifiers. `manifest.json` hashes these public inputs and the exact inherited definitions/reference files. No original personal data or individual derivative is copied into this package; temporary DBF material is outside the repository and deleted by the extractor.

`derive.py::derive()` verifies hashes and reconstructs all envelopes nonmutating from the public aggregates. It independently checks each point endpoint against the duration histogram. Running `python derive.py` writes `summary.json`; its scenarios expose city, tau_minutes, utility_lower and utility_upper for model integration. Optional full raw regeneration is `python extract.py`, requiring NumPy and dbfread plus the existing source file. This run used `/tmp/himcm-parquet-arm/bin/python`, as V48 did. Neither old source files nor model/registry files were changed.
