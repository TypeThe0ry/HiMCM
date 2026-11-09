"""Independent CSV comparison against frozen original and V136 utility exports."""
from pathlib import Path
import csv,hashlib,json,re,subprocess
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/task4_v146_source_coverage'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open()))
def state(l,h):return 'point' if l==h else 'unknown' if (l,h)==(0,1) else 'partial'
def main():
 summary=json.loads((O/'summary.json').read_text());assert summary['primary_data_admissions']==0
 source=R/'data/task4_v117_team_intake/city_indicators.csv';assert sha(source)==summary['original_csv_sha256']=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
 before={(r['city'],r['indicator']):(float(r['utility_lower']),float(r['utility_upper'])) for r in rows(R/'results/task4_user_city_indicators/utility_bounds.csv')}
 current={(r['city'],r['indicator']):(float(r['lower']),float(r['upper'])) for r in rows(R/'results/task4_user_v136_revision/utility_bounds.csv') if r['scenario']=='after_conditional'}
 assert len(before)==len(current)==160
 ledger=rows(O/'cell_coverage.csv');assert len(ledger)==160;changes=set()
 for r in ledger:
  key=r['city'],r['indicator'];assert abs(float(r['lower'])-current[key][0])<1e-12 and abs(float(r['upper'])-current[key][1])<1e-12
  assert r['before_status']==state(*before[key]) and r['current_status']==state(*current[key])
  if before[key]!=current[key]:assert before[key]==(0,1) and state(*current[key])=='partial';changes.add(key)
 assert len(changes)==21
 admitted=rows(O/'admitted_sources.csv');assert len(admitted)==21 and {(r['city'],r['indicator']) for r in admitted}==changes
 ref=(P/'drafts/task4_v137_references.tex').read_text();core=(P/'drafts/task4_v137_core.tex').read_text()
 keys=re.findall(r'\\bibitem\{([^}]+)\}',ref);assert len(keys)==len(set(keys))
 cites={k.strip() for group in re.findall(r'\\cite\{([^}]+)\}',core) for k in group.split(',')}
 assert all(r['bibkey'] in keys and r['bibkey'] in cites for r in admitted)
 assert sum(r['before_explicit_citation']=='False' for r in admitted)==6
 for r in rows(O/'indicator_coverage.csv'):
  selected=[k for k in current if k[1]==r['indicator']]
  for s in ['point','partial','unknown']:assert sum(state(*current[k])==s for k in selected)==int(r[s])
 for name,h in summary['source_sha256'].items():assert sha(R/name)==h,name
 paths=['design/task4_v146_source_map.json','scripts/task4_v146_source_coverage.py','scripts/audit_task4_v146_source_coverage.py','results/task4_user_city_indicators/utility_bounds.csv','results/task4_user_v136_revision/utility_bounds.csv']
 result=dict(status='pass',independent_cells=160,independent_bounds=320,unchanged_original_points=112,unchanged_original_partial=12,fully_unknown_cells_narrowed=21,explicit_admitted_citations=21,repaired_citation_gaps=6,primary_data_admissions=0,source_sha256={n:sha(R/n) for n in paths},result_sha256={str(p.relative_to(R)):sha(p) for p in O.iterdir() if p.suffix in {'.json','.csv'} and p.name!='verification.json'},scope='Citation presence and utility treatment verified; original submitted measurements are not independently certified.')
 (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if not k.endswith('sha256')},indent=2))
if __name__=='__main__':main()
