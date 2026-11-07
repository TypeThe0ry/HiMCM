"""Verify and stream the complete CCD CSV, then preserve all target LEA rows."""
import argparse
from contextlib import ExitStack
import csv
import hashlib
import io
import json
import lzma
from pathlib import Path
import zipfile

P = Path(__file__).resolve().parent


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class HashReader(io.RawIOBase):
    """Hash original CSV bytes as the CSV parser consumes a bounded buffer."""
    def __init__(self, source):
        self.source = source
        self.digest = hashlib.sha256()
        self.size = 0

    def readable(self):
        return True

    def readinto(self, buffer):
        data = self.source.read(len(buffer))
        buffer[:len(data)] = data
        self.digest.update(data)
        self.size += len(data)
        return len(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, default=P / "ccd_lea_052_2425.csv.xz")
    args = parser.parse_args()
    src = args.archive
    archive = json.loads((P / "csv_archive.json").read_text())
    original = json.loads((P / "membership_source.json").read_text())
    is_xz = src.suffix == ".xz"
    expected_hash = archive["sha256"] if is_xz else original["archive_sha256"]
    expected_size = archive["bytes"] if is_xz else original["archive_bytes"]
    assert src.stat().st_size == expected_size, "Archive size differs"
    assert file_hash(src) == expected_hash, "Archive SHA256 differs"
    rows = []
    count = 0
    with ExitStack() as stack:
        if is_xz:
            raw = stack.enter_context(lzma.open(src, "rb"))
        else:
            zipped = stack.enter_context(zipfile.ZipFile(src))
            raw = stack.enter_context(zipped.open(original["csv_member"]))
        hashed = HashReader(raw)
        stream = stack.enter_context(io.TextIOWrapper(io.BufferedReader(hashed),
                                                     encoding="utf-8-sig", newline=""))
        for row in csv.DictReader(stream):
            count += 1
            if row["LEAID"] == "0403860":
                rows.append(row)
        assert hashed.size == archive["csv_bytes"], "CSV size differs"
        assert hashed.digest.hexdigest() == archive["csv_sha256"], "CSV SHA256 differs"
    assert count == original["rows_scanned"]
    assert len(rows) == original["matching_rows"]
    assert all(r["SCHOOL_YEAR"] == "2024-2025" and r["ST"] == "AZ"
               and r["ST_LEAID"] == "AZ-4234" for r in rows)
    with (P / "maricopa_lea_membership_rows.csv").open("w", newline="") as output:
        writer = csv.DictWriter(output, list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    totals = [r for r in rows if r["TOTAL_INDICATOR"] !=
              "Category Set A - By Race/Ethnicity; Sex; Grade"]
    (P / "maricopa_lea_totals.json").write_text(json.dumps(totals, indent=2) + "\n")
    print(json.dumps({"rows_scanned": count, "matching_rows": len(rows),
                      "archive_sha256_verified": True, "csv_sha256_verified": True}))


if __name__ == "__main__":
    main()
