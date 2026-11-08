"""Independent long-double quadratic replay; no model function imports."""
import csv, hashlib, json
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
D=np.longdouble
MAIN=[0,1,2,3,4,5,7,8]; AUX=[6,9]; TOL=D('1e-12')
def read(p):
 with p.open(newline='') as f:return list(csv.DictReader(f))
def terms(z):
 b=np.array([np.mean(z[MAIN]**2),np.mean(z[AUX]**2)],dtype=D)
 a=np.array([np.mean((1-z[MAIN])**2),np.mean((1-z[AUX])**2)],dtype=D)
 return np.array([a[0],a[1]-a[0]]),np.array([b[0],b[1]-b[0]])
def coefficients(x,y):
 a,b=terms(x);c,d=terms(y)
 return np.array([b[0]*c[0]-d[0]*a[0],b[0]*c[1]+b[1]*c[0]-d[0]*a[1]-d[1]*a[0],b[1]*c[1]-d[1]*a[1]],dtype=D)
def feasible(x,others):
 polys=[coefficients(x,y) for y in others]; cuts=[D('.05'),D('.2')]
 for c,b,a in polys:
  roots=[]
  if a==0:
   if b!=0:roots=[-c/b]
  else:
   disc=b*b-4*a*c
   if disc>=0:
    q=-D('.5')*(b+np.copysign(np.sqrt(disc),b))
    roots=[q/a,c/q] if q!=0 else [-b/(2*a)]
  cuts.extend(r for r in roots if D('.05')<r<D('.2'))
 cuts=sorted(set(cuts)); points=cuts+[(a+b)/2 for a,b in zip(cuts[:-1],cuts[1:])]
 margins=[min((a*t+b)*t+c for c,b,a in polys) for t in points]
 best=max(margins)
 return best>=-TOL,best

def main():
 summary=json.loads((P/'summary.json').read_text()); data=read(P/'baseline/utility_bounds.csv')
 cities=list(dict.fromkeys(x['city'] for x in data));names=[x['indicator'] for x in data[:10]];city=cities.index('Phoenix')
 assert len(data)==250 and len(cities)==25 and len(set(names))==10
 lo=np.array([D(x['lower']) for x in data]).reshape(25,10);hi=np.array([D(x['upper']) for x in data]).reshape(25,10)
 assert hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest()==summary['input_bounds_sha256']
 others=np.delete(lo,city,axis=0); rows=read(P/'bundle_thresholds.csv');checked=0; near=[]
 assert len(rows)==128 and len({x['indicators'] for x in rows})==128
 def candidate(js,rho):
  x=hi[city].copy();x[js]=lo[city,js]+rho*(hi[city,js]-lo[city,js]);return x
 for r in rows:
  js=[names.index(n) for n in r['indicators'].split('|') if n];assert len(js)==int(r['size'])
  zero,_=feasible(candidate(js,D(0)),others);assert zero==(r['status']=='cannot_exclude_even_exact')
  if r['status']=='bracketed':
   left,right=D(r['excluded_rho']),D(r['possible_rho']);assert 0<right-left<=D(2)**-40+D('1e-17')
   for rho,expected in [(left,False),(right,True)]:
    actual,margin=feasible(candidate(js,rho),others);checked+=1
    if actual!=expected:
     # Binary64 polynomial arithmetic and decimal CSV replay differ near -tol.
     assert abs(margin+TOL)<D('2e-16')
     near.append(dict(indicators=r['indicators'],rho=float(rho),expected=expected,independent=bool(actual),margin=float(margin)))
   # Resolve arithmetic-scale ambiguities by independently checking an enlarged bracket.
   assert not feasible(candidate(js,max(D(0),left-D('2e-9'))),others)[0]
   assert feasible(candidate(js,min(D(1),right+D('2e-9'))),others)[0]
  else:assert r['status']=='cannot_exclude_even_exact'
 prior=read(P.parent/'task4_v80_precision_frontier/bundle_thresholds.csv');old={r['indicators']:r for r in prior}
 comparison=[]
 for r in rows:
  before=old[r['indicators']]
  entry={k:r[k] for k in ('city','size','indicators')}
  for label,source in [('v80',before),('v94',r)]:
   entry.update({k+'_'+label:source[k] for k in ('status','excluded_rho','possible_rho','witness_alpha')})
  entry['pm_selected']='pm25' in r['indicators'].split('|');comparison.append(entry)
 with (P/'comparison_v80.csv').open('w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=list(comparison[0]));writer.writeheader();writer.writerows(comparison)
 changes=[]
 for selected in (False,True):
  group=[x for x in comparison if x['pm_selected']==selected]
  common=[x for x in group if x['status_v80']==x['status_v94']=='bracketed']
  directions=[D(x['excluded_rho_v94'])-D(x['excluded_rho_v80']) for x in common]
  assert all(d<0 if selected else d>0 for d in directions)
  changes.append(dict(pm_selected=selected,bundles=len(group),exact_excludable_v80=sum(x['status_v80']=='bracketed' for x in group),exact_excludable_v94=sum(x['status_v94']=='bracketed' for x in group),common_thresholds=len(common),common_threshold_direction='decrease' if selected else 'increase'))
 changed=sum(r['status']!=old[r['indicators']]['status'] for r in rows)
 result=dict(model_version=summary['model_version'],input_hash_verified=True,checked_bundles=len(rows),checked_bracket_endpoints=checked,
  classifications_match=True,matched_bundle_groups=changes,endpoint_arithmetic_ambiguities=near,independent_enlarged_bracket_padding=2e-9,
  changed_exact_exclusion_classifications_vs_v80=changed,method='Long-double direct quadratic coefficients and stable analytical roots; same 1e-12 polynomial decision tolerance. No scoring imports.',formal_interval_arithmetic=False)
 (P/'independent_check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
