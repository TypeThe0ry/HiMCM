# Singapore: real school-stage travel distributions, 2020

Official Census2020 table124 supplies five duration bins for current education stages. Downloaded JSON API matches the original report at printed423–424. Table93 supplies all-stage totals174298/56663/72676 for secondary/postsecondary(nontertiary)/polytechnic; the travel table reports172487/55674/71041. The residual1811/989/1635 is retained at utility[0,1], not silently removed. These are household survey weighted estimates; sampling confidence intervals are not manufactured.

`extract.py` applies the unchanged exp(-t/30) utility to bin endpoints, with continuous conservative closures [0,15],[15,30],[30,45],[45,60],[60,infinity]. No bin midpoint or finite tail cap is introduced. Published integer counts and denominators are propagated outward by0.5 for rounding. Unknown proportions across the three education stages are handled by their interval convex hull. The resulting all-stage-proxy utility is[0.2104836424,0.6188393016]. No finite weight mixture is asserted.

This is a historical school-stage proxy, not an identified interval for exactly14–18-year-olds or2025. The conditional16-city revision admits it alongside the inherited mixed-year/proxy inputs; the parallel `withdraw_historical_stage_proxy` scenario restores this cell to[0,1]. Temporal change, within-stage age selection and survey sampling uncertainty are not solved by the bin bounds.

Sources:
- https://data.gov.sg/api/action/datastore_search?resource_id=d_e87b21cfebae1a77150eccded58ab116
- https://www.parliament.gov.sg/docs/default-source/default-document-library/cop2020sr2.pdf
- https://data.gov.sg/datasets/d_e87b21cfebae1a77150eccded58ab116/view

The initial SingStat.pdf URL returned404; the official Parliament mirror and official API succeeded. Source hashes and calculations are in derived_bounds.json. Reproduce with `python3 research/2026-a/data/task4_v120_singapore/extract.py`. PDF is original bytes; the local full-text extraction is expendable and not committed.
