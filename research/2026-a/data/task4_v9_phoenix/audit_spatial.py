"""Entity-level exclusions and bounded graduation of available spatial subset."""
import json,math
from pathlib import Path
import pandas as pd
P=Path(__file__).resolve().parent

def main():
    groups={}
    for r in json.loads((P/'phoenix_search.json').read_text()):
        if r['searchTermTypeId']==1:groups.setdefault(r['educationOrganizationId'],set()).add(r['type'])
    d=pd.read_csv(P/'spatial_outcome_audit.csv');assert d.entity_id.is_unique
    d['all_types']=d.entity_id.map(lambda i:'|'.join(sorted(str(t) for t in groups[i])))
    d['excluded_type']=d.entity_id.map(lambda i:bool(groups[i]&{'Online School','Private School'}))
    rows=[]
    for r in d.to_dict('records'):
        n=r.get('numInCohort');g=r.get('numGraduated');rate=r.get('gradRate')
        if r['excluded_type'] or r.get('all_rows')!=1 or not pd.notna(n) or n<=0:continue
        n=int(n)
        if pd.notna(g) and 0<=g<=n:l=h=int(g)
        elif rate==-98:l=math.floor(.98*n)+1;h=n
        elif rate==-2:l=0;h=math.ceil(.02*n)-1
        else:l=0;h=n
        assert 0<=l<=h<=n
        rows.append(dict(entity_id=r['entity_id'],name=r['name'],cohort=n,graduates_lower=l,graduates_upper=h))
    d.to_csv(P/'spatial_admission_audit.csv',index=False);pd.DataFrame(rows).to_csv(P/'spatial_known_cohort_bounds.csv',index=False)
    n=sum(r['cohort'] for r in rows);l=sum(r['graduates_lower'] for r in rows);h=sum(r['graduates_upper'] for r in rows)
    s=dict(candidate_entities=len(d),excluded_online_or_private=int(d.excluded_type.sum()),known_cohort_schools=len(rows),known_cohort=n,graduates_lower=l,graduates_upper=h,subset_rate_lower=l/n if n else None,subset_rate_upper=h/n if n else None,citywide_admission=False)
    (P/'spatial_bounds_summary.json').write_text(json.dumps(s,indent=2));print(s)
if __name__=='__main__':main()
