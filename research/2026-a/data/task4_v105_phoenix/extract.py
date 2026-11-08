"""Same coverage rules across archived2023/24 and2024/25 official NCES records."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
from matplotlib.path import Path as PolygonPath
HERE=Path(__file__).resolve().parent
for r in json.loads((HERE/'reused_sources.json').read_text()):
 b=(HERE.parent/r['file']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']

def extract(folder,year):
 source=HERE.parent/folder
 ids=json.loads((source/'arizona_ids.json').read_text())['objectIds'];features=[]
 for path in sorted(source.glob('arizona_page_*.json')):
  d=json.loads(path.read_text());assert not d.get('exceededTransferLimit',False);features.extend(d['features'])
 assert len(ids)==len(set(ids))==len(features)
 assert set(ids)=={f['attributes']['OBJECTID'] for f in features}
 a=pd.DataFrame([f['attributes'] for f in features]);a=a.map(lambda x:x.strip() if isinstance(x,str) else x)
 assert a.NCESSCH.is_unique and set(a.SURVYEAR)=={year}
 points=np.array([[f['geometry']['x'],f['geometry']['y']] for f in features]);assert np.isfinite(points).all()
 inside=np.zeros(len(a),bool)
 for f in json.loads((HERE.parent/'task4_v6_phoenix/phoenix_boundary.geojson').read_text())['features']:
  g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
  for poly in polys:
   hit=PolygonPath(poly[0]).contains_points(points)
   for hole in poly[1:]:hit&=~PolygonPath(hole).contains_points(points)
   inside|=hit
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
 missing_fte=sel[sel.FTE<0];missing_n=sel[sel.target_enrollment_upper.isna()]
 explicit=sel[sel.explicit_grade_target_possible]
 ug_upper=float(sel.UG.clip(lower=0).sum())
 assert sel.UG.isin([-2]).all() or not sel.UG.isin([-1,-9]).any()
 sel.to_csv(HERE/(year+'_school_audit.csv'),index=False)
 missing_fte.to_csv(HERE/(year+'_missing_fte.csv'),index=False)
 missing_ug=sel[sel.UG.isin([-1,-9])]
 def ids(frame):return frame.NCESSCH.tolist()
 return dict(year=year,arizona_records=len(a),city_records=len(city),eligible_records=len(sel),explicit_eligible_records=len(explicit),strict_hs_records=int(sel.strict_hs_only.sum()),grade9_12_lower=int(sel.target_enrollment_lower.sum()),grade9_12_upper=None if len(missing_n) else int(sel.target_enrollment_upper.sum()),unknown_enrollment_upper_ids=ids(missing_n),known_ungraded_students=int(ug_upper),unknown_ungraded_records=len(missing_ug),including_possible_ungraded_upper=None if len(missing_n) or len(missing_ug) else int(sel.target_enrollment_upper.sum()+ug_upper),missing_fte_records=len(missing_fte),strict_missing_fte_records=int(missing_fte.strict_hs_only.sum()),known_strict_fte_contributors=int((sel.known_strict_hs_fte_lower>0).sum()),known_strict_teacher_fte_lower=float(sel.known_strict_hs_fte_lower.sum()),allstage_reported_fte_sum=float(sel.loc[sel.FTE>=0,'FTE'].sum()),teacher_fte_upper=None if len(missing_fte) else float(sel.FTE.sum()),membership_grade_conflicts=int(sel.membership_grade_conflict.sum()),unknown_virtual_city_records=int((city.operational & city.VIRTUAL.eq('N')).sum()))

if __name__=='__main__':
 reports=[extract('task4_v85_phoenix_public','2023-2024'),extract('task4_v42_phoenix_coverage','2024-2025')]
 a=pd.read_csv(HERE/'2023-2024_school_audit.csv',dtype={'NCESSCH':str});b=pd.read_csv(HERE/'2024-2025_school_audit.csv',dtype={'NCESSCH':str})
 joined=a.merge(b,on='NCESSCH',suffixes=('_23','_24'))
 transition=dict(shared_eligible_school_ids=len(joined),only_2023_24=len(a)-len(joined),only_2024_25=len(b)-len(joined),missing_to_reported_fte=int(((joined.FTE_23<0)&(joined.FTE_24>=0)).sum()),reported_to_missing_fte=int(((joined.FTE_23>=0)&(joined.FTE_24<0)).sum()))
 joined[['NCESSCH','SCH_NAME_23','SCH_NAME_24','FTE_23','FTE_24']].to_csv(HERE/'matched_fte_comparison.csv',index=False)
 result=dict(control='Identical V85 coverage and conservative grade-allocation rules, public-only, fixed current city boundary',years=reports,matched_school_comparison=transition,main_admitted=False,private_school_data_used=False,assumptions='School-assigned FTE additive; school-located rather than unique resident students. Missing codes retain uncertainty. No same-snapshot compatibility assumption for Hope ADE1178.',consequence='Unknown enrollment upper and missing teachers prevent a bounded citywide public PTR; no citywide/main interval revision.')
 (HERE/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
