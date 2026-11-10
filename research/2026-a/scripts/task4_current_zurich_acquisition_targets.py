"""Quantify conditional source targets without replacing any retained input."""
from pathlib import Path
import csv,hashlib,itertools,json,math,sys
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_user_v204_revision import revised_bounds
from task4_user_city_indicators import evaluate,SOURCE
from task4_v5_model import NAMES,weights,score
R=Path(__file__).resolve().parents[1];O=R/'results/current_zurich_acquisition_targets'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise ValueError('Frozen output exists; replay in a scratch checkout')
 f,lo,hi=revised_bounds();cities=f.city.tolist();z=cities.index('Zurich')
 pupil_source=R/'data/current_zurich_ptr_matching_followup/pupils_dataset.csv'
 with pupil_source.open(encoding='utf-8-sig',newline='') as stream:
  pupils=sum(int(r['anzahl']) for r in csv.DictReader(stream) if r['jahr']=='2024' and r['stufe']=='Sekundarstufe II')
 assert pupils==63925
 cases=[];records=[]
 for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
  base=evaluate(cities,lo,hi,w);winner=base.loc[base.decision_rank.eq(1),'city'].tolist();assert len(winner)==1
  for name in ['upper_secondary_ptr','travel']:
   j=NAMES.index(name);assert hi[z,j]==1
   def calc(u):
    a=lo.copy();a[z,j]=u;return evaluate(cities,a,hi,w)
   def lower(u):
    a=lo[z].copy();a[j]=u;return float(score(a[None,:],w)[0])
   def gap(u):
    t=calc(u);other=t.loc[t.city.ne('Zurich'),'max_regret'].min();return float(t.max_regret.iloc[z]-other)
   thresholds=[]
   if gap(lo[z,j])>1e-10 and gap(1)<-1e-10:
    thresholds.append(('recommendation_tie',None,brentq(gap,float(lo[z,j]),1,xtol=1e-14)))
   uppers=base.score_upper.to_numpy()
   for k,c in enumerate(cities):
    if k!=z and lower(lo[z,j])<uppers[k]<lower(1):
     u=brentq(lambda x:lower(x)-uppers[k],float(lo[z,j]),1,xtol=1e-14)
     thresholds.append(('possible_champion_boundary',c,u))
   for typ,city,u in thresholds:
    rec=dict(weight_reference=ref,indicator=name,event=typ,affected_city=city,utility_lower_threshold=u,
      equality='tie remains possible; strict exclusion requires lower greater than threshold' if city else 'regret tie; strict recommendation requires lower greater than threshold')
    if name=='upper_secondary_ptr':
     ptr=15*(1-u)/u;rec.update(conditional_PTR_upper=ptr,
      illustrative_canton_pupils=pupils,conditional_city_teaching_FTE_lower_needed=pupils/ptr)
    records.append(rec)
    for offset,label in [(-1e-6,'below'),(0,'boundary'),(1e-6,'above')]:
     t=calc(u+offset);choices=t.loc[t.decision_rank.eq(1),'city'].tolist()
     if typ=='recommendation_tie':
      if label=='below':assert choices==winner
      if label=='above':assert choices==['Zurich']
      assert abs(gap(u))<1e-10
     else:
      flag=bool(t.loc[t.city.eq(city),'possible_champion'].iloc[0])
      if label=='below':assert flag
      if label=='above':assert not flag
     cases.append(t.assign(weight_reference=ref,indicator=name,event=typ,affected_city=city,side=label,utility_lower=u+offset))
   for label,u in [('retained',float(lo[z,j])),('relaxed_endpoint',1.)]:
    cases.append(calc(u).assign(weight_reference=ref,indicator=name,event='endpoint',affected_city=None,side=label,utility_lower=u))
    assert not calc(u).necessary_champion.any()
 np.testing.assert_array_equal(revised_bounds()[1],lo);np.testing.assert_array_equal(revised_bounds()[2],hi)
 paths=[Path(__file__),SOURCE,pupil_source,R/'data/current_zurich_ptr_matching_followup/README.md',R/'results/current_zurich_ptr_matching_followup/extraction.json',R/'design/task4_user_v204_snapshot.json']
 paths += [Path(m.__file__).resolve() for m in list(sys.modules.values()) if getattr(m,'__file__',None) and Path(m.__file__).resolve().parent==R/'scripts']
 O.mkdir(parents=True);pd.DataFrame(records).to_csv(O/'thresholds.csv',index=False);pd.concat(cases,ignore_index=True).to_csv(O/'city_cases.csv',index=False)
 report=dict(status='pass conditional acquisition targets',primary_model='V204 unchanged',thresholds=records,
  source_sha256={str(p.relative_to(R)):sha(p) for p in sorted(set(paths))},
  output_sha256={n:sha(O/n) for n in ['thresholds.csv','city_cases.csv']},
  city_cases=sum(len(t) for t in cases),primary_admissions=0,actual_primary_width_reduction=0,changes_primary_model=False,changes_manuscript=False,
  scope='One Zurich lower utility coordinate at a time; all upper bounds, other utilities and weights retained. Thresholds are numerical conditional planning targets, not observations. Equality denotes a mathematical boundary: raw floating-point decision_rank may not display a tie, while champion flags use score tolerance1e-12. The checked below/above cases are1e-6 away from each root. Pupil63925 is a published canton total, not an admitted target upper bound. Conditional FTE thresholds require separately proving target pupil coverage, disjoint city upper-stage actual teaching activity, reference/date/provider compatibility and outward precision. Travel target is a utility bound for the retained population, not an inferred mean, support, trip distribution or school-population substitution. No finite sampled search certifies acquisition feasibility or unique real-world champion.')
 (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'threshold_count':len(records),'city_cases':report['city_cases']}))
if __name__=='__main__':main()
