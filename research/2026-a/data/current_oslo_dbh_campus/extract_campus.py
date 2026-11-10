#!/usr/bin/env python3
"""Extract Oslo municipality campus rows for semesters 1 and 3 of 2025–2026."""

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CAMPUS_SOURCE = ROOT / "api_662.csv"
INSTITUTION_SOURCE = ROOT / "api_211.csv"
METADATA_SOURCE = ROOT / "api_002.csv"
OUTPUT = ROOT / "oslo_campus_2025_2026.csv"
SUMMARY = ROOT / "summary.json"
PERIODS = [(year, semester) for year in ("2025", "2026") for semester in ("1", "3")]
FLAG_TERMS = {"nett": "nett", "online": "online", "uplassert": "uplassert"}


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames, list(reader)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    campus_fields, campus_rows = read_csv(CAMPUS_SOURCE)
    institution_fields, institution_rows = read_csv(INSTITUTION_SOURCE)
    metadata_fields, metadata_rows = read_csv(METADATA_SOURCE)

    by_code = defaultdict(list)
    for row in institution_rows:
        by_code[row["Institusjonskode"]].append(row)

    selected = [
        row for row in campus_rows
        if row["Kommunenummer campus"] == "0301"
        and (row["Årstall"], row["Semester"]) in PERIODS
    ]
    output_fields = campus_fields + ["institution_metadata_candidates_json"] + [
        f"label_{name}_diagnostic" for name in FLAG_TERMS
    ]
    key_counts = Counter(
        (row["Årstall"], row["Semester"], row["Institusjonskode"], row["Stedkode campus"])
        for row in selected
    )
    duplicate_keys = [
        {"year": key[0], "semester": key[1], "institution_code": key[2],
         "campus_code": key[3], "count": count}
        for key, count in sorted(key_counts.items()) if count > 1
    ]
    diagnostic_counts = Counter()
    institution_counts = {}

    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=output_fields, lineterminator="\n")
        writer.writeheader()
        for row in selected:
            candidates = by_code.get(row["Institusjonskode"], [])
            result = dict(row)
            result["institution_metadata_candidates_json"] = json.dumps(
                candidates, ensure_ascii=False, separators=(",", ":")
            )
            searchable = " ".join(row.values()).casefold()
            for name, term in FLAG_TERMS.items():
                flag = term in searchable
                result[f"label_{name}_diagnostic"] = "true" if flag else "false"
                diagnostic_counts[name] += int(flag)
            writer.writerow(result)

    for year, semester in PERIODS:
        rows = [row for row in selected if (row["Årstall"], row["Semester"]) == (year, semester)]
        institution_counts[f"{year}-{semester}"] = {
            "campus_rows": len(rows),
            "distinct_institution_codes": len({row["Institusjonskode"] for row in rows}),
        }

    summary = {
        "scope": {
            "municipality_code": "0301",
            "years": [2025, 2026],
            "semesters": [1, 3],
            "selection": "Exact municipality/year/semester filter on api_662.csv.",
            "interpretation_limit": (
                "These are campus registry rows for Oslo municipality. They do not establish "
                "active teaching at each location or a complete inventory of Oslo higher education."
            ),
        },
        "source_tables": {
            "api_002.csv": {"rows": len(metadata_rows), "columns": len(metadata_fields), "sha256": sha256(METADATA_SOURCE),
                            "url": "https://dbh-data.dataporten-api.no/Tabeller/bulk-csv?rptNr=002"},
            "api_211.csv": {"rows": len(institution_rows), "columns": len(institution_fields), "sha256": sha256(INSTITUTION_SOURCE),
                            "url": "https://dbh-data.dataporten-api.no/Tabeller/bulk-csv?rptNr=211"},
            "api_662.csv": {"rows": len(campus_rows), "columns": len(campus_fields), "sha256": sha256(CAMPUS_SOURCE),
                            "url": "https://dbh-data.dataporten-api.no/Tabeller/bulk-csv?rptNr=662"},
        },
        "output": {"file": OUTPUT.name, "rows": len(selected), "raw_campus_columns_preserved": campus_fields,
                   "institution_metadata_join": "Exact Institusjonskode; all matched rows retained as JSON candidates."},
        "period_counts": institution_counts,
        "institution_table_code_audit": {
            "rows": len(institution_rows),
            "distinct_exact_codes": len(by_code),
            "codes_with_multiple_rows": {code: len(rows) for code, rows in sorted(by_code.items()) if len(rows) > 1},
            "ambiguous_codes_in_selected_rows": sorted({row["Institusjonskode"] for row in selected
                                                         if len(by_code.get(row["Institusjonskode"], [])) > 1}),
        },
        "duplicate_campus_keys": {
            "key": ["year", "semester", "institution_code", "campus_code"],
            "duplicates": duplicate_keys,
        },
        "diagnostic_labels_only_no_exclusion": dict(diagnostic_counts),
        "excluded_inputs": ["enrolment_response.csv was not read or used."],
    }
    with SUMMARY.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(summary, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
