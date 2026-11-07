"""Exact reported 14–18 age scope; preserve conditional stage and optional records."""
from collections import Counter
from pathlib import Path
from zipfile import ZipFile
import csv, hashlib, importlib.util, io, json
P = Path(__file__).resolve().parent
OLD = P.parent / 'task4_v15_mexico2020'
spec = importlib.util.spec_from_file_location('mexico_v15', OLD/'extract_commute.py')
v15 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v15)

def classify(row, low=14, high=18):
    age = int(row['EDAD'])
    if age != 999 and not low <= age <= high: return None
    if row['ASISTEN'] not in ('1', '9'): return None
    level, grade = int(row['NIVACAD']), int(row['ESCOLARI'])
    reconstructed = (level == 3 and grade == 3) or (level in (4,5,7) and 0 <= grade < 3)
    unspecified = level == 99 or grade == 99
    if not reconstructed and not unspecified: return None
    if age != 999 and row['ASISTEN'] == '1' and reconstructed: return 'conditional_classified'
    return 'optional'

def derive():
    for entry in json.loads((OLD/'manifest.json').read_text()):
        assert hashlib.sha256((OLD/entry['file']).read_bytes()).hexdigest() == entry['sha256']
    groups = {s: {'known':Counter(), 'optional':Counter(), 'ages_known':Counter(), 'ages_optional':Counter(), 'n_known':0, 'n_optional':0} for s in ('age3_17','age14_18')}
    ids=set()
    with ZipFile(OLD/'Censo2020_CA_cdmx_csv.zip') as z:
        for row in csv.DictReader(io.TextIOWrapper(z.open('Personas09.CSV'),encoding='utf-8-sig')):
            assert row['ENT']=='09' and row['ID_PERSONA'] not in ids
            ids.add(row['ID_PERSONA']); w=int(row['FACTOR']); assert w>0
            for scope, limits in [('age3_17',(3,17)),('age14_18',(14,18))]:
                category=classify(row,*limits)
                if category is None: continue
                kind='known' if category=='conditional_classified' else 'optional'
                g=groups[scope];g[kind][row['TIE_TRASLADO_ESCU']]+=w
                g['ages_'+kind][row['EDAD']]+=w;g['n_'+kind]+=1
    assert len(ids)==276007
    result={'year':2020,'new_downloads':0,'current_stage_directly_observed':False,
            'stage_assumption':'Current attendance with completed secondary3 or completed grades0–2 at levels4/5/7; progression is conditional, not directly observed current high-school stage.',
            'age_rule':'Known ages14–18 inclusive; age999 remains optional. Known nonattenders excluded; unspecified attendance/stage/grade retained as optional under prior broad stage rule.',
            'sampling_uncertainty_included':False,'person_rows':len(ids),'scopes':{}}
    for scope,g in groups.items():
        lo,hi=v15.optional_membership(g['known'],g['optional'])
        result['scopes'][scope]={**g,'utility_lower':lo,'utility_upper':hi,'known_weight':sum(g['known'].values()),'optional_weight':sum(g['optional'].values())}
    old=json.loads((P.parent/'task4_v23_mexico_membership/summary.json').read_text())['scopes']['age3_17']
    g=result['scopes']['age3_17']
    assert dict(g['known'])==old['known_time_bins']
    assert dict(g['optional'])==old['corrected_optional_time_bins']
    for key in ('utility_lower','utility_upper'):assert abs(g[key]-old[key])<1e-14
    result['sources']=[{'path':'../task4_v15_mexico2020/'+f,'sha256':hashlib.sha256((OLD/f).read_bytes()).hexdigest()} for f in ['Censo2020_CA_cdmx_csv.zip','dictionary.xlsx','completed_grade_metadata.html','education_level_metadata.html','school_attendance_metadata.html','school_time_metadata.html','extract_commute.py']]
    return result

if __name__=='__main__':
    result=derive();(P/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['scopes'],indent=2))
