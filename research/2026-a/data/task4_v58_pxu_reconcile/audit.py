"""Localize the published cohort-total discrepancy without inferring people."""
import csv,hashlib,json
from pathlib import Path

P=Path(__file__).resolve().parent
S=P.parent/'task4_v57_school_union'

def main():
    files=json.loads((S/'refresh_manifest.json').read_text())
    data={};manifest=[]
    for item in files:
        file=S/item['file'];raw=file.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==item['sha256']
        assert len(raw)==item['bytes']
        eid=int(file.stem);records=json.loads(raw)
        assert all(r['educationOrganizationId']==eid and r['fiscalYear']==2025 for r in records)
        groups={r['studentGroupDescription']:r for r in records}
        assert len(groups)==len(records)
        data[eid]=groups
        manifest.append(dict(file='../task4_v57_school_union/'+item['file'],
                             bytes=len(raw),sha256=item['sha256'],url=item['url'],reused=True))
    district=data.pop(4286);rows=[];omitted=[]
    for eid,groups in sorted(data.items()):
        if 'All' not in groups:
            omitted.append(dict(entity_id=eid,reason='no All row; not zero'))
            continue
        counts={g:groups[g]['numInCohort'] for g in ['All','Female','Male']}
        assert all(n>=0 and n==int(n) for n in counts.values())
        assert counts['All']==counts['Female']+counts['Male']
        rows.append(dict(entity_id=eid,all_cohort=counts['All'],female_cohort=counts['Female'],male_cohort=counts['Male']))
    result=[]
    for group,col in [('All','all_cohort'),('Female','female_cohort'),('Male','male_cohort')]:
        total=sum(r[col] for r in rows);dn=district[group]['numInCohort']
        result.append(dict(group=group,school_sum=total,district_cohort=dn,difference=total-dn,contributing_entities=len(rows)))
    assert [(r['school_sum'],r['district_cohort']) for r in result]==[(6287,6285),(3118,3117),(3169,3168)]
    assert district['All']['numInCohort']==district['Female']['numInCohort']+district['Male']['numInCohort']
    with (P/'school_sex_counts.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    report=dict(cohort=2024,report_fiscal_year=2025,groups=result,omitted=omitted,
                within_entity_sex_sum_checks_passed=True,cause_identified=False,
                duplicate_person_upper_bound_identified=False,main_admitted=False)
    (P/'audit.json').write_text(json.dumps(report,indent=2)+'\n')
    (P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
