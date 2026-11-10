# Locked environment for the current model and paper check

A newly created Python environment installed from this hash-locked profile reproduced the registered **16-city V203 model and all 27 paper pages**. The run did not load packages from `.venv-v120` or user/system site-packages. A second run with ordinary system Poppler binaries also passed, so the app's renderer wrapper was not required for this host test.

This profile targets **Linux x86_64 and CPython 3.11.18**. Its four direct requirements preserve the existing tested versions: NumPy 1.26.4, pandas 2.3.1, SciPy 1.13.1 and matplotlib 3.9.2. Matplotlib is retained because the current runner reports its installed version; this checker does not regenerate the figures. Fourteen distributions, including dependencies, are fixed in `constraints.txt` and `requirements.lock`.

## Restore and run

Run from the research checkout. The matching `HiMCM-Overleaf` checkout must be clean and synchronized, with one `main.tex` and its compile dependencies. Choose **new paths outside both repositories** for the environment and output; the reproducer rejects nonempty output directories. Do not point these variables at an existing environment you need to keep.

```bash
HIMCM_CHECK_ENV=/data/scratch/himcm-current-check-env-new
HIMCM_CHECK_OUTPUT=/data/scratch/himcm-current-check-output-new
UV_CACHE_DIR=/data/scratch/uv-cache uv venv --python 3.11.18 "$HIMCM_CHECK_ENV"
UV_CACHE_DIR=/data/scratch/uv-cache uv pip sync --python "$HIMCM_CHECK_ENV/bin/python" --require-hashes --only-binary :all: research/2026-a/environment/current-check/requirements.lock
env -u PYTHONPATH PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 "$HIMCM_CHECK_ENV/bin/python" -s research/2026-a/scripts/task4_current_reproduce.py --output-dir "$HIMCM_CHECK_OUTPUT"
```

Use `--paper-root /absolute/path/to/checkout` if the manuscript checkout is not the default sibling. The script locates the research root relative to itself and accepts an explicit `--research-root` as well. Successful execution writes `report.json` under the selected output; it does not alter either checkout or publish a manuscript.

## Native tools and TeX resources

Bootstrap and lock maintenance use `uv` (tested version 0.13.6); the installed checker does not invoke uv. The tested host has `git` 2.53.0, Tectonic 0.17.0, and Poppler `pdftotext`/`pdftoppm` 26.01.0 on PATH. These executables are not Python packages and are not installed by this lock. The final test used PATH `/usr/local/bin:/usr/bin:/bin`, selecting the ordinary system Poppler tools.

Tectonic is invoked with `--only-cached`: the manuscript's TeX bundle/resources must already be available. Both tests reused this host's existing cache and base CPython interpreter. This is a **fresh virtual-environment check**, not a clean-machine, uncached-TeX or new-network bootstrap claim. Package installation may use the local uv cache or contact the configured index; wheel hashes are enforced either way.

## Scope and maintenance

`requirements.in` declares the current checker requirements; `constraints.txt` records the tested dependency closure; `requirements.lock` contains exact versions and artifact hashes. Rebuild deliberately with:

```bash
UV_CACHE_DIR=/data/scratch/uv-cache uv pip compile research/2026-a/environment/current-check/requirements.in --constraint research/2026-a/environment/current-check/constraints.txt --python 3.11.18 --generate-hashes --only-binary :all: --output-file research/2026-a/environment/current-check/requirements.lock
```

Validate a newly compiled lock in another fresh environment before replacing the recorded result. This profile does not replace `requirements-research.txt` or cover every historical extractor, spatial-figure generator, Monte Carlo replay, private AI transcript check or optional workbook audit. In particular, the Zurich workbook auditor has its separately pinned openpyxl command; the AI-source auditor needs private files that are not distributed here.

Evidence is saved in `research/2026-a/results/current_environment_review/`: installed-package and tool metadata, hash-enforced installation receipt, two isolated reproduction reports and their verification summary. The scientific data, weights, interval rules, current manuscript and PDF remain unchanged.
