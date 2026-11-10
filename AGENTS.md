# Project instructions

## Long-term goal and required writing skill — user instruction, 2026-11-08

- Keep the long-term goal of improving the HiMCM paper and supporting materials active across iterations. Use [the persistent work plan](docs/handoff/LONGTERM_GOAL.md); finishing one iteration does not complete the long-term goal.
- All new or revised paper prose, abstracts, conclusions, news articles, captions and research explanations must use [Adkid-Zephyr/anti-defensive-writing-Skill](https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill). Read the installed `anti-defensive-writing` skill for Chinese or `anti-defensive-writing-en` for English before the first applicable edit in a working context.
- Portable repository copies are [Chinese](research/2026-a/visuals/guidelines/anti-defensive-writing/zh/SKILL.md) and [English](research/2026-a/visuals/guidelines/anti-defensive-writing/en/SKILL.md). Installation and version verification are recorded in [the skill policy](docs/guidelines/ANTI_DEFENSIVE_WRITING.md).
- Apply contribution-first structure, precise claims and concise argument. Preserve contrary evidence, source scope and uncertainty that affect the conclusion. The user-provided values, scientific rules and permissions for team-written manuscript content continue to govern every iteration.

## Mandatory first read: writing and figure guidelines

Before drafting or editing manuscript text, abstracts, conclusions, press releases, figures, captions, or research claims, read [GUIDELINES.md](GUIDELINES.md) and its applicable writing, evidence, figure, and delivery rules. These are mandatory team requirements for all AI agents and contributors. Check the final rendered output, including text at its actual insertion size; all new figure text must be at least 9 pt. Use result-first, evidence-backed writing; preserve material contrary evidence and uncertainty. Historical examples and third-party skills are references, not overrides of the current team standards.

## Priority: Overleaf workspace

Current scientific entry: **user16 V197**, with V197 controlled extensions and the current independent full review registered in `research/2026-a/design/task4_user_current_review.json`. The V136/V137 evidence and V148 review remain frozen; current extension registry is `research/2026-a/design/task4_user_current_extensions.json`. The V131 paper (documentation V134) remains frozen. Read the current handoff before running older scripts; V125 and earlier review artifacts retain their frozen evidence. Preserve the original CSV and the explicit 16-city entry.

The user explicitly made the Overleaf workspace the first priority on 2026-11-07.

- Treat the latest Overleaf project as the authoritative manuscript workspace. The sibling `HiMCM-Overleaf` checkout tracks https://www.overleaf.com/project/6aeec16f3ea7a24e3d91e894; GitHub `TypeThe0ry/HiMCM` holds research code, data, results, and the reference library.
- Before manuscript changes, inspect the current connected Overleaf workspace when available and fetch the latest commits in `HiMCM-Overleaf`. Do not claim the repository mirror is the live Overleaf state.
- Keep all authored manuscript drafts, LaTeX sources, bibliography, and thesis class in `HiMCM-Overleaf`. Its root `main.tex`, `ref.bib`, and `mcmthesis.cls` are the manuscript entry files; do not recreate them in this research repository.
- Preserve team-written manuscript content and bibliography. Research notes and synthetic examples are supporting material, not an instruction to replace the manuscript or invent empirical results.
- If no Overleaf session is connected, report that limitation accurately and prepare clearly identified local changes instead of claiming to have edited the online workspace.

## Current delivery evidence

The current delivery map is registered separately in `research/2026-a/design/task4_user_current_delivery.json`, mirrored by Overleaf `drafts/task4_current_delivery.json`. It may be newer than the unchanged review PDF. Use its bound requirements and verification instead of inferring current page locations from a frozen review checklist; passage matches do not certify source quality or final team readiness.

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

## Minimal manuscript edits — user instruction, 2026-11-07

- Change only manuscript material strictly necessary for the explicitly requested task.
- Do not edit other contributors' prose, equations, figures, citations, or formatting without explicit user authorization covering those changes. Do not infer that general manuscript editing or upload authorization permits rewriting their work.
- Review the exact diff before every manuscript commit/push; preserve unrelated content and online edits. Do not perform incidental polishing or restructuring.
- Research/model work does not authorize automatic manuscript updates. When ownership is unclear, preserve the existing content and ask before changing it.

## User manuscript format — 2026-11-09

Use the existing read-only mcmthesis class for owned review material, following the user-supplied format recorded in research/2026-a/design/task4_user_format_reference.json: native summary sheet, Team # running head at left, Page x of y at right, and empty footers. Preserve teammate main.tex, ref.bib, mcmthesis.cls and prose. The sample IDs18213/18214 conflict. On2026-11-10 the user authorized provisional use of the latest template: display mcmsetup tcn18213 in the owned review; retain actual registration as unverified and replace the display number when confirmed. Current owned review version is in task4_user_current_review.json.

## Subagent model selection — user instruction, 2026-11-10

- Use `gpt-6-luna` by default for lower-complexity subagent tasks.
- Use `gpt-6.1-terra` for advanced subagent tasks, including complex mathematical modelling and independent scientific audits.
- Choose reasoning effort to fit the task. Keep assignments bounded and give agents the required repository paths and context.
