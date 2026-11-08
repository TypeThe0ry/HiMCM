"""Partial public pool inventories; preserve attachment populations unchanged."""
from pathlib import Path
import csv
import hashlib
import json

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'task4_v117_team_intake/city_indicators.csv'

def extract():
    rows={r['city']:r for r in csv.DictReader(SOURCE.open(encoding='utf-8-sig'))}
    zurich=['Hallenbad Altstetten','Hallenbad Bläsi','Hallenbad Bungertwies','Hallenbad City','Hallenbad Leimbach','Hallenbad Oerlikon','Wärmebad Käferberg']
    milan=['ARIOLI VENEGONI','CAMBINI FOSSATI','CARDELLINO',"CARELLA CANTU'",'DE MARCHI','ISEO','MINCIO','MURAT','MUGGIANO','PARRI MENGONI','QUARTO CAGNINO',"SANT’ABBONDIO",'SUZZANI','BACONE','COZZI','PROCIDA','SOLARI']
    definitions=[('Zurich',zurich,2026,'zurich_provider_capture.json','https://www.stadt-zuerich.ch/de/stadtleben/sport-und-erholung/sport-und-badeanlagen/hallenbaeder.html'),('Milan',milan,2025,'milan_provider_capture.json','https://www.milanosport.it/workspace/uploads/nuovi-tariffari-1-giugno-2025-agg-9-10-2025.pdf')]
    out=[]
    for city,venues,year,filename,url in definitions:
        capture=json.loads((HERE/filename).read_text())
        text='\n'.join(c.get('text','') for c in capture['result']['content']).upper().replace('’',"'")
        for name in venues:assert name.upper().replace('’',"'") in text,name
        assert len(set(venues))==len(venues)
        assert not rows[city]['pools_per_100k'].strip()
        population=int(rows[city]['population'])
        assert population=={'Zurich':440935,'Milan':1399079}[city]
        density=len(venues)*100000/population
        out.append(dict(city=city,indicator='public_pool_density',utility_before=[0,1],utility_after=[density/(1+density),1],raw_count=len(venues),population=population,population_year=int(rows[city]['population_year']),population_source='Existing attachment; retained without external verification or revision',sourceyear=year,lower_bound_only=True,density_lower=density,utility_anchor=1,venues=venues,source_locator=url,source_file=filename,scope=('Current official directory of seven public indoor pool venues, accessed2026-11-08;2026facilitysnapshot divided by unchanged2025attachmentpopulation. Excludes school pools, river/lake baths and outdoor venues; partial inventory.' if city=='Zurich' else 'Official public indoor swimming tariff effective2025-06-01 names13 tariff-A venues and4 tariff-B venues. Count physical facility names once; current operator directory corroborates venue identities. Partial inventory; other operators/outdoor venues unknown.'),limitations='Facility supply only, not teenage access, continuous operation or a complete city count. Upper utility remains1.'))
    return out

if __name__=='__main__':
    out=extract();(HERE/'observations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in HERE.iterdir() if f.is_file() and f.name!='manifest.json'}
    hashes['../task4_v117_team_intake/city_indicators.csv']=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    (HERE/'manifest.json').write_text(json.dumps(hashes,indent=2)+'\n')
    print(json.dumps([{k:r[k] for k in ['city','raw_count','population','utility_after']} for r in out],indent=2))
