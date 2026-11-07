"""Verify archived ASDB evidence without treating K–12 data as high school."""
import hashlib
import json
from pathlib import Path

from pypdf import PdfReader


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "manifest.json").read_text())
    for name, entry in manifest["files"].items():
        raw = (root / name).read_bytes()
        assert len(raw) == entry["bytes"], name
        assert hashlib.sha256(raw).hexdigest() == entry["sha256"], name
    reader = PdfReader(root / "asdb_nov2025.pdf")
    assert len(reader.pages) == 14
    page = " ".join(reader.pages[2].extract_text().split())
    for value in ("Schools (K-12)", "Phoenix Day School for the Deaf",
                  "193", "29.25", "6.60", "AZ360", ".71", "1 FTE",
                  "October 1, 2025", "more than 100 FTE"):
        assert value in page, value
    assert manifest["model_admitted"] is False
    print("ASDB archive verified: 14 PDF pages; page 3 K–12/FTE evidence; not admitted")


if __name__ == "__main__":
    main()
