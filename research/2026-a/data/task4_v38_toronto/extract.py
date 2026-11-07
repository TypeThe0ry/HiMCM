"""Extract actual 2024/25 board data; no municipal-model admission."""
import csv
from pathlib import Path
P=Path(__file__).resolve().parent
BOARDS=['Toronto DSB','Toronto Catholic DSB','Conseil scolaire Viamonde','CSC MonAvenir']
with (P/'financial_2024_25.csv').open(encoding='utf-8-sig',newline='') as f:
    reader=csv.DictReader(f)
    rows=list(reader)
selected=[]
for row in rows:
    area=row['Area:']; sub=row['SubCategory:']
    if ((area.startswith('Sch. 13') and ('Secondary' in sub or 'Grades 9 to 12' in sub)) or
        (area.startswith('App. H') and sub in ['Secondary','Spec Ed. Secondary'])):
        selected.append({k:row[k] for k in list(row)[:8]+BOARDS})
with (P/'four_boards_secondary_extract.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(selected[0]));w.writeheader();w.writerows(selected)
assert len({r['Cell Name:'] for r in selected})==len(selected)
lookup={r['Cell Name:']:r for r in rows if r['Cell Name:']}
ids=['SC13_00140S','SC13_00404S','SC13_00168S','SC13_00144S','SC13_00146S','SC13_00164S','AP0H_00667S','AP0H_00670S']
with (P/'key_cells.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(selected[0]));w.writeheader()
    for key in ids:w.writerow({k:lookup[key][k] for k in list(selected[0])})
print(f'Extracted {len(selected)} source rows and {len(ids)} key cells. No city PTR computed.')
