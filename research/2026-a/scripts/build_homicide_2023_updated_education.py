#!/usr/bin/env python3
"""Build 2023 and explicitly dated nearby-year pairs from archived official data.

The updated ratio is DERIVED: SE.SEC.ENRL / SE.SEC.TCHR, same country/year.
It is not a newly published observation of SE.SEC.ENRL.TC.ZS.
Default: offline rebuild; --csv-only avoids the openpyxl dependency.
"""

import argparse
import csv
import hashlib
import io
import json
import math
import zipfile
from collections import Counter
from decimal import Decimal, localcontext
from pathlib import Path

from build_country_year_homicide_education import read_indicator, write_csv


OUTPUT = Path(__file__).resolve().parents[1] / "data/homicide_2023_secondary_ratio_updated"
COUNTS = {
    "secondary_students": ("SE.SEC.ENRL", "secondary_students_worldbank.zip", "20082"),
    "secondary_teachers": ("SE.SEC.TCHR", "secondary_teachers_worldbank.zip", "20182"),
}
FIELDS = [
    "country_name", "wb_country_code", "homicide_year", "homicide_rate_per_100k",
    "education_year", "secondary_students", "secondary_teachers",
    "secondary_pupil_teacher_ratio_derived", "education_year_gap",
    "education_after_homicide", "pair_status", "ratio_origin",
]
LABELS = {
    "country_name": "国家或地区（英文）", "wb_country_code": "世界银行国家代码",
    "homicide_year": "凶杀率年份", "homicide_rate_per_100k": "凶杀率（每10万人）",
    "education_year": "教育数据年份", "year": "年份",
    "secondary_students": "中等教育学生总数", "secondary_teachers": "中等教育教师总数",
    "secondary_pupil_teacher_ratio_derived": "生师比（由官方总数计算）",
    "education_year_gap": "教育年份减2023", "education_after_homicide": "教育数据晚于2023（1是0否）",
    "pair_status": "匹配状态", "ratio_origin": "比率来源类型",
    "uis_reference_status": "与UIS数值核对结果",
    "students_magnitude": "UIS学生数Magnitude", "students_qualifier": "UIS学生数Qualifier",
    "teachers_magnitude": "UIS教师数Magnitude", "teachers_qualifier": "UIS教师数Qualifier",
    "countries_with_students": "学生数非空国家地区数",
    "countries_with_teachers": "教师数非空国家地区数",
    "countries_with_derived_ratio": "可计算生师比国家地区数",
    "countries_paired_homicide_2023": "可对应2023凶杀率国家地区数",
}


def read_uis(raw):
    with zipfile.ZipFile(raw / "uis_secondary_counts_2018_2025_excerpt.zip") as archive:
        rows = list(csv.DictReader(io.StringIO(archive.read(
            "OPRI_DATA_NATIONAL_secondary_2018_2025.csv"
        ).decode("utf-8-sig"))))
        notes = list(csv.DictReader(io.StringIO(archive.read(
            "OPRI_METADATA_secondary_2018_2025.csv"
        ).decode("utf-8-sig"))))
    observations = {(row["INDICATOR_ID"], row["COUNTRY_ID"], int(row["YEAR"])): row for row in rows}
    assert len(observations) == len(rows)
    return observations, notes


def verify_manifest(output):
    manifest = json.loads((output / "download_manifest.json").read_text(encoding="utf-8"))
    for source in manifest["sources"]:
        content = (output / source["file"]).read_bytes()
        assert len(content) == source["bytes"], source["file"]
        assert hashlib.sha256(content).hexdigest() == source["sha256"], source["file"]
    return manifest


def workbook(output, tables, manifest, summary):
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    book = Workbook()
    book.remove(book.active)
    numeric = {
        "homicide_rate_per_100k", "secondary_students", "secondary_teachers",
        "secondary_pupil_teacher_ratio_derived",
    }
    for title, filename, rows, fields in tables:
        sheet = book.create_sheet(title)
        sheet.append([LABELS.get(field, field) for field in fields])
        for row in rows:
            sheet.append([
                None if row[field] == "" else float(row[field]) if field in numeric else row[field]
                for field in fields
            ])
        sheet.freeze_panes = "C2"
        sheet.auto_filter.ref = sheet.dimensions
        for i, field in enumerate(fields, 1):
            sheet.column_dimensions[get_column_letter(i)].width = 34 if field == "country_name" else 25
            if field in numeric:
                for cells in sheet.iter_rows(min_row=2, min_col=i, max_col=i):
                    cells[0].number_format = "0.000000"
    sheet = book.create_sheet("方法与限制")
    sheet.append(["项目", "说明"])
    for row in method_notes(summary):
        sheet.append(row)
    sheet.column_dimensions["A"].width = 32
    sheet.column_dimensions["B"].width = 115
    for row in sheet.iter_rows(min_row=2):
        sheet.row_dimensions[row[0].row].height = 68
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    sheet = book.create_sheet("数据来源")
    sheet.append(["文件", "来源URL", "SHA256"])
    for source in manifest["sources"]:
        sheet.append([source["file"], source["url"], source["sha256"]])
        sheet.cell(sheet.max_row, 2).hyperlink = source["url"]
    for col, width in zip("ABC", [54, 105, 70]):
        sheet.column_dimensions[col].width = width
    for sheet in book:
        sheet.sheet_view.showGridLines = False
        sheet.row_dimensions[1].height = 36
        for cell in sheet[1]:
            cell.fill = PatternFill("solid", fgColor="17365D")
            cell.font = Font(color="FFFFFF", bold=True)
            cell.alignment = Alignment(wrap_text=True, vertical="center")
    path = output / "homicide_2023_updated_secondary_ratio.xlsx"
    book.save(path)
    check = load_workbook(path, read_only=True, data_only=True)
    for title, filename, rows, fields in tables:
        assert check[title].max_row == len(rows) + 1
        for actual, row in zip(check[title].iter_rows(min_row=2, values_only=True), rows):
            for value, field in zip(actual, fields):
                if row[field] == "":
                    assert value is None
                elif field in numeric:
                    assert math.isclose(value, float(row[field]), rel_tol=1e-14, abs_tol=1e-14)
                else:
                    assert value == row[field]
    check.close()


def method_notes(summary):
    return [
        ("计算方式", "生师比=同一国家、同一年SE.SEC.ENRL学生总数÷SE.SEC.TCHR教师总数。比率是本项目计算值，原始计数由UIS经WDI发布；不是旧SE.SEC.ENRL.TC.ZS序列的新观测。"),
        ("层级和分母", "中等教育整体（ISCED 2+3），公私立，教师不限定合格教师。各国教师人数/全时当量处理可能不同；保留发布计数口径，不保证统一FTE，也不是平均班额。"),
        ("严格2023", f"2023年可计算生师比的国家和地区{summary['education_2023_countries']}个；有2023凶杀率的{summary['homicide_2023_countries']}个，与生师比交集{summary['strict_2023_complete_pairs']}个。主分析优先使用严格同年完整表。"),
        ("邻近年份规则", "只在2021—2025中选择同国同年的学生+教师，两者不跨年。按距2023绝对年差最小选择；距离相同优先较早年份：2023→2022→2024→2021→2025。凶杀率始终只取2023；缺失不换年。"),
        ("教育年份标记", "education_year保留原始观测年；education_year_gap=教育年−2023；education_after_homicide=1表示教育数据晚于凶杀率。后于2023的数据只适合补充敏感性分析，不能当成2023观测或先验预测特征。跨年学年按结束年标记。"),
        ("缺失和状态", "空白=缺失，不补零、不插值。pair_status的exact_2023/nearby_year表示两指标均有效；homicide_missing/education_missing/both_missing表示缺失。ratio_origin仅当比率存在时为derived_from_official_counts。"),
        ("UIS核对与注释", "与UIS摘录按两个指标各自的国家+年份核对，数值允许1e-7相对容差（发布舍入差异）。MAGNITUDE/QUALIFIER原样保留，空白不保证不存在估计。Data reporting元数据中的NA不等于VALUE缺失。详细观测注释见uis_observation_notes.csv及raw摘录。"),
        ("范围与版本", "217个国家和单列地区/经济体，排除世界银行汇总组；国家代码与2023凶杀率沿用上一版归档。旧生师比原始序列及旧版表格保留于相邻country_year_homicide_education目录，不将新派生值混填进旧序列。"),
    ]


def build(output, csv_only=False):
    manifest = verify_manifest(output)
    raw = output / "raw"
    countries_api = json.loads((raw / "countries_worldbank.json").read_text(encoding="utf-8-sig"))
    assert countries_api[0]["pages"] == 1 and len(countries_api[1]) == int(countries_api[0]["total"])
    countries = {row["id"]: row["name"] for row in countries_api[1] if row["region"]["value"] != "Aggregates"}
    homicide = read_indicator(raw / "homicide_worldbank.zip", "VC.IHR.PSRC.P5")[0]
    counts = {field: read_indicator(raw / filename, code)[0] for field, (code, filename, uis_id) in COUNTS.items()}
    uis, notes = read_uis(raw)
    recent, ratios, crosscheck = [], {}, Counter()
    for country, name in sorted(countries.items(), key=lambda item: item[1]):
        for year in range(2018, 2026):
            key = (country, year)
            row = {"country_name": name, "wb_country_code": country, "year": year}
            matched_sources = 0
            for field, (code, filename, uis_id) in COUNTS.items():
                value = counts[field].get(key, "")
                row[field] = value
                reference = uis.get((uis_id, country, year))
                prefix = "students" if field == "secondary_students" else "teachers"
                row[prefix + "_magnitude"] = reference["MAGNITUDE"] if reference else ""
                row[prefix + "_qualifier"] = reference["QUALIFIER"] if reference else ""
                if value != "" and reference and reference["VALUE"] != "":
                    assert math.isclose(float(value), float(reference["VALUE"]), rel_tol=1e-7, abs_tol=1e-7), (key, field)
                    crosscheck["count_values_verified_with_uis"] += 1
                    matched_sources += 1
                elif value != "":
                    crosscheck["count_values_without_uis_reference"] += 1
            students, teachers = row["secondary_students"], row["secondary_teachers"]
            invalid_flags = {row["students_magnitude"], row["teachers_magnitude"]} & {"NA", "SUPP", "INCLUDED"}
            ratio = ""
            if students != "" and teachers != "" and Decimal(teachers) > 0 and not invalid_flags:
                with localcontext() as context:
                    context.prec = 28
                    ratio = format(Decimal(students) / Decimal(teachers), ".15g")
                ratios[key] = ratio
                assert math.isclose(float(ratio) * float(teachers), float(students), rel_tol=1e-14)
            row["secondary_pupil_teacher_ratio_derived"] = ratio
            row["uis_reference_status"] = "both_counts_agree_within_tolerance" if matched_sources == 2 else "incomplete_reference"
            recent.append(row)
    recent_index = {(row["wb_country_code"], row["year"]): row for row in recent}

    def pair(country, year):
        h = homicide.get((country, 2023), "")
        ratio = ratios.get((country, year), "") if year is not None else ""
        education = recent_index[(country, year)] if year is not None else {}
        complete = h != "" and ratio != ""
        return dict(zip(FIELDS, [
            countries[country], country, 2023, h, year if year is not None else "",
            education.get("secondary_students", ""), education.get("secondary_teachers", ""), ratio,
            year - 2023 if ratio != "" else "", int(year > 2023) if ratio != "" else "",
            ("exact_2023" if year == 2023 else "nearby_year") if complete else
            "homicide_missing" if h == "" and ratio != "" else "education_missing" if h != "" else "both_missing",
            "derived_from_official_counts" if ratio != "" else "",
        ]))

    strict, nearby = [], []
    for country in sorted(countries, key=countries.get):
        strict.append(pair(country, 2023))
        available = [year for year in range(2021, 2026) if (country, year) in ratios]
        chosen = min(available, key=lambda year: (abs(year - 2023), year > 2023)) if available else None
        nearby.append(pair(country, chosen))
    complete = [row for row in strict if row["pair_status"] == "exact_2023"]
    annual = [{
        "year": year,
        "countries_with_students": sum((country, year) in counts["secondary_students"] for country in countries),
        "countries_with_teachers": sum((country, year) in counts["secondary_teachers"] for country in countries),
        "countries_with_derived_ratio": sum((country, year) in ratios for country in countries),
        "countries_paired_homicide_2023": sum((country, year) in ratios and (country, 2023) in homicide for country in countries),
    } for year in range(2018, 2026)]
    for rows in (strict, nearby):
        assert len(rows) == len(countries) == len({row["wb_country_code"] for row in rows})
    for row in nearby:
        if row["secondary_pupil_teacher_ratio_derived"] != "":
            assert abs(row["education_year_gap"]) <= 2
        if row["pair_status"] == "exact_2023":
            assert row == next(item for item in strict if item["wb_country_code"] == row["wb_country_code"])
    singapore = next(row for row in complete if row["wb_country_code"] == "SGP")
    official_sg = json.loads((raw / "singapore_official_ptr.json").read_text())["result"]["records"]
    published_sg = next(row for row in official_sg if row["DataSeries"] == "Pupil-Teacher Ratio In Secondary School")
    assert round(float(singapore["secondary_pupil_teacher_ratio_derived"]), 1) == float(published_sg["2023"])
    summary = {
        "country_economy_count": len(countries),
        "homicide_2023_countries": sum((country, 2023) in homicide for country in countries),
        "education_2023_countries": sum((country, 2023) in ratios for country in countries),
        "strict_2023_complete_pairs": len(complete),
        "nearby_2021_2025_complete_pairs": sum(row["pair_status"] in {"exact_2023", "nearby_year"} for row in nearby),
        "education_years_for_complete_nearby_pairs": dict(sorted(Counter(
            row["education_year"] for row in nearby if row["pair_status"] in {"exact_2023", "nearby_year"}
        ).items())),
        "ratio_origin": "derived_from_official_counts: SE.SEC.ENRL / SE.SEC.TCHR",
        "count_basis": "published counts; headcount/FTE handling may differ across countries",
        "crosschecks": dict(crosscheck),
        "singapore_2023_official_rounded_ptr": float(published_sg["2023"]),
        "validation": {"raw_sha256_verified": True, "unique_country_year_keys": True,
                       "same_country_year_numerator_denominator": True, "excel_readback_verified": not csv_only},
    }
    tables = [
        ("2023同年完整", "matched_2023_complete.csv", complete, FIELDS),
        ("2023全部国家", "countries_2023_all.csv", strict, FIELDS),
        ("邻近年份补充", "nearby_years_2021_2025.csv", nearby, FIELDS),
        ("近年教育明细", "secondary_counts_ratios_2018_2025.csv", recent, list(recent[0])),
        ("年度覆盖", "year_coverage.csv", annual, list(annual[0])),
    ]
    for title, filename, rows, fields in tables:
        path = output / filename
        write_csv(path, rows, fields)
        with path.open(encoding="utf-8-sig", newline="") as stream:
            assert list(csv.DictReader(stream)) == [{field: str(row[field]) for field in fields} for row in rows]
    write_csv(output / "uis_observation_notes.csv", notes, list(notes[0]))
    write_csv(output / "method_notes.csv", [{"topic": topic, "note_zh": note} for topic, note in method_notes(summary)], ["topic", "note_zh"])
    if not csv_only:
        workbook(output, tables, manifest, summary)
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    parser.add_argument("--csv-only", action="store_true")
    arguments = parser.parse_args()
    build(arguments.output_dir, arguments.csv_only)
