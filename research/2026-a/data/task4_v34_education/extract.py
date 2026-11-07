"""Extract Delhi higher-secondary counts from official UDISE+ 2024-25 PDF."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parent
for item in json.loads((ROOT/'manifest.json').read_text()):
    raw=(ROOT/item['file']).read_bytes()
    assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
text=subprocess.check_output(['pdftotext','-layout',str(ROOT/'udise_2024_25.pdf'),'-'],text=True)
(ROOT/'udise_2024_25.txt').write_text(text)
pages=text.split('\f')
def row(page,heading,n):
    assert heading in pages[page-1]
    line=next(x for x in pages[page-1].splitlines() if re.match(r'^\s*Delhi\s',x))
    vals=[int(v) for v in re.findall(r'\b\d+\b',line)]
    assert len(vals)==n,(page,line)
    return vals
teachers=row(58,'Table 4.7:',10)
pupils=row(85,'Table 5.1:',7)
ptr=row(63,'Table 4.12:',4)
assert sum(teachers[1:])==teachers[0]
assert pupils[2]+pupils[3]==pupils[4]
assert pupils[1]+pupils[4]+pupils[5]+pupils[6]==pupils[0]
assert (teachers[-2],teachers[-1],pupils[-1],ptr[-1])==(3420,26766,603437,20)
participating=teachers[-1]+teachers[-2];ratio=pupils[-1]/participating
assert round(ratio)==ptr[-1]
a=15
r=dict(city='Delhi',year='2024/25',geography='Delhi NCT; not just New Delhi and not wider NCR',stage='Higher Secondary grades11-12; all management in UDISE+',students=pupils[-1],dedicated_high_school_teachers=teachers[-1],shared_secondary_high_school_teachers=teachers[-2],participating_teacher_headcount=participating,ptr=ratio,published_rounded_ptr=ptr[-1],utility_headcount=a/(a+ratio),allocation_utility_lower=a/(a+pupils[-1]/teachers[-1]),allocation_utility_upper=a/(a+ratio),teacher_row=teachers,enrollment_row=pupils,ptr_row=ptr,source_pages_one_based=[58,63,85,188],main_admitted=False,scope='Administrative school count, not a census of student residence; teacher headcount includes teachers teaching both grades9-10 and11-12. Optional shared-allocation interval is not published FTE or a sampling confidence interval.')
(ROOT/'observation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
