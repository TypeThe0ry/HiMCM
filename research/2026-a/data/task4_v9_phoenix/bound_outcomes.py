"""Bound graduation for matched schools with known cohort counts only."""
import json,math
from pathlib import Path
import pandas as pd
P=Path(__file__).resolve().parent

def main():
    d=pd.read_csv(P/'school_outcome_audit.csv');rows=[]
    for r in d.to_dict('records'):
        n=r.get('numInCohort');g=r.get('numGraduated');rate=r.get('gradRate')
        if not pd.notna(n) or n<=0:continue
        assert int(n)==n;n=int(n)
        if pd.notna(g) and 0<=g<=n:lo=hi=int(g);kind='observed_count'
        elif rate==-98:lo=math.floor(.98*n)+1;hi=n;kind='rate_gt98'
        elif rate==-2:lo=0;hi=math.ceil(.02*n)-1;kind='rate_lt2'
        else:lo=0;hi=n;kind='suppressed_count_unrestricted'
        assert 0<=lo<=hi<=n
        rows.append(dict(entity_id=r['entity_id'],name=r['name'],cohort=n,graduates_lower=lo,graduates_upper=hi,kind=kind))
    n=sum(r['cohort'] for r in rows);l=sum(r['graduates_lower'] for r in rows);h=sum(r['graduates_upper'] for r in rows)
    s=dict(schools=len(rows),cohort=n,graduates_lower=l,graduates_upper=h,rate_lower=l/n,rate_upper=h/n,citywide_admission=False)
    pd.DataFrame(rows).to_csv(P/'known_cohort_school_bounds.csv',index=False)
    (P/'known_cohort_bounds.json').write_text(json.dumps(s,indent=2));print(s)
if __name__=='__main__':main()
