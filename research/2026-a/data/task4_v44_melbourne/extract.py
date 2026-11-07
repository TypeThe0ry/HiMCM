"""VISTA secondary attenders: first weekday education journey, explicit unknowns."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import t as student_t

CRITICAL = float(student_t.ppf(0.975, 9))

P = Path(__file__).resolve().parent


def estimate(d, duration="journey_elapsed_time"):
    input_persons = len(d)
    complete_weights = np.isfinite(d.perspoststratweight) & (d.perspoststratweight > 0)
    for r in range(1, 11):
        wr = d['perspoststratweight_GROUP_' + str(r)]
        complete_weights &= np.isfinite(wr) & (wr >= 0)
    excluded_weights = int((~complete_weights).sum())
    d = d[complete_weights].copy()
    w = d.perspoststratweight.to_numpy(float)
    assert np.isfinite(w).all() and (w > 0).all()
    t = pd.to_numeric(d[duration], errors='coerce').to_numpy(float)
    valid = np.isfinite(t) & (t >= 0) & (d.destplace2 == 'Secondary School').to_numpy()
    u = np.exp(-np.where(valid, t, 0) / 30)
    lo, hi = np.where(valid, u, 0), np.where(valid, u, 1)
    means = [float(np.average(x, weights=w)) for x in (lo, hi)]
    endpoints = []
    replicates = []
    linear_endpoints = []
    for values, mean in zip((lo, hi), means):
        reps = []
        for r in range(1, 11):
            wr = d['perspoststratweight_GROUP_' + str(r)].to_numpy(float)
            assert np.isfinite(wr).all() and (wr >= 0).all() and wr.sum() > 0
            reps.append(float(np.average(values, weights=wr)))
        assert 0 < mean < 1 and all(0 < x < 1 for x in reps)
        logit = lambda v: np.log(np.asarray(v) / (1 - np.asarray(v)))
        se = float(np.sqrt(9 / 10 * np.sum((logit(reps) - logit(mean)) ** 2)))
        ci = 1 / (1 + np.exp(-(logit(mean) + np.array([-1, 1]) * CRITICAL * se)))
        linear_se = float(np.sqrt(9 / 10 * np.sum((np.array(reps) - mean) ** 2)))
        linear_endpoints.append(np.clip(mean + np.array([-1, 1]) * CRITICAL * linear_se, 0, 1).tolist())
        endpoints.append(ci.tolist())
        replicates.append(reps)
    return dict(persons=len(d), input_persons=input_persons,
                persons_with_missing_or_invalid_weights=excluded_weights,
                strict_target_interval_if_unbounded_missing_weights=[0.0, 1.0] if excluded_weights else None,
                no_recorded_journey=int(d.journey_elapsed_time.isna().sum()), households=int(d.hhid.nunique()),
                age_bands=d.agegroup.value_counts().to_dict(),
                destination_categories=d.destplace2.fillna('Missing journey').value_counts().to_dict(),
                verified_secondary_destination=int(valid.sum()),
                uncertain_destination_or_duration=int((~valid).sum()),
                invalid_duration=int((~np.isfinite(t) | (t < 0)).sum()),
                sum_person_weights=float(w.sum()),
                duration_variable=duration,
                weighted_minutes_for_reported_journeys=float(np.average(t[np.isfinite(t)], weights=w[np.isfinite(t)])),
                utility_identification_interval=means,
                endpoint_jackknife_intervals=endpoints,
                sampling_envelope=[endpoints[0][0], endpoints[1][1]],
                linear_sampling_envelope=[linear_endpoints[0][0], linear_endpoints[1][1]],
                critical_value=CRITICAL, endpoint_replicates=replicates)


def main():
    for r in json.loads((P / 'manifest.json').read_text()):
        b = (P / r['file']).read_bytes()
        assert len(b) == r['bytes'] and hashlib.sha256(b).hexdigest() == r['sha256']
    persons = pd.read_csv(P.parent / 'task4_school_commute_extra/person_vista_2024_2025.csv')
    journeys = pd.read_csv(P.parent / 'task4_school_commute_extra/journey_to_education_vista_2024_2025.csv')
    stops = pd.read_csv(P / 'stops_vista_2024_2025.csv', low_memory=False)
    households = pd.read_csv(P.parent / 'task4_school_commute_extra/household_vista_2024_2025.csv')
    assert persons.persid.is_unique and stops.stopid.is_unique and households.hhid.is_unique
    d = journeys.merge(persons, on=['hhid', 'persid'], suffixes=('', '_person'),
                       validate='many_to_one', how='left', indicator=True)
    assert (d._merge == 'both').all()
    d = d.drop(columns='_merge').merge(stops[['stopid', 'hhid', 'persid', 'destplace2', 'destpurp2']],
            left_on=['end_stopid', 'hhid', 'persid'], right_on=['stopid', 'hhid', 'persid'],
            validate='many_to_one', how='left', indicator=True)
    assert (d._merge == 'both').all()
    d = d.drop(columns='_merge').merge(households[['hhid', 'homelga']], on='hhid', validate='many_to_one')
    assert (d.homeregion_ASGS == d.homeregion_ASGS_person).all()
    d = d[(d.studying == 'Secondary') & (d.homeregion_ASGS == 'Greater Melbourne') &
          (d.dayType == 'Weekday')].copy()
    assert (d.start_loc == 'FROM_HOME').all() and (d.end_loc == 'TO_EDUCATION').all()
    assert np.allclose(d.end_time - d.start_time, d.journey_elapsed_time)
    all_journeys = len(d)
    d = d.sort_values(['persid', 'start_time', 'jteid']).drop_duplicates('persid').copy()
    cols = ['hhid', 'persid', 'jteid', 'agegroup', 'studying', 'homelga', 'homeregion_ASGS',
            'dayType', 'start_loc', 'end_loc', 'destplace2', 'destpurp2', 'start_time', 'end_time',
            'journey_travel_time', 'journey_elapsed_time', 'journey_weight', 'perspoststratweight']
    cols += ['perspoststratweight_GROUP_' + str(r) for r in range(1, 11)]
    d[cols].to_csv(P / 'first_weekday_journeys.csv', index=False)
    eligible = persons[(persons.studying == 'Secondary') &
                       (persons.homeregion_ASGS == 'Greater Melbourne') & (persons.dayType == 'Weekday')]
    reported = d[['persid', 'destplace2', 'journey_elapsed_time', 'journey_travel_time']]
    residents = eligible.merge(reported, on='persid', how='left', validate='one_to_one')
    summary = dict(source='VISTA 2024-25, official public microdata',
                   target='Greater Melbourne secondary students with a recorded weekday home-to-education journey; first such journey per person',
                   geographic_scope='ABS Greater Melbourne, not City of Melbourne municipality',
                   exact_14_18_membership_identified=False,
                   main_admission=False,
                   secondary_weekday_persons=int(len(eligible)),
                   persons_without_home_education_journey=int((~eligible.persid.isin(d.persid)).sum()),
                   weekday_secondary_journeys=all_journeys,
                   repeated_journeys_removed=all_journeys-len(d),
                   weight='person poststratification; weekday multiplier 7/5 cancels in ratios',
                   uncertainty_method='10 official person jackknife replicate weights; logit endpoint variance 9/10 sum squared deviations; t(9,.975) critical value. Approximate endpoint envelope, not simultaneous confidence coverage.',
                   all_secondary=estimate(d),
                   secondary_age_15_19=estimate(d[d.agegroup == '15->19']),
                   all_resident_secondary=estimate(residents),
                   all_resident_secondary_age_15_19=estimate(residents[residents.agegroup == '15->19']),
                   secondary_age_15_19_leg_time=estimate(d[d.agegroup == '15->19'], 'journey_travel_time'),
                   all_resident_secondary_age_15_19_leg_time=estimate(residents[residents.agegroup == '15->19'], 'journey_travel_time'))
    (P / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print('All resident conditional 15–19:', summary['all_resident_secondary_age_15_19']['sampling_envelope'])
    for name in ['all_secondary', 'secondary_age_15_19']:
        print(name, json.dumps({k:v for k,v in summary[name].items() if k!='endpoint_replicates'}))


if __name__ == '__main__':
    main()
