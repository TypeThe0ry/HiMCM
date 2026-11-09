"""Independently check source scope and compare current V154 deterministic results."""
from pathlib import Path
from html.parser import HTMLParser
import csv, hashlib, json, re
import numpy as np
import pandas as pd
from task4_user_v154_revision import revised_bounds
from task4_user_city_indicators import evaluate
from task4_v5_model import NAMES, weights

R = Path(__file__).resolve().parents[1]
P = R.parents[2] / 'HiMCM-Overleaf'
O = R / 'results/task4_v165_staff_routes'


def read(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


class Attributes(HTMLParser):
    def __init__(self):
        super().__init__()
        self.attributes = []

    def handle_starttag(self, tag, attrs):
        self.attributes.append((tag, dict(attrs)))


def main():
    source_count = 0
    for folder in ['task4_v165_zurich_staff', 'task4_v165_dublin_routes']:
        d = R / 'data' / folder
        for row in read(d / 'retrieval.json'):
            assert row['status'] == 200 and sha(d / row['file']) == row['sha256']
            assert (d / row['file']).stat().st_size == row['bytes']
            source_count += 1
    d = R / 'data/task4_v165_zurich_staff'
    parser = Attributes()
    parser.feed((d / 'staff_page_original.html').read_text())
    snippet_url = next(a['data-snippet-url'] for _, a in parser.attributes
                       if '895902676' in a.get('data-snippet-url', ''))
    receipt = {r['file']: r for r in read(d / 'retrieval.json')}
    assert receipt['chart_snippet_original.html']['url'] == 'https://www.zh.ch' + snippet_url
    snippet = (d / 'chart_snippet_original.html').read_text()
    assert receipt['chart_module_original.js']['url'] in snippet
    module = (d / 'chart_module_original.js').read_text()
    route = re.search(r'function _uri\(\)\{return\(\s*"([^"]+)"', module)[1]
    general = (d / 'chart_general_original.js').read_text()
    api = re.search(r'this.url = "([^"]+)"', general)[1]
    path = re.search(r'this.route = "([^"]+)"', general)[1]
    assert receipt['staff_data_original.json']['url'] == api + path + route + '?refreshcache=false'
    raw = read(d / 'staff_data_original.json')
    with (d / 'observations.csv').open() as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == len(raw['data']) == 20
    for a, b in zip(rows, raw['data']):
        assert a['Schuljahr'] == b['Schuljahr'] and a['Schultyp'] == b['Schultyp']
        assert float(a['Vollzeiteinheiten']) == b['Vollzeiteinheiten']
    assert 'öffentlich finanzierten' in raw['meta']['description']
    assert 'im Kanton' in raw['meta']['readingExampleContent']
    assert set(raw['data'][0]) == {'Schuljahr', 'Schultyp', 'Vollzeiteinheiten'}
    assert 'Schulen (öffentliche und private)' in (d / 'survey_page_original.html').read_text()
    z = read(d / 'scope_audit.json')
    for y, value in z['selected_cantonal_publicly_financed_Mittelschule_VZE'].items():
        assert value == next(r['Vollzeiteinheiten'] for r in raw['data']
                             if r['Schuljahr'] == y and r['Schultyp'] == 'Mittelschule')
    assert z['primary_data_admissions'] == z['primary_utility_interval_change'] == 0
    d = R / 'data/task4_v165_dublin_routes'
    e = read(d / 'eurostat_dublin_education_original.json')
    assert dict(zip(e['id'], e['size'])) == {'freq': 1, 'indic_ur': 14, 'cities': 1, 'time': 36}
    assert e['dimension']['cities']['category']['label'] == {'IE001C': 'Dublin (greater city)'}
    assert not any(re.search(r'teacher|teaching|\bFTE\b|full.time.equivalent', s, re.I)
                   for s in e['dimension']['indic_ur']['category']['label'].values())
    c = read(d / 'cso_wmi07_teachers_original.json')
    assert [c['dimension'][k]['label'] for k in c['id']] == ['Statistic', 'Year', 'Sex', 'Country']
    labels = c['dimension'][c['id'][-1]]['category']['label']
    assert len(labels) == 41 and labels['IE'] == 'Ireland' and not any('Dublin' in s for s in labels.values())
    assert read(d / 'scope_audit.json')['admitted_cells'] == 0
    snapshot = read(R / 'design/task4_user_v154_snapshot.json')['source_sha256']
    for n, h in snapshot.items():
        assert sha(R / n) == h, n
    protected = read(O / 'protected_files.json')['manuscript']
    for n, h in protected.items():
        assert sha(P / n) == h, n
    frame, lo, hi = revised_bounds()
    before = pd.read_csv(R / 'results/task4_user_v154_revision/utility_bounds.csv')
    before = before[before.scenario == 'after_conditional']
    assert lo.shape == hi.shape == (16, 10)
    for i, city in enumerate(frame.city):
        for j, indicator in enumerate(NAMES):
            row = before[(before.city == city) & (before.indicator == indicator)].iloc[0]
            np.testing.assert_allclose([lo[i, j], hi[i, j]], [row.lower, row.upper], atol=2e-15, rtol=0)
    historical = pd.read_csv(R / 'results/task4_user_v154_revision/current_ranks.csv')
    comparisons = []
    for reference, w in [('fixed', weights(.1)), ('equal', np.ones(10) / 10)]:
        current = evaluate(frame.city.tolist(), lo, hi, w)
        old = historical[historical.weight_reference == reference].set_index('city').loc[current.city]
        for column in ['score_lower', 'score_upper', 'max_regret', 'decision_rank', 'best_rank', 'worst_rank']:
            np.testing.assert_allclose(current[column].to_numpy(), old[column].to_numpy(), atol=3e-13, rtol=0)
        assert current.possible_champion.tolist() == old.possible_champion.tolist()
        assert current.necessary_champion.tolist() == old.necessary_champion.tolist()
        comparisons.append(dict(weight_reference=reference,
                                before_mean_width=float((old.score_upper-old.score_lower).mean()),
                                after_mean_width=float((current.score_upper-current.score_lower).mean()),
                                mean_width_reduction=0,
                                conservative_recommendation=current.loc[current.decision_rank == 1, 'city'].tolist(),
                                possible_champions=int(current.possible_champion.sum()),
                                necessary_champions=int(current.necessary_champion.sum())))
    (O / 'comparison.json').write_text(json.dumps(comparisons, indent=2) + '\n')
    result = dict(status='pass', iteration='V165', new_original_responses=source_count,
                  protected_scientific_files=len(snapshot), protected_manuscript_files=len(protected),
                  utility_cells_compared=160, deterministic_city_weight_cases=32,
                  source_scope_independently_checked=True,
                  primary_data_admissions=0, primary_score_width_change=0,
                  model='V154 unchanged', paper='V164 unchanged',
                  no_MC_rerun=True, no_new_PDF=True, goal='active')
    (O / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
