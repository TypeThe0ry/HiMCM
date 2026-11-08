"""Verify source identities and derive conservative physical-facility lower bounds."""
from pathlib import Path
import json,csv,hashlib,subprocess,re
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
def run():
    for r in json.loads((P/'manifest.json').read_text()):
        assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
    source=ROOT/'data/task4_v7_istanbul/official_web_verified_values.json'
    pop=json.loads(source.read_text())['population2025'];assert pop['value']==15754053 and pop['year']==2025
    t=subprocess.check_output(['pdftotext','-layout',str(P/'iett2025.pdf'),'-']).decode()
    assert 'İstanbul genelinde bulunan 12.426 adet durağa' in t
    assert re.search(r'QR KODLU LEVHA TAKILAN DURAK SAYISI\s+7\.000\s+12\.426',t)
    assert '2025' in t and 'montajı tamamlanmıştır' in t
    roster=list(csv.DictReader((P/'pool_venues2025.csv').open()))
    names=[r['name'] for r in roster];assert len(names)==len(set(names))==24
    assert all(r['snapshot_date']=='2025-01-01' for r in roster)
    proof=json.loads((P/'pool_source_verification.json').read_text());assert proof['verified_swimming_venues']==24
    rows=[]
    for indicator,count,anchor,locator,scope in [
      ('public_transport_density',12426,50,'IETT2025 PDF pages63 and91 (printed124–125 and180–181); actual QR-equipped stop count12426 versus target7000',
       'Actual identified physical stops across Istanbul receiving Braille/QR signage, a bus-network subset; not route occurrences, not all modes, upper unknown. Official administrative distinct-stop count accepted; no separate GTFS geocoding/dedup performed.'),
      ('public_pool_density',24,1,'Official IBB article dated2025-01-01, swimming-services named venue list; manual verified rendering plus independent indexed-source crosscheck',
       'Partial list of distinct municipal venues providing paid public swimming services as of January2025, paired with same-year December population. Not complete city inventory, not pool basins, not year-round or teenager-specific access. Other operators/venues unknown.')]:
        density=count/pop['value']*100000;u=density/(density+anchor)
        rows.append(dict(city='Istanbul',indicator=indicator,utility_before=[0,1],utility_after=[u,1],raw_count=count,population=pop['value'],sourceyear=2025,population_year=2025,source_locator=locator,scope=scope,density_per_100000=density,utility_anchor=anchor,lower_bound_only=True,source_population_sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
    (P/'observations.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))
if __name__=='__main__':run()
