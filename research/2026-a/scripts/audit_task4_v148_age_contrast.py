"""Verify coupled bounds without the producer's stationary-point formula."""
from pathlib import Path
import csv,hashlib,json,math
R=Path(__file__).resolve().parents[1];O=R/'results/task4_v148_age_contrast'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 s=json.loads((O/'summary.json').read_text());d=json.loads((R/'data/task4_v116_ibb/aggregate_results.json').read_text());g=d['age_groups'];e=d['age_groups_optional_membership'];a=g['14–15'];b=g['16–18'];T=e['14–15']['weight_optional_unknown_age'];assert T==e['16–18']['weight_optional_unknown_age']==612
 A=a['weight_total']+e['14–15']['weight_optional_known_age'];B=b['weight_total']+e['16–18']['weight_optional_known_age'];na=a['utility_known_numerator'];nb=b['utility_known_numerator'];ua=a['weight_unknown']+e['14–15']['weight_optional_known_age'];ub=b['weight_unknown']+e['16–18']['weight_optional_known_age']
 # The low contrast is convex; the high contrast is concave on [0,T].
 # Endpoint derivative signs establish the exact constrained optima at x=T.
 ca=A-na-ua;cb=B-nb-ub;assert ca>0 and cb>0
 dl=-na/(A+T)**2+cb/B**2;dh=ca/(A+T)**2-nb/B**2;assert dl<0<dh
 expected=[na/(A+T)-(nb+ub)/B,(na+ua+T)/(A+T)-nb/B]
 for x,y in zip(expected,s['joint_difference_closure']):assert abs(x-y)<1e-14
 # Independently enumerate a triangular grid, including unused shared mass:
 # younger allocation x, older allocation y, x+y<=T. No shared mass is duplicated.
 count=0;minimum=1;maximum=-1
 for i in range(101):
  x=T*i/100
  for j in range(101-i):
   y=T*j/100;lo=na/(A+x)-(nb+ub+y)/(B+y);hi=(na+ua+x)/(A+x)-nb/(B+y)
   assert lo>=expected[0]-1e-14 and hi<=expected[1]+1e-14
   minimum=min(minimum,lo);maximum=max(maximum,hi);count+=1
 assert abs(minimum-expected[0])<1e-14 and abs(maximum-expected[1])<1e-14
 rows=list(csv.DictReader((O/'witnesses.csv').open()));assert len(rows)==2
 for r in rows:
  x=float(r['shared_mass_younger']);y=float(r['shared_mass_older']);qy=float(r['unknown_utility_younger']);qo=float(r['unknown_utility_older']);assert x==T and y==0 and 0<qy<1 and 0<qo<1
  yy=(na+qy*(ua+x))/(A+x);oo=(nb+qo*(ub+y))/(B+y)
  for val,key in [(yy,'mean_utility_younger'),(oo,'mean_utility_older'),(yy-oo,'difference')]:assert abs(val-float(r[key]))<1e-14
  assert (yy>oo)==(r['witness']=='younger_higher')
  for q,key in [(qy,'unknown_duration_younger_minutes'),(qo,'unknown_duration_older_minutes')]:assert abs(math.exp(-float(r[key])/30)-q)<1e-14
 assert expected[0]<0<expected[1] and s['naive_marginal_subtraction'][0]<expected[0] and expected[1]<s['naive_marginal_subtraction'][1]
 frozen={}
 for name,key in [('design/task4_user_v136_snapshot.json','source_sha256'),('results/task4_v137_revision/audit.json','result_sha256'),('results/task4_v138_priority/summary.json','source_sha256')]:frozen.update(json.loads((R/name).read_text())[key])
 for n,h in frozen.items():assert sha(R/n)==h,n
 for n,h in s['source_sha256'].items():assert sha(R/n)==h,n
 assert sha(R/'scripts/task4_v148_age_contrast.py')==s['generator_sha256'] and sha(O/'witnesses.csv')==s['witnesses_sha256']
 result=dict(status='pass',joint_difference_closure=expected,analytic_certificate='Low contrast convex with derivative negative at T; high contrast concave with derivative positive at T. Optional endpoint inclusion improves the relevant contrast, so exclusion cannot improve extrema.',allocation_grid_points=count,finite_interior_witnesses=len(rows),closure_not_finite_zero_trips=True,primary_data_admissions=0,protected_scientific_files=len(frozen),protected_scientific_sha256=frozen,result_sha256={str(p.relative_to(R)):sha(p) for p in [O/'summary.json',O/'witnesses.csv']},verifier_sha256=sha(Path(__file__)),scope='Independent aggregate-set calculation; not raw-person revalidation, exact ages, preferences, significance, causal age effects or current-year estimates.')
 (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print('Verified analytic signs,',count,'allocation-grid points and two finite interior witnesses;',len(frozen),'scientific files unchanged.')
if __name__=='__main__':main()
