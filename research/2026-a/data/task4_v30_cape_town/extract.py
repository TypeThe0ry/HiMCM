#!/usr/bin/env python3
"""Reproduce GHS2023 Cape Town pupil-weighted descriptive identification bounds.
Reads the original ZIP in memory; exports aggregates only. No sampling inference.
"""
import csv
import hashlib
import io
import json
import math
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
TAU = 30.0
TIME_BINS = {1: (0,15), 2:(15,30), 3:(30,60), 4:(60,90), 5:(90,math.inf)}
REQUIRED = {'uqnr','personnr','psu','prov','stratum','metro_code','age','edu_attend','edu_edui','edu_corr','edu_grde','edu_time','person_wgt'}

def integer(row, field):
    try:
        return int(row[field])
    except (ValueError,TypeError):
        return None

def load_records():
    with ZipFile(ROOT / 'GHS2023.zip') as archive:
        reader = csv.DictReader(io.TextIOWrapper(archive.open('GHS2023PERSON.csv'), encoding='utf-8-sig'))
        assert REQUIRED <= set(reader.fieldnames)
        return list(reader)

def classify(row, age_range=None):
    """Definite/optional/excluded membership; observed contradictions exclude.
    Structural N/A in downstream fields is unresolved unless an upstream answer
    excludes membership. Missing age remains optional in the sensitivity subset.
    """
    age = integer(row,'age')
    if age is not None and age < 5:
        return 'excluded'
    if age_range and age is not None and not age_range[0] <= age <= age_range[1]:
        return 'excluded'
    values = {f: integer(row,f) for f in ['edu_attend','edu_edui','edu_corr','edu_grde']}
    exclusions = {'edu_attend':{2},'edu_edui':{1,3,4,5,6,7,8,9},'edu_corr':{1},'edu_grde':set(range(10))|{13,14,15,16}}
    if any(values[f] in codes for f,codes in exclusions.items()):
        return 'excluded'
    known = values['edu_attend']==1 and values['edu_edui']==2 and values['edu_corr']==2 and values['edu_grde'] in {10,11,12}
    return 'definite' if known and (not age_range or age is not None) else 'optional'

def weight(row):
    try:
        w=float(row['person_wgt'])
        return w if math.isfinite(w) and w > 0 else None
    except (ValueError,TypeError):
        return None

def utility_bounds(row):
    lo,hi=TIME_BINS.get(integer(row,'edu_time'),(0,math.inf))
    return math.exp(-hi/TAU), math.exp(-lo/TAU)

def profile(rows):
    weights=[weight(r) for r in rows]
    positive=[w for w in weights if w is not None]
    return dict(n=len(rows), households=len({r['uqnr'] for r in rows}), psus=len({(r['prov'],r['psu']) for r in rows}), strata=len({r['stratum'] for r in rows}), weight_sum=sum(positive), missing_or_nonpositive_weight_n=len(weights)-len(positive), kish_weight_only_effective_n=sum(positive)**2/sum(w*w for w in positive) if positive else None)

def summarize(rows,age_range=None):
    definite=[r for r in rows if classify(r,age_range)=='definite']
    optional=[r for r in rows if classify(r,age_range)=='optional']
    invalid=[r for r in definite+optional if weight(r) is None]
    dweight=sum(weight(r) for r in definite if weight(r) is not None)
    oweight=sum(weight(r) for r in optional if weight(r) is not None)
    # Optional members receive [0,1], a conservative envelope including unknown
    # membership and time. Missing weights prevent bounded weighted identification.
    nums=[sum(weight(r)*utility_bounds(r)[k] for r in definite if weight(r) is not None) for k in (0,1)]
    bounds=[nums[0]/(dweight+oweight),(nums[1]+oweight)/(dweight+oweight)] if dweight and not invalid else [0,1]
    unknown_time=[r for r in definite if integer(r,'edu_time') not in TIME_BINS]
    return dict(definite=profile(definite),optional=profile(optional), missing_time=profile(unknown_time), time_code_counts=dict(sorted(Counter(r['edu_time'] for r in definite).items())), grade_counts=dict(sorted(Counter(r['edu_grde'] for r in definite).items())), age_counts=dict(sorted(Counter(r['age'] for r in definite).items(),key=lambda x:int(x[0]))), utility_lower=bounds[0],utility_upper=bounds[1], interval_type='weighted descriptive identification interval; not confidence interval',sampling_inference_included=False)

def main():
    records=load_records()
    city=[r for r in records if integer(r,'metro_code')==2]
    assert len({(r['uqnr'],r['personnr']) for r in records})==len(records)
    assert all(len({r['stratum'] for r in records if r['psu']==p})==1 for p in {r['psu'] for r in city})
    outputs=[]
    for name,ages in [('grades10_12_all_ages',None),('grades10_12_ages14_18',(14,18))]:
        for status in ['definite','optional']:
            selected=[r for r in city if classify(r,ages)==status]
            for code in ['1','2','3','4','5','6','8','9','other']:
                group=[r for r in selected if (r['edu_time'] if r['edu_time'] in {'1','2','3','4','5','6','8','9'} else 'other')==code]
                outputs.append(dict(population=name,membership=status,time_code=code,**profile(group)))
    summary=dict(survey='Statistics South Africa General Household Survey 2023',geography='City of Cape Town metropolitan municipality; metro_code=2',source_zip_sha256=hashlib.sha256((ROOT/'GHS2023.zip').read_bytes()).hexdigest(),person_member='GHS2023PERSON.csv',national_person_n=len(records),city=profile(city),weight_variable='person_wgt',household_variable='uqnr',psu_variable='psu',stratum_variable='stratum',tau_minutes=TAU,utility_definition='exp(-one_way_usual_school_trip_minutes / 30)',time_bin_minutes={str(k):[a,None if math.isinf(b) else b] for k,(a,b) in TIME_BINS.items()},source_bin_labels={'1':'Less than 15 minutes','2':'15–30 minutes','3':'31–60 minutes','4':'61–90 minutes','5':'More than 90 minutes'},bin_interpretation='Conservative continuous-time closure expands code3 lower endpoint31 to30 and code4 lower endpoint61 to60, avoiding integer-minute precision assumptions. Closure bounds for <15 and >90. No within-bin distribution or midpoint assumption.',primary_population='ages14_18',sensitivity_population='all_ages',membership_definition='Current attendance=1, formal school=2, current grade 10/11/12, distance institution=2. Ages14–18 primary, all ages sensitivity; observed ages below education-question universe5 excluded. Unknown downstream values are optional unless a known answer rules eligibility out.',missing_policy='Unknown time including unexpected not-applicable=[0,1]. Optional eligibility=[0,1] and optional denominator. Any nonpositive/missing target weight => [0,1] because unknown weight mass is not bounded.',all_ages=summarize(city),ages14_18=summarize(city,(14,18)),actual_grade10_12_before_attendance_distance_filters=profile([r for r in city if integer(r,'edu_grde') in {10,11,12}]),excluded_distance_actual_grade10_12=profile([r for r in city if integer(r,'edu_grde') in {10,11,12} and integer(r,'edu_corr')==1]),limitations=['Grouped travel time identifies an interval rather than a point.','These bounds describe the weighted sample; a separate survey-design uncertainty calculation is required for population inference.','Formal in-person school pupils in actual grades10-12; not all youth, all educational institutions, or hypothetical school accessibility.','2023 municipal residential geography and reported usual one-way travel; survey year differs from other cities.'])
    (ROOT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    with (ROOT/'aggregate_counts.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(outputs[0])); writer.writeheader(); writer.writerows(outputs)
    print(json.dumps({k:summary[k] for k in ['all_ages','ages14_18']},indent=2))
if __name__=='__main__':
    main()
