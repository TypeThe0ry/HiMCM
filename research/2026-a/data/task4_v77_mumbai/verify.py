"""Verify original hashes and manually transcribed grade reconciliation."""
import csv
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE.parent / "task4_v40_mumbai"
HASHES = {
    "city2025.pdf": "55ed1b28efbde68b858abbb4902eaf75a5916f412878351567b94bb898c289c1",
    "suburban2025.pdf": "bd1da155c04f07f0c6990ea5b515d1a6a0237c03abb2f363c538e70014db44f2",
}
for filename, expected in HASHES.items():
    assert hashlib.sha256((ORIGINAL / filename).read_bytes()).hexdigest() == expected
with (HERE / "grade_reconciliation.csv").open() as f:
    rows = list(csv.DictReader(f))
for row in rows:
    boys = int(row["grade11_boys"]) + int(row["grade12_boys"])
    girls = int(row["grade11_girls"]) + int(row["grade12_girls"])
    delta = boys + girls - int(row["table8_3_boys"]) - int(row["table8_3_girls"])
    if row["district"] == "Mumbai Suburban":
        assert boys == int(row["table8_3_boys"])
        assert girls == int(row["table8_3_girls"])
    else:
        assert boys + girls == 71840 and delta == 14315
    print(row["district"], row["division"], "grade11_12=", boys + girls, "delta=", delta)
for field in ("grade11_boys", "grade11_girls", "grade12_boys", "grade12_girls"):
    assert int(rows[1][field]) + int(rows[2][field]) == int(rows[3][field])
with (HERE / "school_category_totals.csv").open() as f:
    categories = list(csv.DictReader(f))
for district, target in [("Mumbai City", (198367, 185022)),
                         ("Mumbai Suburban", (686155, 638024))]:
    group = [r for r in categories if r["district"] == district]
    for key, expected in zip(("boys", "girls"), target):
        assert sum(int(r[key]) for r in group) == expected
    assert all(r["reference_year"] == "2024-25" for r in group)
teachers = sum(int(r["teachers"]) for r in categories)
pupils = sum(sum(int(rows[i][k]) for k in ("grade11_boys", "grade11_girls",
                                         "grade12_boys", "grade12_girls"))
             for i in (0, 3))
assert teachers == 54723 and pupils == 278538
print("CONDITIONAL only: N=", pupils, "T_pool=", teachers, "N/T_pool=", pupils / teachers)
