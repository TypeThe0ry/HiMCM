"""Refresh public aggregate rows together to investigate cross-level discrepancy."""
import hashlib,json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
import requests
import pandas as pd

P=Path(__file__).resolve().parent

def main():
    ids=pd.read_csv(P/'identity_join.csv').entity_id.astype(int).tolist()+[875776,4286]
    folder=P/'refreshed';folder.mkdir(exist_ok=True)
    def fetch(eid):
        url=requests.Request('GET','https://azreportcards.azed.gov/api/DataApi/Graduation Rate',params=dict(reportSection='Graduation Rate',fiscalYear=2025,educationOrganizationId=eid)).prepare().url
        path=folder/f'{eid}.json'
        now=datetime.now(timezone.utc).isoformat()
        response=requests.get(url,timeout=45);response.raise_for_status()
        data=response.json();assert isinstance(data,list)
        path.write_bytes(response.content)
        return dict(file='refreshed/'+path.name,url=url,retrieved_at=now,bytes=len(response.content),sha256=hashlib.sha256(response.content).hexdigest())
    with ThreadPoolExecutor(max_workers=4) as pool:manifest=list(pool.map(fetch,ids))
    (P/'refresh_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Refreshed',len(manifest),'cohort files')

if __name__=='__main__':main()
