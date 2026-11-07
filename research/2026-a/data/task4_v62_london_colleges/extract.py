"""Verify new FEWDC provider data and official location matching; no imputation."""
from pathlib import Path
import hashlib,json
import pandas as pd
P=Path(__file__).resolve().parent
for r in json.loads((P/'manifest.json').read_text()):
    raw=(P/r['file']).read_bytes()
    assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
f=pd.read_csv(P/'provider_workforce.csv');g=pd.read_csv(P/'ofsted_provider_location.csv')
assert len(f)==60360
x=f[(f.time_period==202425)&(f.main_role_type=='Teacher')&(f.contract_type=='Total')&f.provider_type.isin(['Sixth Form College','School Based Providers'])]
assert not x.provider_ukprn.duplicated().any()
z=x.merge(g,left_on='provider_ukprn',right_on='Provider UKPRN',validate='one_to_one')
z=z[z.Region=='London'].copy()
expected={10001416:92,10003899:141,10005859:87,10006135:62,10006148:54,10008007:60,10039420:68,10046350:25,10087582:78}
assert z.set_index('provider_ukprn').number_staff_hc.to_dict()==expected
cols=['provider_ukprn','provider_name','provider_type','number_staff_hc','Local authority','Provider URN']
z[cols].to_csv(P/'london_provider_matches.csv',index=False)
assert z.number_staff_hc.sum()==667
out=dict(academic_year='2024/25',source_rows=len(f),matched_provider_count=len(z),
    reported_teacher_main_role_sum=667,city_unique_teacher_count_identified=False,
    stage_specific_teacher_count_identified=False,matched_same_year_stage_students=False,
    complete_city_provider_universe_verified=False,main_admitted=False,changed_model_cells=0,
    matching='Exact UKPRN one-to-one with Ofsted July2025 provider location; Region London. No name-based matching.',
    limitations=['Provider headquarters location can differ from staff sites.',
      'Sixth Form College or School Based Provider type does not prove all teaching is upper-secondary.',
      'Provider headcounts are not a deduplicated city total.',
      'Zero source cells may reflect incomplete submission, not an observed absence.',
      'Matched set is an inspected-provider subset, not a complete city census.',
      'No same-reference-date total city upper-secondary pupil denominator established.'])
(P/'audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
