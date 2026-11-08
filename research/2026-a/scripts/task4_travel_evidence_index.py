"""Index only current travel inputs, rejecting unregistered or mismatched evidence.

This audit does not change model inputs or establish joint confidence coverage.
Historical source files are not evidence of current use without an endpoint match.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from task4_v5_model import ROOT, CITIES, NAMES

# Paths are relative to the research root, never selected by newest filename.
SOURCES = {
    'New York': dict(path='data/task4_v21_nyc_chains/summary.json',
        keys=['scopes', 'under19'], endpoints=['sampling_lower', 'sampling_upper'],
        year='2010–2011', age_stage='Under 19, current grades 9–12; coarse younger-than-16 band; optional unknown membership',
        geography='NYC five residence counties', observation='Reported RHTS linked trips; recovered transport-only chains',
        conditions='Exploratory household bootstrap; historical period; exact ages 14–18 not identified',
        original_source='data/task4_v20_nyc_travel/CSV.zip'),
    'Mexico City': dict(path='data/task4_v107_mexico/summary.json',
        keys=['scenarios', 'boundary3_optional'], endpoints=['utility_lower', 'utility_upper'],
        year='2025', age_stage='Ages 14–18; completed-secondary transition membership optional; remaining upper-secondary stage conditional',
        geography='CDMX habitual residents in sampled private dwellings, all16 boroughs',
        observation='Reported home-to-school duration bins with official person expansion weights',
        conditions='No sampling confidence envelope; current stage not directly observed; unknown travel retained; original raw local-only, sufficient aggregates public',
        original_source='data/task4_v107_mexico'),
    'Sao Paulo': dict(path='data/task4_v48_saopaulo_age/summary.json',
        keys=['scopes', 'age14_18'], endpoints=['sampling_lower', 'sampling_upper'],
        year='2023', age_stage='Actual ages 14–18; current ESTUDA=4 upper-secondary enrolment',
        geography='Municipality 36 / IBGE 3550308 residents, not metro-wide',
        observation='Reported OD2023 travel diaries; unresolved journeys retained',
        conditions='Public research mirror; official byte identity unverified; exploratory household bootstrap',
        original_source='data/task4_v10_saopaulo'),
    'Cape Town': dict(path='data/task4_v63_cape_travel/inference_summary.json',
        keys=['age14_18'], endpoints='joint_95_percent_approximate_envelope',
        year='2025', age_stage='Ages 14–18, current high-school attendance',
        geography='City of Cape Town metropolitan residents',
        observation='GHS reported school-travel bins',
        conditions='Approximate design-based endpoint envelope; fixed calibrated weights; coverage and period conditional',
        original_source='data/task4_v63_cape_travel'),
    'Melbourne': dict(path='data/task4_v44_melbourne/summary.json',
        keys=['all_resident_secondary_age_15_19'], endpoints='linear_sampling_envelope',
        year='2024–2025', age_stage='Released age 15–19 band, current Secondary; not exact 14–18 upper-secondary',
        geography='ABS Greater Melbourne, not City of Melbourne municipality',
        observation='VISTA weekday reported journeys; destination verification; unknown journeys retained',
        conditions='Official person jackknife replicate weights; linear endpoint envelope; conditional on available person weights (one age15–19 student lacks weight); scope conditional',
        original_source='data/task4_v44_melbourne'),
}
WITHDRAWN = {'Singapore': dict(path='data/task4_v70_singapore/summary.json',
    keys=[], endpoints='revised_travel_interval', year='2020',
    age_stage='Census broad Secondary; target age/current-high-school subgroup unidentified',
    geography='Singapore resident school-travel population',
    observation='Observed broad-group bins withdrawn as target-subgroup bounds in V70',
    conditions='No same-population target subgroup mass lower bound; V71 MOE counts not admitted',
    original_source='data/task4_school/sg_travel_api.json')}


def source_bounds(record, root=ROOT):
    path = root / record['path']
    raw = path.read_bytes()
    row = json.loads(raw)
    for key in record['keys']:
        row = row[key]
    keys = record['endpoints']
    bound = row[keys] if isinstance(keys, str) else [row[key] for key in keys]
    bound = np.asarray(bound, float)
    if bound.shape != (2,) or not np.isfinite(bound).all() or not 0 <= bound[0] <= bound[1] <= 1:
        raise ValueError('Invalid source bound: ' + record['path'])
    return bound, hashlib.sha256(raw).hexdigest()


def build_index(lo, hi, cities=CITIES, sources=None, withdrawn=None, root=ROOT):
    sources = SOURCES if sources is None else sources
    withdrawn = WITHDRAWN if withdrawn is None else withdrawn
    lo, hi = np.asarray(lo, float), np.asarray(hi, float)
    if lo.shape != (len(cities),) or hi.shape != lo.shape or len(set(cities)) != len(cities):
        raise ValueError('Travel city identities or dimensions invalid')
    if not np.isfinite([lo, hi]).all() or not np.all((0 <= lo) & (lo <= hi) & (hi <= 1)):
        raise ValueError('Invalid current travel bounds')
    informative = {c for c, l, h in zip(cities, lo, hi) if (l, h) != (0., 1.)}
    if informative != set(sources):
        raise ValueError('Informative cities differ from explicit evidence registration: ' +
                         repr(sorted(informative.symmetric_difference(sources))))
    if set(sources) & set(withdrawn) or not set(withdrawn).issubset(cities):
        raise ValueError('Invalid withdrawn evidence registration')
    rows = []
    for city, lower, upper in zip(cities, lo, hi):
        record = sources.get(city, withdrawn.get(city))
        row = dict(city=city, lower=float(lower), upper=float(upper),
                   status='informative_conditional' if city in sources else 'unknown',
                   main_admitted=False, bound_verified=False)
        if record:
            bound, digest = source_bounds(record, root)
            if not np.allclose(bound, [lower, upper], rtol=0, atol=1e-12):
                raise ValueError('Current/source travel bound mismatch: ' + city)
            if not (root / record['original_source']).exists():
                raise ValueError('Missing original source path: ' + city)
            row.update({k: record[k] for k in ['year', 'age_stage', 'geography', 'observation', 'conditions', 'original_source']})
            row.update(source_summary=record['path'], source_summary_sha256=digest,
                       source_keys=json.dumps(record['keys'] + [record['endpoints']]), bound_verified=True)
            if city in withdrawn:
                row['status'] = 'unknown_withdrawn_v70'
        else:
            row.update(year='', age_stage='Target high-school travel not identified',
                       geography=city, observation='No informative current travel bound',
                       conditions='[0,1] retained; historical files do not imply current admission',
                       original_source='', source_summary='', source_summary_sha256='', source_keys='')
        rows.append(row)
    return pd.DataFrame(rows)


def run(out):
    from task4_current_model import current_bounds, REGISTRY
    lo, hi, config = current_bounds()
    j = NAMES.index('travel')
    frame = build_index(lo[:, j], hi[:, j])
    out.mkdir(parents=True, exist_ok=True)
    csv = out / 'currenttravel_evidence.csv'
    frame.to_csv(csv, index=False)
    result = dict(model_version=config['model_version'], factory=config['module'] + '.' + config['factory'],
        registry_sha256=hashlib.sha256(REGISTRY.read_bytes()).hexdigest(),
        evidence_csv_sha256=hashlib.sha256(csv.read_bytes()).hexdigest(), cities=len(frame),
        informative_cities=frame.loc[frame.status == 'informative_conditional', 'city'].tolist(),
        unknown_cities=frame.loc[frame.status != 'informative_conditional', 'city'].tolist(),
        informative_count=int((frame.status == 'informative_conditional').sum()),
        unknown_count=int((frame.status != 'informative_conditional').sum()),
        source_bounds_verified=int(frame.bound_verified.sum()), main_admitted=False,
        limitations='Current-input provenance audit only; no new evidence admission, input change, ranking improvement or joint confidence claim.')
    (out / 'currenttravel_summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'results/task4_v71_intake')
    run(parser.parse_args().output)
