"""Offline checks for new primary sources; no model observations generated."""
from pathlib import Path
import hashlib,json,subprocess
P=Path(__file__).resolve().parent

def run():
    texts={}
    for r in json.loads((P/'manifest.json').read_text()):
        b=(P/r['file']).read_bytes()
        assert b.startswith(b'%PDF') and len(b)==r['bytes']
        assert hashlib.sha256(b).hexdigest()==r['sha256']
        texts[r['file']]=subprocess.check_output(['pdftotext','-layout',str(P/r['file']),'-']).decode()
    d=texts['devkota_highschool_locations.pdf']
    assert 'Travel behaviour of students was not captured' in d
    assert 'four districts' in d and 'total 20 schools' in d
    assert '5.4 km/' in d and 'divide the total populations' in d
    t=texts['ozdogru2021_time_use.pdf']
    assert '180' in t and '118' in t and '62' in t
    assert 'Uygun örneklem' in t and '15 ila 18' in t
    assert 'sekiz farklı aktivite' in t and 'Diğer:' in t
    a=json.loads((P/'audit.json').read_text())
    assert a['new_admitted_observations']==0 and a['utility_before']==a['utility_after']==[0,1]
    print('PASS: both primary PDFs, scope and questionnaire checks; zero model admissions')

if __name__=='__main__':run()
