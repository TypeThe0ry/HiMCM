"""Reproduce a dated public-school roster; preserve missing staff and coverage."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
from matplotlib.path import Path as PolygonPath
HERE=Path(__file__).resolve().parent

def extract():
    for r in json.loads((HERE/'manifest.json').read_text()):
        b=(HERE/r['file']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
    ref=json.loads((HERE/'reused_source.json').read_text());boundary=HERE.parent/ref['file'];assert hashlib.sha256(boundary.read_bytes()).hexdigest()==ref['sha256']
    ids=json.loads((HERE/'arizona_ids.json').read_text())['objectIds']
    features=[]
    for p in sorted(HERE.glob('arizona_page_*.json')):
        d=json.loads(p.read_text());assert not d.get('exceededTransferLimit',False);features.extend(d['features'])
    assert len(ids)==len(set(ids))==len(features)==2609
    assert set(ids)=={f['attributes']['OBJECTID'] for f in features}
    a=pd.DataFrame([f['attributes'] for f in features]);a=a.map(lambda x:x.strip() if isinstance(x,str) else x)
    assert a.NCESSCH.is_unique and set(a.SURVYEAR)=={'2023-2024'} and set(a.LSTATE)=={'AZ'}
    points=np.array([[f['geometry']['x'],f['geometry']['y']] for f in features]);assert np.isfinite(points).all()
    inside=np.zeros(len(a),bool)
    for f in json.loads(boundary.read_text())['features']:
        g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
        for poly in polys:
            b=PolygonPath(poly[0]).contains_points(points)
            for hole in poly[1:]:b&=~PolygonPath(hole).contains_points(points)
            inside|=b
    a['inside_current_boundary']=inside
    def gr(v):
        if v=='PK':return -1
        if v=='KG':return 0
        try:return int(v)
        except (TypeError,ValueError):return None
    target=['G09','G10','G11','G12'];other=['PK','KG']+[f'G{i:02d}' for i in range(1,9)]+['G13','UG']
    records=[]
    for r in a.to_dict('records'):
        low,high=gr(r['GSLO']),gr(r['GSHI']);known=low is not None and high is not None
        effective={c:(0 if r[c]==-2 and known and not low<=int(c[1:])<=high else r[c]) for c in target}
        nlo=sum(max(0,v) for v in effective.values());otherlo=sum(max(0,r[c]) for c in other)
        conflict=r['MEMBER']>=0 and r['MEMBER']<nlo+otherlo
        complete=all(v>=0 for v in effective.values())
        nhi=nlo if complete else (max(nlo,r['MEMBER']-otherlo) if r['MEMBER']>=0 and not conflict else None)
        explicit_possible=not known or low<=12 and high>=9 or nlo>0
        possible=explicit_possible or r['UG']>0
        strict=known and 9<=low<=high<=12 and all(r[c] in [0,-2] for c in other+['AE'])
        r.update(operational=r['STATUS'] in ['1','3','4','5','8'],nonvirtual=r['VIRTUAL']=='Not Virtual',target_possible=bool(possible),explicit_grade_target_possible=bool(explicit_possible),strict_hs_only=bool(strict),target_enrollment_lower=nlo,target_enrollment_upper=nhi,non_target_known_lower=otherlo,membership_grade_conflict=conflict,known_strict_hs_fte_lower=r['FTE'] if strict and nlo>0 and r['FTE']>=0 else 0)
        records.append(r)
    a=pd.DataFrame(records);city=a[a.inside_current_boundary];sel=city[city.operational&city.nonvirtual&city.target_possible]
    city.to_csv(HERE/'city_public_records.csv',index=False,lineterminator='\n');sel.to_csv(HERE/'secondary_public_records.csv',index=False,lineterminator='\n')
    missing_fte=sel[sel.FTE<0];missing_n=sel[sel.target_enrollment_upper.isna()]
    missing_fte.to_csv(HERE/'missing_staff_records.csv',index=False,lineterminator='\n')
    explicit=sel[sel.explicit_grade_target_possible]
    ug_upper=float(sel.UG.clip(lower=0).sum())
    assert sel.UG.isin([-2]).all() or not sel.UG.isin([-1,-9]).any()
    hope=sel[sel.NCESSCH=='040386003535'];assert len(hope)==1
    h=hope.iloc[0];assert [int(h[c]) for c in target]==[6,7,19,51] and h.MEMBER==83 and h.FTE==4
    def items(f):return f[['NCESSCH','SCH_NAME','MEMBER','FTE']].to_dict('records')
    report=dict(school_year='2023-2024',source='Official historical NCES EDGE MapServer, not mutable current layer',arizona_records=len(a),city_records=len(city),operational_nonvirtual_possible_hs_records=len(sel),strict_hs_only_records=int(sel.strict_hs_only.sum()),grade9_12_enrollment_lower=int(sel.target_enrollment_lower.sum()),grade9_12_enrollment_upper=None if len(missing_n) else int(sel.target_enrollment_upper.sum()),missing_enrollment_upper_records=items(missing_n),missing_teacher_fte_count=len(missing_fte),missing_teacher_fte_file='missing_staff_records.csv',explicit_grade_eligible_records=len(explicit),explicit_grade_missing_fte_count=int((explicit.FTE<0).sum()),ungraded_students_upper=int(ug_upper),ungraded_positive_records=int((sel.UG>0).sum()),including_possible_ungraded_student_upper=int(sel.target_enrollment_upper.sum()+ug_upper),known_strict_hs_fte_contributing_records=int((sel.known_strict_hs_fte_lower>0).sum()),known_strict_hs_teacher_fte_lower=float(sel.known_strict_hs_fte_lower.sum()),reported_nonnegative_allstage_fte_sum=round(float(sel.loc[sel.FTE>=0,'FTE'].sum()),2),allstage_teacher_fte_upper=None if len(missing_fte) else float(sel.FTE.sum()),membership_grade_conflicts=int(sel.membership_grade_conflict.sum()),hope=dict(nces_id=str(h.NCESSCH),grade9_12=[int(h[c]) for c in target],students=83,teacher_fte=4,physical_address='6401 S 16TH ST, PHOENIX'),unknown_virtual_city_records=int((city.operational & city.VIRTUAL.eq('N')).sum()),main_admitted=False,interpretation='Public records and private PSS now share2023/24year, but unknown staff, ungraded allocation, nonresponse/private coverage and current-boundary overlay remain. Known FTE lower assumes additive school-assigned instructional FTE; missing staff contributes no observed value, not an observed zero. Hope83is historical and cannot fill2024/25suppression.')
    (HERE/'summary.json').write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':print(json.dumps(extract(),indent=2))
