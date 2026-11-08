"""Published Census2020 school-stage travel-bin bounds; no midpoints."""
import json,hashlib,math,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
raw=json.loads((P/'travel_table_api.json').read_text())['result']
assert raw['total']==6
rows={r['Number']:r for r in raw['records']}
bins=['Up to 15','16 - 30','31 - 45','46 - 60','More than 60']
# Continuous conservative closures: do not assume integer-minute precision.
left=[0,15,30,45,60];right=[15,30,45,60,math.inf]
profiles=[]
all_stage={'Secondary_Total':174298,'Post_Secondary_Non_Tertiary_Total':56663,'PolytechnicDiploma_Total':72676}
pdftext=subprocess.check_output(['pdftotext','-layout',str(P/'cop2020sr2.pdf'),'-'],text=True)
assert '174,298' in pdftext and '56,663' in pdftext and '72,676' in pdftext
for field in ['Secondary_Total','Post_Secondary_Non_Tertiary_Total','PolytechnicDiploma_Total']:
 c=[int(rows[b][field]) for b in bins];n=int(rows['Total'][field])
 assert abs(sum(c)-n)<=3
 lo=sum((x-.5)*math.exp(-b/30) for x,b in zip(c,right))/(n+.5)
 hi=min(1,sum((x+.5)*math.exp(-a/30) for x,a in zip(c,left))/(n-.5))
 N=all_stage[field]
 resident_lo=sum((x-.5)*math.exp(-b/30) for x,b in zip(c,right))/(N+.5)
 missing_hi=(N+.5)-sum(x-.5 for x in c)
 resident_hi=min(1,(sum((x+.5)*math.exp(-a/30) for x,a in zip(c,left))+missing_hi)/(N-.5))
 profiles.append(dict(field=field,count=n,counts=c,utility_lower=lo,utility_upper=hi,all_stage_estimate=N,uncovered_estimate=N-n,resident_lower=resident_lo,resident_upper=resident_hi))
result=dict(city='Singapore',indicator='travel',year=2020,profiles=profiles,
 stage_hull=[min(x['resident_lower'] for x in profiles),max(x['resident_upper'] for x in profiles)],
 traveller_only_secondary_postsecondary_hull=[min(x['utility_lower'] for x in profiles[:2]),max(x['utility_upper'] for x in profiles[:2])],
 source_url='https://data.gov.sg/api/action/datastore_search?resource_id=d_e87b21cfebae1a77150eccded58ab116',
 pdf_url='https://www.parliament.gov.sg/docs/default-source/default-document-library/cop2020sr2.pdf',
 source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'travel_table_api.json',P/'cop2020sr2.pdf']},
 rule='exp(-t/30) endpoint integration, continuous bin closure, unbounded tail; rounded cell and total counts +/-0.5 propagated outward',
 scope='Resident school travellers in published education stages in 2020; excludes home study and overseas >=6 months. Stage means do not identify ages14-18 or2025 outcomes. All-stage denominator from Table93; unrepresented resident students retain utility[0,1]. Convex hull leaves stage mixture unknown. These are weighted household survey estimates, not complete headcounts. Conditional on published survey estimates; not a sampling confidence interval.')
(P/'derived_bounds.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
