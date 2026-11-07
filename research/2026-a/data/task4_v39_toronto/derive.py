"""Conditional public day-school FTE diagnostic, never main-model admission."""
import csv, json, hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
raw=P.parent/'task4_v38_toronto/financial_2024_25.csv'
BOARDS=['Toronto DSB','Toronto Catholic DSB','Conseil scolaire Viamonde','CSC MonAvenir']
with raw.open(encoding='utf-8-sig',newline='') as f:
    rows=list(csv.DictReader(f))
cells={r['Cell Name:']:r for r in rows if r['Cell Name:']}
# Exclude aggregate other-pupil rows to avoid double counting their components.
student_ids=['SC13_00140S','SC13_00404S','SC13_00168S','SC13_00142S','SC13_00144S','SC13_00146S','SC13_00170S','SC13_00172S','SC13_00174S']
staff_ids=['AP0H_00667S','AP0H_00670S','AP0H_00344S']
output=[]
for b in BOARDS:
    s=sum(float(cells[k][b]) for k in student_ids)
    regular=float(cells[staff_ids[0]][b]); special=float(cells[staff_ids[1]][b]); ecpp=float(cells[staff_ids[2]][b])
    output.append(dict(board=b,october_secondary_student_fte=s,regular_classroom_instruction_fte=regular,special_classroom_instruction_fte=special,ecpp_instruction_fte=ecpp,non_ecpp_instruction_fte=regular+special-ecpp))
with (P/'board_fte.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(output[0]));w.writeheader();w.writerows(output)
se=sum(x['october_secondary_student_fte'] for x in output[:2]);sf=sum(x['october_secondary_student_fte'] for x in output[2:]);te=sum(x['non_ecpp_instruction_fte'] for x in output[:2]);tf=sum(x['non_ecpp_instruction_fte'] for x in output[2:])
result=dict(status='independent_conditional_diagnostic_not_main_model',year='2024-25',count_date='2024-10-31',raw_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),student_cells=student_ids,staff_cells=staff_ids,english_student_fte=se,french_board_student_fte_upper=sf,english_instruction_fte=te,french_board_instruction_fte_upper=tf,conditional_outer_ratio_lower=se/(te+tf),conditional_outer_ratio_upper=(se+sf)/te,assumptions=['Board jurisdiction used as school-service boundary, not student residence.','All regular secondary day-school pupil FTE and non-ECPP classroom instructional FTE correspond; adult day-school classification must be checked.','French municipal student and instructional shares unknown independently between zero and whole-board totals.','Private schools, provincial schools and separate school authorities excluded.','Not a 14–18-only population and not teacher headcount; not an achievement-quality measure.'])
(P/'conditional_diagnostic.json').write_text(json.dumps(result,indent=2)+'\n')
with (P/'source_cells.csv').open('w',newline='') as f:
    fields=list(rows[0])[:8]+BOARDS;w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for k in student_ids+staff_ids:w.writerow({a:cells[k][a] for a in fields})
assert se>0 and te>0 and sf>=0 and tf>=0
print(json.dumps(result,indent=2))
