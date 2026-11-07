"""Reproduce universe diagnostics from unchanged official V59 DNEMIS tables."""
import hashlib,json
from pathlib import Path
import pandas as pd
P=Path(__file__).resolve().parent
SRC=P.parent/'task4_v59_secondary_sources'
STATE='H2ZhSMudlMI'
def main():
    files=['fact.parquet','fact_schooltype.parquet','fact_typeown.parquet','dx.parquet','ou.parquet']
    manifests={x['file']:x for x in json.loads((SRC/'lagos_manifest.json').read_text())}
    hashes={}
    for file in files:
        hashes[file]=hashlib.sha256((SRC/file).read_bytes()).hexdigest()
        assert hashes[file]==manifests[file]['sha256']
    f=pd.read_parquet(SRC/'fact.parquet')
    t=f.pivot(index='ou',columns='dx',values='value')
    ou=pd.read_parquet(SRC/'ou.parquet').set_index('id')
    pair=t[['ABJrmFcIpT3','Dw7f4gs9RcS']].dropna()
    mismatch=pair[pair.iloc[:,0]!=pair.iloc[:,1]].join(ou.name)
    mismatch.rename(columns={'ABJrmFcIpT3':'MD_total_teachers','Dw7f4gs9RcS':'ASC_GEN_teachers'}).to_csv(P/'teacher_field_disagreements.csv')
    lga=t.loc[ou.index[ou.parent_id==STATE],['OTZHZUXsMeN','jZtYw0T5xJl','wVjDYI2HuQb','U8ytqWQMFwD','BXTUMWSq4zQ']].join(ou.name)
    lga.columns=['sss_reports','sss_expected','md_total_schools','md_public_schools','md_private_schools','name']
    lga['sss_missing_reports']=lga.sss_expected-lga.sss_reports
    lga['ownership_minus_md_total']=lga.md_public_schools+lga.md_private_schools-lga.md_total_schools
    lga.to_csv(P/'lagos_lga_universe.csv')
    s=pd.read_parquet(SRC/'fact_schooltype.parquet')
    s=s[(s.ou==STATE)&(s.category_id=='o62AI6qkSgS')].set_index('dx').value
    result={'source_sha256':hashes,'org_units_by_level':{str(int(k)):int(v) for k,v in ou.level.value_counts().items()},'school_level_rows_available':False,
            'teacher_field_comparable_units':len(pair),'teacher_field_equal_units':int((pair.iloc[:,0]==pair.iloc[:,1]).sum()),
            'lagos_MD_teachers':int(t.loc[STATE,'ABJrmFcIpT3']),'lagos_ASC_GEN_teachers':int(t.loc[STATE,'Dw7f4gs9RcS']),
            'public_sss_reported_enrolment':int(s['jwjKmtVK2wj']),'public_sss_MD_teachers':int(s['ABJrmFcIpT3']),
            'public_sss_official_ratio':float(s['eie1tIO5HtX']),'public_sss_arithmetic_ratio':float(s['jwjKmtVK2wj']/s['ABJrmFcIpT3']),
            'lagos_MD_total_schools':int(t.loc[STATE,'wVjDYI2HuQb']),
            'lagos_ownership_school_sum':int(t.loc[STATE,'U8ytqWQMFwD']+t.loc[STATE,'BXTUMWSq4zQ']),
            'lga_MD_total_schools_sum':int(lga.md_total_schools.sum()),
            'public_sss_missing_reports':int(lga.sss_missing_reports.sum()),
            'missing_public_sss_report_LGAs':lga[lga.sss_missing_reports>0]['name'].tolist(),
            'registry_teacher_universe_verified':False,'reported_only_matching_universe_verified':False,
            'finite_full_population_upper_bound_identified':False,'main_admitted':False,'changed_model_cells':0}
    assert len(pair)==770 and len(mismatch)==5
    assert result['lagos_MD_teachers']==result['lagos_ASC_GEN_teachers']==131636
    assert result['lagos_MD_total_schools']==14582 and result['lagos_ownership_school_sum']==14622
    assert result['public_sss_missing_reports']==4
    assert round(result['public_sss_arithmetic_ratio'],1)==result['public_sss_official_ratio']==30.1
    assert int(lga.ownership_minus_md_total.sum())==41
    assert result['lga_MD_total_schools_sum']==14581
    (P/'universe_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
