"""Deterministically check Zurich's retained broadband value against the archived Ookla page."""
from pathlib import Path
import csv, hashlib, html, json, re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "data/task4_v5_resources/ookla_global_index.html"
MANIFEST = ROOT / "data/task4_v5_resources/manifest.json"
CSV = ROOT / "data/task4_v117_team_intake/city_indicators.csv"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
record = next(item for item in manifest if item["file"] == SOURCE.name)
raw = SOURCE.read_bytes()
assert len(raw) == record["bytes"]
assert hashlib.sha256(raw).hexdigest() == record["sha256"]
text = raw.decode("utf-8")
columns = list(re.finditer(r'id="column-([^\"]+)"', text))
idx = next(i for i, match in enumerate(columns) if match.group(1) == "fixedMedian")
start = columns[idx].start()
end = columns[idx + 1].start() if idx + 1 < len(columns) else len(text)
section = text[start:end]
needle = 'href="/global-index/switzerland?city=Zürich#fixed"'
rows = [(match.start() + start, match.group(0)) for match in re.finditer(r"<tr\b[^>]*>.*?</tr>", section, re.S) if needle in match.group(0)]
assert len(rows) == 1, len(rows)
row_offset, row = rows[0]
cells = [" ".join(html.unescape(re.sub(r"<[^>]*>", " ", cell)).split()) for cell in re.findall(r"<td\b[^>]*>(.*?)</td>", row, re.S)]
assert cells == ["18", "+3", "Zürich , Switzerland", "286.35"], cells
month = re.findall(r'<div class="month">([^<]+)</div>', text)
assert month == ["September 2026"], month
with CSV.open(encoding="utf-8-sig", newline="") as stream:
    submitted = next(item for item in csv.DictReader(stream) if item["city"] == "Zurich")
assert submitted["broadband_mbps"] == cells[3]
assert submitted["broadband_mbps_year"] == "2026"
assert submitted["broadband_mbps_flag"] == "ok"
line_start = raw[:len(text[:row_offset].encode("utf-8"))].count(b"\n") + 1
byte_start = len(text[:row_offset].encode("utf-8"))
byte_end = byte_start + len(row.encode("utf-8"))
result = {
    "status": "pass",
    "city_csv_label": "Zurich",
    "publisher_city_label": "Zürich",
    "country": "Switzerland",
    "indicator": "fixed broadband download speed",
    "publisher_measure_field": "fixedMedian",
    "statistic": "median",
    "direction": "download",
    "network": "fixed broadband",
    "publisher_value_mbps": 286.35,
    "publisher_rank": 18,
    "publication_label": month[0],
    "period_note": "Publisher page says results are updated mid-month for the previous three months; retained page does not state exact start/end dates for this city row.",
    "source_url": record["url"],
    "archive_access_date": record["accessed"],
    "archive_access_utc": None,
    "original_csv_extraction_url": None,
    "original_csv_extraction_time": None,
    "archive_file": str(SOURCE.relative_to(ROOT)),
    "source_sha256": {
        str(SOURCE.relative_to(ROOT)): sha(SOURCE),
        str(MANIFEST.relative_to(ROOT)): sha(MANIFEST),
        str(CSV.relative_to(ROOT)): sha(CSV),
    },
    "publisher_row_html": row,
    "extraction_coordinates": {
        "section_id": "column-fixedMedian",
        "row_link": needle,
        "line_start_1based": line_start,
        "line_end_1based": line_start + row.count("\n"),
        "byte_start_0based": byte_start,
        "byte_end_exclusive": byte_end,
        "html_cells": cells,
    },
    "source_footer": "Results are updated mid-month for the previous three months.",
    "submitted_value_matches_publisher": True,
    "original_csv_extraction_lineage_verified": False,
    "municipal_boundary_equivalence_verified": False,
    "primary_admissions": 0,
    "model_or_paper_changed": False,
    "scope": "Exact publisher value, field and publication-label match. It does not establish the original CSV extraction route, exact city-row measurement dates, representativeness, or equivalence between the publisher city geography and Zurich city proper.",
}
footer = "Results are updated mid-month for the previous three months."
assert footer in " ".join(html.unescape(re.sub(r"<[^>]*>", " ", text)).split())
print(json.dumps(result, ensure_ascii=False, indent=2))
