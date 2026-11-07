"""Regression checks for target validity and evidence-driven updates."""
import numpy as np
import pandas as pd
from task4_v5_model import build,CITIES,NAMES,weights
from task4_v6_model import inputs,admit_observations,admit_travel
from task4_champion_acquisition import certificates,selfcheck


def main():
    l0,h0,_=build();l,h,audit=admit_observations(l0,h0,inputs());l,h,ta=admit_travel(l,h)
    assert np.all(l>=l0-1e-12) and np.all(h<=h0+1e-12)
    assert np.all(l<=h)
    # FTE complete-record subset must not change Phoenix citywide headcount target.
    i=CITIES.index('Phoenix');j=NAMES.index('upper_secondary_ptr')
    assert l[i,j]==0 and h[i,j]==1
    assert l[i,NAMES.index('travel')]==0 and h[i,NAMES.index('travel')]==1
    rejected=[r for r in audit if r['city']=='Phoenix'];assert rejected and not any(r['admitted'] for r in rejected)
    for c in ['New York','Singapore','Melbourne']:
        i=CITIES.index(c);assert l[i,7]==l0[i,7] and h[i,7]==h0[i,7]
    for c in ['Istanbul','Jakarta']:
        i=CITIES.index(c);assert 0<l[i,j]==h[i,j]<1
    # Geography and years are in source rows, rather than erased on ingestion.
    assert all(r.get('scope') and r.get('source_url') and r.get('year') for r in audit)
    mi=CITIES.index('Mexico City')
    assert np.isclose(l[mi,7],0.0182157874085163) and h[mi,7]==1
    sl,sh,sa=admit_travel(l0,h0,strict_archived=True)
    assert sl[mi,7]==0 and sh[mi,7]==1 and not sa[0]['admitted']
    for r in ta:
        if r['admitted']:assert 0<float(r['utility_lower'])<float(r['utility_upper'])<=1
    # Acquisition explores hypothetical outcomes without changing evidence arrays.
    lcopy=l.copy();hcopy=h.copy()
    cert,_=certificates(l,h,weights(),NAMES,CITIES)
    assert np.array_equal(l,lcopy) and np.array_equal(h,hcopy)
    phoenix=next(r for r in cert if r['city']=='Phoenix')
    assert phoenix['minimum_city_local_exact_measurements']==4
    for flag in ['False',False,np.nan,'',None]:
        fake=pd.DataFrame([dict(city='Phoenix',indicator='travel',mapping_robust=flag,
                                status='conditional_manual_primary_index',utility_lower=.2,utility_upper=1)])
        a,b,records=admit_travel(l0,h0,frame=fake)
        assert np.array_equal(a,l0) and np.array_equal(b,h0) and not records[0]['admitted']
    selfcheck()
    print('PASS: V5→V6 evidence nesting, Phoenix rejected FTE subset, inherited genuine travel, new PTRs, provenance, no hypothetical-data mutation')
if __name__=='__main__':main()
