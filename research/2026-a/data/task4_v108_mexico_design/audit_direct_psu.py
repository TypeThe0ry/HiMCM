"""Check public candidate SEs independently against local PSU residuals."""
from pathlib import Path
from collections import defaultdict
import json,math
from derive_design import derive
P=Path(__file__).resolve().parent
result=derive();raw=json.loads((P/'local_only/psu_weighted_bins.json').read_text());strata=defaultdict(list)
for row in raw:strata[row['stratum']].append(row['weighted_bins'])
errors=[];count=0
for scenario in result['scenarios'].values():
 for endpoint in scenario.values():
  for candidate in endpoint['candidates']:
   a=candidate['numerator_coefficients'];b=candidate['denominator_coefficients'];r=candidate['ratio'];B=candidate['B'];variance=0.
   for vv in strata.values():
    residual=[sum((a[k]-r*b[k])*v[k] for k in range(24)) for v in vv]
    n=len(residual);mean=sum(residual)/n
    variance+=n/(n-1)*sum((v-mean)**2 for v in residual)/B**2
   se=math.sqrt(variance);errors.append(abs(se-candidate['taylor_se']));count+=1
assert max(errors)<1e-12
report={'passed':True,'candidates_checked':count,'maximum_absolute_se_difference':max(errors),'method':'Direct PSU residuals centered separately in each full observed stratum, compared with public moment-matrix quadratic form','psu_records_published':False}
(P/'audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
