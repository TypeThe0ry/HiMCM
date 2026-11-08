"""Independent numerical replay; no production scoring/ranking helpers used."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import pandas as pd
from scipy.stats import rankdata,kendalltau
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from task4_current_model import current_bounds
from task4_v5_model import CITIES,NAMES
out=ROOT/'results/task4_v112_ahp_mc'
s=json.loads((out/'summary.json').read_text())
lo,hi,config=current_bounds()
b=pd.read_csv(out/'utility_bounds.csv',float_precision='round_trip')
np.testing.assert_array_equal(b.lower.to_numpy().reshape(lo.shape),lo)
np.testing.assert_array_equal(b.upper.to_numpy().reshape(hi.shape),hi)
weight_table=pd.read_csv(out/'weights.csv',float_precision='round_trip')
centers={'inherited_policy':weight_table.inherited_weight.to_numpy(), 'neutral_symmetry':np.asarray(s['neutral_ahp']['weights'])}
assert s['ahp_status']=='neutral_reference_only_no_elicited_judgments'
np.testing.assert_allclose(centers['neutral_symmetry'],np.ones(10)/10,atol=1e-15,rtol=0)
np.testing.assert_array_equal(s['neutral_ahp']['matrix'],np.ones((10,10)))
assert s['neutral_ahp']['CR']==0
assert int(((lo==0)&(hi==1)).sum())==132
assert hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest()==s['source_bounds_sha256']
def scores(x,w):
    a=np.sqrt(np.einsum('dj,ij->di',w,x*x))
    b=np.sqrt(np.einsum('dj,ij->di',w,(1-x)**2))
    return 100*a/(a+b)
summary=pd.read_csv(out/'monte_carlo_city_summary.csv',float_precision='round_trip')
checks=[]
for center_name,conc in [(n,k) for n in s['mc_centers'] for k in s['concentrations']]:
    center=centers[center_name]
    ws=np.random.default_rng(np.random.SeedSequence([s['seed'],conc])).dirichlet(conc*center,size=s['draws_per_center_concentration'])
    expected=s['monte_carlo'][center_name+'_'+str(conc)]
    assert hashlib.sha256(ws.astype('<f8').tobytes()).hexdigest()==expected['sampled_weights_sha256']
    lower,upper,mid=[scores(x,ws) for x in (lo,hi,(lo+hi)/2)]
    ranks=rankdata(-mid,axis=1)
    possible=np.zeros(mid.shape,bool);necessary=possible.copy();regrets=np.zeros(mid.shape)
    best=np.zeros(mid.shape,int);worst=best.copy()
    for i in range(len(CITIES)):
        ul=np.delete(upper,i,axis=1);ll=np.delete(lower,i,axis=1)
        possible[:,i]=upper[:,i]>=ll.max(axis=1)-1e-12
        necessary[:,i]=lower[:,i]>=ul.max(axis=1)-1e-12
        regrets[:,i]=np.maximum(0,ul.max(axis=1)-lower[:,i])
        best[:,i]=1+(ll>upper[:,i,None]+1e-12).sum(axis=1)
        worst[:,i]=1+(ul>lower[:,i,None]+1e-12).sum(axis=1)
    rr=rankdata(regrets,axis=1)
    # Actual draws have no ties. Synthetic tie handling is checked separately by unit tests.
    assert np.all(np.sort(ranks,axis=1)==np.arange(1,26))
    assert np.all(np.sort(rr,axis=1)==np.arange(1,26))
    got=summary[(summary.concentration==conc)&(summary.center==center_name)].set_index('city').loc[CITIES]
    columns={
      'midpoint_mean_rank':ranks.mean(axis=0),
      'midpoint_mean_rank_order':rankdata(ranks.mean(axis=0)),
      'midpoint_first_frequency':(ranks==1).mean(axis=0),
      'midpoint_top3_frequency':(ranks<=3).mean(axis=0),
      'possible_champion_weight_frequency':possible.mean(axis=0),
      'necessary_champion_weight_frequency':necessary.mean(axis=0),
      'minimax_recommendation_weight_frequency':(rr==1).mean(axis=0),
      'minimax_mean_decision_rank':rr.mean(axis=0),
      'sampled_best_possible_rank':best.min(axis=0),
      'sampled_worst_possible_rank':worst.max(axis=0),
      'sampled_score_lower_min':lower.min(axis=0),
      'sampled_score_upper_max':upper.max(axis=0)}
    for col,values in columns.items():np.testing.assert_allclose(got[col],values,atol=1e-11,rtol=0,err_msg=col)
    counts=possible.sum(axis=1)
    assert counts.min()==expected['observed_possible_champion_count_min']
    assert counts.max()==expected['observed_possible_champion_count_max']
    assert counts.mean()==expected['observed_possible_champion_count_mean']
    assert [c for c,p in zip(CITIES,possible.any(axis=0)) if p]==expected['sampled_possible_champion_union']
    checks.append(dict(center=center_name,concentration=conc,draws=len(ws),replayed_city_draws=int(mid.size),verified_summary_cells=int(len(columns)*len(CITIES)),possible_count_range=[int(counts.min()),int(counts.max())],midpoint_leader=CITIES[np.argmin(ranks.mean(axis=0))],minimax_most_frequent=CITIES[np.argmax((rr==1).mean(axis=0))]))
result=dict(status='passed',independent_formula=True,unchanged_bound_cells=250,fully_unknown_cells=132,nonpoint_cells=int((hi-lo>1e-12).sum()),ahp_not_claimed_as_elicited=True,checks=checks,input_summary_sha256=hashlib.sha256((out/'summary.json').read_bytes()).hexdigest(),limitations=['Replays numerical sensitivity, not empirical validity of weight prior.','Midpoint scenario is not observed complete data.','Finite sampled weights do not certify full-simplex winner exclusion.'])
Path(__file__).with_name('validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
