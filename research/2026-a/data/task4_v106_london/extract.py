"""Extract historic school-located Year10 aggregates, not current London residents."""
from pathlib import Path
import hashlib,json,re,subprocess
P=Path(__file__).resolve().parent
f=P/'LondonChallenge2006_RR823.pdf';m=json.loads((P/'manifest.json').read_text())
assert hashlib.sha256(f.read_bytes()).hexdigest()==m['sha256']
t=subprocess.check_output(['pdftotext','-layout',str(f),'-'],text=True)
start=t.index('Table 15.       How long does it take you to get to school?')
block=t[start:t.index('Due to rounding, percentages may not sum to 100',start)]
labels=['Less than 15 minutes','15 to 30 minutes','31 to 45 minutes','46 minutes to 1 hour','More than 1 hour','No response']
rows=[]
for label in labels:
    match=re.search(r'^'+re.escape(label)+r'\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$',block,re.M)
    assert match,label
    rows.append({'duration_bin':label,'London_Year10_published_percent':int(match[2])})
assert re.search(r'^N\s+25,276\s+22,451\s+6784\s+6454',block,re.M)
assert [r['London_Year10_published_percent'] for r in rows]==[30,36,15,7,3,8]
page=next(i for i,p in enumerate(t.split('\f'),1) if 'Table 15.       How long does it take you to get to school?' in p)
o={'survey_year':2006,'school_stage':'current Year10','geographic_definition':'London school location; residence not verified','question':'How long does it take you to get to school?','table':15,'PDF_page':page,'London_Year10_respondents':22451,'published_percentages':rows,'rounded_total_percent':99,'renormalized':False,'exact_age14_18_verified':False,'main_admission':False,'current_London_utility_interval_retained':[0,1]}
(P/'historical_year10_aggregates.json').write_text(json.dumps(o,indent=2)+'\n')
print('Hash, six rows, Year10 column and N verified; rounded total99 retained. PDF page',page)
