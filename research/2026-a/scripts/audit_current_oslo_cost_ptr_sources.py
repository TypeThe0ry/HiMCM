"""Read-only review of three retained Oslo points; no primary admission."""
from pathlib import Path
from html.parser import HTMLParser
import csv, hashlib, json, math
from datetime import datetime
from task4_audit_output import audit_parser, check_output, emit_report
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
P = G.parent / 'HiMCM-Overleaf'
O = R / 'results/current_oslo_cost_ptr_review/verification.json'

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def protected_inputs():
    core = read(R / 'design/task4_user_v203_snapshot.json')['source_sha256']
    current = read(R / 'results/current_paper_review/current_verification.json')
    extra = {}
    for name, group in current.items():
        if name.startswith('additional_') and name.endswith('_sha256'): extra.update(group)
    assert len(core) == 548 and len(extra) == 77
    for name, digest in {**core, **extra, **current['withdrawal_source_sha256']}.items():
        assert sha(R / name) == digest, name
    for name, digest in current['current_files_sha256'].items():
        assert sha(P / name) == sha(G / 'paper/current' / name) == digest, name
    assert sha(G / 'paper/current/main.pdf') == current['pdf_sha256']
    return {'core_bindings_checked': len(core), 'supplemental_bindings_checked': len(extra),
            'withdrawal_evidence_entries_checked': len(current['withdrawal_source_sha256']),
            'paper_dependencies_each_copy': len(current['current_files_sha256']),
            'current_PDF_unchanged': True}

def retained_points():
    with (R / 'data/task4_v117_team_intake/city_indicators.csv').open(encoding='utf-8-sig', newline='') as f:
        row = next(r for r in csv.DictReader(f) if r['city'] == 'Oslo')
    frame, low, high = revised_bounds()
    i = frame.city.tolist().index('Oslo')
    specs = [('cli', 'cost_living_index', 92.9, 2026, 100),
             ('pir', 'price_income_ratio', 9.8, 2026, 10),
             ('pupil_teacher_ratio', 'upper_secondary_ptr', 18.2, 2025, 15)]
    result = []
    with (R / 'results/current_point_withdrawal/cases.csv').open(newline='') as f:
        cases = list(csv.DictReader(f))
    for field, name, value, year, anchor in specs:
        assert float(row[field]) == value and int(row[field+'_year']) == year and row[field+'_flag'] == 'ok'
        utility = anchor / (anchor + value)
        j = NAMES.index(name)
        assert low[i, j] == high[i, j] and math.isclose(low[i, j], utility, rel_tol=0, abs_tol=1e-15)
        selected = [r for r in cases if r['withdrawn_city'] == 'Oslo' and r['indicator'] == name]
        assert len(selected) == 2 and {r['weight_reference'] for r in selected} == {'fixed', 'equal'}
        for r in selected:
            assert json.loads(r['after_choices']) == ['Zurich']
            assert json.loads(r['baseline_choices']) == (['Oslo'] if r['weight_reference'] == 'fixed' else ['Zurich'])
            assert math.isclose(float(r['retained_utility']), utility, rel_tol=0, abs_tol=1e-15)
        result.append({'field': field, 'value': value, 'year': year, 'submitted_flag': 'ok',
                       'utility_unchanged': utility, 'fixed_ignorance_stress_changes_choice': True,
                       'scope': 'Previously verified [0,1] withdrawal stress; not an error finding or probability.'})
    return result

class Rows(HTMLParser):
    """Independent plain table extraction, preserving the source column order."""
    def __init__(self):
        super().__init__(); self.rows = []; self.row = None; self.cell = None
    def handle_starttag(self, tag, attrs):
        if tag == 'tr': self.row = []
        elif tag in ('td', 'th') and self.row is not None: self.cell = []
    def handle_data(self, text):
        if self.cell is not None: self.cell.append(text)
    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            self.row.append(' '.join(''.join(self.cell).split())); self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.rows.append(self.row); self.row = None; self.cell = None

def table_rows(path):
    parser = Rows(); parser.feed(path.read_text()); return parser.rows

class Text(HTMLParser):
    def __init__(self): super().__init__(); self.parts = []
    def handle_data(self, text): self.parts.append(text)

def plain_text(path):
    parser = Text(); parser.feed(path.read_text())
    return ' '.join(' '.join(parser.parts).split())

def receipts(directory):
    receipt = read(directory / ('retrieval.json' if (directory / 'retrieval.json').exists() else 'receipts.json'))
    requests = receipt['requests']
    for request in requests:
        path = directory / request['file']
        assert path.stat().st_size == request['bytes'] and sha(path) == request['sha256'], path
    return len(requests)

def pupil_teacher_source():
    directory = R / 'data/current_oslo_ptr_source'
    count = receipts(directory)
    assert count == 5
    for request in read(directory / 'receipts.json')['requests']:
        assert request['status'] == 200 and request['final_url'].startswith('https://')
        assert datetime.fromisoformat(request['retrieval_utc']).utcoffset() is not None
    query = read(directory / 'ssb_12609_query.json')
    selection = {item['code']: item['selection'] for item in query['query']}
    assert selection == {
        'KOKfylkesregion0000': {'filter': 'item', 'values': ['0300']},
        'ContentsCode': {'filter': 'item', 'values': ['KOSelevperlarsv0000']},
        'Tid': {'filter': 'item', 'values': ['2024', '2025']}}
    assert query['response']['format'] == 'json-stat2'
    data = read(directory / 'ssb_12609_response.json')
    assert data['id'] == ['KOKfylkesregion0000', 'ContentsCode', 'Tid'] and data['size'] == [1, 1, 2]
    assert data['dimension']['KOKfylkesregion0000']['category']['index'] == {'0300': 0}
    metric = data['dimension']['ContentsCode']
    assert metric['category']['index'] == {'KOSelevperlarsv0000': 0}
    assert metric['extension']['refperiod']['KOSelevperlarsv0000'] == '31.12'
    times = data['dimension']['Tid']['category']['index']
    values = {year: data['value'][index] for year, index in times.items()}
    assert values == {'2024': 10.9, '2025': 12.5} and values['2025'] != 18.2
    # Check the scope warning at its historical source; do not assert continuity.
    plain = plain_text(directory / 'ssb_06942_definitions.html')
    assert 'Elever per lærerårsverk, fylkeskommunale skoler' in plain
    assert 'studenter i fagskoleutdanning i fylkeskommunale skoler' in plain
    assert 'avtalte årsverk eksklusive lange fravær' in plain
    assert 'etter skolefylke, pr. 1.10.' in plain
    assessment = read(directory / 'scope.json')['assessment']
    assert assessment['value_match'] is False and assessment['input_lineage_established'] is False
    assert assessment['metadata_full_match'] is False
    return {'raw_receipts_checked': count, 'SSB_table': '12609', 'region': '0300',
            'metric': 'KOSelevperlarsv0000', 'values': values,
            'matches_original18_2': False, 'input_lineage_established': False,
            'historical_definition_continuity_verified': False,
            'scope': 'Current table values and legacy coverage warning independently located; no replacement, exact current methodology continuity or input error established.'}

def cost_sources():
    directory = R / 'data/current_oslo_cost_source'
    count = receipts(directory)
    assert count == 8
    for request in read(directory / 'retrieval.json')['requests']:
        if request['file'].startswith('numbeo_'):
            assert request['status'] == 200 and request['final_url'] == request['url']
            assert datetime.fromisoformat(request['retrieval_utc']).utcoffset() is not None
        else:
            assert request['status'] is None and request['final_url'] is None and request['retrieval_utc'] is None
            assert request['archive_access_date'] == '2026-11-07'
    values = {}
    for kind, header, title, expected in [
        ('cost-of-living', 'Cost of Living Index', 'Cost of Living Index', {'2026': 90.2, 'mid': 92.1, 'current': 93.0}),
        ('property-investment', 'Price To Income Ratio', 'Property Prices Index', {'2026': 11.6, 'mid': 11.0, 'current': 9.8})]:
        values[kind] = {}
        for edition, value in expected.items():
            name = f'{kind}_{edition}.html'; path = directory / name
            assert sha(path) == sha(R / 'data/city_matrix_25_audit/sources' / name)
            rows = table_rows(path)
            headers = [row for row in rows if 'City' in row and header in row]
            assert len(headers) == 1
            city_index = headers[0].index('City'); value_index = headers[0].index(header)
            matched = [row for row in rows if len(row) > value_index and row[city_index] == 'Oslo, Norway']
            assert len(matched) == 1
            observed = float(matched[0][value_index]); assert observed == value
            values[kind][edition] = observed
            source = plain_text(path)
            label = ('Current '+title) if edition == 'current' else (title+' by City 2026'+(' Mid-Year' if edition == 'mid' else ''))
            assert label in source, label
    assert 92.9 not in values['cost-of-living'].values()
    assert values['property-investment']['current'] == 9.8
    assert all(value != 9.8 for edition, value in values['property-investment'].items() if edition != 'current')
    definitions = plain_text(directory / 'numbeo_cost_indices_explained.html')
    assert 'New York City (NYC)' in definitions and '100%' in definitions
    assert 'Cost of Living Index (Excl. Rent)' in definitions and 'excludes housing costs like rent or mortgage payments' in definitions
    property_definition = plain_text(directory / 'numbeo_property_indicators_explained.html')
    assert '1.5 * the average net salary' in property_definition and 'median apartment size is 90 square meters' in property_definition
    scope = read(directory / 'scope.json')
    assert scope['csv_extraction_lineage']['status'] == 'not established'
    provenance = read(R / 'data/city_matrix_25_audit/provenance.json')
    assert provenance['access_date'] == '2026-11-07'
    return {'raw_receipts_checked': count, 'copied_archived_tables': 6,
            'new_definition_responses': 2, 'archived_Oslo_values': values,
            'CLI_exact_match_in_checked_editions': False,
            'PIR_exact_match_only_rolling_Current': True,
            'input_lineage_established': False, 'municipal_boundary_equivalence_verified': False,
            'annual_2026_match_either_input': False,
            'scope': 'Only Oslo rows are reviewed. Reusing historical archived publisher pages does not use the old 25-city model. Original response status/times unknown for six copies; Current is an archive snapshot, not a live or annual 2026 value.'}

def main():
    a = audit_parser(__doc__).parse_args(); check_output(a, O, G)
    protected = protected_inputs()
    points = retained_points()
    ptr = pupil_teacher_source(); cost = cost_sources()
    directories = [R / 'data/current_oslo_ptr_source', R / 'data/current_oslo_cost_source']
    sources = [p for d in directories for p in sorted(d.iterdir()) if p.is_file()]
    sources.extend([Path(__file__), R / 'scripts/task4_audit_output.py', R / 'data/city_matrix_25_audit/provenance.json'])
    report = {'status': 'pass scoped source review', **protected,
              'retained_points': points, 'pupil_teacher_source': ptr, 'cost_sources': cost,
              'original_extraction_lineages_established': 0, 'primary_admissions': 0,
              'actual_primary_width_reduction': 0, 'changes_manuscript': False,
              'source_sha256': {str(p.relative_to(R)): sha(p) for p in sources},
              'scope': 'Three influential original points retained. Source differences do not prove input error. No policy, weights, intervals, CSV or paper change; no agency contact or full point-matrix certification.'}
    emit_report(report, a, O, G)

if __name__ == '__main__': main()
