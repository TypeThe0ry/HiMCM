"""Offline geofilter of official NCES school data; diagnostic subset, not whole-city PTR."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
from matplotlib.path import Path as PolygonPath
ROOT=Path(__file__).resolve().parent

def extract():
    for row in json.loads((ROOT/'manifest.json').read_text()):
        if 'sha256' in row:
            assert hashlib.sha256((ROOT/row['file']).read_bytes()).hexdigest()==row['sha256'],row['file']
    raw=json.loads((ROOT/'nces_arizona_secondary.json').read_text())
    assert not raw.get('exceededTransferLimit',False)
    attrs=pd.DataFrame([r['attributes'] for r in raw['features']])
    # ArcGIS fixed-width source strings retain trailing blanks.
    for col in attrs.select_dtypes(include='object').columns:
        attrs[col]=attrs[col].str.strip()
    assert attrs.NCESSCH.is_unique and set(attrs.LSTATE)=={'AZ'}
    assert set(attrs.SURVYEAR)=={'2024-2025'}
    points=np.array([[r['geometry']['x'],r['geometry']['y']] for r in raw['features']])
    assert np.isfinite(points).all()
    inside=np.zeros(len(points),bool)
    for feature in json.loads((ROOT/'phoenix_boundary.geojson').read_text())['features']:
        geo=feature['geometry'];polys=geo['coordinates'] if geo['type']=='MultiPolygon' else [geo['coordinates']]
        for poly in polys:
            local=PolygonPath(poly[0]).contains_points(points)
            for hole in poly[1:]:local &= ~PolygonPath(hole).contains_points(points)
            inside |= local
    attrs['within_current_phoenix_boundary']=inside
    attrs['pure_9_12']=(attrs.GSLO=='09')&(attrs.GSHI=='12')
    attrs['not_virtual']=attrs.VIRTUAL=='Not Virtual'
    attrs['operational']=attrs.STATUS.isin(['1','3','4','5','8'])
    attrs['valid_membership_teacher']=(attrs.MEMBER>=0)&(attrs.FTE>0)
    attrs['grade_total']=attrs[['G09','G10','G11','G12']].sum(axis=1)
    attrs['valid_grade_counts']=(attrs[['G09','G10','G11','G12']]>=0).all(axis=1)
    attrs['grade_total_matches_membership']=attrs.grade_total==attrs.MEMBER
    attrs['included_in_complete_subset']=attrs[['within_current_phoenix_boundary','pure_9_12','not_virtual','operational','valid_membership_teacher','valid_grade_counts','grade_total_matches_membership']].all(axis=1)
    attrs.to_csv(ROOT/'school_audit.csv',index=False)
    sub=attrs[attrs.included_in_complete_subset]
    students=int(sub.MEMBER.sum());teachers=float(sub.FTE.sum());ptr=students/teachers
    out=dict(city='Phoenix',indicator='upper_secondary_ptr',value=ptr,year='2024-25',students=students,teachers=teachers,schools=len(sub),unit='students_per_teacher_FTE',source_url='https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest/services/School_Characteristics_Current/FeatureServer/1',scope='Complete-record nonvirtual public schools exclusively grades9-12 geographically inside current Phoenix city boundary; school locations not student residences; includes multiple districts and charters; excludes private and mixed-grade schools; FTE not headcount; not representative all-city estimate',status='diagnostic_complete_record_subset_not_admitted_citywide',lower_bound_only=False)
    pd.DataFrame([out]).to_csv(ROOT/'observations.csv',index=False)
    summary={'arizona_grade_high12_records':len(attrs),'geographic_city_grade_high12_records':int(inside.sum()),'geographic_city_pure9_12':int((inside&attrs.pure_9_12).sum()),'complete_nonvirtual_pure9_12_schools':len(sub),'students':students,'teacher_FTE':teachers,'subset_PTR':ptr,'subset_utility_at_anchor15':15/(15+ptr),'school_districts_or_agencies':int(sub.LEAID.nunique()),'citywide_main_utility_lower':0,'citywide_main_utility_upper':1}
    (ROOT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    assert len(sub)>0 and sub.LEAID.nunique()>1
    assert (sub.grade_total==sub.MEMBER).all()
    assert (sub.MEMBER>=0).all() and (sub.FTE>0).all()
    city=attrs[attrs.within_current_phoenix_boundary]; grades=['G09','G10','G11','G12']
    coverage=dict(city_schools_with_highest_grade12=len(city),
        nonnegative_grade9_12_known_student_sum=int(city[grades].where(city[grades]>=0).sum().sum()),
        unknown_grade_cells=int(city[grades].lt(0).sum().sum()),
        schools_with_any_unknown_grade9_12_count=int(city[grades].lt(0).any(axis=1).sum()),
        full_virtual_school_count=int(city.VIRTUAL.eq('Full Virtual').sum()),
        not_virtual_school_count=int(city.not_virtual.sum()),
        other_virtual_status_school_count=int((~city.VIRTUAL.isin(['Full Virtual','Not Virtual'])).sum()),
        missing_or_nonpositive_FTE_schools=int(city.FTE.le(0).sum()),
        negative_membership_schools=int(city.MEMBER.lt(0).sum()),
        pure9_12_schools=int(city.pure_9_12.sum()),mixed_lower_grade_schools=int((~city.pure_9_12).sum()),
        pure9_12_missing_or_nonpositive_FTE_schools=int((city.pure_9_12&city.FTE.le(0)).sum()),
        note='GSHI12 records only; excludes highest-grade13/other codes. Known enrollments are not de-duplicated resident students; not complete target denominator.')
    (ROOT/'coverage_diagnostic.json').write_text(json.dumps(coverage,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':extract()
