# Cape Town travel-decay sensitivity

Recomputed GHS2025 resident in-person formal-school pupils aged14–18 in actual grades10–12 at decay scales15,20,30,45,60 minutes. The sample remains182 pupils; all216 PSUs in14 relevant strata enter sampling variance, including96 PSUs with no target pupil. No new observations or main-model changes.

`derive.py --rebuild` reads the existing local V63 source ZIP and releases only six-bin weighted totals and a6×6 centered PSU cross-product. `derive.py` reproduces all five results offline from these aggregate sufficient statistics. No individual or PSU identifiers are exported. Source and script hashes are recorded in `summary.json`.

For endpoint-bin utility vector a and weighted bin totals T, let D=1'T and theta=a'T/D. With C=sum_h[n_h/(n_h-1)]sum_p(T_hp-mean_h)(T_hp-mean_h)', the Taylor variance is (a-theta1)'C(a-theta1)/D². This is algebraically the V63 person-residual estimator. The two endpoint intervals use t(202) quantile0.9875; their outward endpoints form the same approximate joint95% envelope.

Time bins retain conservative closures [0,15],[15,30],[30,60],[60,90],[90,infinity). Unknown time stays[0,1]; optional membership was zero in the reviewed extraction. Calibrated weights remain fixed, with no FPC or calibration adjustment. Intervals are per-scale approximations, not a simultaneous confidence band across scales. Larger tau changes the preference penalty for travel, not the observed trip duration.

The tau30 envelope reproduces both the V63 result and current V108 Cape Town travel cell to absolute tolerance2e-14. The other four scales must be combined with equally rescaled city inputs before interpreting ranking sensitivity.
