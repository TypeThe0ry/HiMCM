"""Current-secondary roster bounds from archived official VISTA 2024--25.
Positive official person weights define the conditional analysis population.
No travel record is assigned [0,1]; no-weight people remain explicitly unweighted.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import t as student_t

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'task4_school_commute_extra'
TRANSPORT_PURPOSES={'Education','Change Mode','Accompany Someone','Pick-up or Drop-off Someone'}


def weighted_bounds(lower,upper,weight):
    lower,upper,weight=map(lambda x:np.asarray(x,float),(lower,upper,weight))
    if not (np.isfinite(lower).all() and np.isfinite(upper).all() and np.isfinite(weight).all()):
        raise ValueError('Finite bound values and weights required')
    if np.any(lower<0) or np.any(upper>1) or np.any(lower>upper) or np.any(weight<0) or weight.sum()<=0:
        raise ValueError('Invalid utility interval or weight')
    return np.array([weight@lower,weight@upper])/weight.sum()


def jackknife_envelope(lower,upper,weights,replicates):
    estimate=weighted_bounds(lower,upper,weights)
    rep=np.array([weighted_bounds(lower,upper,w) for w in np.asarray(replicates).T])
    count=len(rep)
    variance=(count-1)/count*((rep-estimate)**2).sum(axis=0)
    se=np.sqrt(variance);critical=float(student_t.ppf(.975,count-1))
    # Each one-sided endpoint error has nominal 2.5% tail; union bound is 5%.
    # Approximation uses provider's grouped-jackknife variance and t(R-1).
    return dict(lower=float(max(0,estimate[0]-critical*se[0])),
                upper=float(min(1,estimate[1]+critical*se[1])),
                endpoint_standard_errors=se.tolist(),replicate_endpoint_estimates=rep.tolist(),
                critical_t=critical,groups=count,df=count-1,
                method='provider grouped jackknife variance; t endpoint envelope, nominal approximation, not provider-published CI')


def load():
    manifest=json.loads((SOURCE/'manifest.json').read_text());sources=[]
    for row in manifest:
        p=SOURCE/row['file'];digest=hashlib.sha256(p.read_bytes()).hexdigest()
        assert digest==row['sha256'],p
        sources.append(dict(file='../task4_school_commute_extra/'+row['file'],url=row['url'],sha256=digest))
    person=pd.read_csv(SOURCE/'person_vista_2024_2025.csv')
    hh=pd.read_csv(SOURCE/'household_vista_2024_2025.csv')
    journeys=pd.read_csv(SOURCE/'journey_to_education_vista_2024_2025.csv')
    assert person.persid.is_unique and hh.hhid.is_unique and journeys.jteid.is_unique
    assert journeys.persid.isin(person.persid).all()
    assert not journeys.duplicated(['persid','start_time']).any()
    person=person.merge(hh[['hhid','homelga']],on='hhid',validate='many_to_one')
    person=person[(person.homeregion_ASGS=='Greater Melbourne')&(person.dayType=='Weekday')&(person.studying=='Secondary')].copy()
    relevant=journeys[journeys.persid.isin(person.persid)].copy()
    assert (relevant.start_loc=='FROM_HOME').all() and (relevant.end_loc=='TO_EDUCATION').all()
    assert (relevant.dayType=='Weekday').all()
    assert (relevant.journey_elapsed_time>=relevant.journey_travel_time).all()
    assert (relevant.journey_elapsed_time>=0).all() and np.isfinite(relevant.journey_elapsed_time).all()
    np.testing.assert_allclose((relevant.end_time-relevant.start_time)%1440,relevant.journey_elapsed_time,rtol=0,atol=1e-9)
    purpose_cols=[f'destpurp1_desc_{i:02d}' for i in range(1,16)]
    relevant['purpose_sequence']=relevant[purpose_cols].apply(lambda r:json.dumps([x for x in r if pd.notna(x)]),axis=1)
    relevant['transport_only']=relevant.purpose_sequence.map(lambda s:all(x in TRANSPORT_PURPOSES for x in json.loads(s)))
    # Select first official JTE before screening its intermediate activities.
    first=relevant.sort_values(['persid','start_time','jteid']).drop_duplicates('persid')
    cols=['persid','jteid','start_time','journey_elapsed_time','journey_travel_time','purpose_sequence','transport_only']
    roster=person.merge(first[cols],on='persid',how='left',validate='one_to_one')
    roster['has_observed_journey']=roster.jteid.notna()
    roster['has_person_weight']=roster.perspoststratweight.notna()
    assert (roster.loc[roster.has_person_weight,'perspoststratweight']>0).all()
    return roster,relevant,sources


def main():
    roster,relevant,sources=load();scopes={};records=[]
    replicate_cols=[f'perspoststratweight_GROUP_{i}' for i in range(1,11)]
    for scope,sel in [('secondary_15_19',roster.agegroup=='15->19'),('secondary_all_ages',np.ones(len(roster),bool))]:
        full=roster[sel].copy();a=full[full.has_person_weight].copy()
        assert a[replicate_cols].notna().all().all()
        variants={}
        for name in ['official_elapsed','transport_stops_only']:
            accepted=a.has_observed_journey.copy()
            if name=='transport_stops_only':accepted &= a.transport_only.eq(True)
            utility=np.exp(-a.journey_elapsed_time.fillna(0).to_numpy()/30)
            lower=np.where(accepted,utility,0.);upper=np.where(accepted,utility,1.)
            weights=a.perspoststratweight.to_numpy();bound=weighted_bounds(lower,upper,weights)
            sampling=jackknife_envelope(lower,upper,weights,a[replicate_cols].to_numpy())
            variants[name]=dict(observed_people=int(accepted.sum()),unknown_people=int((~accepted).sum()),
                positive_person_weight_total=float(weights.sum()),unknown_person_weight=float(weights[~accepted].sum()),
                lower=float(bound[0]),upper=float(bound[1]),jackknife=sampling,
                observed_only_person_weighted_utility=float(np.average(utility[accepted],weights=weights[accepted])))
            records.extend(dict(scope=scope,definition=name,persid=pid,lower=float(l),upper=float(u),person_weight=float(w))
                           for pid,l,u,w in zip(a.persid,lower,upper,weights))
        scopes[scope]=dict(roster_people=len(full),positive_weight_people=len(a),missing_weight_people=int((~full.has_person_weight).sum()),
            no_journey_roster_people=int((~full.has_observed_journey).sum()),
            missing_weight_person_ids=full.loc[~full.has_person_weight,'persid'].tolist(),
            variants=variants,
            utility_lower=variants['official_elapsed']['lower'],utility_upper=variants['official_elapsed']['upper'],
            sampling_lower=variants['official_elapsed']['jackknife']['lower'],sampling_upper=variants['official_elapsed']['jackknife']['upper'],
            observed_only_person_weighted_utility=variants['official_elapsed']['observed_only_person_weighted_utility'],
            default_definition='official_elapsed; includes intermediate activity dwell, unlike NYC transport-only chains',
            missing_weight_statement='No missing person weight imputed or added as extra population. Official person weights are calibrated to Census targets after household nonresponse adjustments. No-weight diary records are retained for audit; their count is not an estimate of omitted population mass. Results rely on the official weighting and coverage assumptions.')
    old=relevant.merge(roster[['persid','agegroup']],on='persid',validate='many_to_one')
    old=old[old.agegroup=='15->19'];old_weight=old.journey_weight.to_numpy();old_utility=np.exp(-old.journey_elapsed_time.to_numpy()/30)
    old_summary=pd.read_csv(SOURCE/'melbourne_summary.csv').set_index('group').loc['secondary_15_19']
    old_mean=float(np.average(old_utility,weights=old_weight));assert abs(old_mean-old_summary.mean_exp_utility_tau30)<1e-14
    city=roster[roster.homelga=='Melbourne (C)']
    out=dict(main_admitted=False,source_year='2024-25',geography='Greater Melbourne GCCSA',
        current_secondary_verified=True,upper_secondary_grade_verified=False,age15_19_is_not_exact14_18=True,
        first_journey_definition='Earliest numeric start_time among official JTE records per person, selected before intermediate-purpose filter.',
        transport_purpose_whitelist=sorted(TRANSPORT_PURPOSES),sources=sources,scopes=scopes,
        city_of_melbourne_check=dict(secondary_weekday_people=len(city),households=int(city.hhid.nunique()),agegroups=city.agegroup.value_counts().to_dict(),admitted_as_city_estimate=False),
        old_journey_replication=dict(journeys=len(old),persons=int(old.persid.nunique()),households=int(old.hhid.nunique()),mean_exp_utility=old_mean),
        variance_reference=dict(file='../task4_school_commute_extra/vista_2021_2026_explanatory_document-updated-2026.pdf',section='3.5.2',formula='variance=(R-1)/R sum_r (theta_r-theta)^2; t(df=R-1)',scope='Official grouped replicate person weights. Endpoint mean uses same ratio functional in every replicate. Nominal approximation does not cover missing school stage, no-weight coverage, geographic transfer, measurement error, or choice of journey definition.'))
    roster[['persid','hhid','agegroup','studying','homelga','has_person_weight','perspoststratweight','has_observed_journey','jteid','start_time','journey_elapsed_time','purpose_sequence','transport_only']+replicate_cols].to_csv(HERE/'roster_audit.csv',index=False)
    pd.DataFrame(records).to_csv(HERE/'person_utility_bounds.csv',index=False)
    (HERE/'summary.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:{'roster':v['roster_people'],'weighted':v['positive_weight_people'],'variants':{n:{z:x[z] for z in ['observed_people','unknown_people','lower','upper']} for n,x in v['variants'].items()}} for k,v in scopes.items()},indent=2))

if __name__=='__main__':main()
