"""Bounded audit of V48's 15 non-home-first-school records; no bound replacement."""
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from dbfread import DBF

P = Path(__file__).resolve().parent
OLD = P.parent / 'task4_v10_saopaulo'
V48 = P.parent / 'task4_v48_saopaulo_age'

def main():
    inputs = [OLD/'Banco2023_divulgacao_190225.dbf.gz', OLD/'Layout_BD_OD2023_190225.xlsx',
              V48/'municipal_students_audit.csv', V48/'summary.json']
    manifest = [dict(file=str(p.relative_to(P.parent)), bytes=p.stat().st_size,
                    sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in inputs]
    raw = gzip.decompress(inputs[0].read_bytes())
    expected = json.loads((OLD/'microdata_manifest.json').read_text())['files'][0]
    assert len(raw) == expected['bytes'] and hashlib.sha256(raw).hexdigest() == expected['sha256']
    ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(inputs[1]) as z:
        strings = [''.join(n.itertext()) for n in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', ns)]
        layout = []
        for row in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//m:row', ns):
            vals = []
            for c in row.findall('m:c', ns):
                v = c.find('m:v', ns)
                value = '' if v is None else v.text
                vals.append(strings[int(value)] if c.get('t') == 's' else value)
            layout.append(vals)
    index = next(i for i,r in enumerate(layout) if 'MOTIVO_O' in r)
    service = next(i for i,r in enumerate(layout) if 'SERVIR_O' in r)
    codes = {int(r[-1].split(' - ')[0]): r[-1].split(' - ',1)[1] for r in layout[index:index+11]}
    assert set(codes) == set(range(1,12)) and codes[8] == 'Residência'
    audit48 = list(csv.DictReader(inputs[2].open()))
    target = [r for r in audit48 if r['age14_18'] == 'True']
    counts = Counter(r['status'] for r in target)
    assert counts == {'observed_direct_journey':1489, 'no_school_journey':186,
                      'first_school_journey_not_from_home':15}
    ids = {r['person_id'] for r in target if r['status']=='first_school_journey_not_from_home'}
    people = defaultdict(list)
    with tempfile.TemporaryDirectory() as td:
        f = Path(td)/'source.dbf'; f.write_bytes(raw)
        for r in DBF(str(f), encoding='latin1'):
            if str(r['ID_PESS']) in ids: people[str(r['ID_PESS'])].append(r)
    rows = []
    for pid, diary in sorted(people.items()):
        diary.sort(key=lambda r:r['N_VIAG'])
        school = min((r for r in diary if r['MOTIVO_D']==4),key=lambda r:r['N_VIAG'])
        prior = [r for r in diary if r['N_VIAG']<school['N_VIAG'] and r['MOTIVO_O']==8]
        assert prior
        home = max(prior,key=lambda r:r['N_VIAG'])
        chain = [r for r in diary if home['N_VIAG']<=r['N_VIAG']<=school['N_VIAG']]
        assert len(chain)==2 and [r['N_VIAG'] for r in chain]==[1,2]
        def dep(r):return r['H_SAIDA']*60+r['MIN_SAIDA']
        def arr(r):return r['H_CHEG']*60+r['MIN_CHEG']
        duration_ok = all(0<=r['H_SAIDA']<24 and 0<=r['H_CHEG']<24 and
            0<=r['MIN_SAIDA']<60 and 0<=r['MIN_CHEG']<60 and
            r['DURACAO']>0 and (arr(r)-dep(r))%1440==r['DURACAO'] for r in chain)
        same_date = len({r['DATA'] for r in chain})==1
        purpose_ok = home['MOTIVO_D']==school['MOTIVO_O']
        zone_ok = home['ZONA_D'] is not None and home['ZONA_D']==school['ZONA_O']
        nonoverlap = arr(home)<=dep(school)
        flags = [r[k] for r in chain for k in ['SERVIR_O','SERVIR_D']]
        assert all(v=='N' for v in flags)
        purpose = home['MOTIVO_D']
        assert purpose in (2,3,10)
        rows.append(dict(person_id=pid,first_school_journey=school['N_VIAG'],
            last_home_journey=home['N_VIAG'],intermediate_purpose=purpose,
            intermediate_label=codes[purpose],date=str(home['DATA']),
            recorded_day_code=home['DIA_SEM'],calendar_iso_weekday=home['DATA'].isoweekday(),
            consecutive_journeys=True,same_reported_date=same_date,
            purpose_continuity=purpose_ok,zone_continuity=zone_ok,
            clocks_match_duration=duration_ok,times_nonoverlap=nonoverlap,
            departure_minute=dep(home),first_arrival_minute=arr(home),
            second_departure_minute=dep(school),school_arrival_minute=arr(school),
            intermediate_dwell_minutes=dep(school)-arr(home),
            service_origin_first=home['SERVIR_O'],service_destination_first=home['SERVIR_D'],
            service_origin_second=school['SERVIR_O'],service_destination_second=school['SERVIR_D'],
            recovered=False,utility_lower=0,utility_upper=1,
            reason='nontransport_work_stop' if purpose in (2,3) else 'personal_affairs_not_documented_transport'))
    assert len(rows)==15
    with (P/'chain_audit.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
    result = dict(source='Existing public research mirror of OD2023; no new official download',
        official_byte_identity_verified=False, scope='Municipality 36, ESTUDA=4, actual IDADE 14..18',
        examined=15,recovered=0,intermediate_purpose_counts=dict(Counter(r['intermediate_label'] for r in rows)),
        preserved_status_counts=dict(counts),model_inputs_changed=False,bootstrap_rerun=False,
        bootstrap_reason='No recovered observations; V48 endpoints and all paired replicates remain unchanged by construction.',
        continuity_checks={k:sum(r[k] for r in rows) for k in ['consecutive_journeys','same_reported_date',
            'purpose_continuity','zone_continuity','clocks_match_duration','times_nonoverlap']},
        service_flag_note="Layout states 1=Sim, 2=Não; these 60 DBF fields are raw 'N'. No numeric mapping or positive service inference imposed.",
        date_note='Reported date equality checked; DATA calendar weekday is retained separately from DIA_SEM. No calendar recoding changes the V48 direct sample.',
        layout_purpose_rows=layout[index:index+12],layout_service_rows=layout[service:service+4],
        unchanged_v48_age14_18=json.loads(inputs[3].read_text())['scopes']['age14_18'])
    (P/'summary.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    (P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['examined','recovered','intermediate_purpose_counts','continuity_checks']},ensure_ascii=False))

if __name__=='__main__':main()
