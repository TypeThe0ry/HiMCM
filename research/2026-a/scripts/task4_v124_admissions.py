"""Freeze reviewed V124 missing-cell supplements; preserve all V121 bounds."""
import hashlib,json
from task4_user_city_indicators import SOURCE
from task4_user_v121_revision import revised_bounds
from task4_v5_model import ROOT,NAMES,SPEC

DIRECTORIES=['task4_v124_madrid','task4_v124_transport']
EXPECTED={('Madrid','public_transport_density'),('Tokyo','public_pool_density')}
def main():
    frame,lo,hi=revised_bounds();rows=[];files=[]
    for name in DIRECTORIES:
        directory=ROOT/'data'/name
        for candidate in json.loads((directory/'observations.json').read_text()):
            row=dict(candidate);row.pop('candidate_only',None)
            key=(row['city'],row['indicator']);assert key in EXPECTED
            i=frame.city.tolist().index(key[0]);j=NAMES.index(key[1]);assert (lo[i,j],hi[i,j])==(0,1)
            assert row['lower_bound_only'] and row['raw_count']>0
            assert int(frame.iloc[i].population)==row['population']
            x=row['raw_count']*100000/row['population'];utility=x/(SPEC[j][2]+x)
            assert abs(utility-row['utility_after'][0])<1e-12 and row['utility_after'][1]==1
            row['admissible']='conditional_inventory_lower_bound';row['candidate_file']=str((directory/'observations.json').relative_to(ROOT));rows.append(row)
        files.extend(p for p in directory.iterdir() if p.is_file() and p.suffix not in {'.md','.pyc'})
    assert {(r['city'],r['indicator']) for r in rows}==EXPECTED and len(rows)==len(EXPECTED)
    files.extend(ROOT/p for p in ['design/task4_user_v121_admissions.json','scripts/task4_user_v121_revision.py',
        'scripts/task4_user_v124_revision.py','scripts/task4_v124_admissions.py','scripts/task4_v5_model.py',
        'scripts/task4_user_city_indicators.py','scripts/task4_interval_decision.py','scripts/task4_ahp_mc_baseline.py'])
    manifest=dict(version='V124',baseline='V121 user16',access_date='2026-11-09',input_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        source_policy='All139 V121 nonfullymissing cells, original CSV, weights and anchors preserved; only2 fullymissing facility cells supplemented.',
        scope='Madrid2026 registered metro subset and Tokyo2026 open municipal indoor-pool subset; fixed original population denominators; lower bounds only, not2025 same-year or all-provider inventories. No school-travel, unmatched teacher ratio, fabricated preference or finite facility upper bound.',
        observations=rows,source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(files))})
    assert manifest['input_sha256']=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
    (ROOT/'design/task4_user_v124_admissions.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print('Reviewed observations:',len(rows),'source hashes:',len(manifest['source_hashes']))
if __name__=='__main__':main()
