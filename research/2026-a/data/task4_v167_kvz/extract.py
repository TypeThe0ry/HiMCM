"""Keep an organizational annual-average FTE ceiling distinct from teaching FTE."""
from pathlib import Path
import hashlib, json, re, subprocess
D = Path(__file__).resolve().parent


def main():
    receipt = json.loads((D/'retrieval.json').read_text())
    assert len(receipt)==1
    row = receipt[0]; pdf = D/row['file']
    assert row['status']==200 and pdf.stat().st_size==row['bytes']
    assert hashlib.sha256(pdf.read_bytes()).hexdigest()==row['sha256']
    pages = subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True).split('\f')
    assert len(pages)-1==52
    finance, note = pages[32], pages[35]
    assert re.search(r'Erfolgsrechnung\s*\(\s*in CHF\s*\)',finance)
    assert '31.12.2024' in finance and '31.12.2023' in finance
    assert re.search(r'Personalaufwand Lehrende.*28.462.596.*28.193.081',finance)
    assert 'A2 Anzahl Mitarbeitende' in note
    assert 'Vollzeitstellen im Jahresdurchschnitt' in note
    assert '(und im Vorjahr) unter 250' in note
    assert 'private Berufsschule' in note
    report = dict(status='pass_nonadmission_scope_audit',admitted_cells=0,
        raw_sources_sha256={row['file']:row['sha256']},pdf_pages=52,
        provider='Wirtschaftsschule KV Zürich',report_label='Schuljahr2024/25',
        financial_reference_year=2024,comparison_year=2023,
        organizational_FTE_disclosure=dict(pdf_page=36,printed_page=36,section='A2 Anzahl Mitarbeitende',
            quantity='annual-average full-time positions',strict_upper=250,exact_value_recovered=False,
            current_and_previous_reporting_year=True,teaching_only=False),
        teacher_payroll=dict(pdf_page=33,printed_page=33,unit='CHF',reported_expense_2024=-28462596,reported_expense_2023=-28193081,
            actual_teaching_FTE_recovered=False),
        institution_type='Private vocational school per A1; this does not imply a lack of public funding',
        decision='Organizational annual-average positions below250 are not a teacher FTE point, a teaching-only split, a September census count or a city-all-provider ceiling. Payroll CHF cannot identify FTE without a justified workload mapping.',
        no_PTR_or_utility_computed=True,no_salary_to_FTE_conversion=True)
    (D/'scope_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASS:52 pages; organizational annual-average ceiling and CHF units preserved;0 admission')


if __name__=='__main__':main()
