# V95: observed mode cross-tabs narrow the Jakarta sample subgroup bounds

The same 262 SMA/SMK respondents now have a travel-utility envelope of **[0.339290, 0.794402]**, versus V94's **[0.313785, 0.861130]**. Its width falls **16.85%**, using newly acquired cross-tabulated observations and unchanged time-bin endpoints. The city-level Jakarta interval remains [0,1]: these results concern the surveyed Central Jakarta public-school respondents.

## Original source acquired

The [official ITB thesis record](https://digilib.itb.ac.id/gdl/view/74988/stated-preference) identifies Afrian Argarisma's 2023 thesis and labels its chapters PUBLIC. Three original PDFs were acquired through the site's advertised public viewer flow: chapter 5 (81 pages), chapter 3 (14 pages), and appendix (28 pages). `manifest.json` records stable source endpoints, byte sizes and hashes; ephemeral viewer parameters are omitted. The journal's PDF bytes remain unacquired; this package contains the thesis originals instead.

Chapter 5 supplies mode × school type (Table V.11, printed p75), mode × travel time (V.18, p86), and mode × age band (V.9, p72). All nine mode totals agree, with 573 respondents and 262 SMA/SMK students. The exact-age histogram (p64) reports two aged13 and eleven aged19–20. These four pages were rendered locally and visually checked. The appendix contains aggregate statistical output and blank questionnaire/scenario forms, not identified student records.

Source distinctions remain: the thesis time table uses under5, whereas the journal prose used under15; the matched comparison keeps the V94 conservative [0,15] first bin. The blank appendix questionnaire combines the above60 tail, while the results table splits60–89 and above90; analysis uses the published result counts and flags this instrument/result distinction. No stated-choice scenario duration enters the observed-travel calculation.

## Fixed school-type subgroup: same-target improvement

Let `n_mb` be the observed number in mode m and time bin b, and `H_m` the observed SMA+SMK count in that mode. The unknown subgroup bin counts `z_mb` satisfy

`0 <= z_mb <= n_mb`, `sum_b z_mb = H_m`.

Minimize `sum_mb lower_u_b*z_mb /262` and maximize the corresponding upper endpoint, using `u(t)=exp(-t/30)`. Unlike V94's single mass constraint, each mode now has an observed subgroup total. Independent extremal filling within modes gives the narrower interval above. The 16.85% comparison holds the population, utility, time closures and missing-joint-data treatment fixed; only the real mode cross-tabs are added.

## Age14–18 intersected with SMA/SMK

This is a separate target whose size is not observed. Per mode, let `O_m` be the published age19–24 count and `Y_m` the age13–15 count. The two age13 respondents have unknown mode allocation `q_m`, with `0<=q_m<=Y_m` and `sum_m q_m=2`. Then age-eligible count is `A_m=N_m−O_m−q_m`. The high-school-and-age target satisfies

`max(0,H_m+A_m−N_m) <= sum_b z_mb <= min(H_m,A_m)`.

Minimize/maximize `sum u_b*z_mb / sum z_mb`, retaining time capacities. The implementation uses `t=1/sum z`, `y=z*t`, `v=q*t` to obtain a linear program, with `sum y=1`, `sum v=2t`, and `1/262<=t<=1/249`.

The resulting envelope is **[0.331088, 0.807390]**. Lower and upper endpoints have target counts249 and251 respectively; transformed solutions return integer count allocations satisfying every original constraint. Thus the continuous solution also supplies attainable count configurations under these published marginals (time-bin open tails are interpreted as endpoint limits). This target change is not included in the 16.85% same-subgroup improvement claim.

These are unweighted sample identification envelopes, not confidence intervals or observed individual joint tables. Current school type is known; individual grade, residence-based city coverage, nonresponse adjustment and survey weights remain unresolved. No city-model input or manuscript is changed.

## Reproduce

Run `python3 research/2026-a/data/task4_v95_jakarta/audit.py` from the repository root. It verifies source hashes, extracts and cross-checks all three tables, recomputes both targets, checks inverse-transformed witnesses and writes [summary.json](summary.json). [V94 comparison](../task4_v94_travel/README.md).

独立复核脚本 `independent_check.py` 使用另行转录的原始表格，枚举249至262人的全部14个整数目标人数，计算28个未变换线性规划，并核对两个整数分配证据。结果与线性分式变换一致；运行 `python3 research/2026-a/data/task4_v95_jakarta/independent_check.py` 可复现。
