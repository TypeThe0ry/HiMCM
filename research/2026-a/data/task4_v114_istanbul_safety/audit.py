"""Recheck new source rejection and independent facility cross-captures."""
from pathlib import Path
import csv, hashlib, json, subprocess
from bs4 import BeautifulSoup
P = Path(__file__).resolve().parent

def run():
    for row in json.loads((P/'manifest.json').read_text()):
        assert row['status'] == 200
        assert hashlib.sha256((P/row['file']).read_bytes()).hexdigest() == row['sha256']
    text = BeautifulSoup((P/'media_methodology.html').read_bytes(), 'html.parser').get_text(' ', strip=True)
    assert '307' in text and '186' in text and 186 < 307
    recorded = json.loads((P/'facilities_crossaudit.json').read_text())
    for file, sha in recorded['source_hashes'].items():
        assert hashlib.sha256((P.parent/file).read_bytes()).hexdigest() == sha
    Q = P.parent/'task4_v114_istanbul_facilities'
    names = [r['name'] for r in csv.DictReader((Q/'pool_venues2025.csv').open())]
    body = ' '.join((P/'pool_index_crosscapture.txt').read_text().split())
    prefix = ' '.join((P/'pool_prefix_crosscapture.txt').read_text().split())
    assert len(names) == len(set(names)) == 24
    assert all(' '.join(n.split()) in body for n in names[1:])
    assert names[0] == '75. YIL YÜZME HAVUZU'
    assert 'YÜZME HİZMETİ SUNAN İBB TESİSLERİ 75.' in prefix
    assert 'YIL YÜZME HAVUZU' in body
    pdf = subprocess.check_output(['pdftotext','-layout', str(Q/'iett2025.pdf'), '-']).decode()
    assert '2025 yılı itibarıyla İstanbul genelinde bulunan 12.426 adet durağa' in ' '.join(pdf.split())
    assert 'QR KODLU LEVHA TAKILAN DURAK SAYISI' in pdf
    print('PASS: raw hashes, no new safety bound, 24 distinct named pool venues, 12426 reported Istanbul stops.')

if __name__ == '__main__':
    run()
