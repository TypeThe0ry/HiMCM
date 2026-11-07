"""Reproduce the known school-record FTE lower sum; no pupil imputation."""
from pathlib import Path
import json
import pandas as pd
P=Path(__file__).resolve().parent

def main():
 a=pd.read_csv(P/'phoenix_secondary_roster.csv',dtype={'NCESSCH':str})
 non=['PK','KG']+[f'G{i:02d}' for i in range(1,9)]+['G13','UG','AE']
 a['strict_non_target_zero_or_structural_N']=a[non].isin([0,-2]).all(axis=1)
 a['strict_fte_lower_eligible']=a.within_9_12_only & a.strict_non_target_zero_or_structural_N & (a.FTE>=0)
 a.to_csv(P/'strict_teacher_fte_audit.csv',index=False)
 s=a[a.strict_fte_lower_eligible];s.to_csv(P/'strict_teacher_fte_lower_roster.csv',index=False)
 assert s.NCESSCH.is_unique and (s.FTE>=0).all() and s[non].isin([0,-2]).all().all()
 assert a.target_enrollment_upper.isna().sum()==1
 assert a.loc[a.target_enrollment_upper.isna(),'NCESSCH'].iloc[0]=='040386003535'
 out=dict(known_FTE_lower=float(s.FTE.sum()),eligible_schools=len(s),non_target_fields=non,non_target_allowed_values=[0,-2],missing_FTE_not_zero_filled=True,scope='Grade9-12-only operational nonvirtual public-school records in current Phoenix boundary; teacher FTE by school, not unique teacher headcount',conditions=['NCES -2 is structural not applicable, not unknown','FTE reporting is comparable across these schools','School-level FTE allocations are additive across schools; no duplicated full FTE assignments','Current school locations valid for reporting vintage'],school_grade9_12_student_lower=float(a.target_enrollment_lower.sum()),school_grade9_12_student_upper=None,hope_alternate_FY2025_total=1178,hope_snapshot_compatibility_verified=False,conditional_student_upper_if_compatible=float(a.target_enrollment_lower.sum())+1178,main_admission=False)
 (P/'strict_fte_bound.json').write_text(json.dumps(out,indent=2)+'\n');print(f'{len(s)} schools; FTE lower sum {s.FTE.sum():.2f}; student upper unresolved')
if __name__=='__main__':main()
