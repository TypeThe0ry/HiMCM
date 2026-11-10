#!/usr/bin/env python3
"""Recheck source bytes, selected institutional decisions and submitted arithmetic."""
import csv, hashlib, json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from bs4 import BeautifulSoup

base=Path(__file__).resolve().parents[2]
data=Path(__file__).resolve().parent
out=base/'results/current_zurich_he_scope_followup'
receipts=json.loads((data/'retrievals.json').read_text())
for r in receipts:
    assert r['status']==200
    assert hashlib.sha256((data/r['file']).read_bytes()).hexdigest()==r['sha256']
text=BeautifulSoup((data/'canton_entry.html').read_text(), 'html.parser').get_text(' ',strip=True)
for term in ['ETH Zürich','Universität Zürich','ZHAW','ZHdK','PHZH','HfH','HWZ']:
    assert term in text, term
page=BeautifulSoup((data/'accreditation_decisions.html').read_text(),'html.parser')
need=['ETH Zürich','HWZ Hochschule für Wirtschaft Zürich','Interkantonale Hochschule für Heilpädagogik','Kalaidos Fachhochschule Schweiz','Pädagogische Hochschule Zürich','Universität Zürich','Zürcher Hochschule der Künste','Zürcher Hochschule für Angewandte Wissenschaften']
rows=[]
for term in need:
    found=[list(tr.stripped_strings) for tr in page.select('tr') if term in ' '.join(tr.stripped_strings) and 'Institutionelle Akkreditierung' in ' '.join(tr.stripped_strings)]
    assert len(found)==1,(term,len(found))
    row=found[0]
    from datetime import datetime
    start=datetime.strptime(row[2],'%d.%m.%Y').date(); end=datetime.strptime(row[3],'%d.%m.%Y').date()
    assert start.isoformat() <= '2026-11-10' <= end.isoformat()
    rows.append({'institution':row[0],'decision':row[2],'expires':row[3]})
with (base/'data/task4_v117_team_intake/city_indicators.csv').open(encoding='utf-8-sig',newline='') as f:
    zurich=next(r for r in csv.DictReader(f) if r['city']=='Zurich')
pop=Decimal(zurich['population']); count=Decimal(zurich['he_count']); density=count*1000000/pop
assert density.quantize(Decimal('.1'),rounding=ROUND_HALF_UP)==Decimal(zurich['he_per_million'])
files=[data/r['file'] for r in receipts]+[data/'retrievals.json',data/'verify.py',base/'data/task4_v117_team_intake/city_indicators.csv',base/'data/current_all16_ror_rosters/ror_education_rosters.csv',base/'results/current_all16_ror_review/verification.json']
sha={str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
result={'status':'PASS scoped evidence and arithmetic checks','source_sha256':sha,'source_date_utc':'2026-11-10','receipt_count':len(receipts),'canton_selected_seven':['ETH Zürich','Universität Zürich','ZHAW','ZHdK','PHZH','HfH','HWZ'],'institutional_accreditation_rows':rows,'submitted_population':int(pop),'submitted_population_year':zurich['population_year'],'submitted_he_count':int(count),'submitted_density_label_year':zurich['he_per_million_year'],'arithmetic_density_per_million':str(density),'rounds_to_submitted_value':True,'original_extraction_verified':False,'municipal_accredited_institution_count_verified':False,'new_primary_observations_admitted':0,'note':'Seven canton-selected institutions are not a municipal count or exhaustive list. Kalaidos and FFHS appear in canton offerings; SBS is in Kloten. Exact 23 count match and arithmetic do not establish original extraction.'}
out.mkdir(parents=True,exist_ok=True)
(out/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':result['status'],'density':str(density),'accreditation_rows':len(rows),'new_primary_admissions':0},ensure_ascii=False))
