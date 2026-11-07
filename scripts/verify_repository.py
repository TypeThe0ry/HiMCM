"""Check archive integrity, navigation, and the distinction between inputs and results."""
from pathlib import Path
import csv
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "library"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    papers = json.loads((LIBRARY / "catalog.json").read_text())
    assert len(papers) == 68, "Unexpected canonical paper count"
    for paper in papers:
        path = LIBRARY / paper["path"]
        assert path.is_file(), str(path)
        assert digest(path) == paper["sha256"], str(path)
        assert (LIBRARY / paper["report"]).is_file(), paper["report"]

    with (LIBRARY / "catalog.csv").open(encoding="utf-8-sig", newline="") as handle:
        csv_papers = list(csv.DictReader(handle))
    assert {(p["year"], p["team"], p["path"]) for p in papers} == {
        (p["year"], p["team"], p["path"]) for p in csv_papers
    }
    page = (LIBRARY / "index.html").read_text()
    embedded, _ = json.JSONDecoder().raw_decode(page.split("const data=", 1)[1])
    assert {p["path"] for p in embedded} == {p["path"] for p in papers}

    for filename in ["download_log.csv", "official_results_parsed.csv", "duplicates.csv"]:
        with (LIBRARY / filename).open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                if filename == "download_log.csv" and row["status"] != "ok":
                    continue
                for key in ["path", "report", "input", "canonical"]:
                    if row.get(key):
                        assert (LIBRARY / row[key]).is_file(), (filename, row[key])

    links = 0
    for document in ROOT.rglob("*.md"):
        if any(part in document.parts for part in [".git", "source_snapshots", "inputs"]):
            continue
        for target in re.findall(r"\]\(([^)]+)\)", document.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            assert (document.parent / target.split("#", 1)[0]).exists(), (str(document), target)
            links += 1

    research = ROOT / "research/2026-a"
    provenance = json.loads((research / "inputs/team/provenance.json").read_text())
    for item in provenance:
        assert digest(ROOT / item["repository_path"]) == item["sha256"]
    with (research / "data/city_candidates_team_25.csv").open(encoding="utf-8-sig") as handle:
        candidates = list(csv.DictReader(handle))
    assert len(candidates) == 25 and len({row["city"] for row in candidates}) == 25
    assert all(row["candidate_status"] == "proposed_not_frozen" for row in candidates)
    with (research / "data/indicator_matrix_template.csv").open(encoding="utf-8-sig") as handle:
        template = list(csv.DictReader(handle))
    assert len(template) == 216 and all(row["value"] == "" for row in template)
    assert all(json.loads((research / "design/synthetic_results.json").read_text())["checks"].values())
    assert all(
        str(path.relative_to(ROOT)).isascii()
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts
    )
    print(json.dumps({
        "papers_verified": len(papers),
        "reference_pdfs": len(list((LIBRARY / "references").rglob("*.pdf"))),
        "candidate_cities": len(candidates),
        "local_markdown_links": links,
        "original_team_inputs": len(provenance),
        "status": "passed",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
