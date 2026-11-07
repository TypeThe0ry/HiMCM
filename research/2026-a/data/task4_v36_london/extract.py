"""Match official London Year12/13 pupils and school workforce by URN."""
from pathlib import Path
import hashlib,json,re,zipfile,xml.etree.ElementTree as E
import pandas as pd
ROOT=Path(__file__).resolve().parent
for m in json.loads((ROOT/'manifest.json').read_text()):
 b=(ROOT/m['file']).read_bytes();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(ROOT/'workforce.xlsx') as z:
 strings=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml'))]
 root=E.fromstring(z.read('xl/worksheets/sheet1.xml'))
 data=[];head={}
 for row in root.findall('.//m:row',ns):
  num=int(row.attrib['r']);vals={}
  for c in row:
   col=re.sub(r'\d','',c.attrib['r']);v=c.find('m:v',ns)
   if v is not None:vals[col]=strings[int(v.text)] if c.attrib.get('t')=='s' else v.text
  if num==9:head=vals
  elif num>=10:data.append({head[k]:v for k,v in vals.items() if k in head})
w=pd.DataFrame(data);assert w.URN.is_unique
p=pd.read_csv(ROOT/'pupils.csv',encoding='cp1252',low_memory=False,dtype=str);assert p.urn.is_unique
assert set(p.time_period)=={"202425"}
cols=[c for c in p if ('Year group 12' in c or 'Year group 13' in c)]
assert len(cols)==8
# Suppression markers remain unknown; never coerced to zero.
vals=p[cols].apply(pd.to_numeric,errors='coerce');p['upper_students']=vals.sum(axis=1,min_count=len(cols))
a=p[(p.region_name=='London')&(p.phase_type_grouping=='State-funded secondary')].copy()
a=a.merge(w[['URN','Total Number of Teachers (Headcount)','School Name','School Phase']],left_on='urn',right_on='URN',how='left',validate='one_to_one',indicator=True)
a['teacher_headcount']=pd.to_numeric(a['Total Number of Teachers (Headcount)'],errors='coerce')
a['has_observed_pupils']=a.upper_students.notna();a['has_numeric_teacher']=a.teacher_headcount.notna();a['positive_upper_students']=a.upper_students.gt(0)
a[['urn','school_name','upper_students','teacher_headcount','_merge','has_observed_pupils','has_numeric_teacher','positive_upper_students']].to_csv(ROOT/'school_match.csv',index=False)
active=a[a.positive_upper_students];matched=active[active.has_numeric_teacher]
assert a.upper_students.notna().all()
assert a.upper_students.sum()==106046
assert matched.upper_students.sum()+active.loc[~active.has_numeric_teacher,'upper_students'].sum()==106046
assert (matched.teacher_headcount>0).all()
assert (matched.teacher_headcount%1==0).all()
r=dict(all_london_secondary_schools=len(a),positive_year12_13_schools=len(active),unknown_pupil_schools=int(a.upper_students.isna().sum()),total_observed_year12_13_pupils=float(a.upper_students.sum()),positive_schools_with_numeric_teacher=len(matched),matched_pupils=float(matched.upper_students.sum()),missing_teacher_pupils=float(active.loc[~active.has_numeric_teacher,'upper_students'].sum()),matched_all_stage_teacher_headcount=float(matched.teacher_headcount.sum()),missing_teacher_schools=active.loc[~active.has_numeric_teacher,['urn','school_name','upper_students','_merge']].astype({'_merge':str}).to_dict('records'),grade_columns=cols,main_admitted=False,limitations='School teacher total is all stages, not dedicated sixth-form. November2024 versus January2025. Unmatched schools have no upper teacher bound; cannot infer full London PTR. Multiple teacher contracts and headcount summation require population definition.')
(ROOT/'summary.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
