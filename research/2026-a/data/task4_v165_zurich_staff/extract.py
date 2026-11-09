"""Decode the published SSP chart, keeping its provider and geography scope."""
from pathlib import Path
from html.parser import HTMLParser
import csv, hashlib, json

D = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, value):
        self.parts.append(value)


def plain(s):
    parser = Text()
    parser.feed(s)
    return ' '.join(' '.join(parser.parts).split())


def main():
    retrieval = json.loads((D / 'retrieval.json').read_text())
    hashes = {}
    for r in retrieval:
        p = D / r['file']
        assert r['status'] == 200 and p.stat().st_size == r['bytes']
        assert sha(p) == r['sha256'], p
        hashes[r['file']] = r['sha256']
    page = (D / 'staff_page_original.html').read_text()
    assert 'hundert Stellenprozenten' in page
    snippet = (D / 'chart_snippet_original.html').read_text()
    module = (D / 'chart_module_original.js').read_text()
    general = (D / 'chart_general_original.js').read_text()
    assert 'singlepageapplicatio_895902676.zhweb-spa-snippet.zhweb-cache.html' in page
    assert 'https://api.observablehq.com/d/2ebdda3eb4cd0353.js?v=4' in snippet
    assert '/@bildungsplanungzh/general.js?v=4&resolutions=2ebdda3eb4cd0353@1488' in module
    endpoint = 'p_entwicklung_der_anzahl_vollzeiteinheiten_an_mittelschulen_und_berufsfachschulen'
    assert endpoint in module
    assert 'https://www.bista.zh.ch/basicapi/' in general and 'this.route = "zhweb/"' in general
    data = json.loads((D / 'staff_data_original.json').read_text())
    rows, meta = data['data'], data['meta']
    assert len(rows) == 20
    assert all(set(r) == {'Schuljahr', 'Schultyp', 'Vollzeiteinheiten'} for r in rows)
    assert {r['Schuljahr'] for r in rows} == {f'{y}/{str(y+1)[-2:]}' for y in range(2016, 2026)}
    assert {r['Schultyp'] for r in rows} == {'Mittelschule', 'Berufsbildung'}
    assert len({(r['Schuljahr'], r['Schultyp']) for r in rows}) == 20
    assert all(r['Vollzeiteinheiten'] > 0 for r in rows)
    selected = {r['Schuljahr']: r['Vollzeiteinheiten'] for r in rows if r['Schultyp'] == 'Mittelschule'}
    assert selected['2024/25'] == 1759.942307910003
    assert selected['2025/26'] == 1774.584821416001
    assert 'öffentlich finanzierten' in meta['title'] and 'öffentlich finanzierten' in meta['description']
    assert '15.9.' in meta['description']
    assert all(x in meta['description'] for x in ['FMS', 'HMS', 'IMS'])
    survey = plain((D / 'survey_page_original.html').read_text())
    assert all(x in survey for x in ['Vollerhebung', 'Schulen (öffentliche und private)', '15. September'])
    assert 'Schulen mit einem Standort im Kanton Zürich' in survey
    assert 'im Kanton' in meta['readingExampleContent']
    result = {
        'version': 'V165',
        'source_sha256': hashes,
        'publisher': 'Bildungsplanung Kanton Zürich',
        'survey': 'SSP census; public and private schools; school location; 15 September',
        'published_chart': 'Teaching workload in publicly financed Mittelschulen and Berufsfachschulen in the canton',
        'unit': 'Vollzeiteinheiten; one unit is 100 employment percentage points',
        'data_columns': list(rows[0]),
        'rows': len(rows),
        'years': sorted(selected),
        'selected_cantonal_publicly_financed_Mittelschule_VZE': {y: selected[y] for y in ['2024/25', '2025/26']},
        'reference_day': '15 September of the school year; school year is not calendar year',
        'provider_scope': 'Publicly financed; does not establish coverage of all private schools',
        'stage_scope': 'Mittelschule includes FMS, HMS, IMS; data lack a separate Sekundarstufe II selector',
        'geography_scope': 'Canton; data have no municipality or school selector',
        'api_statusDate': meta['statusDate'],
        'api_statusDate_interpretation': 'Response metadata timestamp; not used as observation year or as a verified release date',
        'admission': 'Rejected for city all-provider upper-secondary PTR and its guaranteed denominator upper bound',
        'reason': 'A census collection frame does not expand the published chart subset; no demonstrated containment of all target city teaching FTE',
        'primary_data_admissions': 0,
        'primary_utility_interval_change': 0,
    }
    (D / 'scope_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    with (D / 'observations.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    print('PASS: six-source chart chain, 20 published rows, no city PTR admission')


if __name__ == '__main__':
    main()
