"""Verified Phoenix2024 monitor network; unknown weights preserved as convex hull."""
import hashlib,json,zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from matplotlib.path import Path as Polygon
HERE=Path(__file__).resolve().parent

def extract():
 for name in ['manifest.json','documentation_manifest.json']:
  for f,meta in json.loads((HERE/name).read_text()).items():
   if 'sha256' in meta:
    b=(HERE/f).read_bytes();assert len(b)==meta['bytes'] and hashlib.sha256(b).hexdigest()==meta['sha256']
 with zipfile.ZipFile(HERE/'annual_conc_by_monitor_2024.zip') as z:
  assert z.testzip() is None
  member=z.namelist()[0];data=pd.read_csv(z.open(member))
 assert len(data)==68956 and set(data.Year)=={2024}
 az=data.loc[data['State Code'].eq(4)&data['Parameter Code'].eq(88101)].copy()
 # EPA defines City Name as incorporated city, not CBSA. Geographic overlay is a
 # secondary check; published NAD83/WGS84 coordinates are not silently relabelled.
 annual=az.loc[az['Pollutant Standard'].eq('PM25 Annual 2024') & az['Event Type'].isin(['No Events','Events Included'])].copy()
 ref=json.loads((HERE/'reused_boundary.json').read_text());bp=HERE.parent/ref['file'];assert hashlib.sha256(bp.read_bytes()).hexdigest()==ref['sha256']
 points=annual[['Longitude','Latitude']].to_numpy();inside=np.zeros(len(annual),bool)
 for f in json.loads(bp.read_text())['features']:
  g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
  for poly in polys:
   v=Polygon(poly[0]).contains_points(points)
   for hole in poly[1:]:v &= ~Polygon(hole).contains_points(points)
   inside |= v
 annual['inside_current_boundary_coordinate_check']=inside
 annual['source_city_phoenix']=annual['City Name'].eq('Phoenix')
 assert np.array_equal(inside,annual.source_city_phoenix.to_numpy())
 selected=annual.loc[annual.source_city_phoenix].copy()
 assert len(selected)==8 and selected['Site Num'].nunique()==6
 keys=['State Code','County Code','Site Num','Parameter Code','POC']
 all_city_ids=set(map(tuple,az.loc[az['City Name'].eq('Phoenix'),keys].drop_duplicates().to_numpy()))
 selected_ids=set(map(tuple,selected[keys].to_numpy()))
 assert all_city_ids==selected_ids, 'Omitted city PM2.5 monitor requires explicit review'
 assert selected[['State Code','County Code','Site Num','Parameter Code','POC']].duplicated().sum()==0
 assert set(selected['Completeness Indicator'])=={'Y'} and set(selected['Certification Indicator'])=={'Certified'}
 assert set(selected['Metric Used'])=={'Quarterly Means of Daily Means'}
 assert set(selected['Units of Measure'])=={'Micrograms/cubic meter (LC)'}
 assert set(selected['County Code'])=={13}
 selected['annual_method_ambiguous']=selected['Method Name'].eq('Multiple Methods Used')
 source_methods=[]
 for row in selected.to_dict('records'):
  same=az.loc[az['Site Num'].eq(row['Site Num'])&az.POC.eq(row['POC'])&az['Event Type'].isin(['No Events','Events Included'])]
  hourly=sorted(same.loc[same['Sample Duration'].eq('1 HOUR'),'Method Name'].dropna().unique())
  annual_method=row['Method Name']
  method=hourly if pd.isna(annual_method) else [annual_method]
  assert method, 'Unidentified source method requires explicit review'
  if not row['annual_method_ambiguous']:
   assert 'Multiple Methods Used' not in method, 'Hidden mixed method requires explicit review'
  assert not any(m in ['Teledyne T640 at 5.0 LPM','Teledyne T640X at 16.67 LPM'] for m in method)
  source_methods.append('|'.join(method))
 selected['underlying_method_evidence']=source_methods
 selected['method_fully_identified']=~selected.annual_method_ambiguous
 verified=selected.loc[selected.method_fully_identified]
 concentration=[float(selected['Arithmetic Mean'].min()),float(selected['Arithmetic Mean'].max())]
 assert concentration==[float(verified['Arithmetic Mean'].min()),float(verified['Arithmetic Mean'].max())]
 assert concentration==[7.041457,11.57591]
 utility=[15/(15+concentration[1]),15/(15+concentration[0])]
 annual.to_csv(HERE/'arizona_annual_candidates.csv',index=False)
 selected.to_csv(HERE/'phoenix_selected_monitors.csv',index=False)
 az.loc[az['City Name'].eq('Phoenix')].to_csv(HERE/'phoenix_all_standard_rows.csv',index=False)
 bysite=selected.groupby(['State Code','County Code','Site Num','Local Site Name'])['Arithmetic Mean'].agg(['min','max','count']).reset_index()
 bysite.to_csv(HERE/'phoenix_site_intervals.csv',index=False)
 result=dict(year=2024,source_rows=len(data),source_member=member,parameter=88101,standard='PM25 Annual 2024',
  measure='Quarterly Means of Daily Means, micrograms/cubic meter(LC)',
  phoenix_sites=6,phoenix_monitor_records=8,all_complete_and_certified=True,
  observation_percent_range=[int(selected['Observation Percent'].min()),int(selected['Observation Percent'].max())],
  retained_events='Events Included or No Events; no exceptional-event exclusions for exposure scenario',
  method_ambiguous_monitors=selected.loc[~selected.method_fully_identified,['Site Num','POC']].to_dict('records'),
  fully_identified_method_sites=int(verified['Site Num'].nunique()),
  extrema_unchanged_when_mixed_method_site_omitted=True,
  concentration_convex_hull=concentration,utility_convex_hull=utility,
  interpretation='Any convex weighting of these observed complete monitor annual summaries lies in this hull. It is NOT a bound on unmonitored neighborhoods, resident/high-school population exposure, temporal change or measurement bias.',
  geography='EPA City Name explicitly represents incorporated legal city. Current Phoenix boundary overlay agrees for all Arizona annual88101 candidates; untransformed published NAD83/WGS84 coordinate overlay is a secondary check, not a claim of datum/historical boundary equivalence.',
  weighting='No invented spatial/population weights and no average across duplicate POCs or pollutant-standard/event rows. Repeated monitor observations affect neither convex-hull endpoint.',
  method_advisory='EPA T640 advisory checked: namedoriginal236/238methods not among fullyidentified Phoenix rows. JLGsupersite has2MultipleMethodsUsed records, retained as methodambiguous; both inside extrema established by verified TEOMsites.',
  main_admitted=False)
 (HERE/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
 return result
def main():
 return extract()

if __name__=='__main__':print(json.dumps(main(),indent=2))
