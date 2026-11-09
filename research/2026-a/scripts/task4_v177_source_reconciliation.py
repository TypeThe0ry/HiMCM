"""Check a bounded source reconciliation without changing retained city inputs."""
from pathlib import Path
from html.parser import HTMLParser
from decimal import Decimal, localcontext
import csv
import hashlib
import json
import re
import subprocess

R = Path(__file__).resolve().parents[1]
P = R.parents[2] / 'HiMCM-Overleaf'
D = R / 'data/task4_v177_source_reconciliation'
O = R / 'results/task4_v177_source_reconciliation'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style', 'noscript'}:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in {'script', 'style', 'noscript'}:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def text(path):
    parser = VisibleText()
    parser.feed(path.read_text())
    return ' '.join(' '.join(parser.parts).split())


def main():
    O.mkdir(exist_ok=True)
    scientific = read(R / 'design/task4_user_v154_snapshot.json')['source_sha256']
    names = subprocess.check_output(['git', '-C', str(P), 'ls-files', '-z']).decode().split('\0')[:-1]
    # Keep this round's original protection scope stable when support files are
    # later added to Overleaf; do not silently recapture a different snapshot.
    protected_path = O / 'protected_files.json'
    if protected_path.exists():
        frozen = read(protected_path)
        assert frozen['science'] == scientific
        paper = frozen['paper']
        assert set(paper) <= set(names)
        assert all(sha(P / name) == expected for name, expected in paper.items())
    else:
        paper = {name: sha(P / name) for name in names}
    for name, expected in scientific.items():
        assert sha(R / name) == expected, name
    retrievals = read(D / 'retrievals.json')
    for item in retrievals:
        assert item['http_status'] == 200
        assert sha(D / item['file']) == item['sha256']
    population_text = text(D / 'zurich_population2024_original.html')
    matches = re.findall(r'Ende 2024 (?:waren|wohnten) ([\d ]+?) Personen', population_text)
    assert matches and set(x.replace(' ', '') for x in matches) == {'448664'}
    official_population = Decimal(matches[0].replace(' ', ''))
    notes = text(D / 'ireland_mip2026_notes_original.html')
    anchor = notes.index('Pupil-teacher ratio (4.3)')
    snippet = notes[anchor:anchor+2500]
    assert 'ISCED' in snippet and 'Ireland' in snippet
    assert re.search(r'Ireland.{0,180}ISCED 2', snippet), snippet[:800]
    assert 'title reflects the year of publication' in notes
    source = R / 'data/task4_v117_team_intake/city_indicators.csv'
    with source.open(encoding='utf-8-sig') as stream:
        row = next(x for x in csv.DictReader(stream) if x['city'] == 'Zurich')
    count = Decimal(row['homicide_numerator'])
    rate = Decimal(row['homicide_per_100k'])
    supplied_population = Decimal(row['population'])
    assert (count, rate, supplied_population) == (1, Decimal('.14'), 440935)
    with localcontext() as context:
        context.prec = 50
        factor = Decimal(100000)
        lower_rate, upper_rate = rate-Decimal('.005'), rate+Decimal('.005')
        denominator_lower, denominator_upper = count*factor/upper_rate, count*factor/lower_rate
        alternatives = []
        for name, population in [('retained_2025_population', supplied_population), ('municipal_release_end2024_population', official_population)]:
            alternatives.append(dict(population_source=name, population=str(population),
                arithmetic_count_per100000=str(count*factor/population),
                implied_count_at_point_rate=str(rate*population/factor),
                within_assumed_rounding_envelope=bool(denominator_lower <= population <= denominator_upper)))
        result = dict(version='V177', retained_count=str(count), retained_rate=str(rate),
                      retained_rate_year=row['homicide_per_100k_year'],
                      retained_population_year=row['population_year'],
                      retained_flag=row['homicide_per_100k_flag'],
                      official_population_observation='End2024 municipal population as reported by the archived release;not a crime-rate denominator certification',
                      implied_population_for_exact_point_rate=str(count*factor/rate),
                      assumed_nearest_two_decimal_rate_envelope=[str(lower_rate), str(upper_rate)],
                      rounding_assumption_status='Hypothetical closed outer envelope;actual supplied rounding convention unknown',
                      compatible_population_closed_envelope=[str(denominator_lower), str(denominator_upper)],
                      numerical_display='Decimal values are rounded to50 significant digits;exact endpoints are count*100000/0.145 and count*100000/0.135. No boundary classification relies on display rounding.',
                      alternatives=alternatives,
                      conclusion='Neither of these two specific population totals reconciles count1 with rate0.14, even under the declared rounding envelope. Original rate source, unit and denominator remain unestablished.',
                      inference_not_made=['corrected annual city homicide-victim rate','falsehood of every alternative city definition','one-sided victim-count bound from offence counts','replacement of any user value'],
                      primary_admissions=0, score_interval_width_change=0, manuscript_changed=False)
    scopes = dict(zurich_population=dict(value=448664, year=2024, geography='Stadt Zürich', reference='end of year as reported in the release', use='source reconciliation only'),
                  ireland_notes=dict(publication='20 October2026', geographic_scope='Ireland,not Dublin city', education_section='4.3', stage_warning='Ireland ISCED3 includesISCED2', year_warning='2026 is publication year;indicators use latest available individual vintages', no_matched_city_teaching_FTE_acquired=True, mixed_stage_teacher_superset_not_ruled_out_in_principle=True),
                  bounded_zurich_teacher_search=dict(searches=2, genuinely_new_original_response=False, outcome='Only previously checked routes and old SSP manual search snippets;stopped without treating search snippets as new evidence'),
                  bounded_dublin_teacher_search=dict(searches=2, new_original_response='CSO MIP2026 metadata only', no_numeric_admission=True))
    for name, expected in scientific.items():
        assert sha(R / name) == expected, name
    assert all(sha(P / name) == expected for name, expected in paper.items())
    for name, value in [('reconciliation.json', result), ('source_scope.json', scopes), ('protected_files.json', dict(science=scientific, paper=paper))]:
        (O / name).write_text(json.dumps(value, indent=2) + '\n')
    (O / 'source_bindings.json').write_text(json.dumps(dict(source_csv_sha256=sha(source), retrieval_manifest_sha256=sha(D/'retrievals.json'), script_sha256=sha(Path(__file__)), files={x['file']: x['sha256'] for x in retrievals}, source_scope_support='V144/V145 archived unit distinction remains frozen'), indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
