# Current audit workflow

For the registered model and PDF reproduction, use the [locked current-check environment](../../research/2026-a/environment/current-check/README.md). It is separate from the legacy research environment used in the audit examples below; private AI files and optional workbook dependencies are not included.

Run current audit scripts as checks: their default output is JSON on stdout. The AI-source, point-utility, point-withdrawal, joint-collection, Zurich-source and current-paper auditors do not replace saved evidence reports unless a report destination is explicitly selected. Python and uv may maintain their normal runtime caches; use `PYTHONDONTWRITEBYTECODE=1` to suppress Python bytecode caches.

Use `.venv-v120/bin/python research/2026-a/scripts/audit_current_<name>.py` for the scientific auditors. The AI audit needs the preserved local session path and optionally the private export directory. The Zurich audit instead uses `UV_CACHE_DIR=/data/scratch/uv-cache uv run --no-project --with openpyxl==3.1.5 python research/2026-a/scripts/audit_current_zurich_source2026.py`. The current-paper auditor accepts `--build-dir` for an existing compiled build.

An intentional report update uses `--output PATH --overwrite`. Within the research checkout, each auditor accepts only its own canonical JSON report. Manuscript checkout destinations and symbolic-link destinations are rejected. An external new JSON report needs no overwrite flag. The joint auditor verifies its derived CSV by default; intentional regeneration requires `--rebuild-optimal-table` together with its canonical report output and overwrite flag.

The AI auditor validates the bounded source capture independently of subsequent manuscript edits. To additionally compare the pre-AI body and resources, pass `--paper-baseline COMMIT`, where COMMIT belongs to the Overleaf repository. A failed comparison against an older manuscript is not a failure of the captured source evidence.

After intentional updates, refresh affected hash bindings and dependent verification reports before committing. `scripts/test_current_audit_readonly.py --session PATH [--private-output DIRECTORY]` checks six default auditors, explicit output safeguards and input preservation, including the current manuscript’s separately bound withdrawal evidence. Its own default is stdout; its canonical report is `results/current_audit_workflow/verification.json`.

Overleaf retains one current `main.tex` with its compile dependencies. Local and remote manuscript history are synchronized independently from the research repository; audit report updates do not require new manuscript versions or a paper upload.
