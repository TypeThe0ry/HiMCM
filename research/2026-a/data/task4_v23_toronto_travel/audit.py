"""Offline official TTS public-table coverage audit; no high-school inference."""
import csv
import hashlib
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent


def main():
    manifest=json.loads((ROOT/'download_manifest.json').read_text())
    for item in manifest:
        path=ROOT/item['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']
        assert path.stat().st_size==item['bytes']
    tables={}
    details=[]
    for suffix in ['pd','ward']:
        path=ROOT/f'tts2022_{suffix}_Toronto.csv'
        rows=list(csv.reader(path.open(newline='')))
        assert rows[2][1]=='City of Toronto'
        assert len(rows)==409
        assert len(set(r[0] for r in rows[3:]))==406
        tables[suffix]={r[0]:r[1] for r in rows[3:]}
        assert not any('duration' in r[0].lower() or 'minutes' in r[0].lower() for r in rows[3:])
        details.append(dict(file=path.name,summary_indicators=406,geographic_subdivisions=len(rows[2])-2,
                            high_school_specific_labels=[r[0] for r in rows[3:] if 'high school' in r[0].lower() or 'secondary' in r[0].lower()],
                            suppressed_cells=sum(v=='*' for row in rows[3:] for v in row[1:])))
    assert tables['pd']==tables['ward'], 'City total columns differ between releases'
    pdf=ROOT/'2022TTS_Data_Guide.pdf'
    def pages(first,last):
        return subprocess.check_output(['pdftotext','-f',str(first),'-l',str(last),'-layout',str(pdf),'-'],text=True)
    household=pages(55,55);school=pages(65,65);trips=pages(71,75)
    assert 'n_stu_k12' in household and 'ages 5-17' in household
    assert 'sch_code' in school and 'contact Data Management' in school
    assert 'start_time' in trips and 'Trip departure time' in trips
    assert 'duration' not in trips.lower() and 'end_time' not in trips.lower()
    selected=['Number of full-time students','Number of part-time students','Number of persons with unknown student status',
              'Number of home-based school trips by residents in 24-hours']
    out=dict(main_admitted=False,admitted_high_school_commute_observations=0,city='Toronto',survey_cycle='2022',
        collection_scope='Fall 2022 and Spring 2023; released tables retain cycle label 2022',
        provider='University of Toronto Data Management Group',
        public_tables=details,identical_city_total_columns=True,
        contextual_all_stage_totals={k:int(tables['pd'][k]) for k in selected},
        contextual_totals_are_high_school_data=False,
        data_guide_findings=[
            dict(pages='55',field='n_stu_k12',finding='Household K-12 count includes age 5-17 fallback when school level unknown. Neither a high-school category nor purely directly reported school stage.'),
            dict(pages='63',field='stu_stat',finding='Full-time/part-time/not student/unknown; no school stage.'),
            dict(pages='65',field='sch_code',finding='School lookup could potentially distinguish schools, but guide directs users to contact DMG for detailed school list. Public CSV has no person-school records or lookup.'),
            dict(pages='71-75',field='start_time',finding='Published trip-attribute dictionary contains departure time, purpose, geography and straight-line/Manhattan distances, but no arrival-time or duration variable. Departures at consecutive activities do not identify travel duration.')],
        decision='Retain Toronto high-school commute interval. Do not substitute all-school trip totals, age strata, school-bus counts or modeled network time.',
        remaining_evidence=['Direct current high-school identity or audited current school-code lookup and person records',
                            'Actual travel duration or departure-and-arrival observations',
                            'Toronto resident selection, person/household weights and non-traveller/missing records'])
    (ROOT/'coverage_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
