"""Archive school-level outcomes for exact-name, nearby NCES matches; no city inference."""
from pathlib import Path
import json,hashlib,re,math
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import requests
P=Path(__file__).resolve().parent

def norm(s):return re.sub(r'[^a-z0-9]','',str(s).lower())

def main():
    schools=pd.read_csv(P.parent/'task4_v6_phoenix/school_audit.csv',dtype={'NCESSCH':str})
    schools=schools[schools.within_current_phoenix_boundary & schools.not_virtual & schools.operational]
    entities=json.loads((P/'phoenix_search.json').read_text());matches=[]
    for r in schools.to_dict('records'):
        options=[e for e in entities if e['searchTermTypeId']==1 and norm(e['searchTermDescription'])==norm(r['SCH_NAME'])]
        valid=[]
        for e in options:
            try:
                d=111*math.hypot(float(e['latitude'])-r['LATCOD'],math.cos(math.radians(r['LATCOD']))*(float(e['longitude'])-r['LONCOD']))
                if d<.5:valid.append((e,d))
            except (TypeError,ValueError):pass
        if len(valid)==1:
            e,d=valid[0];matches.append(dict(nces_id=r['NCESSCH'],name=r['SCH_NAME'],entity_id=e['educationOrganizationId'],distance_km=d))
    assert len({r['entity_id'] for r in matches})==len(matches),'Ambiguous entity mapping'
    (P/'school_matches.json').write_text(json.dumps(matches,indent=2))
    (P/'school_outcomes').mkdir(exist_ok=True)
    def fetch(row):
        eid=row['entity_id'];dest=P/f'school_outcomes/{eid}.json'
        url='https://azreportcards.azed.gov/api/DataApi/Graduation Rate'
        params=dict(reportSection='Graduation Rate',fiscalYear=2025,educationOrganizationId=eid)
        if dest.exists():data=json.loads(dest.read_text());status=200;address=requests.Request('GET',url,params=params).prepare().url
        else:
            try:r=requests.get(url,params=params,timeout=30)
            except requests.RequestException as exc:return dict(**row,status='request_failed',error=type(exc).__name__)
            status=r.status_code;address=r.url
            if status!=200:return dict(**row,status=status,url=address)
            data=r.json()
            if not isinstance(data,list):return dict(**row,status='unexpected_schema',url=address)
            dest.write_bytes(r.content)
        allrows=[a for a in data if a.get('studentGroupDescription')=='All']
        result=dict(**row,status=status,url=address,all_rows=len(allrows))
        if len(allrows)==1:result.update(allrows[0])
        return result
    with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(fetch,matches))
    pd.DataFrame(results).to_csv(P/'school_outcome_audit.csv',index=False)
    valid=[r for r in results if r.get('all_rows')==1 and r.get('numInCohort',-1)>0 and 0<=r.get('numGraduated',-1)<=r['numInCohort']]
    denom=sum(r['numInCohort'] for r in valid);num=sum(r['numGraduated'] for r in valid)
    summary=dict(nces_nonvirtual_operational_city_schools=len(schools),exact_name_nearby_matches=len(matches),schools_with_valid_all_counts=len(valid),known_cohort=denom,known_graduates=num,complete_count_subset_rate=num/denom if denom else None,
                 model_admission=False,reason='Matched available public-school subset; school locations not residence; unmatched and suppressed denominator unknown; graduation is not teacher headcount.')
    (P/'city_collection_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
    files=[dict(file=str(f.relative_to(P)),bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in P.rglob('*') if f.is_file() and f.name!='collection_manifest.json']
    (P/'collection_manifest.json').write_text(json.dumps(files,indent=2))
if __name__=='__main__':main()
