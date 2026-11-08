"""Proposed Prague metro-complex subset from original official HTTP responses.

Uses standard-library Python plus optional pdftotext for external-PDF checks.
Writes only derived outputs inside this directory; never changes model inputs.
"""
import csv
import hashlib
import html
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ACCESS = '2026-11-09'
PDF = Path('/data/datasets/HiMCM/source_archives/task4_v127_prague/dpp_annual_report_2025.pdf')
PDF_SHA = '4e84c413e0d6e51702202f0bf7e04a1569e79ad63b01c71eab3cb60b03a1a7b9'
PDF_URL = 'https://www.dpp.cz/cs/data/V%C3%BDro%C4%8Dn%C3%AD%20zpr%C3%A1vy/Annual%20report/DPP_ANNUAL_REPORT_2025.pdf'
SHA = lambda b: hashlib.sha256(b).hexdigest()


def registered_table(bbox):
    # Poppler emitted a PDF control character; remove XML-disallowed controls,
    # preserving all words, diacritics and coordinates used by the table parser.
    xml = ET.fromstring(re.sub('[\x00-\x08\x0b\x0c\x0e-\x1f]', '', bbox))
    words = [(float(e.attrib['xMin']), float(e.attrib['yMin']), e.text or '')
             for e in xml.iter() if e.tag.endswith('word')]
    table = {}
    for line, x0, x1, bottom, expected in [('A',1020,1260,701,17),
            ('B',1260,1500,875,24),('C',1500,1740,782,20)]:
        rows = defaultdict(list)
        for x,y,word in words:
            if x0 <= x < x1 and 235 < y < bottom:
                rows[round(y/5)*5].append((x,word))
        names = [re.sub(r' \(change\)$', '', ' '.join(t for _,t in sorted(row)))
                 for _,row in sorted(rows.items())]
        assert len(names) == len(set(names)) == expected
        table[line] = names
    return table


def main():
    requests = json.loads((HERE/'retrieval_requests.json').read_text())
    assert len(requests) == 21 and all('error' not in r for r in requests)
    script = (HERE/'pid_script.js').read_text()
    assert 'function requestStopTab(char, inPrague, tabId)' in script
    assert 'action: "getStopTab"' in script and 'in_prague: inPrague' in script
    city_page = (HERE/'pid_prague_stops.html').read_text()
    outside_page = (HERE/'pid_outside_prague_stops.html').read_text()
    assert 'data-inprague="1"' in city_page
    assert 'data-inprague=""' in outside_page
    # The two official station lists distinguish Prague from outside Prague;
    # this is not selecting fare zoneP or commuter fare zones0/B.
    assert 'Zastávky v Praze' in city_page and 'Zastávky mimo Prahu' in outside_page
    geo = json.loads((HERE/'geography_control_requests.json').read_text())[0]
    assert geo['form'] == dict(action='getStopTab',char='B',in_prague='',ajax='true')
    outside = json.loads((HERE/geo['file']).read_text())
    assert outside['success'] is True
    assert 'Bořislavka' not in outside['html'] and 'Budějovická' not in outside['html']
    table = registered_table((HERE/'annual_report_page103_bbox.html').read_text())
    registered = defaultdict(set)
    for route,names in table.items():
        for name in names: registered[name].add(route)
    assert sum(map(len,table.values())) == 61 and len(registered) == 58
    assert {n for n,r in registered.items() if len(r)>1} == {'Florenc','Můstek','Muzeum'}
    current = {}
    for receipt in requests:
        assert receipt['form']['in_prague'] == '1'
        file = receipt['file']
        response = json.loads((HERE/file).read_text())
        assert response['success'] is True
        for block in re.findall(r'<li class="links-col-stop">(.*?)</li>', response['html'], re.S):
            name = re.search(r'<a class="is-stop"[^>]*>(.*?)</a>', block, re.S)
            if not name: continue
            name = html.unescape(re.sub('<[^>]+>', '', name.group(1))).strip()
            metro = []
            for url,route in re.findall(r'<a href="([^"]+)"><span>([ABC])</span>',block):
                url = html.unescape(url)
                query = parse_qs(urlparse(url).query)
                assert query['inprague'] == ['1'] and query['nm'] == [name]
                metro.append((route,query['node'][0],url))
            if not metro: continue
            row = current.setdefault(name,dict(routes=set(),node_ids=set(),source_files=set(),route_urls=set()))
            for route,node,url in metro:
                row['routes'].add(route); row['node_ids'].add(node); row['route_urls'].add(url)
            row['source_files'].add(file)
    assert len(current) == 57 and set(current) == set(registered)-{'Flora'}
    for name,row in current.items():
        assert row['routes'] == registered[name] and len(row['node_ids']) == 1
    flora = html.unescape((HERE/'dpp_flora_closure.html').read_text())
    florenc = html.unescape((HERE/'dpp_florenc_partial_access.html').read_text())
    for token in ['Flora','2. 2. 2026','do odvolání','vlaky stanicí projíždějí']:
        assert token in flora, token
    assert 'Omezení bezbariérového přístupu' in florenc
    assert 'Výstup je umožněn pouze' in florenc
    # Annual registered inventory does not establish continuous2025 operation.
    historical = (HERE/'annual_report_page17.txt').read_text()
    assert 'closed from 6 January to 19 December 2025' in historical
    assert '6 January 2025 until around March 2026' in historical
    original_verified = False
    if PDF.exists():
        assert SHA(PDF.read_bytes()) == PDF_SHA
        bbox = subprocess.check_output(['pdftotext','-f','103','-l','103','-bbox',str(PDF),'-']).decode()
        assert registered_table(bbox) == table
        original_verified = True
    rows = [dict(station_complex=name, routes=','.join(sorted(row['routes'])),
                 pid_node_id=next(iter(row['node_ids'])), geographic_scope='in_prague=1, official Prague-only stop list',
                 source_files=';'.join(sorted(row['source_files'])),
                 metro_route_urls=';'.join(sorted(row['route_urls']))) for name,row in sorted(current.items())]
    with (HERE/'station_complexes.csv').open('w',newline='',encoding='utf-8') as f:
        writer = csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    source = ROOT/'data/task4_v117_team_intake/city_indicators.csv'
    digest = SHA(source.read_bytes())
    assert digest == '430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
    with source.open(encoding='utf-8-sig') as f: city=next(r for r in csv.DictReader(f) if r['city']=='Prague')
    population = int(city['population']);assert population == 1407084
    with (ROOT/'results/task4_user_v124_revision/utility_bounds.csv').open() as f:
        prior=next(r for r in csv.DictReader(f) if r['city']=='Prague' and r['indicator']=='public_transport_density' and r['scenario']=='after_conditional')
    assert [float(prior['lower']),float(prior['upper'])] == [0,1]
    density = len(rows)*100000/population
    files = [r['file'] for r in requests]+['retrieval_requests.json','pid_script.js','pid_prague_stops.html',
            'dpp_flora_closure.html','dpp_florenc_partial_access.html',
            'pid_outside_prague_stops.html','pid_outside_prague_letter_B.json','geography_control_requests.json',
            'dpp_annual_reports.html','pid_fare_zones.html','dpp_current_metro_restrictions.html',
            'annual_report_page103_bbox.html','annual_report_page103.txt','annual_report_page103.png',
            'annual_report_page17.txt','annual_report_page17.png']
    hashes = {file:SHA((HERE/file).read_bytes()) for file in files}
    observation = dict(city='Prague',indicator='public_transport_density',raw_count=len(rows),
        population=population,population_year=2025,
        population_source='Unchanged authoritative16-city attachment; not externally rechecked',
        sourceyear=2026,access_date=ACCESS,utility_before=[0,1],utility_after=[density/(50+density),1],
        density_per_100000_lower=density,utility_anchor=50,lower_bound_only=True,
        admission_status='Candidate only; requires parent review',
        source_locator='https://pid.cz/zastavky-pid/zastavky-v-praze/',
        source_files=files,source_hashes=hashes,historical_inventory_proxy=False,
        scope='57 unique named metro station complexes listed with A/B/C route timetables in official Prague-only PID stop-list responses (in_prague=1), accessed2026-11-09. Same named interchange counted once regardless of two serving lines. Official current Flora closure corroborates its absence; Florenc retains service with restricted exits/accessibility. Other modes/operators uncounted.',
        extraction='Original official HTTP-response JSON and HTML; deterministic parsing by named stop, route label and Prague-only node. All57 names/routes cross-match2025DPP registered table (61line appearances minus3 duplicate transfer complexes=58), excluding Flora for the2026snapshot.',
        limitations='Current website snapshot with unchanged2025 population, not a2025 operational count. No claim of every station operating continuously, universal teenage access, service frequency or full all-mode city inventory. Florenc C accessibility restrictions persist. Public web data can be withdrawn to[0,1] if snapshot evidence is not accepted; unknown other supply retains upper1.')
    (HERE/'observations.json').write_text(json.dumps([observation],ensure_ascii=False,indent=2)+'\n')
    metadata = dict(access_date=ACCESS,input_sha256=digest,source_hashes=hashes,
        official_request_endpoint='https://pid.cz/wp-admin/admin-ajax.php',
        request_forms_file='retrieval_requests.json',snapshot_year=2026,
        context_only_files=['pid_fare_zones.html','dpp_current_metro_restrictions.html'],
        response_schema='JSON object: success:true, html:string. HTMLli.links-col-stop contains named a.is-stop and route hyperlinks with spanA/B/C; each selected route URL has node,nm,inprague=1.',
        source_urls={
            'dpp_annual_reports.html':'https://www.dpp.cz/spolecnost/o-spolecnosti/vyrocni-zpravy',
            'pid_prague_stops.html':'https://pid.cz/zastavky-pid/zastavky-v-praze/',
            'pid_outside_prague_stops.html':'https://pid.cz/zastavky-pid/zastavky-mimo-prahu/',
            'pid_fare_zones.html':'https://pid.cz/jizdne-a-tarif/tarifni-pasma-pid/',
            'pid_script.js':'https://pid.cz/wp-content/themes/pid/js/script.js?v=1791020739&ver=7.1',
            'dpp_flora_closure.html':'https://www.dpp.cz/omezeni-a-mimoradne-udalosti/detail/15',
            'dpp_florenc_partial_access.html':'https://www.dpp.cz/omezeni-a-mimoradne-udalosti/detail/39',
            'dpp_current_metro_restrictions.html':'https://www.dpp.cz/omezeni-a-mimoradne-udalosti?exception_types%5B%5D=2&exception_types%5B%5D=3&transport_types%5B%5D=1'},
        raw_original_responses='21byte-preserved PID JSON responses, official JS and HTML; no generative extraction used',
        external_annual_report=dict(url=PDF_URL,path=str(PDF),bytes=56581286,sha256=PDF_SHA,
            original_bytes_in_repository=False,original_checked_this_run=original_verified,
            report_year=2025,publication_year=2026,publication_year_basis='OriginalPDF metadata creation2026-09-01; exact publication date not inferred',
            necessary_extracts='PDF17:2025closure dates; PDF103:line-specific registered station table and declared31Dec2025scope. Original-source page images and text included; fullPDF external.',
            retrieval_command='curl -fL --max-time 180 URL -o EXTERNAL_PATH (if interrupted, curl -fL -C - --max-time 60 URL -o EXTERNAL_PATH); verifySHA256',
            pdf_text_command='pdftotext -f103 -l103 -bbox EXTERNAL_PATH -',
            image_command='pdftoppm -f103 -l103 -scale-to3000 -png -singlefile EXTERNAL_PATH annual_report_page103'),
        dedup=dict(annual_line_station_appearances=61,annual_registered_station_complexes=58,
            interchange_names=['Florenc','Můstek','Muzeum'],current_named_complexes=57,
            omitted_current_closed_station='Flora; official closure from2026-02-02 until further notice',
            historical_year_end_comparison='2025year-end57operating complexes instead omitČeskomoravská, notFlora; not used as current evidence'),
        checks=dict(all57_current_names_match_registered_inventory=True,
            all57_have_prague_only_metro_route_urls=True,same_name_same_unique_pid_node=True,
            official_city_vs_outside_stop_lists_verified=True,not_a_fare_zone_filter=True,
            annual_complexes_not_line_appearances=True,original_pdf_hash_verified=original_verified,
            current_and_historical_closures_distinguished=True,attachment_unchanged=True))
    (HERE/'manifest.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(raw_count=len(rows),density_lower=density,utility_after=observation['utility_after'],
        original_pdf_verified=original_verified),indent=2))


if __name__ == '__main__':main()
