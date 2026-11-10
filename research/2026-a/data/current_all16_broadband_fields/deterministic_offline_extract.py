#!/usr/bin/env python3
"""Compare the original 16 submitted broadband values to the archived Ookla HTML.

No network access is used. Default behavior prints a JSON summary to stdout.
Pass --write to create comparison.csv and summary.json beside this script.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
INPUT = ROOT / "research/2026-a/data/task4_v117_team_intake/city_indicators.csv"
SOURCE = ROOT / "research/2026-a/data/task4_v5_resources/ookla_global_index.html"
MANIFEST = ROOT / "research/2026-a/data/task4_v5_resources/manifest.json"
OUT = Path(__file__).resolve().parent
FIELDS = ("fixedMedian", "fixedMean", "mobileMedian", "mobileMean")
FIELD_LABELS = {
    "fixedMedian": "fixed broadband median download",
    "fixedMean": "fixed broadband mean download",
    "mobileMedian": "mobile broadband median download",
    "mobileMean": "mobile broadband mean download",
}
CITY_ALIASES = {"Zurich": "Zürich"}
BASE_URL = "https://www.speedtest.net"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_only(value: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]*>", " ", value)).split())


def city_rows(raw_html: str, field: str) -> list[dict]:
    # Isolate a results panel by its stable element ID and the next panel ID.
    markers = [(raw_html.find(f'id="column-{name}"'), name) for name in FIELDS]
    markers = sorted((pos, name) for pos, name in markers if pos >= 0)
    start = next((pos for pos, name in markers if name == field), None)
    if start is None:
        raise ValueError(f"Missing HTML panel column-{field}")
    end = next((pos for pos, _ in markers if pos > start), len(raw_html))
    panel = raw_html[start:end]
    results = []
    pattern = re.compile(r'<tr\b(?=[^>]*class="[^"]*data-result results[^"]*")[^>]*>(.*?)</tr>', re.S)
    for match in pattern.finditer(panel):
        row = match.group(0)
        anchor = re.search(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', row, re.S)
        speed = re.search(r'<td\b[^>]*class="speed"[^>]*>\s*([^<]+)', row, re.S)
        rank = re.search(r'<td\b[^>]*class="rank actual-rank"[^>]*>\s*([^<]+)', row, re.S)
        if not (anchor and speed and rank):
            continue
        country_match = re.search(r'<span\b[^>]*class="country_display"[^>]*>(.*?)</span>', row, re.S)
        city = text_only(anchor.group(2))
        country = text_only(country_match.group(1)) if country_match else None
        href = html.unescape(anchor.group(1))
        # Only median panels contain city rows. Country-level rows have no city query.
        is_city = "city=" in href
        results.append({
            "city": city, "country": country, "href": BASE_URL + href,
            "rank": int(text_only(rank.group(1))), "value": text_only(speed.group(1)),
            "geography_level": "city" if is_city else "country",
        })
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write comparison.csv and summary.json")
    args = parser.parse_args()

    source_bytes = SOURCE.read_bytes()
    raw_html = source_bytes.decode("utf-8")
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    input_hash = sha256(INPUT)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest_record = next(item for item in manifest if item["file"] == SOURCE.name)
    if manifest_record["sha256"] != source_hash or manifest_record["bytes"] != len(source_bytes):
        raise ValueError("Archived source does not match its existing manifest")

    inputs = list(csv.DictReader(INPUT.open(encoding="utf-8-sig", newline="")))
    if len(inputs) != 16:
        raise ValueError(f"Expected original 16-city intake, found {len(inputs)} rows")
    extracted = {field: city_rows(raw_html, field) for field in FIELDS}
    output_rows = []
    counts = {"fixedMedian": 0, "fixedMean": 0, "mobileMedian": 0, "mobileMean": 0,
              "no_exact_match": 0, "city_median_exact_match": 0,
              "singapore_country_mean_fallback": 0}
    match_examples = []
    availability = {field: {"city_rows": 0, "singapore_country_fallback_rows": 0, "unavailable": 0} for field in FIELDS}

    for item in inputs:
        city = item["city"]
        alias = CITY_ALIASES.get(city, city)
        country = item["country"]
        value = float(item["broadband_mbps"])
        field_cells = {}
        exact_fields = []
        available_city_fields = []
        for field in FIELDS:
            # Do not match by value. Require the intended city alias and country first.
            candidates = [r for r in extracted[field]
                          if r["geography_level"] == "city" and r["city"] == alias and r["country"] == country]
            # The Singapore country-level row is an explicit country-city-state fallback only.
            if not candidates and city == "Singapore" and country == "Singapore":
                candidates = [r for r in extracted[field]
                              if r["geography_level"] == "country" and r["city"] == "Singapore"]
            rec = candidates[0] if candidates else None
            if rec and rec["geography_level"] == "city":
                available_city_fields.append(field)
                availability[field]["city_rows"] += 1
            elif rec:
                availability[field]["singapore_country_fallback_rows"] += 1
            else:
                availability[field]["unavailable"] += 1
            exact = bool(rec and round(float(rec["value"]), 2) == round(value, 2))
            field_cells[field] = {
                "value": rec["value"] if rec else "",
                "rank": rec["rank"] if rec else "",
                "link": rec["href"] if rec else "",
                "geography_level": rec["geography_level"] if rec else "unavailable",
                "country": rec["country"] if rec and rec["country"] else ("Singapore" if rec else ""),
                "exact_value_match": str(exact).lower(),
            }
            if exact:
                exact_fields.append(field)
                counts[field] += 1
                match_examples.append({"city": city, "field": field, "value": rec["value"], "rank": rec["rank"],
                                       "geography_level": rec["geography_level"]})
        if exact_fields:
            if city == "Singapore" and "fixedMean" in exact_fields:
                status = "exact_match_fixed_mean_country_level_fallback"
                counts["singapore_country_mean_fallback"] += 1
            else:
                status = "exact_match_" + "_and_".join(exact_fields)
                if any(field in ("fixedMedian", "mobileMedian") for field in exact_fields):
                    counts["city_median_exact_match"] += 1
        else:
            status = "no_exact_match_in_available_city_fields" if available_city_fields else "no_city_median_row_available"
            counts["no_exact_match"] += 1
        out = {
            "city": city, "country": country, "iso2": item["iso2"],
            "input_value_mbps": item["broadband_mbps"], "input_year": item["broadband_mbps_year"],
            "input_flag": item["broadband_mbps_flag"], "publisher_city_alias": alias,
            "publisher_country_match": country,
        }
        for field in FIELDS:
            for key in ("value", "rank", "link", "geography_level", "country", "exact_value_match"):
                out[f"{field}_{key}"] = field_cells[field][key]
        out["exact_match_fields"] = ";".join(exact_fields)
        out["comparison_status"] = status
        out["original_csv_lineage"] = "not_established_by_publisher_value_match"
        output_rows.append(out)

    # Publication metadata visible in the retained HTML, kept at its stated precision.
    pub = re.search(r'<div class="month">([^<]+)</div>', raw_html)
    footer = re.search(r"Results are updated ([^.]+\.)", raw_html)
    summary = {
        "purpose": "Exact-value field classification of the 16 original submitted broadband values against one archived Speedtest Global Index snapshot.",
        "input": {"path": str(INPUT.relative_to(ROOT)), "sha256": input_hash, "rows": len(inputs),
                  "lineage_note": "The original CSV contains no extraction URL; a publisher match does not establish that the original value was taken from this archive."},
        "source": {"path": str(SOURCE.relative_to(ROOT)), "url": "https://www.speedtest.net/global-index",
                   "sha256": source_hash, "bytes": len(source_bytes), "manifest_sha256_matches": True,
                   "manifest_accessed": manifest_record.get("accessed"),
                   "publication_label": text_only(pub.group(1)) if pub else "unknown",
                   "rolling_period_note": text_only(footer.group(1)) if footer else "not found in HTML",
                   "date_precision": "The page states the publication label and rolling-quarter policy; exact window boundaries are not assigned here."},
        "geography": {"city_matching": "City name (explicit aliases only) and country must match before comparing values; matching is not done by value across different cities.",
                      "alias_map": CITY_ALIASES,
                      "singapore_fallback": "Singapore country-level row may be compared only to submitted Singapore (country-city-state), whose intake flag is NATIONAL. This is reported as a country-level fallback, not a city-row match.",
                      "other_country_rows": "Not used as substitutes for city measurements.",
                      "publisher_boundary": "The archived table does not supply municipal polygons or prove equivalence to city-proper boundaries."},
        "fields": FIELD_LABELS,
        "counts": counts,
        "field_row_availability": availability,
        "matches": match_examples,
        "mixed_field_finding": "The submitted Singapore value 667.71 exactly matches the Singapore fixed broadband mean (country-level row, rank 1); the same archived snapshot lists 476.02 for Singapore fixed broadband median. The other 15 submitted values exactly match their named city rows in fixed broadband median. This is a publisher-field classification, not proof of original CSV extraction lineage.",
        "interpretation": "A nonmatch is an unresolved source/value match in this archived snapshot; it does not establish that the submitted value is erroneous. Blank field cells mean the corresponding city-level field was unavailable in this snapshot, not zero.",
    }
    if args.write:
        target = OUT / "comparison.csv"
        with target.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(output_rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(output_rows)
        (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
