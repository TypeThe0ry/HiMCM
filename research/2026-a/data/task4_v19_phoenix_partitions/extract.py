"""Lower bounds on unique outcomes from disjoint demographic groups.
School overlap is unrestricted; stable cross-record category membership is conditional.
"""
from pathlib import Path
import hashlib,json,math
import pandas as pd
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'task4_v9_phoenix'
GROUPS={'sex':['Female','Male'],'race_ethnicity':['African American','Asian','Hispanic','Native American','White','Multiple Races','Pacific Islander']}


def subgroup_lower(row):
    """No suppression code becomes a count; only strict rate endpoints constrain it."""
    n=row['numInCohort'];g=row['numGraduated'];rate=row['gradRate']
    if n<0:return (int(g) if g>=0 else 0),0
    assert int(n)==n and n>=0;n=int(n)
    if 0<=g<=n:gl=gh=int(g)
    elif rate==-98:gl=math.floor(.98*n)+1;gh=n
    elif rate==-2:gl=0;gh=math.ceil(.02*n)-1
    else:gl=0;gh=n
    assert 0<=gl<=gh<=n
    return gl,n-gh


def main():
    schools=pd.read_csv(SOURCE/'expanded_known_cohort_bounds.csv')
    audit=pd.read_csv(SOURCE/'expanded_admission_audit.csv').set_index('entity_id')
    assert len(schools)==96 and schools.entity_id.is_unique
    records=[];sources=[];coverage=[]
    for school in schools.itertuples():
        source=audit.loc[school.entity_id,'source_file']
        rel=str(source) if pd.notna(source) else f'recovered/{school.entity_id}_graduation.json'
        path=SOURCE/rel;raw=json.loads(path.read_text());sources.append(dict(path=str(path.relative_to(HERE.parents[1])),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
        rows={r['studentGroupDescription']:r for r in raw};assert len(rows)==len(raw)
        assert rows['All']['numInCohort']==school.cohort
        for name,groups in GROUPS.items():
            known_n=0
            for group in groups:
                row=rows.get(group)
                if row is None:gl=fl=0
                else:
                    assert row['fiscalYear']==2025 and row['educationOrganizationId']==school.entity_id
                    gl,fl=subgroup_lower(row)
                    if row['numInCohort']>=0:known_n+=row['numInCohort']
                records.append(dict(entity_id=school.entity_id,school=school.name,partition=name,group=group,graduates_lower=gl,nongraduates_lower=fl,row_present=row is not None))
            assert known_n<=school.cohort,(school.entity_id,name,known_n,school.cohort)
            coverage.append(dict(entity_id=school.entity_id,partition=name,cohort=school.cohort,sum_unsuppressed_group_cohorts=known_n))
    frame=pd.DataFrame(records);witnesses=[];partitions=[]
    for name,groups in GROUPS.items():
        totals={'graduates_lower':0,'nongraduates_lower':0}
        for group in groups:
            subset=frame[(frame.partition==name)&(frame.group==group)]
            for metric in totals:
                row=subset.loc[subset[metric].idxmax()];v=int(row[metric]);totals[metric]+=v
                witnesses.append(dict(partition=name,group=group,metric=metric,lower=v,entity_id=int(row.entity_id),school=row.school))
        partitions.append(dict(partition=name,**totals))
    all_g=int(schools.graduates_lower.max());all_f=int((schools.cohort-schools.graduates_upper).max())
    gl=max([all_g]+[r['graduates_lower'] for r in partitions]);fl=max([all_f]+[r['nongraduates_lower'] for r in partitions])
    state_path=SOURCE/'state_graduation_2025.json';state_rows=json.loads(state_path.read_text());state=next(r for r in state_rows if r['studentGroupDescription']=='All')
    gs=state['numGraduated'];fs=state['numInCohort']-gs
    assert gl<=gs and fl<=fs
    result=dict(main_admitted=False,school_count=96,new_downloads=0,previous_unique_graduates_lower=all_g,previous_unique_nongraduates_lower=all_f,
        partitions=partitions,unique_graduates_lower=gl,unique_nongraduates_lower=fl,state_graduates=gs,state_nongraduates=fs,
        previous_quality_lower=all_g/(all_g+fs),previous_quality_upper=gs/(gs+all_f),quality_lower=gl/(gl+fs),quality_upper=gs/(gs+fl),
        assumptions=['Groups within each named partition are mutually exclusive and stable for a person across school records','Same cohort graduate status agrees across schools and statewide totals','Inherited Phoenix geography and public-school target conditions remain; current-vs-2024 school locations unresolved'],
        non_assumptions=['School records need not be disjoint','Groups need not exhaust the cohort','Different partitions are combined by maximum, never summed'])
    frame.to_csv(HERE/'subgroup_lower_counts.csv',index=False);pd.DataFrame(witnesses).to_csv(HERE/'witnesses.csv',index=False);pd.DataFrame(coverage).to_csv(HERE/'coverage_checks.csv',index=False)
    for rel in ['expanded_known_cohort_bounds.csv','expanded_admission_audit.csv','state_graduation_2025.json']:
        p=SOURCE/rel;sources.append(dict(path=str(p.relative_to(HERE.parents[1])),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    (HERE/'source_hashes.json').write_text(json.dumps(sources,indent=2)+'\n');(HERE/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
