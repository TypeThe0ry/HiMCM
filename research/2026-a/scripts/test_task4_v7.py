"""Evidence-direction and microdata-integration regression checks."""
import numpy as np
import pandas as pd
from task4_v7_model import baseline,collect,apply_bounds
from task4_v5_model import CITIES,NAMES,weights,score
from task4_champion_acquisition import elimination_threshold

def main():
 l0,h0=baseline();rows=collect();l,h,audit=apply_bounds(l0,h0,rows)
 assert len([r for r in audit if r['admitted']])==4
 assert np.all(l>=l0-1e-12) and np.all(h<=h0+1e-12)
 i=CITIES.index('Istanbul');j=NAMES.index('homicide_rate')
 r=rows[(rows.city=='Istanbul')&(rows.indicator=='homicide_rate')].iloc[0]
 assert l[i,j]==0 and np.isclose(h[i,j],2/(2+r.raw_lower))
 assert np.isinf(r.raw_upper) and 0<h[i,j]<1
 hr=rows[(rows.city=='Istanbul')&(rows.indicator=='research_he_density')].iloc[0]
 assert hr.numerator==60 and np.isclose(hr.raw_lower,60/15907951*100000)
 i=CITIES.index('Mexico City');j=NAMES.index('travel')
 assert np.isclose(l[i,j],.2696298111470688) and np.isclose(h[i,j],.544893204638767)
 assert h[i,j]-l[i,j]<h0[i,j]-l0[i,j]
 for c in ['New York','Singapore','Melbourne','Phoenix']:
  i=CITIES.index(c);assert l[i,7]==l0[i,7] and h[i,7]==h0[i,7]
 i=CITIES.index('Phoenix');assert l[i,4]==0 and h[i,4]==1
 # The newly actionable Istanbul travel cutoff certifies strict exclusion.
 i=CITIES.index('Istanbul');j=NAMES.index('travel');t=elimination_threshold(l,h,weights(),i,j)
 assert np.isclose(t,.3521967321838868)
 a=h.copy();a[i,j]=t-1e-6
 rival=max(score(l,weights())[k] for k in range(len(CITIES)) if k!=i)
 assert score(a,weights())[i]<rival
 a[i,j]=t+1e-6;assert score(a,weights())[i]>rival
 # Exclude every newly transcribed record, including ones without manual in status.
 sl,sh,sa=apply_bounds(l0,h0,rows,'no_manual')
 assert {r['city'] for r in sa if r['admitted']}=={'Mexico City'}
 for flag in ['False',False,np.nan,None,'']:
  fake=rows[rows.indicator=='travel'].copy();fake['raw_data_archived']=flag
  a,b,ar=apply_bounds(l0,h0,fake)
  assert np.array_equal(a,l0) and np.array_equal(b,h0) and not ar[0]['admitted']
 # A conflicting value must raise, never silently overwrite a previous bound.
 fake=rows[rows.indicator=='travel'].copy();fake['utility_lower']=0;fake['utility_upper']=.001
 try:apply_bounds(l0,h0,fake)
 except ValueError:pass
 else:raise AssertionError('Conflict accepted')
 print('PASS: four admissions, nesting, partial-risk upper bound, Mexico microdata, preserved prior travel/Phoenix missingness, manual-source ablation, false flags, conflict rejection')
if __name__=='__main__':main()
