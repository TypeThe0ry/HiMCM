"""Current V44 raw-roster rescaling; V26 NYC verified reuse, no raw output."""
from pathlib import Path
import hashlib,importlib.util,json
import numpy as np
import pandas as pd
from scipy.stats import t as student_t
P=Path(__file__).resolve().parent
DATA=P.parent;ROOT=DATA.parent
TAUS=[15,20,30,45,60]

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    v44=DATA/'task4_v44_melbourne';sources=[]
    for r in json.loads((v44/'manifest.json').read_text()):
        path=(v44/r['file']).resolve();assert digest(path)==r['sha256']
        sources.append(dict(path=str(path.relative_to(ROOT)),sha256=r['sha256']))
    ex=DATA/'task4_school_commute_extra'
    people=pd.read_csv(ex/'person_vista_2024_2025.csv')
    journeys=pd.read_csv(ex/'journey_to_education_vista_2024_2025.csv')
    stops=pd.read_csv(v44/'stops_vista_2024_2025.csv',usecols=['stopid','hhid','persid','destplace2'])
    assert people.persid.is_unique and stops.stopid.is_unique
    roster=people[(people.studying=='Secondary')&(people.homeregion_ASGS=='Greater Melbourne')&(people.dayType=='Weekday')&(people.agegroup=='15->19')].copy()
    trips=journeys.merge(roster[['hhid','persid']],on=['hhid','persid'],validate='many_to_one')
    assert trips.start_loc.eq('FROM_HOME').all() and trips.end_loc.eq('TO_EDUCATION').all()
    np.testing.assert_allclose(trips.end_time-trips.start_time,trips.journey_elapsed_time)
    trips=trips.merge(stops,left_on=['end_stopid','hhid','persid'],right_on=['stopid','hhid','persid'],validate='many_to_one',how='left',indicator=True)
    assert trips._merge.eq('both').all()
    first=trips.sort_values(['persid','start_time','jteid']).drop_duplicates('persid')
    roster=roster.merge(first[['persid','destplace2','journey_elapsed_time']],on='persid',how='left',validate='one_to_one')
    weightcols=['perspoststratweight']+['perspoststratweight_GROUP_'+str(k) for k in range(1,11)]
    ws=roster[weightcols].to_numpy(float)
    complete=np.isfinite(ws).all(axis=1)&(ws[:,0]>0)&(ws[:,1:]>=0).all(axis=1)
    assert len(roster)==171 and complete.sum()==170
    roster=roster[complete].copy();ws=ws[complete]
    durations=pd.to_numeric(roster.journey_elapsed_time,errors='coerce').to_numpy(float)
    observed=np.isfinite(durations)&(durations>=0)&roster.destplace2.eq('Secondary School').to_numpy()
    assert observed.sum()==100 and (~observed).sum()==70
    critical=float(student_t.ppf(.975,9));out=[]
    for tau in TAUS:
        value=np.exp(-np.where(observed,durations,0)/tau)
        endpoints=[np.where(observed,value,0),np.where(observed,value,1)]
        means=[];se=[];replicates=[]
        for x in endpoints:
            mean=float(np.average(x,weights=ws[:,0]))
            reps=np.array([np.average(x,weights=ws[:,k]) for k in range(1,11)])
            means.append(mean);se.append(float(np.sqrt(.9*np.sum((reps-mean)**2))));replicates.append(reps.tolist())
        interval=[max(0,means[0]-critical*se[0]),min(1,means[1]+critical*se[1])]
        out.append(dict(tau_minutes=tau,utility_lower=means[0],utility_upper=means[1],sampling_lower=interval[0],sampling_upper=interval[1],endpoint_se=se,endpoint_replicates=replicates))
    old=json.loads((v44/'summary.json').read_text())['all_resident_secondary_age_15_19'];base=out[2]
    np.testing.assert_allclose([base['sampling_lower'],base['sampling_upper']],old['linear_sampling_envelope'],atol=1e-14,rtol=0)
    np.testing.assert_allclose(base['endpoint_replicates'],old['endpoint_replicates'],atol=1e-14,rtol=0)
    np.testing.assert_allclose([base['utility_lower'],base['utility_upper']],old['utility_identification_interval'],atol=1e-14,rtol=0)
    assert roster.journey_elapsed_time.isna().sum()==old['no_recorded_journey']==63
    # Verify archived NYC source identity before reusing its paired bootstrap.
    v26=DATA/'task4_v26_nyc_tau';nyc=json.loads((v26/'summary.json').read_text())
    for r in nyc['sources']:assert digest(ROOT/r['path'])==r['sha256']
    spec=importlib.util.spec_from_file_location('verified_nyc_tau',v26/'extract_tau.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    persons,hh,_=module.reproduce_roster()
    assert len(persons)==603 and len(hh)==5766
    nrows=[r for r in nyc['scenarios'] if r['age_scope']=='under19'];assert len(nrows)==5
    assert all(r['known_students']==460 and r['optional_students']==33 for r in nrows)
    oldnyc=json.loads((DATA/'task4_v21_nyc_chains/summary.json').read_text())['scopes']['under19']
    nbase=next(r for r in nrows if r['tau_minutes']==30)
    for key in ['sampling_lower','sampling_upper']:assert abs(nbase[key]-oldnyc[key])<1e-14
    for r in nrows:
        changed=module.rescale(persons,r['tau_minutes']);unknown=persons.duration_minutes.isna()
        np.testing.assert_array_equal(changed.loc[unknown,['lower','upper']],persons.loc[unknown,['lower','upper']])
    extras=[v44/'summary.json',v44/'extract.py',v26/'summary.json',v26/'scenarios.csv',v26/'extract_tau.py']
    sources.extend(dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in extras)
    combined=[dict(city='Melbourne',tau_minutes=r['tau_minutes'],utility_lower=r['sampling_lower'],utility_upper=r['sampling_upper'],point_lower=r['utility_lower'],point_upper=r['utility_upper']) for r in out]+[dict(city='New York',tau_minutes=r['tau_minutes'],utility_lower=r['sampling_lower'],utility_upper=r['sampling_upper'],point_lower=r['utility_lower'],point_upper=r['utility_upper']) for r in nrows]
    return dict(passed=True,main_admitted=False,scenarios=combined,melbourne_scenarios=out,melbourne_scope=dict(input_persons=171,complete_weight_persons=170,unbounded_missing_weight_persons=1,strict_full_target_interval=[0,1],verified_destination_and_duration=100,uncertain_destination_or_duration=70,no_recorded_journey=63,age='15–19, not exact14–18',geography='Greater Melbourne, not City of Melbourne municipality',membership='Current Secondary study status, weekday residents; first home-to-education journey; non-secondary/unknown destination and missing duration retained [0,1]',inference='Same V44 linear t9 jackknife endpoint envelope,10 official replicate weights,variance factor9/10; conditional complete-weight target, not simultaneous confidence coverage'),nyc_reuse=dict(source='task4_v26_nyc_tau',raw_hashes_and_v21_roster_verified=True,bootstrap_rerun=False,roster=603,observed_journeys=410,households=5766,known_under19=460,optional_under19=33,scenarios=nrows,scope='Current grade9–12, under19 with unknown ages optional; historical2010–11; same exploratory fixed-weight county-household bootstrap, not official design CI'),sources=sources)

if __name__=='__main__':
    result=run();(P/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    pd.DataFrame(result['scenarios']).to_csv(P/'scenarios.csv',index=False)
    print(json.dumps({k:v for k,v in result.items() if k not in ['sources','melbourne_scenarios']},indent=2))
