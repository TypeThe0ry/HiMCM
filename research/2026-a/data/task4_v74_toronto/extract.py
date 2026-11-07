"""Audit school-local plans and reported staff entries; do not infer actual FTE."""
from pathlib import Path
import hashlib,json,re,subprocess
from decimal import Decimal
P=Path(__file__).resolve().parent

def page_text(name,page):
    return subprocess.check_output(['pdftotext','-f',str(page),'-l',str(page),'-layout',str(P/name),'-'],text=True)

def derive():
    for row in json.loads((P/'manifest.json').read_text()):
        raw=(P/row['file']).read_bytes()
        assert len(raw)==row['bytes']
        assert hashlib.sha256(raw).hexdigest()==row['sha256']
    staff=page_text('toronto_ouest_staff2024_25.pdf',1)
    assert '2024-2025' in staff
    block=staff.split('Personnel enseignant')[1].split('Aide-enseignants')[0]
    entries=[line for line in block.splitlines() if '@' in line]
    emails=[line.split()[-1].lower() for line in entries]
    assert len(entries)==len(set(emails))==28
    budget=page_text('viamonde_budget2024_25.pdf',25)
    assert 'Dotation du personnel secondaire' in budget and 'Budget 2024-2025' in budget
    block=budget.split('Grand Toronto')[1].split('Dufferin Peel')[0]
    rows=[]
    for line in block.splitlines():
        nums=re.findall(r'\d+,\d{2}',line)
        if not nums:continue
        assert len(nums)==7
        name=re.split(r'\d+,\d{2}',line)[0].strip()
        rows.append({'school':name,'planned_personnel_enseignant':str(Decimal(nums[2].replace(',','.')))})
    assert len(rows)==4
    assert [r['planned_personnel_enseignant'] for r in rows]==['13.83','18.83','17.00','7.83']
    elementary=page_text('viamonde_budget2024_25.pdf',17)
    assert 'Toronto Ouest 7-8' in elementary
    return {'main_admitted':False,'year':'2024–2025','school_staff_directory_entries':28,
            'school_staff_directory_is_fte':False,'school_staff_directory_has_grade_allocation':False,
            'budget_pdf_page':25,'budget_printed_page':'3-3','budget_actual_october_staffing':False,
            'school_planned_secondary_allocations':rows,
            'planned_secondary_allocation_sum':str(sum(Decimal(r['planned_personnel_enseignant']) for r in rows)),
            'toronto_ouest_grade7_8_separate_budget_enrolment':True,
            'admission_reason':'Budget allocations are plans; staff entries lack FTE/current-grade allocation and cannot establish actual October municipal teacher resources. Current Toronto education interval stays [0,1].'}

if __name__=='__main__':
    result=derive();(P/'summary.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))
