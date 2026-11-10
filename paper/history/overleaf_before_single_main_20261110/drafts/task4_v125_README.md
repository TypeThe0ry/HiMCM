# V125 frozen complete independent review

**Current full review: [V128](task4_v128_README.md), using V127 primary evidence. This V125 document is retained unchanged on its frozen V124 basis.**

`task4_v125_paper.tex/.pdf` is the earlier full review draft: **V124 user16 evidence with V125 preference, future, method and uncertainty-revision analyses**. V126 updates documentation and citations while preserving those numerical analyses. Summary, collection examples, baseline table/figure, scenario claims, conclusion and two-page news article use that same basis. The main answer is 18 pages including summary, contents, news and references; an explicitly incomplete two-page AI-use record follows (20 pages total).

The update is numerical as well as editorial. Independent-living rank correlation relative to the baseline is 0.883333, fixed midpoint TOPSIS/VIKOR correlation is 0.500000, and equal-weight midpoint/interval correlation is 0.650000. Oslo's baseline concentration 100 mean decision rank is 2.1071. The newly paired Singapore-proxy withdrawal stress arm is reported explicitly. The accumulated 17 supplements reduce mean fixed score-interval width by 14.14%; the latest two-cell increment remains 0.204%. Neither improvement identifies a certain champion: Zurich is the conservative baseline recommendation and all 16 cities remain possible champions.

The mandatory English anti-defensive-writing skill is applied throughout. Existing values, weights, anchors, uncertainty rules and historical-case scope remain. The root manuscript, bibliography, class, older complete draft and evidence companion are hash-protected and unchanged. There was no connected document session; this contribution uses the fetched Overleaf Git checkout, with remote synchronization verified separately. Shared `main.tex` still fails compilation at the existing missing `framework.png`; this independent file does not repair or replace teammates' prose.

## Build and check

From the repository root, with the restored research Python environment active
(on this workstation: `source ../HiMCM/.venv-v120/bin/activate`):

```sh
python drafts/build_task4_v125.py --research-root /path/to/HiMCM/research/2026-a
tectonic --keep-logs --keep-intermediates drafts/task4_v125_paper.tex > /tmp/himcm-v125-build.log 2>&1
python drafts/check_task4_v125.py --compiler-output /tmp/himcm-v125-build.log
```

The builder requires the independent research audit at `results/task4_v125_revision/audit.json`. It generates four tables, current numerical macros, the diagnostic subsection, one score-interval figure and selected supporting CSVs. Historical-case prose is retained from the owned earlier contribution only after the migration's byte/numeric controls. New text and editable narrative reside in `task4_v125_{front,core,conclusion,news,ai,references}.tex`; generated files are clearly marked.

For documentation-only edits use `--refresh-manifest-only`: it verifies all previously recorded research/protected-file hashes, copies the selected V126 provenance receipts and updates manuscript hashes without regenerating numerical tables or figures. The checker now reads captured compiler stdout/stderr as well as the TeX log, so PDF-backend warnings cannot pass as a clean build.

V126 records the actual local model label `gpt-6.1-sol` and Codex client `0.166.0-alpha.5.1`, and identifies Exa retrieval/extraction from saved receipts. A selected 52-message export was independently checked and remains outside both repositories. The appendix states its coverage; it does not claim a complete team transcript or a fixed serving build. The historical country paragraph now cites the frozen case data, Numbeo 2025 affordability inputs and WHO 2021 monitoring values; `country_source_index.json` traces ten unchanged claim inputs to their source rows and hashes.

All figure text is 12.5 pt at a 6.45-inch source width, producing a minimum 12.51 pt at the 164-mm insertion width. Main prose, tables, captions and headers use nominal 12 pt or larger; mathematical scripts follow normal typesetting. Text macros retain trailing separator spaces; numeric macros do not add a space before percentages. The final PDF is compiled without warnings or unresolved references and every page has been rendered and visually reviewed, including paragraph breaks, figure labels and news pagination. `--render-review-confirmed` records that separate image review and must not be used before it occurs.

## Remaining completion requirements

This is **not submission-ready**. Team Control Number remains PENDING because the inherited template contains conflicting numbers; actual full-team AI history, versions and saved query/output records remain to be reconciled. The appended record states that gap rather than inventing exact transcripts. Integration into the shared root manuscript requires specific authorization covering teammates' content. Keep the long-term goal active while completing these requirements and further evidence work.
