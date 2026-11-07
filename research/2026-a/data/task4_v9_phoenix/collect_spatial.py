"""Public official entity locations, independently selected by Phoenix boundary."""
import json,hashlib,math
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests
import pandas as pd
from matplotlib.path import Path as PolygonPath
P=Path(__file__).resolve().parent

def main():
    geometry=json.loads((P.parent/'task4_v6_phoenix/phoenix_boundary.geojson').read_text())
    polygons=[]
    for f in geometry['features']:
        g=f['geometry'];polygons.extend(g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']])
    def inside(lon,lat):
        return any(PolygonPath(p[0]).contains_point((lon,lat)) and not any(PolygonPath(h).contains_point((lon,lat)) for h in p[1:]) for p in polygons)
    entities=json.loads((P/'phoenix_search.json').read_text());selected=[];missing=[]
    for e in entities:
        if e['searchTermTypeId']!=1:continue
        try:
            lat,lon=float(e['latitude']),float(e['longitude'])
            if not(math.isfinite(lat) and math.isfinite(lon)):raise ValueError()
        except (TypeError,ValueError):missing.append(e);continue
        if inside(lon,lat):selected.append(e)
    (P/'spatial_entity_aliases.json').write_text(json.dumps(selected,indent=2))
    selected=list({r['educationOrganizationId']:r for r in selected}.values())
    (P/'spatial_entities.json').write_text(json.dumps(selected,indent=2))
    (P/'statewide_missing_locations.json').write_text(json.dumps(missing,indent=2))
    out=P/'spatial_responses';out.mkdir(exist_ok=True)
    def get(e):
        i=e['educationOrganizationId'];old=P/f'school_outcomes/{i}.json';dest=out/f'{i}.json'
        row=dict(entity_id=i,name=e['searchTermDescription'],type=e['type'])
        url='https://azreportcards.azed.gov/api/DataApi/Graduation Rate';params=dict(reportSection='Graduation Rate',fiscalYear=2025,educationOrganizationId=i)
        row['url']=requests.Request('GET',url,params=params).prepare().url
        if old.exists():data=json.loads(old.read_text());row['source_file']=str(old.relative_to(P))
        elif dest.exists():data=json.loads(dest.read_text());row['source_file']=str(dest.relative_to(P))
        else:
            try:
                r=requests.get(url,params=params,timeout=20);r.raise_for_status();data=r.json()
                assert isinstance(data,list)
                dest.write_bytes(r.content);row['source_file']=str(dest.relative_to(P))
            except (requests.RequestException,ValueError,AssertionError) as ex:return dict(row,status=type(ex).__name__)
        allrows=[r for r in data if r.get('studentGroupDescription')=='All'];row.update(status='ok',all_rows=len(allrows))
        if len(allrows)==1:row.update(allrows[0])
        return row
    with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(get,selected))
    df=pd.DataFrame(rows);df.to_csv(P/'spatial_outcome_audit.csv',index=False)
    summary=dict(spatial_entities=len(selected),statewide_missing_coordinates=len(missing),successful=int((df.status=='ok').sum()),unique_all_records=int((df.all_rows==1).sum()),citywide_admitted=False)
    (P/'spatial_summary.json').write_text(json.dumps(summary,indent=2));print(summary)
if __name__=='__main__':main()
