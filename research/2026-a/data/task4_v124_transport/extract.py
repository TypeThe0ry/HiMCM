"""Reproduce a conservative, named Tokyo23 municipal pool-venue subset.

Run with .venv-v120/bin/python; only standard-library dependencies.
No network requests and no writes outside this directory.
"""
import csv
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ACCESS = '2026-11-09'
BASE = 'https://www.city.nerima.tokyo.jp/'
PATHS = {
    'nerima_facilities': 'shisetsu/koen/index.html',
    **{k: f'shisetsu/koen/taiku/{k}.html' for k in
       ['nakamuraminami', 'kamishakujii', 'oizumigakuen', 'hikarigaoka', 'heiwadai']},
    'miharadai': 'shisetsu/koen/pool/miharadai.html',
    'miharadai_closure': 'kankomoyoshi/sports/oshirase/20260929.html',
    'heiwadai_closure': 'kankomoyoshi/sports/oshirase/20261027.html',
}


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.pieces = []

    def handle_data(self, data):
        self.pieces.append(data)


def plaintext(file):
    parser = Text()
    parser.feed(file.read_text(encoding='utf-8'))
    return re.sub(r'\s+', ' ', ' '.join(parser.pieces)).strip()


def main():
    sources, texts = {}, {}
    for key, path in PATHS.items():
        file = HERE / (key + '.html')
        text = plaintext(file)
        texts[key] = text
        update = re.search(r'更新日：(\d+年\d+月\d+日)', text)
        sources[file.name] = dict(url=BASE+path, accessed=ACCESS,
                                 sha256=hashlib.sha256(file.read_bytes()).hexdigest(),
                                 representation='Original HTTP response body, byte-preserved HTML',
                                 page_updated=update.group(1) if update else None,
                                 provider='Nerima municipal government', language='Japanese')
    # Five address-distinct municipal venues in one of Tokyo's 23 special wards.
    # Allowlist deliberately omits the outdoor/seasonal venue and currently closed Heiwadai.
    selected = [
        ('nakamuraminami', '中村南スポーツ交流センター温水プール', '練馬区中村南1丁目2番32号'),
        ('kamishakujii', '上石神井体育館温水プール', '練馬区上石神井1丁目32番37号'),
        ('oizumigakuen', '大泉学園町体育館温水プール', '練馬区大泉学園町5丁目14番24号'),
        ('hikarigaoka', '光が丘体育館温水プール', '練馬区光が丘4丁目1番4号'),
        ('miharadai', '三原台温水プール', '練馬区三原台2丁目11番29号'),
    ]
    rows = []
    for key, name, address in selected:
        assert name in texts['nerima_facilities'], name
        assert address in texts['nerima_facilities'], address
        assert ('25メートル' in texts[key] or '25m' in texts[key]), key
        assert 'プール' in texts[key] and '開館時間' in texts[key], key
        assert '休館日' in texts[key], key
        rows.append(dict(venue=name, address=address, ward='練馬区',
                         unit='distinct public swimming venue, not basins or lanes',
                         source_file=key+'.html', source_url=BASE+PATHS[key],
                         locator='施設内容 (pool specification); 開館時間; 休館日; index プール table',
                         observation='municipal currently-listed operational facility stock; routine closures apply'))
    # Notice distinguishes a future planned closure from a currently indefinite closure.
    assert '令和9年2月1日' in texts['miharadai_closure']
    assert '5月31日' in texts['miharadai_closure']
    assert '現在プールを休場' in texts['heiwadai_closure']
    assert '再開時期は未定' in texts['heiwadai_closure']
    assert len({r['address'] for r in rows}) == len(rows) == 5
    file = HERE / 'pool_venues.csv'
    with file.open('w', encoding='utf-8', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    source = ROOT / 'data/task4_v117_team_intake/city_indicators.csv'
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    assert digest == '430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
    with source.open(encoding='utf-8-sig') as inp:
        tokyo = next(r for r in csv.DictReader(inp) if r['city'] == 'Tokyo')
    pop = int(float(tokyo['population']))
    assert pop == 9983365 and not tokyo['pools_per_100k']
    density = len(rows)*100000/pop
    observation = dict(city='Tokyo', indicator='public_pool_density', raw_count=len(rows),
        population=pop, population_year=2026, sourceyear=2026, access_date=ACCESS,
        population_source='Unchanged authoritative 16-city user attachment; not externally rechecked',
        input_sha256=digest, utility_before=[0, 1], utility_after=[density/(1+density), 1],
        density_per_100000_lower=density, utility_anchor=1, lower_bound_only=True,
        source_locator=BASE+PATHS['nerima_facilities'], source_file='nerima_facilities.html',
        source_files=list(sources), source_hashes={k:v['sha256'] for k,v in sources.items()},
        scope='Five distinct-address Nerima municipal indoor swimming venues, wholly inside Tokyo23 special-ward scope. Other Tokyo wards/providers uncounted. Venues, not basins, swimming lanes, capacity or operators.',
        historical_inventory_proxy=False,
        extraction='Deterministic named-venue allowlist verified against original municipal HTML index and each facility page. Closed-Heiwadai and future-Miharadai notices explicitly checked.',
        limitations='Operational facility-stock subset as accessed 2026-11-09, not a complete city census or a claim that every venue is open today. Routine maintenance days and limited special sessions apply. Miharadai announces closure 2027-02-01 through 2027-05-31. Heiwadai currently closed with unknown reopening is excluded. No inference about adolescent use, within-city equity or individual accessibility. Upper utility remains1.')
    (HERE/'observations.json').write_text(json.dumps([observation],ensure_ascii=False,indent=2)+'\n')
    sources['provider_capture.json'] = dict(
        url=['https://www.sports-tokyo-info.metro.tokyo.lg.jp/seisaku/sports_facility_r4/data/sports_facility_r07_01.pdf',
             'https://www.tokyometro.jp/corporate/enterprise/passenger_rail/transportation/passengers/index.html'],
        accessed=ACCESS, sha256=hashlib.sha256((HERE/'provider_capture.json').read_bytes()).hexdigest(),
        representation='Exa clean-markdown tool response JSON; NOT original PDF or HTML. Not admitted.',
        limitation='Official PDF original download returned403; extraction contains row-order ambiguity. No source-page image was successfully recovered. Candidate uses independent original Nerima HTML instead.')
    (HERE/'manifest.json').write_text(json.dumps(dict(accessed=ACCESS, sources=sources,
        input_sha256=digest, admission_count=1, venues=5),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(venues=len(rows), population=pop, density_lower=density,
                         utility_bounds=observation['utility_after'], source_originals=len(PATHS)),indent=2))


if __name__ == '__main__':
    main()
