"""Move completed-secondary transition records to uncertain current membership."""
from collections import Counter
from pathlib import Path
from zipfile import ZipFile
import csv,hashlib,importlib.util,io,json
P=Path(__file__).resolve().parent
OLD=P.parent/'task4_v15_mexico2020'
spec=importlib.util.spec_from_file_location('mexico72_source',P.parent/'task4_v72_mexico/extract.py')
v72=importlib.util.module_from_spec(spec);spec.loader.exec_module(v72)


def classify(row):
    category=v72.classify(row)
    if category=='conditional_classified' and int(row['NIVACAD'])==3 and int(row['ESCOLARI'])==3:return 'transition_optional'
    return category


def derive():
    for r in json.loads((OLD/'manifest.json').read_text()):
        assert hashlib.sha256((OLD/r['file']).read_bytes()).hexdigest()==r['sha256']
    metadata=(OLD/'completed_grade_metadata.html').read_text()
    assert 'vacaciones por terminación de ciclo escolar' in metadata and 'grado y nivel que acaba de aprobar' in metadata
    counts={k:Counter() for k in ['conditional_classified','transition_optional','optional']};samples=Counter();ids=set()
    with ZipFile(OLD/'Censo2020_CA_cdmx_csv.zip') as z:
        for row in csv.DictReader(io.TextIOWrapper(z.open('Personas09.CSV'),encoding='utf-8-sig')):
            assert row['ENT']=='09' and row['ID_PERSONA'] not in ids;ids.add(row['ID_PERSONA'])
            category=classify(row)
            if category is None:continue
            w=int(row['FACTOR']);assert w>0
            counts[category][row['TIE_TRASLADO_ESCU']]+=w;samples[category]+=1
    assert len(ids)==276007
    old=json.loads((P.parent/'task4_v72_mexico/summary.json').read_text())['scopes']['age14_18']
    assert dict(counts['conditional_classified']+counts['transition_optional'])==old['known'] and dict(counts['optional'])==old['optional']
    old_interval=v72.v15.optional_membership(counts['conditional_classified']+counts['transition_optional'],counts['optional'])
    new_interval=v72.v15.optional_membership(counts['conditional_classified'],counts['transition_optional']+counts['optional'])
    assert abs(old_interval[0]-old['utility_lower'])<1e-14 and abs(old_interval[1]-old['utility_upper'])<1e-14
    assert new_interval[0]<=old_interval[0] and new_interval[1]>=old_interval[1]
    return dict(year=2020,person_rows=len(ids),new_downloads=0,old_utility=old_interval,revised_utility=new_interval,
        groups={k:dict(weighted_time_bins=dict(v),sample_rows=samples[k],expanded_weight=sum(v.values())) for k,v in counts.items()},
        source_hashes={f:hashlib.sha256((OLD/f).read_bytes()).hexdigest() for f in ['Censo2020_CA_cdmx_csv.zip','completed_grade_metadata.html','school_attendance_metadata.html']},
        scope='Mexico City private-household residents, known ages14-18; unknown age/attendance/stage still optional. Completed-secondary3 no longer treated as definite current high school. Levels4/5/7 grades0-2 retain the earlier conditional stage interpretation.',
        interpretation='Widening from removing a cross-stage progression assumption, not a new estimate of misclassification. Weighted sample identification bounds, not sampling confidence intervals. No probability is assigned to optional membership.')

if __name__=='__main__':
    result=derive();(P/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
