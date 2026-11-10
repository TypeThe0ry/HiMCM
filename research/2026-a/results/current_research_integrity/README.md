# Current registered-research integrity and paper reproduction

The current reproducer now verifies the research additions alongside the V203 model and sole current manuscript. It checks268live hash-bound files,19current audit reports and one explicitly pinned historical source version. The full27-page rebuild matches the canonical paper's text and72dpi grayscale render on every page, with native page layout and headers/footers checked. Neither research inputs nor either checkout changed during validation.

| Verification | Result |
| --- | --- |
| Focused binding tests |15pass|
| Read-only workflow checks |14pass/expected rejection cases;914protected files unchanged|
| Registered current audit reports |19report files and their19direct source maps checked|
| Explicit current file bindings |268distinct files|
| Historical source |Route CSV at commit4baa23ec09bb15bc3eae5ef17f952ec17f6d9921verified separately from its current counterpart|
| Current scientific check |160utility cells/32city-weight scalar cases plus inherited controls|
| Local manuscript rebuild |27pages, all text and rendered pages equal; original canonical PDF unchanged|

## Check and reproduce

The standard `scripts/task4_current_reproduce.py` entry now reads both the extensions and acquisition registries. It runs `scripts/task4_current_research_bindings.py` before building and protects the verified files through completion. The normal locked-environment command and clean Overleaf checkout requirement remain as documented in `../../environment/current-check/README.md`. No extra package is needed for the binding helper.

For an integrity-only check, run `PYTHONDONTWRITEBYTECODE=1 /data/scratch/himcm-current-check-env/bin/python research/2026-a/scripts/audit_current_research_bindings.py`. It prints JSON by default. Saving requires explicit `--output` and replacement requires `--overwrite`; the shared report-output guards continue to protect manuscript and unrelated repository paths. Focused tests run with the same interpreter and `scripts/test_current_research_bindings.py`; their Git fixtures live under `/data/scratch`.

`design/task4_current_research_integrity.json` classifies current hash-paired reports. Each report's direct `source_sha256` and/or `source_hashes` map is validated once. Referenced upstream report bytes stay pinned without interpreting all their historical children as current files. The staff/duration report recorded an earlier route index; the helper checks that exact file at its immutable Git commit without checkout, and binds the current route index separately. The historical object must exist in local Git history; a shallow checkout may need history fetched before verification.

When adding a current hash-paired report, declare its source-map policy in the contract. When intentionally changing a live source/index, review and update its current binding. Preserve frozen reports and their historical references. Unknown policies, conflicting hashes, malformed maps, missing/changed files, unsafe/symlink paths and unavailable historical Git objects fail the check. The15tests cover these boundaries, including the intentional one-level boundary and read-only behavior.

## Evidence scope

`verification.json` contains the registered file-binding result; `readonly_workflow.json` records14workflow checks; `reproduction.json` records the isolated exact-paper-HEAD build; `workflow_verification.json` binds their hashes and current code. The research workingtree was allowed to contain the pending checker changes; its baseHEADand exact runner/code hashes are recorded. The paper checkout was clean at1cbec98b3c1bd86b7f2b2f4385c749ff105167f6. The verification-build PDF has its own metadata hash while matching canonical content/render; no replacement paper PDF or extra Overleaf version is published.

These checks establish integrity relative to the current registry/contract metadata. The new research-binding stage does not replay addendum calculations, Monte Carlo or source-semantic audits, or independently authenticate the metadata. The existing core science check and each earlier independent addendum audit retain their specific scopes. Online Overleaf compilation and final team submission remain outside this local run. Primary values, weights, intervals, current recommendations and manuscript contents are unchanged; primary admissions and actual width reduction are zero.
