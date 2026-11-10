# V124 evidence companion

`task4_v124_update.tex/.pdf` is a three-page companion containing the two newly verified facility inventories, the controlled V121-to-V124 baseline comparison, and the implications for further evidence collection. The source numbers and two-row table are generated from audited research results, not hand-transcribed. The mandatory English anti-defensive-writing skill governs the prose: the actual precision gain leads, its size and unchanged recommendations remain explicit.

The primary research registry is now V124 (16 cities, 10 indicators). Fixed-weight average score width falls 16.18302472→16.15002092, about0.204%; static decision orders under fixed/equal weights are unchanged, with Zurich conservative recommendation and 16 possible champions. The current inventory is112 point/29partial/19fullymissing cells. All139 previously nonfullymissing cells and the raw CSV remain unchanged.

**Version boundary:** the complete V123 review paper, V122 chapters and their preference/future/method extensions remain frozen on V121. The companion does not relabel their results or claim that they have been migrated. Recompute those extensions on V124 and then unify the full paper before calling a later complete draft current. The actual Team Control Number and full AI records are still pending; this companion is not a final contest submission. No teammate prose or shared entry file is changed.

Build from repository root with pandas and Tectonic:

```sh
python drafts/build_task4_v124_update.py --research-root /path/to/HiMCM/research/2026-a
tectonic --keep-logs --keep-intermediates drafts/task4_v124_update.tex
python drafts/check_task4_v124_update.py
```

The manifest records research source hashes and unchanged shared/V123 manuscript hashes. The checker verifies headers, pages, warning/reference status and key generated values. `--render-review-confirmed` must be used only after separately rendering and visually reviewing all final pages. Final three-page rendering has passed; compiler output is warning-free. Original source archives remain in the research repository, with official URLs in the companion bibliography.

The unified full migration is now available in `task4_v125_paper.tex/.pdf`, using V124 evidence and audited V125 extensions. This evidence companion remains a frozen record of the two-cell update.
