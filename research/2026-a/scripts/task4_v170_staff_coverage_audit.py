"""Check new source packages, original workbook consistency, and frozen V154 comparison."""
from pathlib import Path
import csv,hashlib,json,re,subprocess,zipfile,xml.etree.ElementTree as E
import numpy as np
import pandas as pd
from task4_user_v154_revision import revised_bounds
from task4_user_city_indicators import evaluate
from task4_v5_model import NAMES,weights
R=Path(__file__).resolve().parents[1]; P=R.parents[2]/'HiMCM-Overleaf'; O=R/'results/task4_v170_staff_coverage'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 count=0
 for folder in ['task4_v170_dublin','task4_v170_zurich']:
  d=R/'data'/folder
  for row in read(d/'retrieval.json'):
   if row.get('status')==200:
    assert sha(d/row['file'])==row['sha256'] and (d/row['file']).stat().st_size==row['bytes'];count+=1
 d=R/'data/task4_v170_dublin'; ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
 with zipfile.ZipFile(d/'registration_q4_2025_original.xlsx') as z:
  strings=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',ns)]
  cells={}
  for sheet in [1,4]:
   root=E.fromstring(z.read(f'xl/worksheets/sheet{sheet}.xml'));cells[sheet]={}
   for c in root.findall('.//s:c',ns):
    v=c.find('s:v',ns)
    if v is not None:cells[sheet][c.attrib['r']]=strings[int(v.text)] if c.get('t')=='s' else v.text
   if sheet==4:
    b=[c for c in root.findall('.//s:c',ns) if re.fullmatch(r'B(?:[4-9]|[1-5][0-9])',c.get('r',''))]
    assert len(b)==56 and all(c.find('s:f',ns) is None and c.get('t') not in ['s','str','inlineStr'] for c in b)
    total=sum(int(c.find('s:v',ns).text) for c in b)
  assert cells[1]['A5']=='Post-primary ' and int(cells[1]['B5'])==52010
  assert total==52104 and total-int(cells[1]['B5'])==94
  assert cells[4]['A34']=='Co. Dublin' and cells[4]['B34']=='5331'
  assert '24/12/2025' in cells[1]['A1'] and 'more than one route' in cells[1]['A17']
 a=read(d/'scope_audit.json');assert a['admitted_cells']==0
 assert a['registration']['county_sheet_postprimary_column_sum']==total
 assert a['registration']['county_sum_minus_national_postprimary']==94
 assert len(a['registration']['selected_geography_rows'])==23
 q=subprocess.check_output(['pdftotext','-layout',str(d/'quality_original.pdf'),'-'],text=True).split('\f')
 m=subprocess.check_output(['pdftotext','-layout',str(d/'methodology_original.pdf'),'-'],text=True).split('\f')
 assert all(t in q[3] for t in ['published at this level','county level','private schools','salary is paid'])
 assert 'do not make any microdata' in ' '.join(m[5].split())
 zdir=R/'data/task4_v170_zurich'
 zscope=read(zdir/'source_scope.json')
 assert zscope['admitted_cells']==0 and not zscope['PTR_or_utility_computed']
 assert zscope['extractor_sha256']==sha(zdir/'extract.py')
 for n,h in zscope['source_sha256'].items():assert sha(zdir/n)==h,n
 chart=read(zdir/'official_staff_all_types_data_original.json')
 assert 'öffentlich finanzierten' in chart['meta']['title']
 assert set(chart['data'][0])=={'Schuljahr','Personalkategorie','Schultyp','Vollzeiteinheiten'}
 with zipfile.ZipFile(zdir/'bfs_staff_2024_25_original.xlsx') as z:
  strings=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',ns)]
  rel={x.get('Id'):x.get('Target') for x in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
  sheets={x.get('name'):'xl/'+rel[x.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
          for x in E.fromstring(z.read('xl/workbook.xml')).findall('s:sheets/s:sheet',ns)}
  selected={}
  for name in ['T8','T10','T11']:
   values={}
   for c in E.fromstring(z.read(sheets[name])).findall('.//s:c',ns):
    v=c.find('s:v',ns)
    if v is not None:values[c.get('r')]=strings[int(v.text)] if c.get('t')=='s' else v.text
   selected[name]=values
  t8,t10,t11=[selected[n] for n in ['T8','T10','T11']]
  assert 'öffentliche Schulen' in t8['B3'] and '2024/25' in t8['B3'] and t8['A7']=='Zürich'
  assert 'Lehrkräfte' in t10['C3'] and t10['A10']=='Privatschulen'
  assert 'Nicht auf Stufen' in t10['I5'] and 'Schulleitungspersonal' in t11['C3']
  for value,expected in [(t8['H7'],13797.7),(t8['E7'],938.3),(t10['J7'],86866.4),
    (t10['J11'],10242.2),(t10['F11'],695.2),(t10['G11'],1767.5),(t10['I11'],3453.2)]:
   assert abs(float(value)-expected)<1e-10
 source_check=dict(Dublin_registration_sheet4_sum=total,Dublin_registration_national_route=52010,
  discrepancy=94,county_column_numeric_cells_without_formulas=56,
  Zurich_chart_rows=len(chart['data']),Zurich_chart_status_date=chart['meta']['statusDate'],
  bfs_workbook='2024/25',Zurich_public_all_stage_FTE=13797.7,
  Swiss_private_all_stage_FTE=10242.2,Swiss_private_unassignable_stage_FTE=3453.2,
  candidate_only='National private FTE adds real coverage information. Complete enclosing-denominator and same-period city student lower-bound conditions have not been certified; no candidate PTR or utility bound admitted.',
  school_leaders_excluded=True)
 (O/'source_validation.json').write_text(json.dumps(source_check,indent=2)+'\n')
 snapshot=read(R/'design/task4_user_v154_snapshot.json')['source_sha256']
 for n,h in snapshot.items():assert sha(R/n)==h,n
 protected=read(O/'protected_files.json')['manuscript']
 for n,h in protected.items():assert sha(P/n)==h,n
 frame,lo,hi=revised_bounds();before=pd.read_csv(R/'results/task4_user_v154_revision/utility_bounds.csv')
 before=before[before.scenario=='after_conditional']
 for i,city in enumerate(frame.city):
  for j,indicator in enumerate(NAMES):
   row=before[(before.city==city)&(before.indicator==indicator)].iloc[0]
   np.testing.assert_allclose([lo[i,j],hi[i,j]],[row.lower,row.upper],atol=2e-15,rtol=0)
 historical=pd.read_csv(R/'results/task4_user_v154_revision/current_ranks.csv');comparisons=[]
 for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
  current=evaluate(frame.city.tolist(),lo,hi,w)
  old=historical[historical.weight_reference==ref].set_index('city').loc[current.city]
  for col in ['score_lower','score_upper','max_regret','decision_rank','best_rank','worst_rank']:
   np.testing.assert_allclose(current[col],old[col],atol=3e-13,rtol=0)
  assert current.possible_champion.tolist()==old.possible_champion.tolist()
  assert current.necessary_champion.tolist()==old.necessary_champion.tolist()
  comparisons.append(dict(weight_reference=ref,before_mean_width=float((old.score_upper-old.score_lower).mean()),
   after_mean_width=float((current.score_upper-current.score_lower).mean()),mean_width_reduction=0,
   conservative_recommendation=current.loc[current.decision_rank==1,'city'].tolist(),
   possible_champions=int(current.possible_champion.sum()),necessary_champions=int(current.necessary_champion.sum())))
 (O/'comparison.json').write_text(json.dumps(comparisons,indent=2)+'\n')
 result=dict(version='V170',passed=True,successful_official_responses=count,science_files_unchanged=len(snapshot),
  existing_overleaf_files_unchanged=len(protected),utility_cells_compared=160,deterministic_city_weight_cases=32,
  primary_data_admissions=0,score_width_reduction=0,registration_count_discrepancy=94,
  primary_science='V154 unchanged',current_paper='V168 unchanged',MC_rerun=False,
  source_scope='Dublin PDF publication scope and XLSX mismatch; Zurich API public scope and BFS T8/T10/T11 actual cells independently checked',goal='active')
 result['source_scope_sha256']={str(f.relative_to(R)):sha(f) for f in [d/'scope_audit.json',zdir/'source_scope.json']}
 (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
