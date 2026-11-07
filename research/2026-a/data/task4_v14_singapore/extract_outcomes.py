"""Keep exam achievement distinct from graduation and cohort completion."""
from pathlib import Path
import json,hashlib,csv
P=Path(__file__).resolve().parent

def main():
    manifest=json.loads((P/'manifest.json').read_text())
    for r in manifest['files']:
        assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
    raw=json.loads((P/'alevel_timeseries.json').read_text());assert raw['success']
    records=raw['result']['records'];assert len(records)==raw['result']['total']==130
    assert len({r['_id'] for r in records})==len(records)
    overall=[dict(year=int(r['year']),published_percentage=float(r['percentage_pass'])) for r in records if r['race']=='Overall']
    assert len({r['year'] for r in overall})==len(overall)==26
    with (P/'overall_exam_outcomes.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=['year','published_percentage']);w.writeheader();w.writerows(overall)
    trans=json.loads((P/'candidate_outcomes_transcription.json').read_text());checks=[]
    for year in ['2024','2025']:
        r=trans[year];fraction=r['meeting_criterion']/r['candidates']
        assert round(fraction*100,1)==r['published_percent']
        if year=='2024':assert next(x['published_percentage'] for x in overall if x['year']==2024)==r['published_percent']
        checks.append(dict(year=int(year),candidates=r['candidates'],meeting_criterion=r['meeting_criterion'],fraction=fraction,criterion=r['criterion']))
    (P/'audit.json').write_text(json.dumps(dict(main_admitted=False,raw_rows=len(records),overall_years=len(overall),candidate_checks=checks,reason='Exam-threshold outcomes, not four-year graduation; 2025 criterion changes.'),indent=2)+'\n')
    print(json.dumps(checks,indent=2))
if __name__=='__main__':main()
