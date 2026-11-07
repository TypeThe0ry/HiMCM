"""Audit official DNEMIS public parquet files; requires pandas and pyarrow."""
import hashlib,json
from pathlib import Path
import pandas as pd

P=Path(__file__).resolve().parent
STATE='H2ZhSMudlMI'
SSS='o62AI6qkSgS'

def main():
    for item in json.loads((P/'lagos_manifest.json').read_text()):
        raw=(P/item['file']).read_bytes()
        assert len(raw)==item['bytes']
        assert hashlib.sha256(raw).hexdigest()==item['sha256']
    tables={k:pd.read_parquet(P/(k+'.parquet')) for k in ['dx','ou','fact','fact_ownership','fact_schooltype','fact_typeown']}
    for key in ['fact','fact_ownership','fact_schooltype','fact_typeown']:
        d=tables[key]
        assert set(d.periodType)=={'YEARLY'} and set(d.pe.astype(float))=={2024.}
    def value(table,dx,ou=STATE,**filters):
        rows=tables[table];rows=rows[(rows.ou==ou)&(rows.dx==dx)]
        for k,v in filters.items():rows=rows[rows[k]==v]
        assert len(rows)==1,(table,dx,ou,filters,len(rows))
        v=rows.iloc[0].value;assert v>=0 and v==int(v)
        return int(v)
    n=value('fact','IYNEmLyFgbe')
    public_n=value('fact_ownership','IYNEmLyFgbe',category_name='Public')
    private_n=value('fact_ownership','IYNEmLyFgbe',category_name='Private')
    public_school_n=value('fact_schooltype','jwjKmtVK2wj',category_id=SSS)
    teacher=value('fact_schooltype','ABJrmFcIpT3',category_id=SSS)
    private_teacher_pool=value('fact_schooltype','ABJrmFcIpT3',category_name='Private')
    assert n==public_n+private_n==413720
    assert public_school_n==public_n==268413 and private_n==145307
    assert teacher==8920 and private_teacher_pool==104805
    # SSS school-type records explicitly cross-classify as public. A private
    # school-type pool is all-stage, so it cannot supply a private SSS denominator.
    s=tables['fact_typeown'];s=s[(s.ou==STATE)&(s.cat1_id==SSS)]
    assert set(s.cat2_name)=={'Public'}
    lgas=tables['ou'][tables['ou'].parent_id==STATE]
    assert len(lgas)==20
    rows=[]
    for r in lgas.to_dict('records'):
        rows.append(dict(lga_id=r['id'],lga_name=r['name'],
                         sss_enrolment=value('fact','IYNEmLyFgbe',ou=r['id']),
                         public_sss_teachers=value('fact_schooltype','ABJrmFcIpT3',ou=r['id'],category_id=SSS)))
    out=pd.DataFrame(rows)
    assert out.sss_enrolment.sum()==n and out.public_sss_teachers.sum()==teacher
    out.to_csv(P/'lagos_lga_sss.csv',index=False)
    reporting=dict(public_sss_reports=value('fact','OTZHZUXsMeN'),public_sss_expected=value('fact','jZtYw0T5xJl'),
                   private_all_stage_reports=value('fact','Jx7wWJI1WpR'),private_all_stage_expected=value('fact','q5mnwKasEpF'))
    assert reporting==dict(public_sss_reports=329,public_sss_expected=333,private_all_stage_reports=10213,private_all_stage_expected=11922)
    result=dict(geography='Lagos State, all 20 LGAs; not a verified metropolitan-city boundary',
                census_period=2024,displayed_school_year='2024/2025',
                sss_students_reported=n,public_sss_students=public_n,private_sss_students=private_n,
                public_sss_reported_teachers=teacher,private_all_stage_teacher_pool=private_teacher_pool,
                school_type_sss_is_public_in_archived_crossclassification=True,
                lga_sums_match=True,reporting=reporting,
                public_sss_arithmetic_ratio_not_admitted=public_n/teacher,
                teacher_indicator='MD: Total teachers (ABJrmFcIpT3); reporter universe alignment unresolved',
                private_sss_teacher_count_identified=False,full_population_coverage=False,
                main_admitted=False,changed_model_cells=0)
    (P/'lagos_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
