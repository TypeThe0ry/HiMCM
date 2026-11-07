"""Extract citywide administrative four-year graduation cohorts; no school sums.

Run with Python + openpyxl. Unknown outcomes remain separate from known
non-graduation outcomes. Citywide scope excludes charters and includes some
out-of-district placements; this is not an all-resident graduation estimate.
"""
from pathlib import Path
import csv
import hashlib
import json
import openpyxl

HERE=Path(__file__).resolve().parent
RAW=HERE/'2025-graduation-rates-public-citywide.xlsx'

def main():
    digest=hashlib.sha256(RAW.read_bytes()).hexdigest()
    manifest=json.loads((HERE/'manifest.json').read_text())
    assert digest==manifest['files']['2025-graduation-rates-public-citywide.xlsx']['sha256']
    workbook=openpyxl.load_workbook(RAW,data_only=True,read_only=True)
    all_rows=list(workbook['All'].values);head=all_rows[0]
    records=[dict(zip(head,row)) for row in all_rows[1:]]
    assert len(records)==48
    assert len({(r['Category'],r['Cohort Year'],r['Cohort']) for r in records})==len(records)
    outcomes=['# Grads','# Still Enrolled','# Dropout','# SACC (IEP Diploma)','# TASC (GED)']
    selected=[]
    for r in records:
        assert r['Category']=='All Students'
        n=int(r['# Total Cohort']);g=int(r['# Grads'])
        assert 0<=g<=n and abs(100*g/n-r['% Grads'])<1e-5
        assert g==r['# Total Regents']+r['# Local']
        if r['Cohort Year'] not in [2020,2021] or r['Cohort'] not in ['4 year June','4 year August']:continue
        known=sum(int(r[k]) for k in outcomes);unknown=n-known
        assert unknown>=0
        selected.append(dict(city='New York',cohort_entry_year=int(r['Cohort Year']),graduation_class_year=int(r['Cohort Year'])+4,
            outcome_period=r['Cohort'],cohort=n,graduates=g,known_non_graduation=known-g,unknown_outcomes=unknown,
            reported_rate=g/n,diploma_outcome_lower=g/n,diploma_outcome_upper=(g+unknown)/n,
            source_sheet='All',source_excel_row=records.index(r)+2))
    assert len(selected)==4
    for year in [2020,2021]:
        june=next(r for r in selected if r['cohort_entry_year']==year and r['outcome_period']=='4 year June')
        august=next(r for r in selected if r['cohort_entry_year']==year and r['outcome_period']=='4 year August')
        assert june['cohort']==august['cohort'] and june['graduates']<=august['graduates']
    with (HERE/'cohort_outcomes.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(selected[0]));w.writeheader();w.writerows(selected)
    summary=dict(source_sha256=digest,source_rows_validated=len(records),rows=selected,main_admitted=False,
        estimand='NYC accountability cohort, charter-excluded, some out-of-district placements included; all current city residents not identified',
        outcome='Local or Regents diploma within four years; June and August reported separately',
        missing_outcome_rule='Nonnegative residual between cohort and listed mutually exclusive outcomes is unknown; observed diploma count is lower bound and all residual cases graduating is upper bound. Administrative reported rate itself is G/N.',
        limitations=['No charter or all-resident coverage weight','Some private placements paid by NYC included','NYC diploma rules differ from Arizona; this is a conditional administrative completion comparison, not harmonized learning quality','Unknown outcomes must not automatically be treated as known non-graduates','Historical COVID Regents waivers affect cross-cohort interpretation'])
    summary['scopes']={}
    for year in [2024,2025]:
        august=next(r for r in selected if r['graduation_class_year']==year and r['outcome_period']=='4 year August')
        june=next(r for r in selected if r['graduation_class_year']==year and r['outcome_period']=='4 year June')
        summary['scopes'][str(year)]=dict(year=year,cohort_entry_year=year-4,period='4 year August',lower=august['diploma_outcome_lower'],upper=august['diploma_outcome_upper'],graduates=august['graduates'],cohort=august['cohort'],unknown_outcomes=august['unknown_outcomes'],reported_rate=august['reported_rate'],june_comparison=june)
    summary['source_notes']=[dict(sheet='NOTES',row=2,meaning='Cohort follows first grade-9 entry; graduation is Local or Regents diploma'),dict(sheet='NOTES',row=9,meaning='Charter schools excluded'),dict(sheet='NOTES',row=16,meaning='Citywide cohort includes out-of-district placements; school-level sums do not reproduce it'),dict(sheet='NOTES',row=17,meaning='Some students have unknown graduation outcomes, so the reported outcome categories do not always sum to cohort'),dict(sheet='NOTES',row=3,meaning='Some previous cohorts revised for NYC-paid private placements with IEPs')]
    (HERE/'graduation_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
