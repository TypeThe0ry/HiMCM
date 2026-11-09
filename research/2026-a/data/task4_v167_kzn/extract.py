"""Offline scope check of KZN 2024/25 originals; no pupil-teacher ratio inferred."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    receipt = json.loads((HERE / 'retrieval.json').read_text())
    assert len(receipt) == 2
    for row in receipt:
        assert row['status'] == 200
        path = HERE / row['file']
        assert len(path.read_bytes()) == row['bytes'] and sha(path) == row['sha256']
    pdf = HERE / 'kzn_annual_2024_2025_original.pdf'
    assert pdf.read_bytes().startswith(b'%PDF')
    pages = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-']).decode().split('\f')
    assert len(pages) - 1 == 39
    overview, pupils, personnel = pages[5], pages[36], pages[37]
    assert '301' in overview and 'Lehrpersonen' in overview and '2339' in overview
    assert 'Jahresbericht 2024/2025' in overview
    assert 'Per 15. September 2024' in pupils
    assert re.search(r'Untergymnasium\s+225\s+201\s+426', pupils)
    assert re.search(r'Gesamttotal\s+2339', pupils)
    assert re.search(r'Zwischentotal\s+225\s+201\s+368\s+313\s+247\s+296\s+1650', pupils)
    assert 'Personenanzahl' in personnel
    assert re.search(r'Lehrpersonen\s*\(\s*exklusiv acht Schulleitende\s*\)\s+284', personnel)
    assert re.search(r'Rektor\s+1', personnel)
    assert re.search(r'Prorektorinnen und Prorektoren\s+7', personnel)
    checked_terms = [r'Vollzeit\w*', r'\bVZE\b', r'\bFTE\b', r'Pensum', r'Pensen',
                     r'Stellenprozent\w*', r'Stellenplan\w*', r'100\s*(?:%|Prozent)',
                     r'Arbeitszeit\w*', r'Lehrauftrag\w*']
    fulltext = '\f'.join(pages)
    hits = {term: len(re.findall(term, fulltext, re.I)) for term in checked_terms}
    assert all(count == 0 for count in hits.values())
    archive = (HERE / 'kzn_news_archive_original.html').read_text()
    assert 'jahresbericht-2024-25' in archive and 'Jahresbericht 2024/25' in archive
    report = dict(
        status='pass_nonadmission_scope_audit', admitted_cells=0,
        source='Kantonsschule Zürich Nord annual report2024/2025 and official news archive',
        raw_sources_sha256={r['file']: r['sha256'] for r in receipt},
        retrieval_receipt_sha256=sha(HERE / 'retrieval.json'),
        extractor_sha256=sha(Path(__file__)),
        pdf_pages=39, layout='Some PDF pages contain two printed pages; locators distinguish these',
        evidence=[
            dict(item='overview_teachers', pdf_page=6, printed_page=11,
                 published_value=301, published_label='Lehrpersonen',
                 reference_period='annual report2024/2025; no precise teacher count date printed on this overview',
                 not_FTE=True),
            dict(item='personnel_teachers', pdf_page=38, printed_page=74,
                 published_value=284, published_unit='Personenanzahl',
                 published_exclusion='exklusiv acht Schulleitende',
                 leadership_headcounts=dict(rektor=1, prorektorinnen_und_prorektoren=7),
                 reference_date='No explicit separate date printed in the personnel table. Preceding statistics spread has15September2024, but not assigned to this table without further evidence.',
                 not_FTE=True),
            dict(item='pupils_same_table_and_date', pdf_page=37, printed_page=72,
                 reference_date='2024-09-15', total=2339,
                 undergymnasium=dict(first_year=225, second_year=201, total=426),
                 gymnasium_total_including_under=1650, fachmittelschule_total=689,
                 total_and_under_share_same_explicit_date=True,
                 overview_total_on_pdf6_also_2339=True),
            dict(item='classes', pdf_page=37, printed_page=73,
                 undergymnasium_classes=[8,8], all_classes_total=95),
            dict(item='official_archive', file='kzn_news_archive_original.html',
                 identifies='Jahresbericht2024/25 news entry',
                 linked_news_path='/schulkultur/kulturelle-veranstaltungen/news-detailansicht/jahresbericht-2024-25')],
        teacher_count_reconciliation=dict(
            overview_teacher_count=301, personnel_teacher_count_excluding_eight_leaders=284,
            personnel_plus_eight_leaders=292, difference_from_overview_after_adding_eight=9,
            reconciled=False,
            reason='No explicit footnote or definition explaining301 versus284+8 was recovered in the overview/personnel/statistics tables or surrounding text. Do not attribute the difference to staff turnover, dates, instrumental teachers, visitors or contract fractions without source evidence.'),
        FTE_recovery=dict(actual_teaching_FTE_VZE_recovered=False,
            upper_stage_teaching_FTE_allocation_recovered=False,
            explicit_fulltime_or_100percent_teacher_contracts_recovered=False,
            full_extract_search_term_hit_counts=hits,
            scope='No matching terms in searchable PDF text and no FTE unit in the inspected statistical/personnel tables. This is a bounded recovery finding, not a claim about undisclosed school records.'),
        decision='No admissible teaching FTE or upper-stage allocation. Headcounts are not FTE; total teaching FTE, even if later found, cannot be assumed a lower bound for upper-only teaching when the school includes Untergymnasium.',
        city_coverage='One mixed-stage school, not all Zurich providers; no city ratio or utility derived',
        no_teacher_load_assumption=True, no_PTR_or_utility_computed=True,
        no_other_school_route_expanded=True,
        model_or_manuscript_written=False)
    (HERE / 'scope_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], admitted_cells=0,
        source_pdf_sha256=sha(pdf), audit_sha256=sha(HERE/'scope_audit.json')), indent=2))


if __name__ == '__main__':
    main()
