"""Three city-scoped transport subsets; original attachment populations retained.

Requires Poppler pdftotext. Stockholm and Dublin figures are manual readings,
recorded separately; the script verifies source hashes and recomputes utilities.
It does not claim to machine-extract text absent from the source PDF text layer.
"""
import csv
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ATTACHMENT = HERE.parent / 'task4_v117_team_intake/city_indicators.csv'
PDF_HASHES = {
    'stockholm_vallingby_2025.pdf': 'c81adf01ea0d76c48cfc8cc62fe4899793c41a7f886c9d1a490a8da636691057',
    'paris_apur_atlas.pdf': '877ca2d1926f90665c5d013f3053b8a2e1712270fb43f782ab0f3bc1c39cbf3e',
    'dublin_public_transport_2023.pdf': 'be0f2fdf3c77b3714ca0294af19da00e24f07be8562ceec71dfe01a97275d4fe',
}
SOURCE_URLS = {
    'Stockholm': 'https://meetingspublic.stockholm.se/welcome-sv/namnder-styrelser/hasselby-vallingby-stadsdelsnamnd/mote-2025-12-18/agenda/6-lagesbild-2025-samverkansoverenskommelse-mellan-hasselby-vallingby-sdf-och-lokalpolisomrade-vallingbypdf?downloadMode=open',
    'Paris': 'https://www.apur.org/sites/default/files/atlas_activites_paris_immobilier.pdf',
    'Dublin': 'https://www.dublincity.ie/sites/default/files/2024-04/06-dublin-city-centre-transport-plan-public-transport-technical-note.pdf',
}


def pdf_text(filename, first, last):
    return subprocess.check_output(
        ['pdftotext', '-f', str(first), '-l', str(last), '-layout', str(HERE / filename), '-'],
        text=True,
    )


def extract():
    assert hashlib.sha256(ATTACHMENT.read_bytes()).hexdigest() == '430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
    for filename, digest in PDF_HASHES.items():
        assert hashlib.sha256((HERE / filename).read_bytes()).hexdigest() == digest, filename
    population_rows = {r['city']: r for r in csv.DictReader(ATTACHMENT.open(encoding='utf-8-sig'))}
    manual = json.loads((HERE / 'manual_figure_readings.json').read_text())
    stockholm = manual['Stockholm']
    assert stockholm['pdf_page'] == 11
    assert stockholm['district_counts'] == {'Bromma': 8, 'Hässelby-Vällingby': 5}
    geo = pdf_text('stockholm_vallingby_2025.pdf', 10, 10)
    assert 'Bromma och Hässelby-Vällingby inom' in geo and 'Stockholms stad' in geo
    paris = pdf_text('paris_apur_atlas.pdf', 37, 37)
    assert '244 sta-' in paris and 'tions de métro à Paris intra-muros' in paris
    assert '58 sont des stations de correspondance' in paris and '332 points' in paris
    assert 'Sources : RATP 2021, Apur - BD Équipement 2022' in paris
    assert 'MARS 2022' in pdf_text('paris_apur_atlas.pdf', 1, 1)
    dublin = manual['Dublin']
    assert dublin['pdf_page'] == 23 and dublin['figure'] == '3-7'
    names = dublin['red_line_labels'] + dublin['green_line_labels']
    assert len(names) == len(set(names)) == 19
    dub = pdf_text('dublin_public_transport_2023.pdf', 22, 23)
    assert 'Figure 3-7: Existing Luas Infrastructure within Study Area' in dub
    assert 'The existing Luas network' in dub
    scopes = {
        'Stockholm': '2025 city/police report PDF page11, printed10:13 metro stations, explicitly8 in Bromma plus5 in Hässelby-Vällingby. Previous page states both districts are within Stockholm municipality; the police area also covers Ekerö, but none of the13 is assigned to Ekerö. Stations, not directional platforms. Subset of city metro inventory, not all modes.',
        'Paris': 'March2022 Apur inventory PDF page37:244 metro stations inside Paris intra-muros, including58 interchange stations, distinguished from332 line stop-points. Only244 used, no addition of RER stations with unassessed interchange overlap. Underlying sources explicitly RATP2021 and Apur BDÉquipement2022. Historical inventory with unchanged2023 attachment population.',
        'Dublin': '2023 City Centre Transport Plan technical note, issued2024, PDF page23/printed20 Figure3-7 Existing Luas Infrastructure within Study Area. Manual inventory retains19 distinctly named tram stops plotted inside the red city-centre study boundary; full labels and exclusions in manual_figure_readings.json and source-page PNG. The city-centre study is inside the city proper, not the wider Luas region. Other plotted stops are omitted rather than assigned by assumed regional coverage.',
    }
    observations = []
    for city, count, year, pdf, page in [
        ('Stockholm', sum(stockholm['district_counts'].values()), 2025, 'stockholm_vallingby_2025.pdf', 11),
        ('Paris', 244, 2021, 'paris_apur_atlas.pdf', 37),
        ('Dublin', len(names), 2023, 'dublin_public_transport_2023.pdf', 23),
    ]:
        r = population_rows[city]
        pop = int(r['population'])
        assert pop == {'Stockholm': 999200, 'Paris': 2103778, 'Dublin': 592713}[city]
        density = count * 100000 / pop
        observations.append(dict(
            city=city, indicator='public_transport_density',
            utility_before=[0, 1], utility_after=[density / (50 + density), 1],
            raw_count=count, population=pop, population_year=int(r['population_year']),
            population_source='Unchanged authoritative attachment; not externally rechecked',
            sourceyear=year, reportyear={'Stockholm': 2025, 'Paris': 2022, 'Dublin': 2024}[city],
            density_per_100000_lower=density, utility_anchor=50, lower_bound_only=True,
            source_locator=SOURCE_URLS[city], source_file=pdf, source_pdf_page=page,
            access_date='2026-11-08', scope=scopes[city],
            historical_inventory_proxy=city in {'Paris', 'Dublin'},
            extraction='Manual figure reading with archived source-page PNG' if city != 'Paris' else 'pdftotext assertions on original PDF',
            source_hashes={f'data/task4_v121_transport/{pdf}': PDF_HASHES[pdf]},
            limitations='Facility-supply subset only. Upper utility remains1 for uncounted modes/operators and incomplete inventory. Mixed vintage does not identify current complete supply, travel access or adolescent usage. Historical inventory can be withdrawn to[0,1].',
        ))
    return observations


if __name__ == '__main__':
    observations = extract()
    (HERE / 'observations.json').write_text(json.dumps(observations, ensure_ascii=False, indent=2) + '\n')
    files = [p for p in HERE.iterdir() if p.is_file() and p.name not in {'manifest.json', 'stockholm_yearbook_2026.pdf'}]
    manifest = {
        'access_date': '2026-11-08',
        'input_sha256': hashlib.sha256(ATTACHMENT.read_bytes()).hexdigest(),
        'source_urls': SOURCE_URLS,
        'sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)},
    }
    (HERE / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(observations, ensure_ascii=False, indent=2))
