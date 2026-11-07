"""Official school roster and secondary achievement; no invented pupil weights."""
import csv,json,zipfile,xml.etree.ElementTree as E,statistics,collections,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(P/'school_information_2024_25.xlsx') as z:
    strings=[''.join(t.text or '' for t in si.findall('.//s:t',NS)) for si in E.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',NS)]
    values=[]
    for row in E.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('s:sheetData/s:row',NS):
        d={}
        for c in row:
            col=''.join(x for x in c.attrib['r'] if x.isalpha());v=c.findtext('s:v',default='',namespaces=NS)
            d[col]=strings[int(v)] if c.attrib.get('t')=='s' and v else v
        values.append(d)
headers=values[0];rows=[{headers[k]:r.get(k,'') for k in headers} for r in values[1:] if r.get('A')]
city=[r for r in rows if r['Municipality']=='Toronto, City of' and r['School Level']=='Secondary']
assert city and len({r['School Number'] for r in city})==len(city)
fields=['Board Number','Board Name','School Number','School Name','School Special Condition Code','School Level','Grade Range','Municipality','City','Enrolment','Latitude','Longitude','Percentage of Grade 9 Students Achieving the Provincial Standard in Mathematics','Percentage of Students That Passed the Grade 10 OSSLT on Their First Attempt','Extract Date']
with (P/'toronto_secondary_roster.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({k:r[k] for k in fields} for r in city)
summary={'city_filter':'Municipality == Toronto, City of AND School Level == Secondary','schools':len(city),'by_board':dict(collections.Counter(r['Board Name'] for r in city)),'grade_ranges':dict(collections.Counter(r['Grade Range'] for r in city)),'achievement':{}}
district=[r for r in city if r['Board Number'] in ['B66052','B67059','B66303','B67318']]
summary['four_district_boards_only_school_count']=len(district)
summary['other_city_address_records']=[{'board':r['Board Name'],'school':r['School Name'],'school_number':r['School Number']} for r in city if r not in district]
summary['achievement_scope']='Four district boards only; excludes Independent Learning Centre/TVOntario'
for metric in fields[-3:-1]:
    obs=[float(r[metric][:-1]) for r in district if r[metric].endswith('%')]
    summary['achievement'][metric]={'reported_school_count':len(obs),'missing_or_suppressed':dict(collections.Counter(r[metric] for r in district if not r[metric].endswith('%'))),'school_equal_weight_median_percent':statistics.median(obs) if obs else None,'student_weighted_city_rate':None,'reason':'School grade/cohort test denominators not published in this table; full school enrollment is not a valid test denominator.'}
# Evidence for adult population/staff mismatch, not another ratio.
raw=P.parent/'task4_v38_toronto/financial_2024_25.csv'
with raw.open(encoding='utf-8-sig') as f:financial=list(csv.DictReader(f))
ids=['SC13_00168S','SC13_00184S','SC13_00190S','AP0H_00676C','AP0H0151882']
boards=['Toronto DSB','Toronto Catholic DSB','Conseil scolaire Viamonde','CSC MonAvenir']
with (P/'adult_day_scope_cells.csv').open('w',newline='') as f:
    ff=list(financial[0])[:8]+boards;w=csv.DictWriter(f,fieldnames=ff);w.writeheader()
    for r in financial:
        if r['Cell Name:'] in ids:w.writerow({k:r[k] for k in ff})
summary['decision']='secondary_school_achievement_evidence_and_municipal_roster; no city PTR or pupil-weighted quality admission'
(P/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
