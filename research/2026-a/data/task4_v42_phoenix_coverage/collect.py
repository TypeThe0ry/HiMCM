"""Complete Arizona CCD layer collection and Phoenix grade-count bounds."""
from pathlib import Path
import json,subprocess,hashlib,csv,math
from urllib.parse import urlencode
import numpy as np
import pandas as pd
from matplotlib.path import Path as PolygonPath
P=Path(__file__).resolve().parent
BASE='https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest/services/School_Characteristics_Current/FeatureServer/1/query'

def main():
 manifests=[]
 def fetch(name,params):
  url=BASE+'?'+urlencode(dict(f='json',**params));dest=P/name
  if not dest.exists():
   r=subprocess.run(['curl','--fail','--silent','--show-error','--max-time','40',url],capture_output=True,check=True)
   j=json.loads(r.stdout);assert 'error' not in j,j;dest.write_bytes(r.stdout)
  j=json.loads(dest.read_text());manifests.append(dict(file=name,url=url,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),bytes=dest.stat().st_size));return j
 ids=fetch('arizona_ids.json',dict(where="LSTATE = 'AZ'",returnIdsOnly='true'))['objectIds'];assert len(ids)==len(set(ids))
 features=[]
 for i in range(0,len(ids),500):
  part=sorted(ids)[i:i+500];raw=fetch(f'arizona_page_{i//500}.json',dict(where="LSTATE = 'AZ' AND OBJECTID >= %d AND OBJECTID <= %d"%(part[0],part[-1]),outFields='*',returnGeometry='true',outSR=4326))
  assert not raw.get('exceededTransferLimit',False)
  assert set(f['attributes']['OBJECTID'] for f in raw['features'])==set(part)
  features.extend(raw['features'])
 a=pd.DataFrame([f['attributes'] for f in features]);a=a.map(lambda x:x.strip() if isinstance(x,str) else x) if hasattr(a,'map') else a.applymap(lambda x:x.strip() if isinstance(x,str) else x)
 assert a.NCESSCH.is_unique and set(a.LSTATE)=={'AZ'} and set(a.SURVYEAR)=={'2024-2025'}
 pts=np.array([[f.get('geometry',{}).get('x',np.nan),f.get('geometry',{}).get('y',np.nan)] for f in features]);finite=np.isfinite(pts).all(axis=1);inside=np.zeros(len(a),bool)
 boundary=P.parent/'task4_v6_phoenix/phoenix_boundary.geojson'
 for feature in json.loads(boundary.read_text())['features']:
  geo=feature['geometry'];polys=geo['coordinates'] if geo['type']=='MultiPolygon' else [geo['coordinates']]
  for poly in polys:
   b=PolygonPath(poly[0]).contains_points(pts)
   for hole in poly[1:]:b&=~PolygonPath(hole).contains_points(pts)
   inside|=b
 a['within_current_phoenix_boundary']=inside;a['coordinates_finite']=finite
 a['operational']=a.STATUS.isin(['1','3','4','5','8']);a['nonvirtual']=a.VIRTUAL.eq('Not Virtual')
 grades=['G09','G10','G11','G12'];other=['PK','KG']+[f'G{i:02d}' for i in range(1,9)]+['G13','UG']
 def grade(s):
  if s=='PK':return -1
  if s=='KG':return 0
  try:return int(s)
  except:return None
 rows=[]
 for r in a.to_dict('records'):
  lo,hi=grade(r['GSLO']),grade(r['GSHI']);range_known=lo is not None and hi is not None
  overlap=range_known and lo<=12 and hi>=9
  observed=any(r[g]>0 for g in grades)
  possible=overlap or observed or not range_known
  effective={g:(0 if r[g]==-2 and range_known and not lo<=int(g[1:])<=hi else r[g]) for g in grades}
  targetknown=all(effective[g]>=0 for g in grades)
  lower=sum(max(0,effective[g]) for g in grades);otherlower=sum(max(0,r[g]) for g in other)
  member=r['MEMBER'];conflict=member>=0 and member<lower+otherlower
  upper=lower if targetknown else (max(lower,member-otherlower) if member>=0 and not conflict else None)
  r.update(grade_range_overlaps_9_12=bool(overlap),grade_range_known=range_known,positive_target_grade_count=observed,target_possible=bool(possible),pure_9_12=r['GSLO']=='09' and r['GSHI']=='12',within_9_12_only=bool(range_known and 9<=lo<=hi<=12),target_grade_counts_complete=targetknown,target_enrollment_lower=lower,target_enrollment_upper=upper,membership_grade_conflict=conflict,non_target_enrollment_known_lower=otherlower)
  rows.append(r)
 a=pd.DataFrame(rows);a.to_csv(P/'arizona_school_audit.csv',index=False)
 city=a[a.within_current_phoenix_boundary];city.to_csv(P/'phoenix_all_school_roster.csv',index=False)
 target=city[city.operational & city.nonvirtual & city.target_possible];target.to_csv(P/'phoenix_secondary_roster.csv',index=False)
 added=target[~target.GSHI.eq('12')];added.to_csv(P/'previously_omitted_high_grade_roster.csv',index=False)
 lower=float(target.target_enrollment_lower.sum());missingupper=int(target.target_enrollment_upper.isna().sum());upper=None if missingupper else float(target.target_enrollment_upper.sum())
 summary=dict(arizona_records=len(a),arizona_ids=len(ids),geographic_phoenix_all_public_schools=len(city),arizona_missing_coordinates=int((~a.coordinates_finite).sum()),operational_nonvirtual_secondary_possible_schools=len(target),pure_9_12_schools=int(target.pure_9_12.sum()),within_9_12_only_schools=int(target.within_9_12_only.sum()),mixed_or_other_range_schools=int((~target.within_9_12_only).sum()),omitted_by_previous_GSHI12_query=len(added),previously_omitted_schools=added[['NCESSCH','SCH_NAME','GSLO','GSHI','G09','G10','G11','G12','MEMBER','FTE']].to_dict('records'),school_record_grade9_12_enrollment_lower=lower,school_record_grade9_12_enrollment_upper=upper,schools_without_finite_upper=missingupper,membership_grade_conflicts=int(target.membership_grade_conflict.sum()),unknown_or_negative_FTE=int((target.FTE<0).sum()),scope='2024-25 public school records at current Phoenix municipal locations; nonvirtual operational; enrollment counts are not unique resident students; no private schools; no population inference')
 (P/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');(P/'manifest.json').write_text(json.dumps(manifests+[dict(file='../task4_v6_phoenix/phoenix_boundary.geojson',sha256=hashlib.sha256(boundary.read_bytes()).hexdigest())],indent=2)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k!='previously_omitted_schools'},indent=2));print(added[['SCH_NAME','GSLO','GSHI','MEMBER','FTE']].to_string(index=False))
if __name__=='__main__':main()
