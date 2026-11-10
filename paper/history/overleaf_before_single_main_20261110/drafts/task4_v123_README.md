# V123 complete independent review draft

`task4_v123_paper.tex/.pdf` combines the verified V122 chapter contribution with a one-page summary, introduction, actual assumptions, notation, a controlled uncertainty revision, conclusion and two-page nontechnical news article. The main answer is 17 pages including references and news; a one-page provisional AI report follows. This is an independently reviewable paper draft, not a submission-ready declaration or a replacement of the shared `main.tex`.

The main evidence remains **V121, 16 cities × 10 indicators**. Its primary values, weights, anchors and bounds are unchanged. V122 supplies the preference, future and separate country/equity/age cases. V123 compares a chosen midpoint completion with retained-interval minimax regret on identical evidence: fixed weights change 13 ranks (Kendall tau 0.600), while Zurich remains the conservative recommendation and all 16 cities remain possible champions. A strict-interior completion lets Dublin exceed Zurich. This is a controlled diagnostic, not an invented history of the team's initial model, a new data admission or proof that either city's observed quality changed.

All new prose applies the mandatory installed `anti-defensive-writing-en` skill. The contribution leads the summary and conclusion; contrary results and evidence scope remain. The original V122 contribution, legacy draft, root manuscript, bibliography and class are hash-protected and unchanged. No connected Codex document session was available during preparation; this artifact is built from the fetched Overleaf Git checkout. A successful Git push synchronizes that checkout; it is not a claim about an independently inspected browser editor.

## Build and verify

From the repository root, with pandas and matplotlib available:

```sh
python drafts/build_task4_v123.py --research-root /path/to/HiMCM/research/2026-a
cd drafts
tectonic --keep-logs --keep-intermediates task4_v123_paper.tex
python check_task4_v123.py
```

The build extracts the owned V122 scientific sections/references, inserts `task4_v123_revision.tex`, keeps the two long tables intact, and redraws the score-bound figure with source fonts at least 12.5 pt and a 6.45-inch canvas. At the 164-mm insertion width its minimum font is 12.51 pt. It omits the redundant preference chart while retaining its numerical table. Main prose, tables, captions and headers use nominal 12 pt or larger; mathematical scripts follow normal typesetting.

Generated files are `task4_v123_core.tex`, `task4_v123_references.tex` and `task4_v123_assets/`. Source hashes, protected-file hashes and numeric links are in the asset manifest. The checker reads compiled page labels, headers, reference markers, size and warning status. `--render-review-confirmed` records a separately completed human/agent image review; use it only after rendering and inspecting the actual final PDF. Page renders and compiler intermediates stay outside Git.

## Remaining decisions

The actual Team Control Number is unknown: the shared old template contains conflicting numbers, so the new header reads **PENDING**. The appended AI report explicitly remains incomplete until actual tool versions, all team usage and saved query/output records are reconciled. Neither fact is fabricated to make the file appear ready. Team review and explicit integration authorization are still needed for changes to teammates' root manuscript content.

The current scientific wording distinguishes conservative recommendation, possible champion and conditional simulation frequency. The news article occupies pages 14–15; all 18 final pages were rendered and visually reviewed. Technical QA is in `task4_v123_assets/qa.json`.

## Newer evidence revision, 9 November 2026

The primary research evidence is now V124. This V123 complete review remains frozen on V121. See `task4_v124_update.tex/.pdf` for the audited two-cell facility update and the explicit boundary; the V122 extensions must be rerun before a unified full-paper migration. No numeric claims in the frozen V123 PDF have been silently changed.

## Superseded current-review entry

The unified V124-evidence/V125-analysis full draft is now `task4_v125_paper.tex/.pdf`. This V123 snapshot remains unchanged on V121; use V125 for the current complete independent review.
