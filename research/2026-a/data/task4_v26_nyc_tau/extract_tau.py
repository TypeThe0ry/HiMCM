"""Direct NYC V21 diary rescaling; fixed membership and paired bootstrap draws."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import sys
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
V21=HERE.parent/'task4_v21_nyc_chains'
V20=HERE.parent/'task4_v20_nyc_travel'
sys.path.insert(0,str(V21))
from extract_chains import reconstruct,bounds_and_bootstrap,load_people
TAUS=(15,20,30,45,60)


def rescale(people,tau):
    if not np.isfinite(tau) or tau<=0:
        raise ValueError('Positive finite tau required')
    frame=people.copy(deep=True)
    observed=frame.duration_minutes.notna()
    assert frame.loc[observed,'duration_minutes'].gt(0).all()
    assert frame.loc[~observed,'lower'].eq(0).all() and frame.loc[~observed,'upper'].eq(1).all()
    frame.loc[observed,'lower']=np.exp(-frame.loc[observed,'duration_minutes']/tau)
    frame.loc[observed,'upper']=frame.loc[observed,'lower']
    return frame


def reproduce_roster():
    for source in json.loads((V20/'download_manifest.json').read_text()):
        assert hashlib.sha256((V20/source['file']).read_bytes()).hexdigest()==source['sha256']
    people,hh,audit=load_people()
    selected=people.reason.eq('first_school_trip_not_from_home')
    keys=pd.MultiIndex.from_frame(people.loc[selected,['household','person']])
    with ZipFile(V20/'CSV.zip') as z:
        trips=pd.read_csv(z.open('CSV/LINKED_Public.csv'),encoding='cp1252',low_memory=False)
    keep=pd.MultiIndex.from_frame(trips[['SAMPN','PERNO']]).isin(keys)
    groups={key:g for key,g in trips[keep].groupby(['SAMPN','PERNO'])}
    recovered=0
    for idx,p in people[selected].iterrows():
        chain=reconstruct(groups[(p.household,p.person)])
        if chain['status']=='reconstructed' and chain['transport_stops_only']:
            people.loc[idx,'duration_minutes']=chain['elapsed_minutes']
            people.loc[idx,'lower']=people.loc[idx,'upper']=np.exp(-chain['elapsed_minutes']/30)
            people.loc[idx,'reason']='observed_home_school_transport_stop_chain'
            recovered+=1
    archived=pd.read_csv(V21/'student_journey_audit.csv')
    for col in ['household','person','county','membership','age_group','reason']:
        np.testing.assert_array_equal(people[col],archived[col])
    for col in ['weight','lower','upper','duration_minutes']:
        np.testing.assert_allclose(people[col],archived[col],rtol=0,atol=1e-12,equal_nan=True)
    assert recovered==8 and len(people)==603 and len(hh)==5766
    assert people.duration_minutes.notna().sum()==410
    return people,hh,audit


def main():
    people,hh,audit=reproduce_roster()
    baseline=json.loads((V21/'summary.json').read_text())['scopes']
    scenarios=[]
    for tau in TAUS:
        frame=rescale(people,tau)
        result=bounds_and_bootstrap(frame,hh)
        for scope,row in result.items():
            if tau==30:
                for key in ['membership_lower','membership_upper','sampling_lower','sampling_upper']:
                    assert abs(row[key]-baseline[scope][key])<1e-12,(scope,key)
            scenarios.append(dict(tau_minutes=tau,age_scope=scope,known_students=row['known_students'],
                optional_students=row['optional_students'],utility_lower=row['membership_lower'],
                utility_upper=row['membership_upper'],sampling_lower=row['sampling_lower'],sampling_upper=row['sampling_upper']))
    # Every individual utility increases with tau; paired-draw bounds do too.
    for scope in ['all_age','under19']:
        rows=[s for s in scenarios if s['age_scope']==scope]
        for key in ['utility_lower','utility_upper','sampling_lower','sampling_upper']:
            assert np.all(np.diff([s[key] for s in rows])>=-1e-12)
    paths=[V20/'CSV.zip',V20/'download_manifest.json',V20/'extract_commute.py',V21/'extract_chains.py',
           V21/'student_journey_audit.csv',V21/'summary.json']
    sources=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths]
    summary=dict(main_admitted=False,new_downloads=0,year='2010–2011',school_stage='current grade9–12; original V21 membership retained',
        method='Rebuild V21 direct and transport-stop journeys from raw archive, exp(-observed duration/tau); retain missing[0,1] and exact optional-membership extrema.',
        sampling_method='Same V21 exploratory household bootstrap within county; all5766 NYC sampled households; fixed finalweights; not official design-based CI.',
        bootstrap_replicates=1000,seed=20261107,paired_draws_across_tau=True,source_audit=audit,
        roster_people=len(people),observed_journeys=int(people.duration_minutes.notna().sum()),
        missing_journeys=int(people.duration_minutes.isna().sum()),households_resampled=len(hh),sources=sources,scenarios=scenarios,
        caveats=['Historical evidence, not2026 conditions or GPS','School-purpose and grade identity retain V21 qualifications',
                 'Under19 retains unknown ages as optional; not exact14–18','Official design, reraking and replicateweights unavailable; exploratory sampling only'])
    (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    pd.DataFrame(scenarios).to_csv(HERE/'scenarios.csv',index=False)
    print(pd.DataFrame(scenarios).to_string(index=False))

if __name__=='__main__':main()
