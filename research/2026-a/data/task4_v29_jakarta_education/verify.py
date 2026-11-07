"""Validate the manually transcribed official indexed BPS table, not raw HTML."""
from pathlib import Path
import csv,json,hashlib
p=Path(__file__).resolve().parent
for item in json.loads((p/'manifest.json').read_text())['files']:
    raw=(p/item['file']).read_bytes()
    assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256'],item['file']
rows=list(csv.DictReader((p/'jakarta_sma2025_transcription.csv').open()))
cols=list(rows[0])[1:]
for r in rows:
    for k in cols:r[k]=int(r[k])
    for k in ('schools','teachers','students'):
        assert r[k+'_public']+r[k+'_private']==r[k+'_total']
for k in cols: assert sum(r[k] for r in rows[:-1])==rows[-1][k]
s=json.loads((p/'bps_2025_query_response.json').read_text())
assert all(t in s for t in ['186.461','11.983','Kota Jakarta Utara','24 Februari 2026','\n2025\n','30 November'])
assert len(rows)==7 and len({r['region'] for r in rows})==7
# Parse the first (selected 2025) complete indexed table, not other-year snippets.
body=s.split('Kabupaten/Kota  |',1)[1].split('Sumber :',1)[0]
source_rows={}
for line in body.splitlines():
    cells=[v.strip() for v in line.split('|')]
    if len(cells)==10 and (cells[0].startswith(('Kepulauan Seribu','Kota Jakarta','DKI Jakarta'))):
        name=cells[0].removeprefix('Kota ')
        source_rows[name]=[0 if v in ('-','–') else int(v.replace('.','')) for v in cells[1:]]
assert set(source_rows)=={r['region'] for r in rows}
for r in rows: assert source_rows[r['region']]==[r[c] for c in cols],r['region']
value=rows[-1]['students_total']/rows[-1]['teachers_total']
obs=list(csv.DictReader((p/'observations.csv').open()))
assert len(obs)==1 and obs[0]['academic_year']=='2025/2026'
assert int(obs[0]['numerator'])==rows[-1]['students_total']
assert int(obs[0]['denominator'])==rows[-1]['teachers_total']
assert abs(float(obs[0]['value'])-value)<1e-12
print(json.dumps({'students':186461,'teachers_including_headmasters':11983,'ptr':value,'six_region_sums':'PASS','public_private_sums':'PASS','source_year_selector':'2025','archived_indexed_text':'PASS'},indent=2))
