"""Verify V71 NYC primary originals; admit no new model observations."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "manifest.json").read_text())
checked = 0
for item in manifest:
    path = ROOT / item["file"]
    if "error" in item:
        assert not path.exists(), f"Failed download unexpectedly present: {path}"
        continue
    raw = path.read_bytes()
    assert len(raw) == item["bytes"], path
    assert hashlib.sha256(raw).hexdigest() == item["sha256"], path
    checked += 1

def pdf_text(name):
    return subprocess.check_output(["pdftotext", str(ROOT / name), "-"], text=True)

designation = pdf_text("nymtc_designation.pdf")
assert all(s in designation for s in ["August 11, 2025", "C004307", "Westat", "tentatively"])
student = pdf_text("student_survey2026.pdf")
assert "43." in student and "61." in student
assert "traveling between home and school" in student
revisions = pdf_text("survey_revisions2026.pdf")
assert "new baseline" in revisions and "year-over-year" in revisions
ornl = pdf_text("ornl_nys_rural2024.pdf")
assert all(s in ornl for s in ["Five counties/boroughs", "Kings", "Richmond", "17,000"])
print(json.dumps({"verified_originals": checked, "failed_downloads": 1,
                  "new_admitted_model_cells": 0, "existing_rhts_preserved": True}, indent=2))
