#!/usr/bin/env python3
"""Extract venue-level records using Python's standard-library HTMLParser."""
from __future__ import annotations

import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
RETRIEVAL = json.loads((HERE / "retrieval.json").read_text())
BASELINE_POSTCODES = {
    "756973", "544964", "528523", "469662", "648965", "609517", "158790"
}

class CardParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.card_div_depth = 0
        self.capture = None
        self.fields = {"name": [], "address": [], "weekly_closed_day": []}
        self.provider_url = None
        self.has_closure_label = False
        self.cards = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = set((attrs.get("class") or "").split())
        if tag == "div" and self.card_div_depth == 0 and "cst-list-item" in classes:
            self.card_div_depth = 1
            return
        if self.card_div_depth == 0:
            return
        if tag == "div":
            self.card_div_depth += 1
        if tag == "a" and "view-page-link" in classes:
            self.provider_url = attrs.get("href")
        if tag == "span" and "closed" in classes:
            self.has_closure_label = True
        targets = {
            ("h2", None): "name",
            ("div", "cst-address"): "address",
            ("span", "desk-day"): "weekly_closed_day",
        }
        for (target_tag, target_class), field in targets.items():
            if tag == target_tag and (target_class is None or target_class in classes):
                self.capture = (field, tag)
                break

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if self.card_div_depth == 0:
            return
        if self.capture is not None and tag == self.capture[1]:
            self.capture = None
        if tag == "div":
            self.card_div_depth -= 1
            if self.card_div_depth == 0:
                row = {k: " ".join("".join(v).split()) for k, v in self.fields.items()}
                row["provider_url"] = self.provider_url
                row["has_closure_label"] = self.has_closure_label
                self.cards.append(row)
                self.fields = {"name": [], "address": [], "weekly_closed_day": []}
                self.provider_url = None
                self.has_closure_label = False
                self.capture = None

    def handle_data(self, data):
        if self.capture is not None:
            field, _ = self.capture
            self.fields[field].append(data)

rows = []
page_updates = set()
for page_record in RETRIEVAL["pages"]:
    raw = (HERE / page_record["file"]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != page_record["sha256"]:
        raise ValueError(f"SHA-256 mismatch for {page_record['file']}")
    decoded = raw.decode("utf-8")
    updates = re.findall(r"Last updated:\s*([^<]+)", decoded, flags=re.I)
    if not updates:
        raise ValueError(f"No displayed last-updated date in {page_record['file']}")
    page_updates.update(" ".join(u.split()) for u in updates)
    parser = CardParser()
    parser.feed(decoded)
    if len(parser.cards) != 10 and page_record["file"] != "active_sg_directory_page_3.html":
        raise ValueError(f"Expected 10 cards on {page_record['file']}, got {len(parser.cards)}")
    for card in parser.cards:
        name, address, href = card["name"], card["address"], card["provider_url"]
        match = re.search(r"\bSingapore\s+(\d{6})\b", address)
        if not (name and address and href and match):
            raise ValueError(f"Incomplete directory card: {card}")
        slug = urlparse(href).path.rstrip("/").rsplit("/", 1)[-1]
        closed_day = card["weekly_closed_day"] or None
        rows.append({
            "name": name,
            "address": address,
            "postal_code": match.group(1),
            "provider_id": slug,
            "provider_id_type": "facility-page URL slug (no numeric ID exposed in directory)",
            "provider_url": href,
            "source_page": page_record["file"],
            "listing_category": "Swimming Pool",
            "directory_weekly_maintenance_closed_day": closed_day,
            "in_2025_article_subset_by_postal_code": match.group(1) in BASELINE_POSTCODES,
        })

postcodes = [r["postal_code"] for r in rows]
if len(rows) != 25:
    raise AssertionError(f"Expected directory total 25, extracted {len(rows)}")
if len(set(postcodes)) != 25:
    raise AssertionError("Duplicate postal codes require physical-venue review")
if len({r["provider_id"] for r in rows}) != 25:
    raise AssertionError("Duplicate provider page slugs")
if len(page_updates) != 1:
    raise AssertionError(f"Inconsistent displayed last-updated dates: {page_updates}")

(HERE / "venues.json").write_text(json.dumps({
    "source_name": "ActiveSG Circle swimming-pool facility directory",
    "source_url": "https://www.activesgcircle.gov.sg/facilities/swimming-pools",
    "capture_date_utc": RETRIEVAL["pages"][0]["attempt_utc"][:10],
    "directory_displayed_last_updated": next(iter(page_updates)),
    "directory_displayed_total": 25,
    "extracted_listings": len(rows),
    "distinct_physical_addresses_postcodes": len(set(postcodes)),
    "not_in_2025_article_subset_count": sum(not r["in_2025_article_subset_by_postal_code"] for r in rows),
    "comparison_note": "Article subset matches are by postal code; Our Tampines Hub and Tampines Swimming Complex are treated as the same physical venue at 528523.",
    "venues": rows,
}, indent=2, ensure_ascii=False) + "\n")
print(f"Extracted {len(rows)} cards, {len(set(postcodes))} distinct postcodes, "
      f"{sum(not r['in_2025_article_subset_by_postal_code'] for r in rows)} outside article subset; "
      f"directory update: {next(iter(page_updates))}")
