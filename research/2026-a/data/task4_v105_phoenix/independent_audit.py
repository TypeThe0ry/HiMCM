"""Independent stdlib/Decimal rebuild; does not import the production extractor."""
from pathlib import Path
from decimal import Decimal
import csv,hashlib,json,math
P=Path(__file__).resolve().parent
for item in json.loads((P/'reused_sources.json').read_text()):
    b=(P.parent/item['file']).read_bytes()
    assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
polygons=[]
for f in json.loads((P.parent/'task4_v6_phoenix/phoenix_boundary.geojson').read_text())['features']:
    g=f['geometry'];polygons.extend(g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']])
def ring_inside(x,y,ring):
    # Independent even/odd ray crossing, with holes handled at polygon level.
    hit=False
    for (ax,ay),(bx,by) in zip(ring,ring[1:]+ring[:1]):
        if (ay>y)!=(by>y) and x < ax+(y-ay)*(bx-ax)/(by-ay):hit=not hit
    return hit
def within(f):
    x,y=f['geometry']['x'],f['geometry']['y'];assert math.isfinite(x) and math.isfinite(y)
    return any(ring_inside(x,y,p[0]) and not any(ring_inside(x,y,h) for h in p[1:]) for p in polygons)
def grade(v):
    return {'PK':-1,'KG':0}.get(v,int(v) if str(v).isdigit() else None)
def number(v):return Decimal(str(v))
results=[];selected={}
for folder,year in [('task4_v85_phoenix_public','2023-2024'),('task4_v42_phoenix_coverage','2024-2025')]:
    root=P.parent/folder;fs=[]
    for file in sorted(root.glob('arizona_page_*.json')):
        obj=json.loads(file.read_text());assert not obj.get('exceededTransferLimit');fs+=obj['features']
    ids=json.loads((root/'arizona_ids.json').read_text())['objectIds']
    assert len(ids)==len(set(ids))==len(fs) and set(ids)=={x['attributes']['OBJECTID'] for x in fs}
    city=[];out=[]
    for f in fs:
        r={k:v.strip() if isinstance(v,str) else v for k,v in f['attributes'].items()}
        assert r['SURVYEAR']==year
        if not within(f):continue
        city.append(r)
        if r['STATUS'] not in {'1','3','4','5','8'} or r['VIRTUAL']!='Not Virtual':continue
        lo,hi=grade(r['GSLO']),grade(r['GSHI']);known=lo is not None and hi is not None
        targets=[]
        for j in range(9,13):
            val=r[f'G{j:02d}']
            if val==-2 and known and (j<lo or j>hi):val=0
            targets.append(val)
        nl=sum(v for v in targets if v>0)
        explicit=(not known) or (lo<=12 and hi>=9) or nl>0
        if not explicit and r['UG']<=0:continue
        non=[r[k] for k in ['PK','KG']+[f'G{j:02d}' for j in range(1,9)]+['G13','UG']]
        strict=known and 9<=lo<=hi<=12 and all(v in (0,-2) for v in non+[r['AE']])
        upper=nl if all(v>=0 for v in targets) else (r['MEMBER']-sum(max(v,0) for v in non) if r['MEMBER']>=nl+sum(max(v,0) for v in non) else None)
        r.update(explicit=explicit,strict=strict,nlo=nl,nhi=upper,fte_lower=number(r['FTE']) if strict and nl>0 and r['FTE']>=0 else Decimal(0))
        out.append(r)
    selected[year]={r['NCESSCH']:r for r in out}
    assert len(selected[year])==len(out)
    csv_ids={r['NCESSCH'] for r in csv.DictReader((P/(year+'_school_audit.csv')).open())};assert csv_ids==set(selected[year])
    result={'year':year,'arizona_records':len(fs),'city_records':len(city),'eligible_records':len(out),'explicit_eligible_records':sum(r['explicit'] for r in out),'strict_hs_records':sum(r['strict'] for r in out),'UG_only_added_records':sum(not r['explicit'] for r in out),'known_ungraded_students':sum(max(r['UG'],0) for r in out),'grade9_12_lower':sum(r['nlo'] for r in out),'grade9_12_upper':None if any(r['nhi'] is None for r in out) else sum(r['nhi'] for r in out),'missing_fte_records':sum(r['FTE']<0 for r in out),'strict_missing_fte_records':sum(r['strict'] and r['FTE']<0 for r in out),'known_strict_fte_contributors':sum(r['fte_lower']>0 for r in out),'known_strict_teacher_fte_lower':str(sum((r['fte_lower'] for r in out),Decimal(0)))}
    results.append(result)
expected=json.loads((P/'summary.json').read_text())
for actual,exp in zip(results,expected['years']):
    for key,val in actual.items():
        if key=='UG_only_added_records':assert val==exp['eligible_records']-exp['explicit_eligible_records']
        elif key=='known_strict_teacher_fte_lower':assert Decimal(val)==Decimal(str(exp[key]))
        else:assert val==exp[key],(key,val,exp[key])
a,b=selected.values();shared=set(a)&set(b)
assert len(shared)==158
assert sum(a[i]['FTE']<0<=b[i]['FTE'] for i in shared)==74
assert sum(b[i]['FTE']<0<=a[i]['FTE'] for i in shared)==1
hope=b['040386003535'];assert hope['FTE']==4 and hope['nlo']==0 and hope['nhi'] is None and hope['fte_lower']==0
assert Decimal(results[1]['known_strict_teacher_fte_lower'])+Decimal(4)==Decimal('2512.97')
assert expected['main_admitted'] is False and expected['private_school_data_used'] is False
report={'status':'passed','method':'Independent Python standard-library ray crossing and Decimal arithmetic; raw source hashes and ID sets checked','years':results,'Hope_2024_raw_fields':{k:hope[k] for k in ['NCESSCH','GSLO','GSHI','MEMBER','G09','G10','G11','G12','FTE']},'Hope_exclusion':'No positive observed grades9–12 count; suppressed upper remains unknown; reported4FTE excluded by same rule','matched_ids':158,'missing_to_reported':74,'reported_to_missing':1,'whole_city_lower_bound_admissible':False,'reason':'Public school subset and school-location population do not establish all-city public+private resident enrolment/FTE. Unknown current public enrolment upper also precludes a positive ratio lower from known FTE alone.'}
(P/'independent_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: raw counts, independent geometry, UG expansion, Hope suppression, FTE sum and cross-year transitions.')
