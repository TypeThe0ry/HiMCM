"""Reported school journeys of NYC current grade9–12 students, RHTS2010/11.
Retain non-observed journeys and uncertain membership; no adult commuter proxy.
"""
from pathlib import Path
from zipfile import ZipFile
import hashlib,json
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent
COUNTIES={36005:'Bronx',36047:'Brooklyn (Kings)',36061:'Manhattan (New York)',36081:'Queens',36085:'Staten Island (Richmond)'}
STUDENTS=['Yes - Full Time','Yes - Part Time']


def membership_bounds(known,optional,weights=None):
    """Exact weighted ratio extrema over optional person inclusion, all prefixes."""
    w=known.weight.to_numpy() if weights is None else weights[0]
    ow=optional.weight.to_numpy() if weights is None else weights[1]
    denominator=w.sum();assert denominator>0
    result=[]
    for col,reverse in [('lower',False),('upper',True)]:
        numerator=np.dot(w,known[col]);base=numerator/denominator
        idx=np.argsort(optional[col].to_numpy(),kind='stable')
        if reverse:idx=idx[::-1]
        ratios=(numerator+np.cumsum(ow[idx]*optional[col].to_numpy()[idx]))/(denominator+np.cumsum(ow[idx]))
        candidates=np.r_[base,ratios];result.append(float(candidates.max() if reverse else candidates.min()))
    return result


def load_people():
    with ZipFile(HERE/'CSV.zip') as z:
        hh=pd.read_csv(z.open('CSV/HH_Public.csv'),encoding='cp1252',low_memory=False)
        per=pd.read_csv(z.open('CSV/PER_Public.csv'),encoding='cp1252',low_memory=False)
        trips=pd.read_csv(z.open('CSV/LINKED_Public.csv'),encoding='cp1252',low_memory=False)
    assert hh.SAMPN.is_unique and not per.duplicated(['SAMPN','PERNO']).any()
    assert not trips.duplicated(['SAMPN','PERNO','TOUR_ID','LTRIPNO']).any()
    assert not trips.duplicated(['SAMPN','PERNO','PLANO']).any()
    # Link keys also prove every journey belongs to a known roster member.
    joined=trips[['SAMPN','PERNO']].merge(per[['SAMPN','PERNO']],on=['SAMPN','PERNO'],how='left',indicator=True,validate='many_to_one')
    assert joined._merge.eq('both').all()
    per=per.merge(hh[['SAMPN','CTFIP','DOW','HH_WHT2']],on='SAMPN',validate='many_to_one',suffixes=('','_hh'))
    assert np.allclose(per.HH_WHT2,per.HH_WHT2_hh,rtol=1e-7,atol=1e-8)
    city=per[per.CTFIP.isin(COUNTIES)].copy()
    assert all(city.HFIPS==city.CTFIP.map(COUNTIES)) and city.DOW.between(1,5).all()
    known=city.STUDE.isin(STUDENTS)&city.SCHOL.eq('Grade 9 to 12')&~city.SLOC.eq('Yes')
    optional=(city.STUDE.isin(STUDENTS)&(city.SCHOL.isna()|city.SCHOL.isin(['RF','DK','Other (Specify)'])))|city.STUDE.isin(['RF','DK'])
    optional=optional&~city.SLOC.eq('Yes')&~known
    people=city[known|optional].copy();people['membership']=np.where(known.loc[people.index],'known','optional')
    assert np.isfinite(people.HH_WHT2).all() and (people.HH_WHT2>0).all()
    keys=set(zip(people.SAMPN,people.PERNO))
    school=trips[trips.DTPURP.isin([12,13])].copy()
    school=school[[k in keys for k in zip(school.SAMPN,school.PERNO)]]
    dep=school.TRP_DEP_HR*60+school.TRP_DEP_MIN;arr=school.TRP_ARR_HR*60+school.TRP_ARR_MIN
    valid_clock=school.TRP_DEP_HR.between(0,23)&school.TRP_ARR_HR.between(0,23)&school.TRP_DEP_MIN.between(0,59.999999)&school.TRP_ARR_MIN.between(0,59.999999)
    school['valid_clock']=valid_clock
    school['departure_in_diary']=(dep-180)%1440  # travel day begins at03:00
    school['valid_duration']=valid_clock&school.TRPDUR.gt(0)&school.TRPDUR.lt(1440)&np.isclose(school.TRPDUR,(arr-dep)%1440,rtol=0,atol=1e-8)
    grouped={key:g for key,g in school.groupby(['SAMPN','PERNO'])};records=[]
    for p in people.itertuples():
        g=grouped.get((p.SAMPN,p.PERNO));lower=0.;upper=1.;duration=None;reason='no_reported_school_trip';same_school_taz=None
        if g is not None:
            if not g.valid_clock.all():reason='unknown_trip_order'
            else:
                first=g[g.departure_in_diary==g.departure_in_diary.min()]
                if len(first)!=1:reason='tied_first_school_trip'
                else:
                    row=first.iloc[0]
                    if row.ORIG_HOME!=1:reason='first_school_trip_not_from_home'
                    elif not row.valid_duration:reason='invalid_duration_or_clock'
                    else:
                        duration=float(row.TRPDUR);lower=upper=float(np.exp(-duration/30));reason='observed_direct_home_to_school'
                        school_taz=pd.to_numeric(p.STAZ,errors='coerce');destination_taz=pd.to_numeric(row.DTAZ,errors='coerce')
                        same_school_taz=bool(pd.notna(school_taz) and school_taz>0 and school_taz==destination_taz)
        records.append(dict(household=int(p.SAMPN),person=int(p.PERNO),county=int(p.CTFIP),membership=p.membership,age_group=p.AGE_R,student_status=p.STUDE,school_type=p.SCHOL,weight=float(p.HH_WHT2),lower=lower,upper=upper,duration_minutes=duration,reason=reason,same_school_taz=same_school_taz))
    audit=dict(households=len(hh),persons=len(per),linked_trips=len(trips),nyc_roster_persons=len(city),current_high_school_before_home_exclusion=int((city.STUDE.isin(STUDENTS)&city.SCHOL.eq('Grade 9 to 12')).sum()),homeschool_high_school_excluded=int((city.STUDE.isin(STUDENTS)&city.SCHOL.eq('Grade 9 to 12')&city.SLOC.eq('Yes')).sum()),invalid_short_trip_key_duplicates=int(trips.duplicated(['SAMPN','PERNO','LTRIPNO']).sum()))
    return pd.DataFrame(records),hh[hh.CTFIP.isin(COUNTIES)],audit


def main():
    for source in json.loads((HERE/'download_manifest.json').read_text()):
        assert hashlib.sha256((HERE/source['file']).read_bytes()).hexdigest()==source['sha256']
    people,hh,audit=load_people();known=people[people.membership=='known'];optional=people[people.membership=='optional']
    lower=float(np.dot(known.weight,known.lower)/known.weight.sum());upper=float(np.dot(known.weight,known.upper)/known.weight.sum())
    ml,mh=membership_bounds(known,optional)
    # Exploratory household bootstrap within residence county, ALL sampled households.
    ids=hh.SAMPN.to_numpy();positions={x:i for i,x in enumerate(ids)}
    kp=np.array([positions[x] for x in known.household]);op=np.array([positions[x] for x in optional.household])
    strata=[np.flatnonzero(hh.CTFIP.to_numpy()==county) for county in COUNTIES]
    young=people.age_group.isin(['Younger than 16 years','16-18 years'])
    young_known=people[(people.membership=='known')&young]
    young_optional=people[((people.membership=='optional')&young)|people.age_group.eq('Age not provided')]
    ykp=np.array([positions[x] for x in young_known.household]);yop=np.array([positions[x] for x in young_optional.household])
    yml,ymh=membership_bounds(young_known,young_optional)
    rng=np.random.default_rng(20261107);reps=[];young_reps=[]
    for _ in range(1000):
        sampled=np.concatenate([rng.choice(s,size=len(s),replace=True) for s in strata]);mult=np.bincount(sampled,minlength=len(hh))
        reps.append(membership_bounds(known,optional,(known.weight.to_numpy()*mult[kp],optional.weight.to_numpy()*mult[op])))
        young_reps.append(membership_bounds(young_known,young_optional,(young_known.weight.to_numpy()*mult[ykp],young_optional.weight.to_numpy()*mult[yop])))
    reps=np.array(reps);sl=min(ml,float(np.quantile(reps[:,0],.025)));sh=max(mh,float(np.quantile(reps[:,1],.975)))
    result=dict(main_admitted=False,year='2010–2011',school_stage_directly_observed=True,raw_audit=audit,known_students=len(known),optional_students=len(optional),known_weight=float(known.weight.sum()),optional_weight=float(optional.weight.sum()),known_reason_counts=known.reason.value_counts().to_dict(),optional_reason_counts=optional.reason.value_counts().to_dict(),known_age_counts=known.age_group.value_counts().to_dict(),known_direct_same_school_taz=int(known.same_school_taz.eq(True).sum()),known_stage_utility_lower=lower,known_stage_utility_upper=upper,membership_utility_lower=ml,membership_utility_upper=mh,sampling_envelope_lower=sl,sampling_envelope_upper=sh,bootstrap_replicates=1000,seed=20261107,nyc_households_resampled=len(hh),kish_person_weight_n=float(known.weight.sum()**2/(known.weight**2).sum()),
        caveats=['Historical actual reported trips, not current2026 travel or GPS tracks','School-purpose codes12class/study and13other school activity define journeys; usual-school identity is not verified by these purpose codes','One first school-bound linked trip per currentgrade9–12 non-homeschooled NYC roster member; missing/indirect journeys remain[0,1]','Unknown attendance or stage and Other school-type membership may be optional; unknown homeschooled status is not resolved','All-age current-high-school cohort, including reported adult and unknown ages; age is not used as a proxy for school stage','Household bootstrap within county is exploratory, not official design-based confidence; fixed finalweights, no original poststratification reraking or replicateweights','Replacement alternative for2013–14 modeled routing estimate, not an intersection across years'])
    yr=np.array(young_reps)
    result['under19_alternative']=dict(known_students=len(young_known),optional_students=len(young_optional),known_weight=float(young_known.weight.sum()),optional_weight=float(young_optional.weight.sum()),membership_utility_lower=yml,membership_utility_upper=ymh,sampling_envelope_lower=min(yml,float(np.quantile(yr[:,0],.025))),sampling_envelope_upper=max(ymh,float(np.quantile(yr[:,1],.975))),scope='Currentgrade9–12 with known age<19; unknown ages retained as optional members; no lower age cutoff inferred')
    people.to_csv(HERE/'student_journey_audit.csv',index=False);(HERE/'commute_summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
