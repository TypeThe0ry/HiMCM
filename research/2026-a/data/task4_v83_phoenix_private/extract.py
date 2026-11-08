"""Audit released private-school records; not a census or whole-city estimate."""
from pathlib import Path
import hashlib,json,zipfile
import numpy as np
import pandas as pd
from matplotlib.path import Path as PolygonPath
HERE=Path(__file__).resolve().parent

def extract():
    for item in json.loads((HERE/'manifest.json').read_text()):
        raw=(HERE/item['file']).read_bytes()
        assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
    ref=json.loads((HERE/'boundary_reference.json').read_text())
    boundary=HERE.parent/ref['file']
    assert hashlib.sha256(boundary.read_bytes()).hexdigest()==ref['sha256']
    with zipfile.ZipFile(HERE/'pss2324_pu_csv.zip') as z:
        assert z.testzip() is None
        assert z.namelist()==['pss2324_pu.csv']
        d=pd.read_csv(z.open(z.namelist()[0]),encoding='cp1252',low_memory=False)
    assert len(d)==22510 and d.PPIN.is_unique
    a=d[d.PSTANSI==4].copy()
    points=a[['LONGITUDE24','LATITUDE24']].to_numpy(float)
    finite=np.isfinite(points).all(axis=1);inside=np.zeros(len(a),bool)
    for feature in json.loads(boundary.read_text())['features']:
        g=feature['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
        for poly in polys:
            keep=PolygonPath(poly[0]).contains_points(points)
            for hole in poly[1:]:keep &= ~PolygonPath(hole).contains_points(points)
            inside |= keep
    a['inside_current_boundary']=inside & finite
    a['mailing_city_phoenix']=a.PCITY.str.strip().str.upper().eq('PHOENIX')
    offered=['P265','P275','P285','P295'];counts=['P270','P280','P290','P300']
    grade=np.zeros((len(a),4))
    for j,(offer,count) in enumerate(zip(offered,counts)):
        assert a[offer].isin([1,2]).all()
        assert a.loc[a[offer]==1,count].notna().all()
        assert (a.loc[a[offer]==1,count]>=0).all()
        assert a.loc[a[offer]==2,count].isna().all()
        grade[:,j]=a[count].fillna(0)
    a['released_grade9_12_enrollment']=grade.sum(axis=1)
    a['target_enrollment_flagged']=(a[['F_'+x for x in offered+counts]]!=0).any(axis=1)
    assert (a.PFNLWT>0).all() and (a.NUMTEACH>=0).all()
    city=a[a.inside_current_boundary].copy();target=city[city.released_grade9_12_enrollment>0]
    teacher_cols=['P385','P390','P395','P400','P405']
    teacher_counts=target[teacher_cols].to_numpy(float)
    assert np.isfinite(teacher_counts).all() and (teacher_counts>=0).all()
    midpoint=teacher_counts@np.array([1,.875,.625,.375,.125])
    assert np.max(abs(midpoint-target.NUMTEACH.to_numpy()))<=.050000001
    fte_lower=float(teacher_counts.sum(axis=0)@np.array([1,.75,.5,.25,0]))
    fte_upper=float(teacher_counts.sum(axis=0)@np.array([1,1,.75,.5,.25]))
    cols=['PPIN','PINST','PCITY','PL_CIT','PSTANSI','LATITUDE24','LONGITUDE24','inside_current_boundary','mailing_city_phoenix','NUMSTUDS','NUMTEACH','PFNLWT','released_grade9_12_enrollment','target_enrollment_flagged']+offered+counts+['F_'+x for x in offered+counts]
    city[cols].to_csv(HERE/'released_city_records.csv',index=False,lineterminator='\n')
    mismatch=a[a.inside_current_boundary!=a.mailing_city_phoenix]
    mismatch[cols].to_csv(HERE/'mailing_boundary_disagreements.csv',index=False,lineterminator='\n')
    report=dict(school_year='2023-2024',national_released_records=len(d),arizona_released_records=len(a),arizona_missing_coordinates=int((~finite).sum()),city_released_records=len(city),city_records_with_grade9_12_students=len(target),city_released_grade9_12_count=int(target.released_grade9_12_enrollment.sum()),target_records_with_imputed_or_adjusted_enrollment=int(target.target_enrollment_flagged.sum()),target_all_stage_teacher_fte=float(target.NUMTEACH.sum()),target_all_stage_fte_category_bounds=[fte_lower,fte_upper],target_teacher_category_flagged_records=int((target[['F_'+x for x in teacher_cols]]!=0).any(axis=1).sum()),mailing_boundary_disagreement_records=len(mismatch),main_admitted=False,interpretation='Unweighted released-record sums only, including flagged imputation/adjustment. Not city population estimates or a complete roster. All-stage teacher FTE must not be paired with HS enrollment as an observed HS PTR. Private2023/24 and public2024/25 are separate years. Current boundary is an explicit geographic overlay, not verified historical boundary.')
    (HERE/'summary.json').write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':print(json.dumps(extract(),indent=2))
