# V94: conditional upper-secondary subgroup bounds for a Jakarta school survey

The newly located [primary survey article](https://journal.uinsgd.ac.id/index.php/ministrate/article/download/27005/pdf), printed pages 218–220, reports 573 valid respondents: 311 SMP, 119 SMA and 143 SMK. Its home-to-school time histogram counts are 25, 242, 251, 40, 13 and 2. These are marginal totals; no school-type-by-time table was acquired. The English abstract's “high school” label must not convert all 573 into upper-secondary students.

The primary PDF is available through a text reader, but its original bytes were not downloaded and no screenshot was visually verified. `reader_transcription.json` explicitly records this status. The archived [companion primary paper](https://ejournal.uika-bogor.ac.id/index.php/komposit/article/download/14520/4594) is an original 826,737-byte PDF. It confirms a February–April 2023 Central Jakarta school survey and mixes SMP/SMA/SMK; its stated-choice time attributes are not the observed histogram.

Three source inconsistencies remain: the first-bin prose says under15 minutes while its chart label says under5; reported23 schools contrasts with12+4+6=22; reported76.65% valid contrasts with573/750=76.4%. The calculation conservatively closes time bins at [0,15], [5,15], [15,30], [30,60], [60,90], [90,infinity].

## What the marginals identify

With travel utility `u(t)=exp(-t/30)`, the entire valid sample has a histogram-compatible mean interval **[0.454349, 0.695745]**. Assigning that interval to its 262 SMA/SMK respondents would assume an unobserved joint distribution. Reusing the existing subgroup-capacity solver gives the broader, sharp conditional envelope **[0.313785, 0.861130]**.

Let `c_b` be the published bin counts and `z_b` the unknown SMA/SMK count in each bin. Solve

`min sum(z_b * lower_utility_b)/262` and `max sum(z_b * upper_utility_b)/262`,

subject to `0 <= z_b <= c_b` and `sum(z_b)=262`.

The lower allocation is `[0,0,207,40,13,2]`; the upper allocation is `[25,237,0,0,0,0]`. These integer allocations show that no cross-bin interpolation or fabricated individual record is required. The open-ended tail gives an infimum, not an attained infinite journey. “Sharp” refers to the conservative marginal constraints used here, not to any resolved source conflict or survey inference.

This is an unweighted sample diagnostic conditional on the reader transcription. School type does not reveal every individual's age/current grade. Residence, nonresponse, sampling weights and full-DKI coverage remain unresolved. It does not enter the city model; Jakarta travel remains [0,1]. No hypothetical stated-choice travel attributes, adult commute statistics or school-policy limits are admitted.

## Reproduction

Run `python3 research/2026-a/data/task4_v94_travel/audit.py` from the repository root. The audit checks the archived PDF hash, count totals and then compares the generic subgroup solver with independently specified linear programs and explicit integer allocations. [Summary](summary.json) · [source/transcription status](reader_transcription.json) · [manifest](manifest.json).
