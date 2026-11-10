#!/usr/bin/env python3
"""Extract current named facility cards from the archived Oslo municipal directory response."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "directory_search_response_original.json"
OUTPUT = ROOT / "directory_facilities_extracted.json"
BASE = "https://www.oslo.kommune.no/natur-kultur-og-fritid/svommehaller-i-oslo/"
EXCLUDE = {"Svømmehaller i Oslo", "Kapasitet i svømmehallene", "Billettpriser for Oslo kommunes bad", "Ordensregler for Oslo kommunes bad"}

def main() -> None:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    records = []
    for hit in data.get("hits", []):
        meta = hit.get("meta") or {}
        url = meta.get("url", "")
        if not url.startswith(BASE) or hit.get("name") in EXCLUDE:
            continue
        card = hit.get("card_data") or {}
        coords = (hit.get("map_data") or {}).get("coordinates") or []
        content = " ".join(x.get("content", "") for x in hit.get("editorial_content", []) if x.get("type") == "wysiwyg")
        records.append({
            "name": hit.get("name"),
            "official_page_url": url,
            "official_record_updated_at": meta.get("updated_at"),
            "address": card.get("address"),
            "coordinates_wgs84": coords[0] if coords else None,
            "physical_facility_count": 1,
            "facility_type": "outdoor_seasonal" if hit.get("name") == "Frognerbadet" else "indoor_hall",
            "seasonal_components": ["outdoor area (18 May–23 August, according to captured Tøyenbadet page)"] if hit.get("name") == "Tøyenbadet" else [],
            "public_access_evidence": "Parent directory describes these as swimming halls operated by Oslo municipality; venue text lists ticket purchase at the venue.",
            "operating_or_access_notes": {
                "seasonal_outdoor": hit.get("name") == "Frognerbadet",
                "all_ages_access_claim": False,
                "page_text_excerpt": content[:3000],
            },
        })
    records.sort(key=lambda x: x["name"] or "")
    OUTPUT.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(records)} named directory facilities -> {OUTPUT.name}")

if __name__ == "__main__":
    main()
