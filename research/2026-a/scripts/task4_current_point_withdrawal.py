"""Single retained-point ignorance stress on explicit user16 V203; no primary edits."""
from pathlib import Path
import hashlib,json
import numpy as np,pandas as pd
from task4_user_v203_revision import revised_bounds
from task4_user_city_indicators import SOURCE,build,FIELDS,evaluate
from task4_v5_model import ROOT,NAMES,weights
from task4_interval_decision import interval_decision
O=ROOT/'results/current_point_withdrawal'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def decision(cities,lo,hi,w):
 t=evaluate(cities,lo,hi,w);d=interval_decision(t.score_lower,t.score_upper)
 return t,[cities[i] for i in d['minimax_choices']]
def main():
 f,lo,hi=revised_bounds();raw=pd.read_csv(SOURCE);origlo,orighi,_=build(raw)
 assert f.city.tolist()==raw.city.tolist() and lo.shape==(16,10)
 mask=lo==hi;original=origlo==orighi
 assert mask.sum()==112 and np.array_equal(mask,original)
 np.testing.assert_array_equal(lo[mask],origlo[mask]);np.testing.assert_array_equal(hi[mask],orighi[mask])
 cities=f.city.tolist();cases=[];ranks=[];base={}
 for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
  b,choices=decision(cities,lo,hi,w);base[ref]={'choices':choices,'minimax_regret':float(b.max_regret.min()),'mean_width':float((b.score_upper-b.score_lower).mean())}
  for i,j in zip(*np.where(mask)):
   a,c=lo.copy(),hi.copy();a[i,j]=0;c[i,j]=1
   t,after=decision(cities,a,c,w)
   field=FIELDS[j];original_row=raw.iloc[i];policy_regret=float(b.loc[b.city.isin(choices),'max_regret'].min())
   post_policy_regret=float(t.loc[t.city.isin(choices),'max_regret'].min());post_best=float(t.max_regret.min())
   mean_width=float((t.score_upper-t.score_lower).mean())
   assert mean_width>=base[ref]['mean_width']-1e-12 and post_best>=base[ref]['minimax_regret']-1e-12
   cases.append(dict(weight_reference=ref,withdrawn_city=cities[i],indicator=NAMES[j],input_field=field,submitted_value=original_row[field],submitted_year=original_row.get(field+'_year'),submitted_flag=original_row.get(field+'_flag'),retained_utility=float(lo[i,j]),baseline_choices=json.dumps(choices),after_choices=json.dumps(after),recommendation_set_changed=choices!=after,baseline_choice_excess_regret=post_policy_regret-post_best,post_minimax_regret=post_best,baseline_minimax_regret=policy_regret,mean_width=mean_width,mean_width_increase=mean_width-base[ref]['mean_width'],possible_champions=int(t.possible_champion.sum()),necessary_champions=int(t.necessary_champion.sum())))
   ranks.append(t.drop(columns=['midpoint_illustrative_score','midpoint_illustrative_rank']).assign(weight_reference=ref,withdrawn_city=cities[i],indicator=NAMES[j]))
 O.mkdir(exist_ok=True);out=pd.DataFrame(cases);out.to_csv(O/'cases.csv',index=False);pd.concat(ranks,ignore_index=True).to_csv(O/'ranks.csv',index=False)
 summary={'primary_model':'V203 unchanged','point_cells':112,'existing_interval_cells_held_fixed':48,'weight_references':2,'cases':len(out),'rank_rows':sum(len(x) for x in ranks),'baseline':base,'changed_recommendation_cases':{ref:int(g.recommendation_set_changed.sum()) for ref,g in out.groupby('weight_reference')},'primary_admissions':0,'actual_primary_width_reduction':0,'scope':'Each stress replaces exactly one retained point utility by [0,1]. Ignorance is hypothetical, not evidence of an erroneous measurement, empirical error probability or a new primary model. Cases prioritize source review; they do not authorize changing the original CSV.','source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [SOURCE,Path(__file__),ROOT/'design/task4_user_v203_snapshot.json']},'output_sha256':{n:sha(O/n) for n in ['cases.csv','ranks.csv']}}
 (O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
