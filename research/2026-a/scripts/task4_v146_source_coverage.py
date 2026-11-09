"""Trace each admitted supplement to a primary paper citation; do not admit data."""
from pathlib import Path
import csv,hashlib,json,re,subprocess
import numpy as np
from task4_user_city_indicators import SOURCE,build
from task4_user_v136_revision import revised_bounds
from task4_v5_model import NAMES
ROOT=Path(__file__).resolve().parents[1];PAPER=ROOT.parents[2]/'HiMCM-Overleaf';OUT=ROOT/'results/task4_v146_source_coverage'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def dump(name,value):(OUT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def table(name,rows):
 with (OUT/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def status(l,h):return 'point' if l==h else 'unknown' if l==0 and h==1 else 'partial'
def main():
 OUT.mkdir(exist_ok=True);mapping=read(ROOT/'design/task4_v146_source_map.json');base=mapping['before_overleaf_commit']
 oldref=subprocess.check_output(['git','show',base+':drafts/task4_v137_references.tex'],cwd=PAPER,text=True)
 oldcore=subprocess.check_output(['git','show',base+':drafts/task4_v137_core.tex'],cwd=PAPER,text=True)
 frame,lo,hi=revised_bounds();blo,bhi,_=build(frame);rows=[];sources={};seen=set()
 ref=(PAPER/'drafts/task4_v137_references.tex').read_text();core=(PAPER/'drafts/task4_v137_core.tex').read_text()
 blocks=dict(re.findall(r'\\bibitem\{([^}]+)\}(.*?)(?=\\bibitem|\\end\{thebibliography\})',ref,re.S))
 def cites(s):return {k.strip() for group in re.findall(r'\\cite\{([^}]+)\}',s) for k in group.split(',')}
 before_cites=cites(oldcore);current_cites=cites(core)
 for row in mapping['rows']:
  v=row['admission_version'][1:];path=ROOT/row['admission_manifest'];m=read(path);sources[row['admission_manifest']]=sha(path)
  for n,h in m['source_hashes'].items():assert sha(ROOT/n)==h,n;sources[n]=h
  observations=m.get('observations',[])
  for n in m.get('observation_files',[]):observations+=read(ROOT/n)
  matches=[o for o in observations if (o['city'],o['indicator'])==(row['city'],row['indicator'])];assert len(matches)==1
  o=matches[0];key=(o['city'],o['indicator']);assert key not in seen;seen.add(key)
  i=list(frame.city).index(key[0]);j=NAMES.index(key[1]);assert (blo[i,j],bhi[i,j])==(0,1)
  np.testing.assert_allclose([lo[i,j],hi[i,j]],o['utility_after'],atol=1e-12,rtol=0)
  # Reused sources carry additional complete paths; newer per-row bare names are
  # covered by the enclosing admission manifest's complete source_hashes map.
  for n,h in o.get('source_hashes',{}).items():
   if (ROOT/n).exists():assert sha(ROOT/n)==h,n;sources[n]=h
  k=row['bibkey'];assert k in blocks and k in current_cites,k
  urls=re.findall(r'\\url\{([^}]+)\}',blocks[k]);assert urls,k
  if k in {'sgbus_lta','sgpool_2025','warsawedu2025','zurichpool','milanpool2025','stockholmmetro2025'}:assert row['primary_url'] in urls,k
  rows.append(dict(**row,primary_reference_urls=json.dumps(urls),utility_lower=lo[i,j],utility_upper=hi[i,j],before_explicit_citation=(k in before_cites and '\\bibitem{'+k+'}' in oldref),after_explicit_citation=True,source_hashes=json.dumps(m['source_hashes'],sort_keys=True)))
 cells=[dict(city=city,indicator=n,before_status=status(blo[i,j],bhi[i,j]),current_status=status(lo[i,j],hi[i,j]),lower=lo[i,j],upper=hi[i,j],supplement=(city,n) in seen) for i,city in enumerate(frame.city) for j,n in enumerate(NAMES)]
 counts=[dict(indicator=n,**{s:sum(c['indicator']==n and c['current_status']==s for c in cells) for s in ['point','partial','unknown']}) for n in NAMES]
 assert len(rows)==21 and len(cells)==160
 totals={s:sum(c['current_status']==s for c in cells) for s in ['point','partial','unknown']};assert totals==dict(point=112,partial=33,unknown=15)
 table('admitted_sources.csv',rows);table('cell_coverage.csv',cells);table('indicator_coverage.csv',counts)
 gaps=[{k:r[k] for k in ['city','indicator','bibkey']} for r in rows if not r['before_explicit_citation']];assert len(gaps)==6
 dump('summary.json',dict(documentation_revision='V146',primary_evidence='V136 user16',extensions='V137',primary_data_admissions=0,before_overleaf_commit=base,supplements=21,citations_before=15,citations_after=21,repaired_gaps=gaps,current_counts=totals,per_indicator_counts=counts,original_csv_sha256=sha(SOURCE),source_sha256=sources,scope='Coverage describes interval treatment and explicit supplement citations, not independent validation of the 112 submitted points. Historical source-pack admission flags describe capture-time state; later admission manifests govern reuse.'))
 print('21 supplements traced; six citation gaps repaired; 112/33/15 unchanged.')
if __name__=='__main__':main()
