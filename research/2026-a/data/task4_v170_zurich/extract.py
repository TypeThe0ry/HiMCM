"""Reproduce three bounded Zurich source-scope checks; propose no city bound."""
from pathlib import Path
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def workbook_cells(path):
    ns = {'x':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(path) as z:
        strings = [''.join(n.itertext()) for n in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        rels = {n.attrib['Id']: n.attrib['Target'] for n in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        out = {}
        for sheet in ET.fromstring(z.read('xl/workbook.xml')).find('x:sheets',ns):
            rid=sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            target=rels[rid]
            target=target.lstrip('/') if target.startswith('/') else 'xl/'+target
            cells={}
            for cell in ET.fromstring(z.read(target)).findall('.//x:sheetData/x:row/x:c',ns):
                value=cell.find('x:v',ns)
                if value is None: continue
                cells[cell.attrib['r']]=strings[int(value.text)] if cell.attrib.get('t')=='s' else value.text
            out[sheet.attrib['name']]=cells
        return out


def main():
    receipt=json.loads((HERE/'retrieval.json').read_text())
    for row in receipt:
        assert row['status']==200
        assert sha(HERE/row['file'])==row['sha256']
        assert len((HERE/row['file']).read_bytes())==row['bytes']
    module=(HERE/'official_staff_all_types_module_original.js').read_text()
    endpoint='p_entwicklung_der_anzahl_vollzeiteinheiten_nach_personalkategorie_und_schultyp'
    assert endpoint in module
    d=json.loads((HERE/'official_staff_all_types_data_original.json').read_text())
    assert 'öffentlich finanzierten Schulen' in d['meta']['title']
    assert 'öffentlich finanzierten Schulen' in d['meta']['description']
    assert all(set(r)=={'Schuljahr','Personalkategorie','Schultyp','Vollzeiteinheiten'} for r in d['data'])
    definition=(HERE/'bfs_FTE_definition_2026_original.html').read_text()
    assert 'anhand eines Modells geschätzt' in definition and 'AHV-Lohndaten' in definition
    w=workbook_cells(HERE/'bfs_staff_2024_25_original.xlsx')
    assert w['T10']['A6']=='Öffentliche Schulen' and w['T10']['A10']=='Privatschulen'
    assert 'VZÄ' in w['T10']['C3'] and '2024/25' in w['T10']['C3']
    assert 'Personen' in w['T5']['C3'] and 'Schulleitungspersonal' in w['T11']['C3']
    assert 'öffentliche Schulen' in w['T8']['B3']
    requested={'T10':{'F7':8301.1,'G7':10547.7,'J7':86866.4,'F11':695.2,
                     'G11':1767.5,'I11':3453.2,'J11':10242.2},
               'T8':{'E7':938.3,'F7':1454.3,'H7':13797.7}}
    for sheet,values in requested.items():
        for cell,expected in values.items(): assert abs(float(w[sheet][cell])-expected)<1e-8
    assert w['T8']['A7']=='Zürich'
    assert 'Nicht auf Stufen aufteilbare' in w['T10']['I5']
    footnotes={s:{k:v for k,v in w[s].items() if k in refs} for s,refs in {
        'T1':['A34','A36','A37','A39'],
        'T8':['A33','A35','A36','A38'],
        'T10':['A14','A16','A17','A19']}.items()}
    with zipfile.ZipFile(HERE/'bfs_staff_2024_25_original.xlsx') as z:
        props=ET.fromstring(z.read('docProps/core.xml'))
        dateprops={n.tag.rsplit('}',1)[-1]:n.text for n in props
                   if n.tag.rsplit('}',1)[-1] in ['created','modified','lastPrinted']}
        ns={'x':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        styles=ET.fromstring(z.read('xl/styles.xml'))
        formats={int(n.get('numFmtId')):n.get('formatCode') for n in styles.find('x:numFmts',ns)}
        xfs=list(styles.find('x:cellXfs',ns))
        t10xml=ET.fromstring(z.read('xl/worksheets/sheet11.xml'))
        display_formats={c.get('r'):formats.get(int(xfs[int(c.get('s','0'))].get('numFmtId')),'builtin')
             for c in t10xml.findall('.//x:c',ns) if c.get('r') in ['I7','J7','I11','J11']}
    assert abs(sum(float(w['T10'][c+'11']) for c in 'CDEFGHI')-float(w['T10']['J11']))<1e-8
    missing_symbols={s:{k:v for k,v in w[s].items()
                       if v.strip().startswith(('…','...')) or v.strip().casefold() in ['ss','nc']}
                     for s in ['T1','T8','T10']}
    assert not any(missing_symbols.values())
    assert abs((sum(float(w['T8'][c+'7']) for c in 'BCDEFG')-float(w['T8']['H7']))-.1)<1e-8
    report=dict(status='pass_source_scope_check; no city-bound admission', primary='V154 unchanged',
        inspected_new_routes=3, admitted_cells=0, PTR_or_utility_computed=False,
        source_sha256={r['file']:r['sha256'] for r in receipt}, extractor_sha256=sha(Path(__file__)),
        routes=[
            dict(id='new_all_school_types_chart',
                module_url=receipt[0]['url'], data_url=receipt[1]['url'],
                title=d['meta']['title'], statusDate=d['meta']['statusDate'],
                columns=[v['columnKey'] for v in d['meta']['columns']],
                data_rows=len(d['data']), years=sorted({r['Schuljahr'] for r in d['data']}),
                geography='Kanton Zürich aggregate, no school/city selector',
                provider_scope='Explicitly publicly financed schools; not all private providers',
                decision='Not usable as all-provider city teacher total or covering upper bound. Different endpoint from V165, same material provider exclusion.'),
            dict(id='STATENT_covering_workforce_idea',
                source_url='https://statistik.admin.ch/en/asset/36683267', publication_date='2026-07-03',
                finding='Official definition says STATENT FTE are model estimates based mainly on AHV wages and supplemented by other surveys.',
                decision='No employment estimate treated as a guaranteed one-sided teacher-FTE envelope. No numerical STATENT teacher bound manufactured.'),
            dict(id='new_full_BFS_staff_workbook',
                release_url='https://statistik.admin.ch/de/news/2026-0085',
                source_url='https://dam-api.bfs.admin.ch/hub/api/dam/assets/36478952/master',
                release_date='2026-04-14', represented_year='2024/25', workbook_status='2026-03-30',
                quantitative_finding='T10 publishes teacher FTE separately for public and private schools, at national rather than canton/city geography. This is actual published private-school FTE information, not merely a survey frame.',
                cell_values=requested,
                units=dict(T10='teacher VZÄ, not headcounts or school leadership',T8='public-school teacher VZÄ by canton'),
                relevant_labels=dict(public_row='T10 A6; totals row7',private_row='T10 A10; totals row11',
                    general_upper='T10 F5',vocational_upper='T10 G5',unallocated_stage='T10 I5',all_stages='T10 J5'),
                raw_XML_values={sheet:{cell:w[sheet][cell] for cell in values} for sheet,values in requested.items()},
                retained_sheet_titles={'T1':w['T1']['B3'],'T8':w['T8']['B3'],'T10':w['T10']['C3']},
                retained_sheet_footnotes_and_status=footnotes,
                workbook_core_date_properties=dateprops,
                workbook_dates_interpretation='Old workbook creation/printing dates are template metadata, not reference years; table headers2024/25 and status30March2026 retained separately.',
                numeric_scope_checks=dict(
                    private_stage_C11_through_I11_sum=float(sum(float(w['T10'][c+'11']) for c in 'CDEFGHI')),
                    private_J11_total=float(w['T10']['J11']),
                    private_unallocated_stage_I11_included_in_total=True,
                    public_unallocated_stage_I7=float(w['T10']['I7']),
                    public_canton_T8_H7_total=float(w['T8']['H7']),
                    public_canton_T8_B7_through_G7_sum=float(sum(float(w['T8'][c+'7']) for c in 'BCDEFG')),
                    public_total_and_displayed_component_sum_differ_by_0_1=True,
                    difference_explanation='Observed published-cell arithmetic; no hidden unrounded values reconstructed or specific rounding method certified.'),
                displayed_number_formats=display_formats,
                missing_symbols_in_inspected_sheets=missing_symbols,
                completeness_and_actuality='T10 labels published SSP teacher VZÄ by employment contract, not planned posts or school leaders. T1/T8/T10 supply no explicit missing-report, imputation or completeness certification in their footnotes. No missing symbol found in these sheets does not establish all actual target activity is covered, nor a one-sided error guarantee. Original underlying personnel records were not obtained.',
                matched_student_numerator_used=False,
                previous_V120_mixed_stage_T3_not_used=True,
                not_combined=dict(T5='private teacher persons, not FTE',T11='leadership FTE, not teaching',T12='additional special-needs staff, compulsory stage'),
                bound_status='Potential covering-denominator ingredient only; no city envelope asserted or admitted in this bounded check.',
                remaining_conditions=[
                    'Prove that the relevant actual city upper-secondary teaching activities are all contained in the published public/private teacher populations, including unspecified-stage activities and any programme exclusions.',
                    'Match the exact upper-stage student population and reference year/date; no new matched city student numerator was collected here.',
                    'Check publication completeness, any estimation/allocation conventions, and source precision before calling a total a guaranteed upper bound.',
                    'Private general-upper F11 alone is not a proved city private-upper cover: other private stages/mixed or unallocated activities cannot simply be omitted.'],
                decision='New quantitative private+public FTE lead retained for independent coverage review; do not construct a city PTR or utility from it without those checks.')],
        statement_limit='These three routes do not establish that no suitable source exists elsewhere. No old source, model result, user CSV, registry or manuscript was edited.')
    (HERE/'source_scope.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],routes=3,admitted_cells=0,
        source_scope_sha256=sha(HERE/'source_scope.json')),indent=2))


if __name__=='__main__':main()
