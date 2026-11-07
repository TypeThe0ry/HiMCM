#!/usr/bin/env python3
"""Recreate or verify the small UIS excerpt without committing the 68 MB source.

Input: official February 2026 OPRI.zip. Default verifies the archived excerpt.
--write-to NEW.zip creates an excerpt, refusing to overwrite an existing file.
"""

import argparse
import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path


DATA = Path(__file__).resolve().parents[1] / "data/homicide_2023_secondary_ratio_updated"


def selected_members(archive):
    for filename in ["OPRI_COUNTRY.csv", "OPRI_LABEL.csv", "OPRI_README_RELEASE_2026_February.md"]:
        yield filename, archive.read(filename)
    for filename in ["OPRI_DATA_NATIONAL.csv", "OPRI_METADATA.csv"]:
        result = io.StringIO(newline="")
        with archive.open(filename) as stream:
            reader = csv.DictReader(io.TextIOWrapper(stream, encoding="utf-8-sig"))
            writer = csv.DictWriter(result, fieldnames=reader.fieldnames, lineterminator="\n")
            writer.writeheader()
            for row in reader:
                if row["INDICATOR_ID"] in {"20082", "20182"} and 2018 <= int(row["YEAR"]) <= 2025:
                    writer.writerow(row)
        yield filename.replace(".csv", "_secondary_2018_2025.csv"), result.getvalue().encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--write-to", type=Path)
    args = parser.parse_args()
    manifest = json.loads((DATA / "download_manifest.json").read_text(encoding="utf-8"))
    expected = manifest["upstream_uis_archive"]
    assert args.archive.stat().st_size == expected["bytes"]
    digest = hashlib.sha256()
    with args.archive.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    assert digest.hexdigest() == expected["sha256"], "Source revision differs from this snapshot"
    with zipfile.ZipFile(args.archive) as archive:
        if args.write_to:
            with zipfile.ZipFile(args.write_to, mode="x", compression=zipfile.ZIP_DEFLATED) as output:
                for filename, content in selected_members(archive):
                    output.writestr(filename, content)
        else:
            with zipfile.ZipFile(DATA / "raw/uis_secondary_counts_2018_2025_excerpt.zip") as excerpt:
                names = set()
                for filename, content in selected_members(archive):
                    assert excerpt.read(filename) == content, filename
                    names.add(filename)
                assert set(excerpt.namelist()) == names
    print("Verified upstream SHA-256 and all selected national values, flags, notes and reference members.")


if __name__ == "__main__":
    main()
