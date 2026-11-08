"""Verify official documentation bytes and the field interpretations used in V83."""
from pathlib import Path
import hashlib,json,subprocess,tempfile
HERE=Path(__file__).resolve().parent
for record in json.loads((HERE/'manifest.json').read_text()):
    raw=(HERE/record['file']).read_bytes()
    assert raw.startswith(b'%PDF') and len(raw)==record['bytes']
    assert hashlib.sha256(raw).hexdigest()==record['sha256']
with tempfile.TemporaryDirectory() as directory:
    texts={}
    for filename in ['users_manual.pdf','questionnaire2023_24.pdf','codebook2023_24.pdf','Readme2023_24.pdf','layout2023_24.pdf']:
        out=Path(directory)/(filename+'.txt')
        subprocess.run(['pdftotext','-layout',str(HERE/filename),str(out)],check=True)
        texts[filename]=' '.join(out.read_text().split())
    manual=texts['users_manual.pdf'];q=texts['questionnaire2023_24.pdf'];code=texts['codebook2023_24.pdf']
    assert '73.14 percent' in manual and 'Arizona' in manual
    assert 'NUMTEACH = P385 + (.875 x P390) + (.625 x P395) + (.375 x P400) + (.125 x P405)' in manual
    assert 'REPW1 to REPW88' in manual
    assert 'October 1, 2023' in q and 'typical week at THIS school' in q
    for field,grade in [('P270','Ninth'),('P280','Tenth'),('P290','Eleventh'),('P300','Twelfth')]:
        assert field in code and grade+' Grade Enrollment' in code
    assert '22,510 respondents' in texts['Readme2023_24.pdf']
    assert 'Mailing City' in texts['layout2023_24.pdf'] and 'Location City' in texts['layout2023_24.pdf']
print('Six official PDF hashes and PSS enrollment/FTE/coverage definitions verified.')
