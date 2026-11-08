"""Trace the unchanged historical-case claims to frozen observation records."""
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CITIES = ['Phoenix', 'New York', 'Mumbai', 'Delhi']


def rows(path):
    return list(csv.DictReader((ROOT/path).open()))


def main():
    core = 'data/task4_v5_core/observations.csv'
    air = 'data/task4_v5_air/observations.csv'
    utility = 'results/task4_v117_city_revision/utility_bounds.csv'
    scores = 'results/task4_v125_method_country/country_score_comparison.csv'
    selected = []
    frozen = {(r['city'], r['indicator']): r for r in rows(utility) if r['scenario'] == 'v117'}
    for source, indicators, cities in [(core, ['cost_living_index', 'price_income_ratio'], CITIES),
                                      (air, ['pm25'], ['Mumbai', 'Delhi'])]:
        for record in rows(source):
            if record['city'] not in cities or record['indicator'] not in indicators:
                continue
            anchor = {'cost_living_index': 100, 'price_income_ratio': 10, 'pm25': 15}[record['indicator']]
            u = anchor/(anchor+float(record['value']))
            bounds = frozen[(record['city'], record['indicator'])]
            assert abs(u-float(bounds['lower'])) < 1e-14
            assert abs(u-float(bounds['upper'])) < 1e-14
            selected.append(dict(record, frozen_observation_file=source, utility=u,
                                 transformation=f'{anchor}/({anchor}+x)'))
    assert len(selected) == 10
    payload = dict(
        scope='Separate frozen legacy25 V117 case studies, never V124 user16 inputs',
        purpose='Trace the published affordability and Mumbai/Delhi air-quality contrasts to their actual frozen provider records',
        observations=selected,
        score_comparison=rows(scores),
        source_sha256={p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
                       for p in [core, air, utility, scores, 'scripts/task4_v122_method_country.py']},
        limits='Numbeo 2025 named-city crowdsourced aggregates have no independently harmonized administrative boundaries; WHO air values are 2021 monitoring averages, two Mumbai and one Delhi stations, with unknown temporal coverage. These descriptive contrasts do not establish teenage exposure or a national causal effect.',
        new_observations_admitted=0, original_files_modified=False,
    )
    (HERE/'source_index.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
    print('Traced 10 unchanged historical-case claim inputs; original values and intervals preserved.')


if __name__ == '__main__':
    main()
