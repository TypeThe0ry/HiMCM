"""Extract only published aggregates; no inference of Toronto duration."""
from pathlib import Path
import hashlib,json,re,subprocess
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parent
for x in json.loads((P/'sources.json').read_text()):
    assert hashlib.sha256((P/x['file']).read_bytes()).hexdigest()==x['sha256']
s=BeautifulSoup((P/'Wong2011_OSDUHS2009.html').read_text(),'html.parser')
tables=s.find_all('table')
rows=[[c.get_text(' ',strip=True) for c in tr.find_all(['td','th'])] for tr in tables[0].find_all('tr')]
bins=[]
for row in rows:
    if row and row[0] in ['0-15 minutes','16-30 minutes','≥31 minutes']:
        m=re.fullmatch(r'(\d+) \(([\d.]+)\)',row[2]); assert m
        bins.append({'minutes_bin':row[0],'sample_n':int(m[1]),'published_weighted_percent':float(m[2])})
assert len(bins)==6
assert sum(x['sample_n'] for x in bins[:3])==2479
tr=next(r for r in rows if r[0]=='Toronto');assert tr[2]=='256 (16.6)'
txt=subprocess.check_output(['pdftotext','-layout',str(P/'TTS2016_DataGuide.pdf'),'-'],text=True)
assert 'start_time' in txt
out={'OSDUHS_year':2009,'publication_year':2011,'population':'Ontario publicly funded school students in grades 9–12; not age-filtered 14–18','Toronto_secondary_sample_n':256,'Ontario_secondary_to_school':bins[:3],'Ontario_secondary_from_school':bins[3:],'Toronto_by_duration_joint_available_in_published_tables':False,'main_model_admission':False,'Toronto_main_interval_retained':[0,1]}
(P/'published_aggregates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Verified original hashes and Ontario duration totals; Toronto duration remains unobserved.')
