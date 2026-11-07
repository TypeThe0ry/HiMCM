# Project instructions

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

## Repository layout

- `research/2026-a/` contains research inputs, design notes, candidate data and scripts.
- `library/` contains historical awarded papers and their evidence.
- Preserve raw user inputs byte-for-byte and retain their provenance. Keep hypotheses, unverified numbers, synthetic examples, and measured results distinguishable.
