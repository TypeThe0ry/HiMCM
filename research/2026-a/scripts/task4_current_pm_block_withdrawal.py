"""Withdraw all sixteen PM point utilities in a temporary V203 product box."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
from task4_user_v203_revision import revised_bounds
from task4_user_city_indicators import evaluate
from task4_v5_model import NAMES,weights
R=Path(__file__).resolve().parents[1];O=R/'results/current_pm_block_withdrawal'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    f,lo,hi=revised_bounds();cities=f.city.tolist();j=NAMES.index('pm25')
    assert len(cities)==16 and np.array_equal(lo[:,j],hi[:,j])
    assert f.pm25_ugm3_flag.tolist()==['MODELLED']*16 and f.pm25_ugm3_year.tolist()==[2024]*16
    a=lo.copy();b=hi.copy();a[:,j]=0;b[:,j]=1
    mask=np.ones(lo.shape,dtype=bool);mask[:,j]=False
    assert mask.sum()==144 and np.array_equal(a[mask],lo[mask]) and np.array_equal(b[mask],hi[mask])
    tables=[];bounds=[];cases=[]
    for scenario,ll,hh in [('retained_V203',lo,hi),('all_PM_points_withdrawn',a,b)]:
        bounds.extend(dict(scenario=scenario,city=c,indicator=name,lower=float(ll[i,k]),upper=float(hh[i,k])) for i,c in enumerate(cities) for k,name in enumerate(NAMES))
        for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
            t=evaluate(cities,ll,hh,w);tables.append(t.drop(columns=['midpoint_illustrative_score','midpoint_illustrative_rank']).assign(scenario=scenario,weight_reference=ref))
            cases.append(dict(scenario=scenario,weight_reference=ref,recommendations=t.loc[t.decision_rank.eq(1),'city'].tolist(),possible_champions=int(t.possible_champion.sum()),necessary_champions=int(t.necessary_champion.sum()),mean_width=float((t.score_upper-t.score_lower).mean())))
    contrasts=[]
    for ref in ['fixed','equal']:
        before=next(t for t in tables if (t.scenario.iloc[0],t.weight_reference.iloc[0])==('retained_V203',ref)).set_index('city').loc[cities]
        after=next(t for t in tables if (t.scenario.iloc[0],t.weight_reference.iloc[0])==('all_PM_points_withdrawn',ref)).set_index('city').loc[cities]
        assert (after.score_lower<=before.score_lower+1e-12).all() and (after.score_upper>=before.score_upper-1e-12).all() and (after.max_regret>=before.max_regret-1e-12).all()
        bc=next(x for x in cases if (x['scenario'],x['weight_reference'])==('retained_V203',ref));ac=next(x for x in cases if (x['scenario'],x['weight_reference'])==('all_PM_points_withdrawn',ref))
        contrasts.append(dict(weight_reference=ref,baseline_recommendations=bc['recommendations'],withdrawal_recommendations=ac['recommendations'],recommendation_changed=bc['recommendations']!=ac['recommendations'],decision_rank_changes=int((before.decision_rank!=after.decision_rank).sum()),mean_width_change=ac['mean_width']-bc['mean_width']))
    O.mkdir(exist_ok=True);pd.concat(tables,ignore_index=True).to_csv(O/'ranks.csv',index=False);pd.DataFrame(bounds).to_csv(O/'bounds.csv',index=False)
    summary=dict(primary_model='V203 unchanged',withdrawn_point_utilities=16,other144_ranges_exactly_preserved=True,weights_and_anchors_preserved=True,
        cases=cases,contrasts=contrasts,rank_rows=64,bound_rows=320,primary_admissions=0,actual_primary_width_reduction=0,
        scope='Criterion-block complete-information-withdrawal stress. Full [0,1] utility domain is not a pollutant concentration range, empirical error bound/distribution or probability. Product box permits independent cross-city extremes, with no common publisher/bias or physical joint plausibility assumed. Existing monotone TOPSIS/self-excluded maximum regret applies. No current OECD data, source correction, future trend or manuscript update.',
        source_sha256={str(p.relative_to(R)):sha(p) for p in [R/'data/task4_v117_team_intake/city_indicators.csv',Path(__file__)]},
        output_sha256={n:sha(O/n) for n in ['ranks.csv','bounds.csv']})
    (O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(contrasts))
if __name__=='__main__':main()
