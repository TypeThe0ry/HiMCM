"""Verify original Grade11 responses; retain suppression and uncovered populations."""
import csv,hashlib,json
from pathlib import Path
import pandas as pd
HERE=Path(__file__).resolve().parent

def main():
 for source,expected in json.loads((HERE/'reused_sources.json').read_text()).items():
  assert hashlib.sha256((HERE.parent/source).read_bytes()).hexdigest()==expected
 manifest=json.loads((HERE/'manifest.json').read_text())
 for item in manifest:
  assert item['status']=='acquired'
  p=HERE/item['file'];assert p.stat().st_size==item['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256']
 audit=pd.read_csv(HERE/'school_audit.csv',dtype={'nces_id':str,'official_nces_id':str})
 observations=pd.read_csv(HERE/'grade11_observations.csv',dtype={'nces_id':str,'grade':str})
 assert len(audit)==71 and audit.entity_id.nunique()==71 and audit.nces_id.nunique()==71
 assert not observations.duplicated(['educationOrganizationId','subject']).any()
 rebuilt=[]
 for row in audit.itertuples():
  entities=json.loads((HERE/'responses'/f'{row.entity_id}_entity.json').read_text());assert len(entities)==1
  e=entities[0];n=(str(e['leances'])+str(e['nces']).zfill(5)) if e.get('leances') is not None and e.get('nces') is not None else None
  assert row.identity_verified==(n==row.nces_id)
  assert e['educationOrganizationId']==row.entity_id
  raw=json.loads((HERE/'responses'/f'{row.entity_id}_assessment.json').read_text())
  assert all(r['educationOrganizationId']==row.entity_id and r['fiscalYear']==2025 for r in raw)
  selected=[r for r in raw if r['subgroups']=='All' and str(r['grade'])=='11' and r['type']==1]
  assert all(r['fayType']=='ALL ENROLLED' for r in selected)
  for r in selected:rebuilt.append(dict(nces_id=row.nces_id,school=row.school,identity_verified=row.identity_verified,**r))
 expected=pd.DataFrame(rebuilt)
 pd.testing.assert_frame_equal(observations,expected,check_dtype=False)
 verified=observations.loc[observations.identity_verified].copy()
 reports=[]
 for subject,d in verified.groupby('subject'):
  known=d.loc[d.numberTested.ge(0)];published=known.loc[known.percentagePassed.ge(0)];suppressed=known.loc[known.percentagePassed.lt(0)]
  assert published.percentagePassed.le(100).all()
  n=int(known.numberTested.sum());u=int(suppressed.numberTested.sum());weighted=float((published.numberTested*published.percentagePassed).sum())
  reports.append(dict(subject=subject,verified_school_rows=len(d),known_denominator_rows=len(known),unknown_denominator_rows=int(d.numberTested.lt(0).sum()),
    sum_known_test_records=n,known_denominator_suppressed_rate_rows=len(suppressed),suppressed_rate_test_record_weight=u,
    published_percent_weighted_index_lower=weighted/n,published_percent_weighted_index_upper=(weighted+100*u)/n,
    negative_number_tested_codes={str(int(k)):int(v) for k,v in d.loc[d.numberTested.lt(0),'numberTested'].value_counts().items()},
    negative_percentage_codes={str(int(k)):int(v) for k,v in d.loc[d.percentagePassed.lt(0),'percentagePassed'].value_counts().items()}))
 verified.to_csv(HERE/'verified_grade11_observations.csv',index=False)
 summary=dict(main_admitted=False,requested_fiscal_year=2025,candidate_schools=len(audit),exact_nces_matches=int(audit.identity_verified.sum()),
   matched_schools_with_grade11_results=int(verified.educationOrganizationId.nunique()),all_grade11_subject_rows=len(observations),verified_grade11_subject_rows=len(verified),
   unverified_identity=audit.loc[~audit.identity_verified,['entity_id','nces_id','school']].to_dict('records'),
   matched_schools_without_grade11_rows=audit.loc[audit.identity_verified&audit.grade11_subject_rows.eq(0),['entity_id','school','source_grade11']].to_dict('records'),
   official_entity_returned_years=sorted(audit.entity_returned_year.unique().tolist()),fiscal_years=sorted(verified.fiscalYear.unique().tolist()),
   assessment_type_labels=sorted(verified.assessmentType.unique().tolist()),subject_summaries=reports,
   index_scope='Record-count-weighted published percentage descriptor for matched rows with known tested counts only; suppressed percentages range 0–100. Not an exact underlying pass rate, pass count, distinct-pupil count, all 71-school aggregate, or city estimate. Integer percentage rounding is not verified.',
   geographic_population='Public school records matched by exact NCES ID to 2024–25 CCD current-boundary candidates; current entity endpoints return FY2026 and validate identifiers only, not historic location. Private/unmatched schools and resident catchments remain uncovered.',
   denominator='ALL ENROLLED performance records describe enrolled tested pupils under V53 frontend wording. Participation-rate rows and CCD grade 11 enrollment are not merged into this denominator.',
   source_note='All 142 responses acquired successfully from official public API; legacy AzMerit label preserved without ACT/AzSCI rebranding.')
 (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
