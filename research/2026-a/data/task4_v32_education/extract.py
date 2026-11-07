"""Extract Warsaw youth general upper-secondary denominator bounds from official PDF."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parent
pdf=ROOT/'warsaw_2024.pdf'
manifest=json.loads((ROOT/'manifest.json').read_text())
entry=next(item for item in manifest if item['file']==pdf.name)
raw=pdf.read_bytes()
assert len(raw)==entry['bytes'],'Raw PDF byte count differs from manifest'
assert hashlib.sha256(raw).hexdigest()==entry['sha256'],'Raw PDF hash differs from manifest'
text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],stderr=subprocess.DEVNULL).decode()
(ROOT/'warsaw_2024.txt').write_text(text)
table1=text.split('EDUCATION BY LEVEL a',1)[1].split('TABL. 2 (101)',1)[0]
teachers=table1.split('NAUCZYCIELE',1)[1].split('UCZNIOWIE I STUDENCI',1)[0]
line=next(x for x in teachers.splitlines() if 'licea ogólnokształcące' in x)
values=[int(x) for x in re.findall(r'\b\d+\b',line)]
assert values==[5176,5322,6079]
table12=text.split('TABL. 12 (111)',1)[1].split('TABL. 13 (112)',1)[0]
youth=table12.split('FOR YOUTH',1)[1].split('OF WHICH SPECIAL',1)[0]
adults=table12.split('FOR ADULTS',1)[1]
def pupils(section):
    line=next(x for x in section.splitlines() if 'Uczniowie' in x)
    return [int(x) for x in re.findall(r'\b\d+\b',line)]
youth_values=pupils(youth)
adult_values=pupils(adults)
total_values=pupils(table12.split('FOR YOUTH',1)[0])
assert youth_values==[63188,76586,87999]
assert adult_values==[5181,4929,5773]
assert total_values==[68369,81515,93772]
assert all(y+a==t for y,a,t in zip(youth_values,adult_values,total_values))
# One whole FTE allowance covers integer truncation or nearest rounding.
# No positive lower bound for youth teacher allocation is assumed.
teacher_upper=values[-1]+1
result=dict(city='Warsaw',school_year='2023/24',scope='General upper-secondary schools for youth, including special schools; excludes adult education and vocational/technical schools',youth_pupils=youth_values[-1],adult_pupils=adult_values[-1],all_general_secondary_pupils=total_values[-1],all_general_secondary_teacher_fte=values[-1],teacher_fte_upper_with_release_precision=teacher_upper,teacher_rounding_allowance=1,ptr_lower=youth_values[-1]/teacher_upper,utility_lower=0,utility_upper=15/(15+youth_values[-1]/teacher_upper),main_admitted=False,reason='Teacher FTE includes adult schools; use only an upper bound for youth teacher allocation. General upper-secondary scope, not all upper-secondary routes.',pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),printed_pages=[145,147,152],pdf_pages_one_based=[153,155,160])
(ROOT/'observation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
