"""Check transcription integrity and arithmetic, not original-PDF authenticity."""
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
for item in json.loads((HERE/'manifest.json').read_text()):
    raw=(HERE/item['file']).read_bytes()
    assert len(raw)==item['bytes']
    assert hashlib.sha256(raw).hexdigest()==item['sha256']
d=json.loads((HERE/'reader_observations.json').read_text())
t=d['table_totals']; row=d['selected_row']
old=json.loads((HERE.parent/'task4_v81_barcelona/summary.json').read_text())['periods']['2024/2025']
report=dict(
    source_quality='reader transcription only',
    table_stage_sum=sum(t[k] for k in ['eso','batx','cf']),
    published_table_total=t['published_total_students'],
    stage_sum_minus_total=sum(t[k] for k in ['eso','batx','cf'])-t['published_total_students'],
    pedralbes_stage_sum_minus_total=sum(row[k] for k in ['eso','batx','cf'])-row['published_total_students'],
    ceb_batx=t['batx'],generalitat_public_batx=old['batx_students_by_ownership']['PÚBLIC'],
    public_batx_difference=old['batx_students_by_ownership']['PÚBLIC']-t['batx'],
    dates_consistent=d['enrollment_date_prose']==d['enrollment_date_table_header'],
    main_admitted=False)
assert report['stage_sum_minus_total']==7
assert report['pedralbes_stage_sum_minus_total']==1
assert report['public_batx_difference']==1449
(HERE/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
