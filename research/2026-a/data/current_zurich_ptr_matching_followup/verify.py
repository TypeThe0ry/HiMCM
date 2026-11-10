#!/usr/bin/env python3
"""Offline reproduction; writes only this follow-up's results directory."""
import collections,csv,hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parents[2]
data=root/'data/current_zurich_ptr_matching_followup'
out=root/'results/current_zurich_ptr_matching_followup'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
receipts=json.loads((data/'retrieval.json').read_text())
for a in receipts:
 assert (data/a['file']).stat().st_size==a['bytes'] and sha(data/a['file'])==a['sha256']
with (data/'pupils_dataset.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
selected=[x for x in rows if x['jahr']=='2024' and x['stufe']=='Sekundarstufe II']
by_type=collections.defaultdict(int); by_provider=collections.defaultdict(int)
for r in selected:
 by_type[r['schultyp']]+=int(r['anzahl']);by_provider[r['traegerschaft']]+=int(r['anzahl'])
assert dict(by_type)=={'Mittelschule':14618,'Heim- und Sonderschule':275,'Brückenangebot':2160,'Berufsfachschule':46872}
assert sum(by_type.values())==63925
result={'year':2024,'school_year':'2024/25','reference_date':'2024-09-15','geography':'schools located in canton Zürich','stage':'Sekundarstufe II','rows_selected':len(selected),'school_type_counts':dict(by_type),'provider_counts':dict(by_provider),'total':sum(by_type.values()),'role':'potential canton-wide pupil upper-bound ingredient, subject to target inclusion proof; no matched city teacher FTE lower bound','primary_admissions':0}
out.mkdir(parents=True,exist_ok=True)
(out/'extraction.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
files=[*sorted(data.iterdir()),root/'data/task4_v171_student_scope/README.md',root/'data/task4_v170_zurich/README.md',root/'results/current_swiss_staff_scope_review/verification.json',root/'data/current_zurich_fte_bound/README.md']
files=[p for p in files if p.is_file()]
v={'status':'pass: offline receipt hashes and aggregation','successful_responses':sum(x['status']==200 for x in receipts),'failed_responses':sum(x['status']!=200 for x in receipts),'extraction_sha256':sha(out/'extraction.json'),'source_sha256':{str(p.relative_to(root)):sha(p) for p in files},'new_primary_admissions':0,'ptr_computed':False,'utility_change':False}
(out/'verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
