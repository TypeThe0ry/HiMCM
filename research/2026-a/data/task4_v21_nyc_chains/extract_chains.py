"""Recover transport-stop school journeys; keep other activity episodes diagnostic."""
from pathlib import Path
from zipfile import ZipFile
import sys,json,hashlib
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent
PREVIOUS=HERE.parent/'task4_v20_nyc_travel'
sys.path.insert(0,str(PREVIOUS))
from extract_commute import load_people,membership_bounds,COUNTIES
TRANSPORT_STOPS={4,5,6}  # transfer, dropped off passenger, picked up passenger


def reconstruct(trips):
    g=trips.copy()
    if g.empty:return dict(status='no_trips')
    clock=g.TRP_DEP_HR.between(0,23)&g.TRP_ARR_HR.between(0,23)&g.TRP_DEP_MIN.between(0,59.999999)&g.TRP_ARR_MIN.between(0,59.999999)
    if not clock.all():return dict(status='unknown_order')
    dep=g.TRP_DEP_HR*60+g.TRP_DEP_MIN;arr=g.TRP_ARR_HR*60+g.TRP_ARR_MIN
    g['start']=(dep-180)%1440;g['end']=g.start+g.TRPDUR
    g['duration_valid']=g.TRPDUR.gt(0)&g.TRPDUR.lt(1440)&np.isclose(g.TRPDUR,(arr-dep)%1440,rtol=0,atol=1e-8)
    g=g.sort_values(['start','PLANO']);school=g[g.DTPURP.isin([12,13])]
    if school.empty:return dict(status='no_school_purpose')
    first=school[school.start==school.start.min()]
    if len(first)!=1:return dict(status='ambiguous_school_order')
    target=first.iloc[0];prior=g[g.start<=target.start+1e-8]
    homes=prior[prior.ORIG_HOME==1]
    if homes.empty:return dict(status='no_observed_home_departure')
    latest=homes[homes.start==homes.start.max()]
    if len(latest)!=1:return dict(status='ambiguous_home_departure')
    home=latest.iloc[0];chain=prior[prior.start>=home.start-1e-8].copy()
    if chain.start.duplicated().any():return dict(status='ambiguous_chain_order')
    if not chain.duration_valid.all():return dict(status='invalid_segment_duration')
    if not (np.diff(chain.PLANO)>0).all():return dict(status='place_order_disagreement')
    if (chain.end.to_numpy()[:-1]>chain.start.to_numpy()[1:]+1e-8).any():return dict(status='overlapping_segments')
    if chain.TOUR_ID.nunique()!=1:return dict(status='different_tours')
    if chain.iloc[:-1].DEST_HOME.eq(1).any():return dict(status='unresolved_home_return')
    elapsed=float(target.end-home.start);moving=float(chain.TRPDUR.sum())
    if not 0<elapsed<1440 or moving>elapsed+1e-8:return dict(status='invalid_episode_duration')
    purposes=[int(x) for x in chain.iloc[:-1].DTPURP]
    return dict(status='reconstructed',transport_stops_only=all(x in TRANSPORT_STOPS for x in purposes),segments=len(chain),intermediate_purposes='|'.join(map(str,purposes)),elapsed_minutes=elapsed,moving_minutes=moving,stop_minutes=max(0.,elapsed-moving),home_departure_diary_minute=float(home.start),school_arrival_diary_minute=float(target.end))


def bounds_and_bootstrap(people,hh):
    known=people[people.membership=='known'];optional=people[people.membership=='optional']
    young=people.age_group.isin(['Younger than 16 years','16-18 years'])
    yknown=people[(people.membership=='known')&young];yoptional=people[((people.membership=='optional')&young)|people.age_group.eq('Age not provided')]
    ids=hh.SAMPN.to_numpy();pos={x:i for i,x in enumerate(ids)};strata=[np.flatnonzero(hh.CTFIP.to_numpy()==c) for c in COUNTIES]
    scopes=[(known,optional),(yknown,yoptional)];indices=[(np.array([pos[x] for x in k.household]),np.array([pos[x] for x in o.household])) for k,o in scopes]
    rng=np.random.default_rng(20261107);samples=[[],[]]
    for _ in range(1000):
        mult=np.bincount(np.concatenate([rng.choice(s,size=len(s),replace=True) for s in strata]),minlength=len(hh))
        for j,((k,o),(ki,oi)) in enumerate(zip(scopes,indices)):
            samples[j].append(membership_bounds(k,o,(k.weight.to_numpy()*mult[ki],o.weight.to_numpy()*mult[oi])))
    result={}
    for name,(k,o),reps in zip(['all_age','under19'],scopes,samples):
        l,h=membership_bounds(k,o);a=np.array(reps)
        result[name]=dict(known_students=len(k),optional_students=len(o),membership_lower=l,membership_upper=h,sampling_lower=min(l,float(np.quantile(a[:,0],.025))),sampling_upper=max(h,float(np.quantile(a[:,1],.975))))
    return result


def main():
    for source in json.loads((PREVIOUS/'download_manifest.json').read_text()):
        assert hashlib.sha256((PREVIOUS/source['file']).read_bytes()).hexdigest()==source['sha256']
    people,hh,_=load_people();old=people.copy(deep=True)
    with ZipFile(PREVIOUS/'CSV.zip') as z:trips=pd.read_csv(z.open('CSV/LINKED_Public.csv'),encoding='cp1252',low_memory=False)
    groups={key:g for key,g in trips.groupby(['SAMPN','PERNO'])};records=[]
    for idx,p in people[people.reason=='first_school_trip_not_from_home'].iterrows():
        result=reconstruct(groups[(p.household,p.person)])
        admitted=result['status']=='reconstructed' and result['transport_stops_only']
        records.append(dict(household=int(p.household),person=int(p.person),membership=p.membership,recovered_as_school_journey=admitted,**result))
        if admitted:
            u=float(np.exp(-result['elapsed_minutes']/30));people.loc[idx,['lower','upper']]=u
            people.loc[idx,'duration_minutes']=result['elapsed_minutes'];people.loc[idx,'reason']='observed_home_school_transport_stop_chain'
    direct=old.reason=='observed_direct_home_to_school';pd.testing.assert_frame_equal(people[direct],old[direct])
    assert np.all(people.lower>=old.lower) and np.all(people.upper<=old.upper)
    scopes=bounds_and_bootstrap(people,hh);previous=json.loads((PREVIOUS/'commute_summary.json').read_text())
    for name,current in scopes.items():
        prior=previous if name=='all_age' else previous['under19_alternative']
        assert current['membership_lower']>=prior['membership_utility_lower']-1e-12 and current['membership_upper']<=prior['membership_utility_upper']+1e-12
        assert current['sampling_lower']>=prior['sampling_envelope_lower']-1e-12 and current['sampling_upper']<=prior['sampling_envelope_upper']+1e-12
    audit=pd.DataFrame(records);audit.to_csv(HERE/'chain_audit.csv',index=False);people.to_csv(HERE/'student_journey_audit.csv',index=False)
    hashes=[dict(path=str(p.relative_to(HERE.parents[1])),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [PREVIOUS/'CSV.zip',PREVIOUS/'commute_summary.json',PREVIOUS/'extract_commute.py']]
    summary=dict(main_admitted=False,new_downloads=0,transport_purpose_codes=sorted(TRANSPORT_STOPS),recovered_known=int(((audit.membership=='known')&audit.recovered_as_school_journey).sum()),recovered_optional=int(((audit.membership=='optional')&audit.recovered_as_school_journey).sum()),diagnostic_other_activity_chains=int(((audit.status=='reconstructed')&~audit.recovered_as_school_journey).sum()),unrecovered_status_counts=audit[~audit.recovered_as_school_journey].status.value_counts().to_dict(),bootstrap_replicates=1000,seed=20261107,scopes=scopes,sources=hashes)
    (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
