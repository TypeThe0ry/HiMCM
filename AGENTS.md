# Project instructions

## Mandatory first read: writing and figure guidelines

Before drafting or editing manuscript text, abstracts, conclusions, press releases, figures, captions, or research claims, read [GUIDELINES.md](GUIDELINES.md) and its applicable writing, evidence, figure, and delivery rules. These are mandatory team requirements for all AI agents and contributors. Check the final rendered output, including text at its actual insertion size; all new figure text must be at least 9 pt. Use result-first, evidence-backed writing; preserve material contrary evidence and uncertainty. Historical examples and third-party skills are references, not overrides of the current team standards.

## Priority: Overleaf workspace

The user explicitly made the Overleaf workspace the first priority on 2026-11-07.

- Treat the latest Overleaf project as the authoritative manuscript workspace. GitHub is its synchronization, version-history, and research archive layer.
- Before manuscript changes, inspect the current connected Overleaf workspace when available and fetch the latest GitHub synchronization commits. Do not claim the repository mirror is the live Overleaf state.
- Preserve `main.tex`, `ref.bib`, and `mcmthesis.cls` at the repository root for Overleaf synchronization. Do not rename or move them as part of housekeeping.
- Preserve team-written manuscript content and bibliography. Research notes and synthetic examples are supporting material, not an instruction to replace the manuscript or invent empirical results.
- If no Overleaf session is connected, report that limitation accurately and prepare clearly identified local changes instead of claiming to have edited the online workspace.

## Git synchronization

- Work on `main` unless the user requests another branch. Preserve existing branch history.
- Fetch and integrate remote additions before pushing, especially commits originating in Overleaf. Do not force-push over remote manuscript updates.
- Follow the latest user publishing instruction. The user explicitly requested immediate push after the earlier instruction to wait until after the competition; the old time guard must not override that explicit authorization for the current push.
- The legacy local pre-push date hook remains installed. An explicitly authorized immediate push may bypass it for that invocation; do not silently claim that the hook or a scheduled publication performs synchronization.

## Repository layout — split on 2026-11-07

- This HiMCM repository remains the manuscript repository for Overleaf.
- Keep main.tex, ref.bib, mcmthesis.cls, used final figures and mandatory guidelines here.
- Research, raw inputs, scripts, model outputs and the historical library live in the sibling HiMCM-research repository: https://github.com/TypeThe0ry/HiMCM-research.
- Do not recreate research/ or library/ here. Transfer only selected final manuscript assets with provenance.
- Before committing, run python3 scripts/check_overleaf_size.py after staging. Keep the current tree below 2,000 files and the recommended 100 MB GitHub sync size.
- Preserve raw inputs byte-for-byte in the research archive. Distinguish hypotheses, missing-data intervals, synthetic examples and observations.
