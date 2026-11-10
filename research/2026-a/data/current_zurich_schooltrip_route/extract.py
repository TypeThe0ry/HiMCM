#!/usr/bin/env python3
"""Offline verify saved responses and extract relevant published text."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, re, subprocess
p = Path(__file__).resolve().parent
class Text(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self, data): self.parts.append(data)
def plain(name):
    parser=Text(); parser.feed((p/name).read_text(encoding='utf-8')); return re.sub(r'\s+', ' ', ' '.join(parser.parts))
for r in json.loads((p/'retrievals.json').read_text()):
    b=(p/r['file']).read_bytes()
    assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
def excerpt(s, needle, before=90, after=240):
    i=s.find(needle); assert i>=0, needle
    return s[max(0,i-before):i+len(needle)+after]
city=plain('city_2021_modalsplit.html'); bfs=plain('bfs_2021_national.html'); are=plain('are_mzmv.html')
pdf=subprocess.check_output(['pdftotext','-layout',str(p/'city_2005.pdf'),'-']).decode()
pdf=re.sub(r'\s+',' ',pdf)
leaflet=re.sub(r'\s+',' ', subprocess.check_output(['pdftotext',str(p/'bfs_2025_leaflet.pdf'),'-']).decode())
out={'planned_release':excerpt(leaflet, 'Mitte 2027',100,80), 'city_path_population':excerpt(city,'5493 Wege'), 'purpose_and_return':excerpt(bfs,'wenn der Rückweg nach Hause angetreten wird',0,500), 'education_purpose':excerpt(bfs,'Als Ausbildungswege werden Strecken bezeichnet',0,330), 'microdata_access_statement':excerpt(are,'Datenschutzvertrag'), 'historic_work_definition':excerpt(pdf,'gerechnet von Tür zu Tür',100,40)}
(p/'extraction.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('OK: five source hashes and six scope excerpts verified')
