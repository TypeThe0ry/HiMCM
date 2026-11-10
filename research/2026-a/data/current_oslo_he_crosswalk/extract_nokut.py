#!/usr/bin/env python3
"""Extract NOKUT's four institution categories from the archived HTML snapshot."""
from __future__ import annotations

import csv
from html.parser import HTMLParser
from pathlib import Path

SOURCE = Path(__file__).parents[1] / "current_oslo_he_scope" / "nokut_institutions.html"
OUTPUT = Path(__file__).with_name("national_roster.csv")


class RosterParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.category = ""
        self.in_listing = False
        self.listing_depth = 0
        self.capture: dict[str, str] | None = None
        self.rows: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs)
        if tag == "a" and attrs.get("data-toggle") == "collapse" and (attrs.get("href") or "").startswith("#collapsibleContent_"):
            self.category = ""
            self.in_listing = False
            self.capture = {"category_heading": "", "display_name": "", "title": "", "url": ""}
            self.capture["_kind"] = "category"
        elif tag == "div" and attrs.get("id", "").startswith("collapsibleContent_"):
            self.in_listing = True
            self.listing_depth = 1
        elif tag == "div" and self.in_listing:
            self.listing_depth += 1
        elif tag == "a" and self.in_listing and attrs.get("href") and not (attrs["href"] or "").startswith("#"):
            self.capture = {"category_heading": self.category, "display_name": "", "title": attrs.get("title") or "", "url": attrs["href"] or ""}
            self.capture["_kind"] = "institution"

    def handle_data(self, data: str) -> None:
        if self.capture is None:
            return
        kind = self.capture.get("_kind")
        if kind == "category":
            self.capture["category_heading"] += data
        elif kind == "institution":
            self.capture["display_name"] += data

    def handle_endtag(self, tag: str) -> None:
        if tag == "div" and self.in_listing:
            self.listing_depth -= 1
            if self.listing_depth == 0:
                self.in_listing = False
            return
        if tag != "a" or self.capture is None:
            return
        kind = self.capture.pop("_kind", "")
        if kind == "category":
            self.category = " ".join(self.capture["category_heading"].split())
            self.capture = None
        elif kind == "institution":
            row = {key: " ".join(value.split()) for key, value in self.capture.items()}
            row["category_heading"] = self.category
            row["accreditation_scope"] = (
                "programme-accredited only" if self.category == "University Colleges with accredited study programmes"
                else "institutionally accredited"
            )
            self.rows.append(row)
            self.capture = None


def main() -> None:
    parser = RosterParser()
    parser.feed(SOURCE.read_text(encoding="utf-8"))
    fields = ["category_heading", "accreditation_scope", "display_name", "title", "url"]
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(parser.rows)
    counts: dict[str, int] = {}
    for row in parser.rows:
        counts[row["category_heading"]] = counts.get(row["category_heading"], 0) + 1
    print(f"source={SOURCE}")
    print(f"rows={len(parser.rows)}")
    for category, count in counts.items():
        print(f"{count}\t{category}")


if __name__ == "__main__":
    main()
