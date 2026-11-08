"""Check aggregate controls without retaining or reading personal records."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
a = json.loads((HERE / 'aggregate_controls.json').read_text())
cells = [cell for groups in a['age_status_stage'].values() for cell in groups.values()]
assert sum(c['n'] for c in cells) == 4320
known = [groups['EVET|LİSE'] for groups in a['age_status_stage'].values()]
assert sum(c['n'] for c in known) == a['known']['count'] == 2463
assert sum(c['w'] for c in known) == a['known']['weight'] == 677016
optional = [c for groups in a['age_status_stage'].values() for key, c in groups.items()
            if key in {'null|null', 'EVET|DİĞER', 'EVET|ENGELLİ OKULU'}]
assert sum(c['n'] for c in optional) == a['optional_known_age']['count'] == 13
assert sum(c['w'] for c in optional) == a['optional_known_age']['weight'] == 3875
source = (HERE.parent / 'task4_v116_ibb/provider_catalog_and_schema.txt').read_text()
for phrase in ('Toplam kişiye göre ağırlık', 'Yolculuk bilgisi alınan kişilere göre ağırlık',
               'okuduguOkulunTuru', 'enSonBitirdigiOkul'):
    assert phrase in source
report = (HERE.parent / 'task4_v116_ibb/provider_report.txt').read_text()
assert '16.491 hanede 49.176 kişi' in report
print('PASS: independent aggregate roster controls and metadata anchors')

nulls = a['null_age_status_stage']
assert sum(c['n'] for c in nulls.values()) == a['null_age_rows'] == 21
assert nulls['null|null']['w'] + nulls['EVET|null']['w'] == 612
assert a['optional']['count'] == 13 + 2 == 15
assert a['optional']['weight'] == 3875 + 612 == 4487
assert a['known']['weight'] + a['optional']['weight'] == 681503
