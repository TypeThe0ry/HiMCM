"""Read original SIMCE files; preserve flags and avoid international scale mixing."""
import hashlib,json
from pathlib import Path
import pandas as pd
HERE=Path(__file__).resolve().parent

def main():
 source=json.loads((HERE/'simce_source.json').read_text())
 assert hashlib.sha256((HERE/'simce_2medio_2024.rar').read_bytes()).hexdigest()==source['sha256']
 assert hashlib.sha256((HERE/'chile_public_search_2024.json').read_bytes()).hexdigest()==source['search_sha256']
 for name,info in json.loads((HERE/'simce_members.json').read_text()).items():
  assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==info['sha256']
 schools=pd.read_csv(HERE/'simce2m2024_rbd_final.csv',sep=';',encoding='latin1')
 commune=pd.read_csv(HERE/'simce2m2024_comuna_final.csv',sep=';',encoding='latin1')
 d=schools.loc[schools.cod_com_rbd.eq(13101)].copy();c=commune.loc[commune.cod_com.eq(13101)]
 assert len(d)==64 and d.rbd.nunique()==64 and len(c)==1
 assert set(d.grado)=={'2m'} and set(d.agno)=={2024} and set(d.noaplica)=={0}
 assert set(d.nom_com_rbd.str.upper())=={'SANTIAGO'}
 rows=[]
 for code,name in [('lect','reading'),('mate','mathematics')]:
  n=d[f'nalu_{code}2m_rbd'];v=d[f'prom_{code}2m_rbd'];flag=d[f'marca_{code}2m_rbd'];valid=flag.isna()
  assert n.notna().all() and (n>0).all() and v.notna().all()
  eda=d[[f'palu_eda_{level}_{code}2m_rbd' for level in ['ins','ele','ade']]]
  zero=eda.eq(0).all(axis=1)
  rows.append({'subject':name,'official_commune_mean':float(c.iloc[0][f'prom_{code}2m_com']),
   'reported_test_takers':int(n.sum()),'school_records':len(d),'unflagged_school_records':int(valid.sum()),
   'unflagged_reported_test_takers':int(n[valid].sum()),'flagged_rbd':d.loc[~valid,'rbd'].astype(int).tolist(),
   'flagged_test_takers':int(n[~valid].sum()),
   'weighted_rounded_school_mean_diagnostic_all':float((n*v).sum()/n.sum()),
   'weighted_rounded_school_mean_diagnostic_unflagged':float((n[valid]*v[valid]).sum()/n[valid].sum()),
   'all_zero_proficiency_row_rbd':d.loc[zero,'rbd'].astype(int).tolist(),
   'all_zero_proficiency_test_takers':int(n[zero].sum())})
 summary={'main_admitted':False,'school_commune_code':13101,'school_commune_name':'Santiago','assessment':'SIMCE 2024 Segundo medio','source_school_records':len(schools),'selected_school_records':len(d),'source_grade':sorted(d.grado.unique()),'source_year':sorted(int(x) for x in d.agno.unique()),'source_database_date':sorted(int(x) for x in d.fecha_bbdd.unique()),'source_database_code':sorted(d.codigo_bbdd.unique()),'outcomes':rows,'scope':'Schools in Santiago commune13101, not metropolitan Santiago nor resident students. Current Segundo medio assessment, not all14-18 ages. National SIMCE points are not PISA points; no cross-test calibration is available. Published counts are examinees, not enrolled or resident cohort denominators.',
 'flags':'One school RBD8499 has marca2: results not representative for reasons outside the agency. Scores remain numerical, so filtering nonmissing alone is insufficient. RBD8759 has all-three-proficiency percentages zero despite positive examinees; no percentage aggregate is produced.',
 'aggregation':'Official commune means used directly. Weighted rounded school means are diagnostics only; publication does not establish precise aggregate inclusion or the proficiency-percentage denominator. No statistical confidence interval is inferred from rounded aggregates.',
 'version_note':'Filenames say final; embedded codigo_bbdd remains preliminar20240422v1 and date20250422. Both preserved without silently resolving the discrepancy.'}
 d.to_csv(HERE/'santiago_school_subset.csv',index=False)
 c.to_csv(HERE/'santiago_commune_row.csv',index=False)
 (HERE/'santiago_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 outputs=['santiago_school_subset.csv','santiago_commune_row.csv','santiago_summary.json']
 (HERE/'derived_manifest.json').write_text(json.dumps({name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in outputs},indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
