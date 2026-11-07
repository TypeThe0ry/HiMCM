"""Acquire official identifiers; reuse unchanged cohort2024 school observations."""
import hashlib,json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import pandas as pd
import requests

P=Path(__file__).resolve().parent
OLD=P.parent/'task4_v9_phoenix'

def main():
    roster=pd.read_csv(P.parent/'task4_v56_pxu_roster/roster_join.csv',dtype={'nces_id':str})
    matches=pd.read_csv(OLD/'school_outcome_audit.csv',dtype={'nces_id':str})
    mapping={r.nces_id:int(r.entity_id) for r in matches.itertuples()}
    # IDs from official search directory / previously verified recovery, checked
    # again against GetEntity's NCES identifiers below, never joined by name alone.
    mapping.update({'040633000554':5437,'040633002138':79617,
                    '040633001382':6249,'040633001429':6250})
    rows=roster.drop_duplicates('nces_id')
    rows=rows[~rows.digital_excluded].to_dict('records')
    def fetch(row):
        eid=mapping[row['nces_id']]
        path=P/f'entity_{eid}.json'
        url=requests.Request('GET','https://azreportcards.azed.gov/api/Entity/GetEntity',
                             params={'id':eid,'fiscalYear':2025}).prepare().url
        if not path.exists():
            response=requests.get(url,timeout=40);response.raise_for_status()
            assert isinstance(response.json(),list)
            path.write_bytes(response.content)
        records=json.loads(path.read_text());assert len(records)==1
        entity=records[0]
        official=str(entity['leances'])+str(entity['nces']).zfill(5)
        candidates=[OLD/f'school_outcomes/{eid}.json',OLD/f'spatial_responses/{eid}.json',
                    OLD/f'recovered/{eid}_graduation.json']
        source=next((f for f in candidates if f.exists()),None)
        assert source is not None,eid
        outcomes=[r for r in json.loads(source.read_text()) if r.get('studentGroupDescription')=='All']
        assert len(outcomes)<=1
        return dict(nces_id=row['nces_id'],official_nces_id=official,identity_verified=official==row['nces_id'],entity_id=eid,catalog_name=row['catalog_name'],
                    catalog_address=row['catalog_address'],catalog_city_verified=bool(row['catalog_campus_current_boundary']),
                    entity_file=path.name,entity_url=url,entity_returned_year=entity.get('fiscalYear'),
                    cohort_source=str(source.relative_to(P.parent)),all_rows=len(outcomes))
    with ThreadPoolExecutor(max_workers=4) as pool: result=list(pool.map(fetch,rows))
    pd.DataFrame(result).to_csv(P/'identity_join.csv',index=False)
    manifest=[]
    for row in result:
        f=P/row['entity_file']
        manifest.append(dict(file=f.name,url=row['entity_url'],bytes=f.stat().st_size,
                             sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
        f=P.parent/row['cohort_source']
        manifest.append(dict(file='../'+row['cohort_source'],bytes=f.stat().st_size,
                             sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
    for rel in ['identity_join.csv','../task4_v56_pxu_roster/roster_join.csv','../task4_v9_phoenix/state_graduation_2025.json',
                '../task4_v57_ade_aggregate/fy24_full_reader_audit.json']:
        f=P/rel;manifest.append(dict(file=rel,bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
    (P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Verified',sum(r['identity_verified'] for r in result),'of',len(result),'non-Digital school identities')

if __name__=='__main__':main()
