"""Recompute Phoenix frozen-release homicide rate from verified primary transcriptions."""
from pathlib import Path
import csv,json,hashlib
P=Path(__file__).resolve().parent

def main():
 for r in json.loads((P/'manifest.json').read_text()):
  if r.get('sha256'):assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
 d=json.loads((P/'phoenix_primary_web_extract.json').read_text())
 assert sum(d['monthly_deaths'])==sum(d['quarterly_deaths'])==d['annual_deaths']==138
 assert [sum(d['monthly_deaths'][i:i+3]) for i in range(0,12,3)]==d['quarterly_deaths']
 assert d['annual_deaths']+d['excluded_negligent_deaths']==d['total_criminal_homicide']
 rate=d['annual_deaths']/d['population']*100000;u=2/(2+rate)
 row=dict(city='Phoenix',indicator='homicide_rate',raw_lower=rate,raw_upper=rate,utility_lower=u,utility_upper=u,
          year=2024,source_url=d['homicide_source']+' | '+d['population_source'],scope=d['scope'],
          status='conditional_manual_primary_homicide_rate',raw_pdf_archived=False)
 with (P/'bounds.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=row,lineterminator='\n');w.writeheader();w.writerow(row)
 print('Phoenix homicide rate:',rate,'utility:',u)
if __name__=='__main__':main()
