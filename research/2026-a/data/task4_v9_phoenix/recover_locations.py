"""Recover missing coordinates only after official NCES ID confirmation."""
from pathlib import Path
import json,re
import pandas as pd
import requests
P=Path(__file__).resolve().parent

def norm(s):return re.sub('[^a-z0-9]','',str(s).lower())

def main():
    entities=json.loads((P/'statewide_missing_locations.json').read_text());n=pd.read_csv(P.parent/'task4_v6_phoenix/school_audit.csv',dtype={'NCESSCH':str})
    out=P/'recovered';out.mkdir(exist_ok=True);audit=[]
    for e in {r['educationOrganizationId']:r for r in entities}.values():
        m=n[n.SCH_NAME.map(norm)==norm(e['searchTermDescription'])]
        if len(m)!=1 or not m.iloc[0].within_current_phoenix_boundary:continue
        school=m.iloc[0];eid=e['educationOrganizationId'];f=out/f'{eid}_entity.json'
        params=dict(id=eid,fiscalYear=2025);url='https://azreportcards.azed.gov/api/Entity/GetEntity'
        if not f.exists():
            r=requests.get(url,params=params,timeout=30);r.raise_for_status();f.write_bytes(r.content)
        data=json.loads(f.read_text());assert len(data)==1
        d=data[0];crosswalk=str(d.get('leances',''))+str(d.get('nces','')).zfill(5)
        match=crosswalk==school.NCESSCH
        row=dict(entity_id=eid,name=e['searchTermDescription'],nces_id=school.NCESSCH,official_nces_id=crosswalk,id_verified=match,school_types=d.get('schoolTypes'),latitude=school.LATCOD,longitude=school.LONCOD,source='NCES2024-25 coordinates; ADE FY2025 NCES identifier confirmation')
        if match and not any(x in str(d.get('schoolTypes','')) for x in ['Online','Private']):
            g=out/f'{eid}_graduation.json'
            if not g.exists():
                r=requests.get('https://azreportcards.azed.gov/api/DataApi/Graduation Rate',params=dict(reportSection='Graduation Rate',fiscalYear=2025,educationOrganizationId=eid),timeout=30);r.raise_for_status();g.write_bytes(r.content)
            allrows=[x for x in json.loads(g.read_text()) if x.get('studentGroupDescription')=='All']
            row['all_rows']=len(allrows)
            if len(allrows)==1:row.update(allrows[0])
        audit.append(row)
    pd.DataFrame(audit).to_csv(P/'recovered_location_audit.csv',index=False)
    print(pd.DataFrame(audit)[['entity_id','name','id_verified','numInCohort','numGraduated']].to_string(index=False))
if __name__=='__main__':main()
