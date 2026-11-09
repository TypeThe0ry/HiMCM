"""Joint age-group contrast in the retained 2012 aggregate uncertainty set."""
from pathlib import Path
import csv,hashlib,json,math
R=Path(__file__).resolve().parents[1];SOURCE=R/'data/task4_v116_ibb/aggregate_results.json';O=R/'results/task4_v148_age_contrast'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 O.mkdir(exist_ok=True);d=json.loads(SOURCE.read_text());labels=['14–15','16–18'];a,b=[d['age_groups'][g] for g in labels];ea,eb=[d['age_groups_optional_membership'][g] for g in labels]
 T=ea['weight_optional_unknown_age'];assert T==eb['weight_optional_unknown_age']==612 and ea['n_optional_unknown_age']==eb['n_optional_unknown_age']==2
 A=a['weight_total']+ea['weight_optional_known_age'];B=b['weight_total']+eb['weight_optional_known_age'];NA=a['utility_known_numerator'];NB=b['utility_known_numerator'];UA=a['weight_unknown']+ea['weight_optional_known_age'];UB=b['weight_unknown']+eb['weight_optional_known_age'];CA=A-NA-UA;CB=B-NB-UB
 assert A>NA>0 and B>NB>0 and CA>0 and CB>0
 # x is the shared mass assigned to younger students; all remaining mass is
 # assigned to older students. Including optional mass at the favourable endpoint
 # improves either contrast, so excluding it cannot improve either extremum.
 def low(x):return NA/(A+x)-(NB+UB+T-x)/(B+T-x)
 def high(x):return (NA+UA+x)/(A+x)-NB/(B+T-x)
 xmin=(math.sqrt(NA)*(B+T)-math.sqrt(CB)*A)/(math.sqrt(NA)+math.sqrt(CB));xmax=(math.sqrt(CA)*(B+T)-math.sqrt(NB)*A)/(math.sqrt(CA)+math.sqrt(NB))
 xl=min(T,max(0,xmin));xh=min(T,max(0,xmax));lower=low(xl);upper=high(xh)
 assert xl==xh==T
 marginal_low=ea['lower']-eb['upper'];marginal_high=ea['upper']-eb['lower'];assert marginal_low<lower<0<upper<marginal_high
 witnesses=[]
 for name,uy,uo in [('younger_higher',.95,.05),('older_higher',.05,.95)]:
  young=(NA+uy*(UA+T))/(A+T);old=(NB+uo*UB)/B;diff=young-old
  assert (diff>0)==(name=='younger_higher')
  witnesses.append(dict(witness=name,shared_mass_younger=T,shared_mass_older=0,optional_known_age_membership='all included in their own group',unknown_utility_younger=uy,unknown_utility_older=uo,unknown_duration_younger_minutes=-30*math.log(uy),unknown_duration_older_minutes=-30*math.log(uo),mean_utility_younger=young,mean_utility_older=old,difference=diff))
 with (O/'witnesses.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(witnesses[0]));w.writeheader();w.writerows(witnesses)
 result=dict(iteration='V148',historical_city='Istanbul',observation_year=2012,age_groups=labels,contrast='person-weighted mean q for 14-15 minus mean q for 16-18; q=exp(-t/30)',uncertainty_set='Retained V116 aggregate bounds: unknown utilities [0,1], optional membership, and one shared unknown-age pool; not all raw-record constraints or a sampling model.',shared_unknown_age_weight=T,shared_unknown_age_persons=2,constants=dict(A=A,B=B,NA=NA,NB=NB,UA=UA,UB=UB,CA=CA,CB=CB),joint_difference_closure=[lower,upper],naive_marginal_subtraction=[marginal_low,marginal_high],width_reduction=(marginal_high-marginal_low)-(upper-lower),allocation_at_lower=xl,allocation_at_upper=xh,stationary_points_unconstrained=dict(lower=xmin,upper=xmax),lower_derivative_at_T=-NA/(A+T)**2+CB/B**2,upper_derivative_at_T=CA/(A+T)**2-NB/B**2,endpoint_scope='Sharp infimum/supremum in the retained aggregate set. Utility zero is a closure limit as duration tends to infinity; it is not a finite observed trip. Both feasible ordering witnesses use finite durations and strictly interior utilities.',both_orderings_feasible=True,primary_data_admissions=0,primary_model_changed=False,exact_age14_vs18_identified=False,age_preferences_observed=False,source_sha256={str(SOURCE.relative_to(R)):sha(SOURCE)},witnesses_sha256=sha(O/'witnesses.csv'),generator_sha256=sha(Path(__file__)))
 (O/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['joint_difference_closure','naive_marginal_subtraction','both_orderings_feasible']},indent=2))
if __name__=='__main__':main()
