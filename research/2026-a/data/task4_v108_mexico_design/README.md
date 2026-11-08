# EIC 2025 CDMX design-aware variance diagnostics

## What the source establishes

The official sampling-design PDF and descriptor are preserved in `../task4_v107_mexico/` and their hashes are recorded here. The PDF's printed pages, rather than PDF viewer page indices, are referenced below.

- §1.4, pp. 3–5: one-stage stratified cluster sampling, with simple random sampling **without replacement** within strata. Selected geographic clusters include all inhabited private dwellings. This is not a PPS or two-stage design. UPM normally denotes a block in localities with at least 250 inhabited private dwellings and a whole locality below that threshold. Stratification is within municipality by locality population size.
- §1.6, pp. 7–8: natural expansion factors are N_h/n_h, then corrected for household nonresponse within the sampled UPM. The text does not establish calibration weighting. Final FACTOR must not be inverted to recover the natural sampling fraction.
- §2.1, p. 10: the official total-variance expression includes finite population correction. We do not have verified stratum population PSU counts N_h, so omit that correction and explicitly use a with-replacement approximation.
- §2.5, p. 15: official jackknife guidance for fertility retains singleton-stratum and census-area observations in estimates, although singleton strata do not generate deletions. No singleton occurs in this CDMX person file.
- The census-municipality annex is ordered by entity and contains no entity 09. That does not prove each sampled CDMX stratum has sampling fraction below one. The 83 PSU with final FACTOR=1 are retained; we do not infer certainty status from this value.
- The descriptor names ESTRATO as stratum, UPM as primary sampling unit, and FACTOR as expansion factor. The design document explicitly directs users to these microdata fields.

## Domain and retained design

All 442,778 CDMX person records establish the observed design frame: 49 strata, 3,433 observed PSU, no singleton strata, and 3,384 design degrees of freedom. Every PSU has a constant person expansion weight. There are 586 PSU with a zero target group×time vector; all remain in stratum means and sample sizes. Filtering to eligible students before identifying the design would incorrectly discard these clusters. Another diagnostic counts 399 PSU without any attending 14–18-year-old, a broader cohort than the modeled conditional group.

All observed person-file PSU are retained. This does not prove that wholly nonresponding selected PSU are recoverable from the public person file. Fixed final response-adjusted weights are used; uncertainty in the weights themselves is not modeled. The approximation may overstate the design contribution when sampling fractions are large, but this is not a blanket coverage guarantee for every omitted source of uncertainty.

## Public sufficient statistics

`design_moments.json` contains a city-level vector of 24 expansion-weight totals and a 24×24 symmetric matrix. Labels are three V107 membership groups × fixed codes `1,2,3,4,5,6,9,blank`. For PSU vector z_hj, the matrix is

    W = sum_h [n_h/(n_h-1)] sum_j (z_hj - mean_h)(z_hj - mean_h)^T.

No stratum identifier, PSU identifier or person record is published. The histogram of PSU counts per stratum records the design sizes without geographic labels. Original and intermediate PSU data remain ignored locally. The totals exactly match V107's independently published aggregate bins.

For any fixed candidate numerator a and denominator b, A=a'T, B=b'T, r=A/B, and

    SE(r) = sqrt((a-r*b)' W (a-r*b)) / B.

`derive_design.py::derive_from_moments()` is nonmutating: it verifies the moment-file hash and returns candidate ratio totals, SEs, coefficients and their 2×2 A/B covariance matrices. `derive()` is an alias. Running the script explicitly writes `candidate_ratios.json`. Nine fixed prefixes per endpoint include zero-weight codes and use a deterministic code order to resolve utility ties; the resulting minima/maxima reproduce V107.

The reported selected-candidate SEs are diagnostics, not official INEGI intervals. Coverage for an identification-bound envelope requires an explicit inferential construction; the source package does not select a confidence-envelope rule. Current-stage membership remains conditional, as in V107.

## Reproduction

- Offline: `python3 derive_design.py` uses only public moments.
- Optional original-source regeneration: `python3 extract_design.py` verifies the V107 ZIP hash and processes the local ignored ZIP. It stores per-PSU sufficient counts only under ignored `local_only/`, then publishes city-level moments.
- `audit_direct_psu.py` independently compares every candidate SE with direct stratum-centered PSU residuals from that local intermediate. No identifiers are written to the audit report.
