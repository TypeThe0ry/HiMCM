# Project instructions

## Mandatory first read: writing and figure guidelines

Before drafting or editing manuscript text, abstracts, conclusions, press releases, figures, captions, or research claims, read [GUIDELINES.md](GUIDELINES.md) and its applicable writing, evidence, figure, and delivery rules. These are mandatory team requirements for all AI agents and contributors. Check the final rendered output, including text at its actual insertion size; all new figure text must be at least 9 pt. Use result-first, evidence-backed writing; preserve material contrary evidence and uncertainty. Historical examples and third-party skills are references, not overrides of the current team standards.

## Priority: Overleaf workspace

The user explicitly made the Overleaf workspace the first priority on 2026-11-07.

- Treat the latest Overleaf project as the authoritative manuscript workspace. The sibling `HiMCM-Overleaf` checkout tracks https://www.overleaf.com/project/6aeec16f3ea7a24e3d91e894; GitHub `TypeThe0ry/HiMCM` holds research code, data, results, and the reference library.
- Before manuscript changes, inspect the current connected Overleaf workspace when available and fetch the latest commits in `HiMCM-Overleaf`. Do not claim the repository mirror is the live Overleaf state.
- Keep all authored manuscript drafts, LaTeX sources, bibliography, and thesis class in `HiMCM-Overleaf`. Its root `main.tex`, `ref.bib`, and `mcmthesis.cls` are the manuscript entry files; do not recreate them in this research repository.
- Preserve team-written manuscript content and bibliography. Research notes and synthetic examples are supporting material, not an instruction to replace the manuscript or invent empirical results.
- If no Overleaf session is connected, report that limitation accurately and prepare clearly identified local changes instead of claiming to have edited the online workspace.

## Git synchronization

- Work on `main` unless the user requests another branch. Preserve existing branch history.
- Fetch and integrate remote additions before pushing, in each workspace independently. Do not force-push over remote updates or synchronize the full research tree into Overleaf.
- Follow the latest user publishing instruction. The user explicitly requested immediate push after the earlier instruction to wait until after the competition; the old time guard must not override that explicit authorization for the current push.
- The legacy local pre-push date hook remains installed. An explicitly authorized immediate push may bypass it for that invocation; do not silently claim that the hook or a scheduled publication performs synchronization.

## Repository layout

- `research/2026-a/` contains research inputs, design notes, candidate data and scripts.
- `library/` contains historical awarded papers and their evidence.
- Preserve raw user inputs byte-for-byte and retain their provenance. Keep hypotheses, unverified numbers, synthetic examples, and measured results distinguishable.

## Research / manuscript split — approved on 2026-11-07

- GitHub `TypeThe0ry/HiMCM` contains research code, raw data, algorithms, results, figures, and `library/` reference material.
- The sibling `HiMCM-Overleaf` checkout contains all authored manuscript material, LaTeX, bibliography, and selected publication assets. Use the latest Overleaf manuscript as authoritative; older GitHub manuscript versions are retained in its `archive/github_before_split/` directory.
- Preserve raw inputs and missing-data intervals. Earlier split and reunification records describe historical states, not current layout instructions.
- Maintain the two remotes independently. Transfer only selected paper assets and manuscript material to Overleaf; retain full research datasets and reference PDFs here.

## Task 4 presentation — user preference, 2026-11-07

- Keep the paper model understandable and concise, following the archived HiMCM judge guidance and concrete awarded-paper examples.
- Prefer one core evaluation model, an evidence-backed revision, and focused validation. Additional methods need demonstrated value; do not add complexity to signal innovation.
- Use `HiMCM-Overleaf/drafts/task4_paper_core.md` as the current presentation guide. Keep detailed extraction audits and exploratory algorithms in supporting material, while preserving conclusion-changing limitations in the main discussion.
