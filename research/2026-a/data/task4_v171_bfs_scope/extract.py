#!/usr/bin/env python3
"""Verify archived HTTP receipts and independently locate SSP method evidence.

Offline use: python extract.py. Requires Poppler's pdftotext; reads no model inputs.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent


def main():
    receipts = json.loads((HERE / "retrieval.json").read_text())
    verified = []
    failures = []
    for row in receipts:
        if row.get("file") is None:
            failures.append({"url": row["url"], "status": row["status"], "error": row.get("error")})
            continue
        raw = (HERE / row["file"]).read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        assert digest == row["sha256"], row["file"]
        assert len(raw) == row["bytes"], row["file"]
        verified.append({"file": row["file"], "status": row["status"], "sha256": digest})

    manual = subprocess.check_output(
        ["pdftotext", "-layout", str(HERE / "bfs_SSP_2024_25_manual_original.pdf"), "-"]
    ).decode()
    pages = manual.split("\f")
    checks = {
        "2024_25_reference_year": (4, "Schuljahres 2024/25"),
        "private_school_cantonal_responsibility": (6, "einschliesslich der Privatschulen"),
        "unresolved_gaps_disclosed": (7, "Basisdiffusion auf die Datenlücke"),
        "census": (8, "Vollerhebung"),
        "public_private": (8, "öffentlichen oder privaten Schulen"),
        "upper_secondary_snapshot": (10, "Sekundarstufe I und II"),
        "fte_quotient": (19, "VZÄ = C.7/C.8"),
        "fulltime_basis": (20, "Vollzeitstelle"),
        "gymnasium_stage_separation": (21, "getrennt codiert"),
        "expected_schools": (23, "alle Schulen übermittelt"),
        "activity_split": (31, "Schulart, Schule und Personalkategorie"),
        "distance_exclusion": (34, "Fernstudien"),
    }
    for key, (page, needle) in checks.items():
        assert needle in pages[page - 1], (key, page)
    absent_terms = ["Rundung", "gerundet", "Imputation", "imputiert", "Schätzung", "geschätzt"]
    term_pages = {
        term: [i for i, text in enumerate(pages, 1) if re.search(r"\b" + re.escape(term) + r"\b", text, re.I)]
        for term in absent_terms
    }
    # Absence of these words is a reproducible search result, not proof that
    # rounding or estimation never occurred in published SSP statistics.
    findings = json.loads((HERE / "source_scope.json").read_text())
    assert findings["admitted_cells"] == 0
    assert findings["PTR_or_utility_computed"] is False
    result = {
        "status": "PASS",
        "raw_receipts_verified": verified,
        "failed_attempts": failures,
        "manual_pdf_pages": len(pages) - (not pages[-1].strip()),
        "located_claims": {key: value[0] for key, value in checks.items()},
        "manual_word_search_pages": term_pages,
        "admitted_cells": 0,
        "source_scope_sha256": hashlib.sha256((HERE / "source_scope.json").read_bytes()).hexdigest(),
        "extractor_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (HERE / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "raw_successes": len(verified), "failed_attempts": len(failures), "admitted_cells": 0}))


if __name__ == "__main__":
    main()
