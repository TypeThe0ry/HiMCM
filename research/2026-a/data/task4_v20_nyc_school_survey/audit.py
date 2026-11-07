"""Verify actual CMS2024 school-type/diary coverage; do not infer minor travel."""
from pathlib import Path
import csv,gzip,hashlib,json,collections
HERE=Path(__file__).resolve().parent

def main():
    manifest=json.loads((HERE/'manifest.json').read_text())
    for filename,record in manifest['files'].items():
        data=(HERE/filename).read_bytes();assert hashlib.sha256(data).hexdigest()==record['sha256']
        if filename.endswith('.gz'):assert hashlib.sha256(gzip.decompress(data)).hexdigest()==record['uncompressed_sha256']
    with (HERE/'person_2024.csv').open(newline='') as f:people=list(csv.DictReader(f))
    persons={r['person_id']:r for r in people};assert len(persons)==len(people)==8569
    trips=collections.Counter();ids=set()
    with gzip.open(HERE/'trip_2024.csv.gz','rt',newline='') as f:
        for row in csv.DictReader(f):
            assert row['person_id'] in persons
            assert row['trip_id'] not in ids;ids.add(row['trip_id']);trips[row['person_id']]+=1
    assert len(ids)==115920
    hs=[r for r in people if r['school_type']=='7'];assert len(hs)==365
    groups=collections.defaultdict(lambda:dict(persons=0,positive_person_weights=0,people_with_own_trips=0,own_trip_rows=0))
    for r in hs:
        key=(r['age'],r['is_participant']);group=groups[key];group['persons']+=1
        group['positive_person_weights']+=float(r['person_weight_citywide'].replace(',',''))>0
        group['people_with_own_trips']+=trips[r['person_id']]>0
        group['own_trip_rows']+=trips[r['person_id']]
    result=dict(main_admitted=False,person_rows=len(people),trip_rows=len(ids),current_high_school_roster_members=len(hs),
        age_codes={'2':'5-15','3':'16-17','4':'18-24'},current_school_type_code=7,
        groups=[dict(age_code=k[0],is_participant=k[1],**v) for k,v in sorted(groups.items())],
        definition_source='cms_dictionary_2024.xlsx, Column Information: school_type, age, is_participant, person_weight_citywide',
        conclusion='All 286 current high-school minors lack own trip diaries and have zero person weights. Only35 adult high-school participants have positive person weights and own trips. These adult diaries cannot replace all-high-school travel utility.',
        household_companions='Household-member accompaniment flags occur in adult trips but do not alone identify each child school destination or establish a child-weighted diary sample; not treated as independent child diaries.')
    assert sum(r['own_trip_rows'] for r in result['groups'])==1234
    assert all(r['own_trip_rows']==0 and r['positive_person_weights']==0 for r in result['groups'] if r['age_code'] in ['2','3'])
    (HERE/'coverage_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
