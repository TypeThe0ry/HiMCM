#!/usr/bin/env python3
"""Archive World Bank downloads and build a verified country-year panel.

Default: rebuild offline from the archived raw files after SHA-256 verification.
Use --download --output-dir NEW_DIRECTORY to capture a new, separate snapshot.
CSV processing uses the standard library; Excel export requires openpyxl.
"""

import argparse
import csv
import hashlib
import io
import json
import math
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "data/country_year_homicide_education"
INDICATORS = {
    "homicide_rate_per_100k": ("VC.IHR.PSRC.P5", "homicide_worldbank.zip"),
    "secondary_pupil_teacher_ratio": (
        "SE.SEC.ENRL.TC.ZS", "secondary_pupil_teacher_worldbank.zip"
    ),
}
URLS = {
    filename: f"https://api.worldbank.org/v2/en/indicator/{code}?downloadformat=csv"
    for code, filename in INDICATORS.values()
}
URLS["countries_worldbank.json"] = (
    "https://api.worldbank.org/v2/country?format=json&per_page=1000"
)
PANEL_FIELDS = [
    "country_name", "wb_country_code", "year", "homicide_rate_per_100k",
    "secondary_pupil_teacher_ratio", "data_status",
]
LABELS = {
    "country_name": "国家或地区（英文）",
    "wb_country_code": "世界银行国家代码",
    "year": "年份",
    "homicide_rate_per_100k": "凶杀率（每10万人）",
    "secondary_pupil_teacher_ratio": "中学生师比（学生/教师）",
    "data_status": "数据可用状态",
    "homicide_observations": "凶杀率有效年份数",
    "homicide_first_year": "凶杀率最早年份",
    "homicide_last_year": "凶杀率最晚年份",
    "secondary_ratio_observations": "生师比有效年份数",
    "secondary_ratio_first_year": "生师比最早年份",
    "secondary_ratio_last_year": "生师比最晚年份",
    "matched_observations": "同年双指标完整数",
    "matched_first_year": "同年完整最早年份",
    "matched_last_year": "同年完整最晚年份",
    "region": "当前世界银行地区分类",
    "income_group": "当前世界银行收入分类",
    "countries_total": "国家和地区总数",
    "countries_homicide": "有凶杀率的国家地区数",
    "countries_secondary_ratio": "有生师比的国家地区数",
    "countries_both": "同年两项都有的国家地区数",
    "countries_neither": "两项都缺失的国家地区数",
}


def download(output):
    """Never overwrite an archived snapshot."""
    if (output / "download_manifest.json").exists() or (output / "raw").exists():
        raise ValueError("下载目标已有原始快照，请使用新的 --output-dir。")
    raw = output / "raw"
    raw.mkdir(parents=True)

    def fetch(item):
        filename, url = item
        request = Request(url, headers={"User-Agent": "HiMCM-research/1.0"})
        with urlopen(request, timeout=60) as response:
            content = response.read()
            metadata = {
                "file": "raw/" + filename,
                "url": url,
                "resolved_url": response.url,
                "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
                "content_type": response.headers.get("Content-Type"),
            }
        (raw / filename).write_bytes(content)
        return metadata

    with ThreadPoolExecutor(max_workers=3) as pool:
        sources = list(pool.map(fetch, URLS.items()))
    write_json(output / "download_manifest.json", {"sources": sources})


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verify_raw(output):
    manifest = json.loads((output / "download_manifest.json").read_text(encoding="utf-8"))
    expected = {"raw/" + name for name in URLS}
    assert {item["file"] for item in manifest["sources"]} == expected
    assert len(manifest["sources"]) == len(expected)
    for source in manifest["sources"]:
        content = (output / source["file"]).read_bytes()
        assert len(content) == source["bytes"], source["file"]
        assert hashlib.sha256(content).hexdigest() == source["sha256"], source["file"]
    return manifest


def read_indicator(path, expected_code):
    with zipfile.ZipFile(path) as archive:
        members = [name for name in archive.namelist() if name.startswith("API_")]
        assert len(members) == 1
        text = archive.read(members[0]).decode("utf-8-sig")
        lines = list(csv.reader(io.StringIO(text)))
        header_index = next(i for i, row in enumerate(lines) if row[:1] == ["Country Name"])
        updated = next(row[1] for row in lines[:header_index] if row[:1] == ["Last Updated Date"])
        header = lines[header_index]
        years = [int(field) for field in header if field.isdigit()]
        values, names = {}, {}
        for row in lines[header_index + 1:]:
            if not row:
                continue
            record = dict(zip(header, row))
            assert record["Indicator Code"] == expected_code
            code = record["Country Code"]
            assert code not in names, f"Duplicate country: {code}"
            names[code] = record["Country Name"]
            for year in years:
                value = record[str(year)]
                if value != "":
                    number = float(value)
                    assert math.isfinite(number) and number >= 0, (code, year, value)
                    values[(code, year)] = value  # Preserve original numeric strings in CSV.
        metadata_name = next(n for n in archive.namelist() if n.startswith("Metadata_Indicator_"))
        metadata_rows = list(csv.DictReader(io.StringIO(archive.read(metadata_name).decode("utf-8-sig"))))
        assert len(metadata_rows) == 1 and metadata_rows[0]["INDICATOR_CODE"] == expected_code
    return values, names, years, updated, metadata_rows[0]


def write_csv(path, rows, fields):
    # BOM helps Excel display UTF-8 correctly; csv.DictReader uses utf-8-sig.
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def export_excel(output, tables, dictionary, manifest):
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    workbook = Workbook()
    workbook.remove(workbook.active)
    for title, rows, fields in tables:
        sheet = workbook.create_sheet(title)
        sheet.append([LABELS.get(field, field) for field in fields])
        for row in rows:
            cells = []
            for field in fields:
                value = row[field]
                if value == "" or value is None:
                    value = None
                elif field in INDICATORS:
                    value = float(value)
                cells.append(value)
            sheet.append(cells)
        for col, field in enumerate(fields, 1):
            sheet.column_dimensions[get_column_letter(col)].width = 33 if field == "country_name" else 25
            if field in INDICATORS:
                for cells in sheet.iter_rows(min_row=2, min_col=col, max_col=col):
                    cells[0].number_format = "0.000000"
        sheet.freeze_panes = "D2" if fields == PANEL_FIELDS else "C2"
        sheet.auto_filter.ref = sheet.dimensions
    sheet = workbook.create_sheet("字段与口径")
    sheet.append(["字段", "中文含义", "说明"])
    for row in dictionary:
        sheet.append([row["field"], row["label_zh"], row["definition_zh"]])
    sheet.column_dimensions["A"].width = 36
    sheet.column_dimensions["B"].width = 29
    sheet.column_dimensions["C"].width = 100
    sheet = workbook.create_sheet("数据来源")
    sheet.append(["文件", "来源链接", "下载时间UTC", "SHA256"])
    for source in manifest["sources"]:
        sheet.append([source["file"], source["url"], source["retrieved_at_utc"], source["sha256"]])
        sheet.cell(sheet.max_row, 2).hyperlink = source["url"]
        sheet.cell(sheet.max_row, 2).style = "Hyperlink"
    for col, width in zip("ABCD", [52, 100, 35, 70]):
        sheet.column_dimensions[col].width = width
    for sheet in workbook:
        sheet.sheet_view.showGridLines = False
        sheet.row_dimensions[1].height = 32
        for cell in sheet[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="17365D")
            cell.alignment = Alignment(vertical="center", wrap_text=True)
        if sheet.title in ("字段与口径", "数据来源"):
            sheet.freeze_panes = "A2"
            for row in sheet.iter_rows(min_row=2):
                sheet.row_dimensions[row[0].row].height = 54
                for cell in row:
                    cell.alignment = Alignment(vertical="top", wrap_text=True)
    path = output / "country_year_homicide_education.xlsx"
    workbook.save(path)
    # Read back every data cell, including blanks and numeric conversion.
    check = load_workbook(path, read_only=True, data_only=True)
    for title, rows, fields in tables:
        sheet = check[title]
        assert sheet.max_row == len(rows) + 1
        for actual, expected in zip(sheet.iter_rows(min_row=2, values_only=True), rows):
            for value, field in zip(actual, fields):
                original = expected[field]
                if original == "" or original is None:
                    assert value is None
                elif field in INDICATORS:
                    assert math.isclose(value, float(original), rel_tol=1e-14, abs_tol=1e-14)
                else:
                    assert value == original, (title, field, value, original)
    check.close()


def build(output, csv_only=False):
    manifest = verify_raw(output)
    country_api = json.loads((output / "raw/countries_worldbank.json").read_text(encoding="utf-8-sig"))
    assert country_api[0]["pages"] == 1
    assert len(country_api[1]) == int(country_api[0]["total"])
    countries = {row["id"]: row for row in country_api[1] if row["region"]["value"] != "Aggregates"}
    all_codes = {row["id"] for row in country_api[1]}
    series, source_info, grid_years, country_sets = {}, {}, set(), []
    for field, (indicator, filename) in INDICATORS.items():
        values, names, years, updated, metadata = read_indicator(output / "raw" / filename, indicator)
        assert set(names) <= all_codes
        assert countries.keys() <= names.keys(), "Missing economy in source archive"
        country_sets.append(set(names))
        grid_years.update(years)
        series[field] = values
        retained = {key: value for key, value in values.items() if key[0] in countries}
        source_info[field] = {
            "indicator_code": indicator,
            "indicator_page": f"https://data.worldbank.org/indicator/{indicator}",
            "archive": "raw/" + filename,
            "wdi_last_updated": updated,
            "source_organization": metadata["SOURCE_ORGANIZATION"],
            "source_note": metadata["SOURCE_NOTE"],
            "non_null_observations": len(retained),
            "countries_with_data": len({key[0] for key in retained}),
            "first_observed_year": min(key[1] for key in retained),
            "last_observed_year": max(key[1] for key in retained),
        }
    assert country_sets[0] == country_sets[1]
    years = sorted(grid_years)
    panel, matched, coverage = [], [], []
    homicide = series["homicide_rate_per_100k"]
    secondary = series["secondary_pupil_teacher_ratio"]
    for code, country in sorted(countries.items(), key=lambda item: item[1]["name"]):
        available_h, available_s, available_both = [], [], []
        for year in years:
            h, s = homicide.get((code, year), ""), secondary.get((code, year), "")
            both = h != "" and s != ""
            row = dict(zip(PANEL_FIELDS, [
                country["name"], code, year, h, s,
                "both" if both else "homicide_only" if h != "" else "secondary_ratio_only" if s != "" else "neither",
            ]))
            panel.append(row)
            if h != "":
                available_h.append(year)
            if s != "":
                available_s.append(year)
            if both:
                matched.append(row)
                available_both.append(year)
        country_coverage = {
            "country_name": country["name"], "wb_country_code": code,
            "region": country["region"]["value"], "income_group": country["incomeLevel"]["value"],
        }
        for prefix, available in [
            ("homicide", available_h), ("secondary_ratio", available_s), ("matched", available_both)
        ]:
            country_coverage.update({
                prefix + "_observations": len(available),
                prefix + "_first_year": min(available) if available else "",
                prefix + "_last_year": max(available) if available else "",
            })
        coverage.append(country_coverage)
    annual = []
    for year in years:
        rows = [row for row in panel if row["year"] == year]
        annual.append({
            "year": year, "countries_total": len(rows),
            "countries_homicide": sum(row["homicide_rate_per_100k"] != "" for row in rows),
            "countries_secondary_ratio": sum(row["secondary_pupil_teacher_ratio"] != "" for row in rows),
            "countries_both": sum(row["data_status"] == "both" for row in rows),
            "countries_neither": sum(row["data_status"] == "neither" for row in rows),
        })
    assert len(panel) == len(countries) * len(years)
    assert len({(row["wb_country_code"], row["year"]) for row in panel}) == len(panel)
    for field, values in series.items():
        exported = {(row["wb_country_code"], row["year"]): row[field] for row in panel if row[field] != ""}
        assert exported == {key: value for key, value in values.items() if key[0] in countries}
    assert len(matched) == sum(row["countries_both"] for row in annual)
    dictionary = [
        {"field": "country_name", "label_zh": LABELS["country_name"], "definition_zh": "世界银行国家API的英文名称；包含国家和单列地区/经济体。"},
        {"field": "wb_country_code", "label_zh": LABELS["wb_country_code"], "definition_zh": "世界银行三位代码；通常对应ISO3，但不保证全部为ISO标准国家代码。与year共同构成唯一键。"},
        {"field": "year", "label_zh": LABELS["year"], "definition_zh": "原始数据的观测年份。教育指标跨年学年按结束年份标记；不是下载年或数据库更新年。"},
        {"field": "homicide_rate_per_100k", "label_zh": LABELS["homicide_rate_per_100k"], "definition_zh": "VC.IHR.PSRC.P5：故意杀人受害者数/人口×100000；每10万人。原始来源UNODC，经WDI发布。"},
        {"field": "secondary_pupil_teacher_ratio", "label_zh": LABELS["secondary_pupil_teacher_ratio"], "definition_zh": "SE.SEC.ENRL.TC.ZS：中等教育学生数/同层级教师数，学生/教师；含初中和高中整体，不是平均班额。原始来源UNESCO UIS，经WDI发布。"},
        {"field": "data_status", "label_zh": LABELS["data_status"], "definition_zh": "both=同年两项都有；homicide_only=仅凶杀率；secondary_ratio_only=仅生师比；neither=均缺失。空白是缺失，不是0。"},
        {"field": "coverage", "label_zh": "覆盖表", "definition_zh": "国家覆盖表列各指标及同年双指标的有效数、首末年；年度覆盖表列各年的有效国家地区数。region和income_group是下载时分类，不是历史分类。"},
        {"field": "scope", "label_zh": "地域与缺失处理", "definition_zh": "排除世界、区域、收入组等Aggregates汇总；国家/地区数据不能直接充当城市数据（城市国家需单独判断）。保留原值；不插值、不补零、不前向填充、不跨年配对。"},
    ]
    tables = [
        ("国家年份总表", panel, PANEL_FIELDS),
        ("同年双指标完整", matched, PANEL_FIELDS),
        ("国家覆盖", coverage, list(coverage[0])),
        ("年度覆盖", annual, list(annual[0])),
    ]
    for (_, rows, fields), filename in zip(tables, [
        "country_year.csv", "country_year_both_observed.csv", "country_coverage.csv", "year_coverage.csv"
    ]):
        path = output / filename
        write_csv(path, rows, fields)
        with path.open(encoding="utf-8-sig", newline="") as stream:
            assert list(csv.DictReader(stream)) == [
                {key: str(row[key]) for key in fields} for row in rows
            ]
    write_csv(output / "data_dictionary.csv", dictionary, ["field", "label_zh", "definition_zh"])
    summary = {
        "country_economy_count": len(countries),
        "excluded_aggregate_count": len(country_sets[0] - countries.keys()),
        "panel_year_start": min(years), "panel_year_end": max(years),
        "panel_rows": len(panel),
        "rows_with_any_observation": sum(row["data_status"] != "neither" for row in panel),
        "rows_with_both_observations": len(matched),
        "countries_with_both_observations": len({row["wb_country_code"] for row in matched}),
        "first_matched_year": min(row["year"] for row in matched),
        "last_matched_year": max(row["year"] for row in matched),
        "indicators": source_info,
        "validation": {
            "raw_sha256_verified": True, "unique_country_year_keys": True,
            "all_non_null_values_equal_archived_source_strings": True,
            "csv_roundtrip_verified": True, "excel_cell_roundtrip_verified": not csv_only,
        },
    }
    if not csv_only:
        export_excel(output, tables, dictionary, manifest)
    write_json(output / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--download", action="store_true", help="下载到新目录；拒绝覆盖已有原始快照")
    parser.add_argument("--csv-only", action="store_true", help="只生成CSV和JSON，不需要openpyxl")
    args = parser.parse_args()
    if args.download:
        download(args.output_dir)
    build(args.output_dir, csv_only=args.csv_only)


if __name__ == "__main__":
    main()
