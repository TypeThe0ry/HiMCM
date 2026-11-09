"""Hold supplied values fixed; test dependence on two work-commute proxies."""
import hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd
from task4_user_v181_revision import revised_bounds
from task4_user_city_indicators import evaluate,SOURCE
from task4_v5_model import ROOT,NAMES,weights
O=ROOT/'results/task4_v184_source_review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    O.mkdir(exist_ok=True);f,lo,hi=revised_bounds();cities=f.city.tolist();original=np.stack([lo,hi]).copy();j=NAMES.index('travel')
    rows=[];bounds=[];reports=[]
    cases={'retained_input':[],'withdraw_Zurich_work_commute':['Zurich'],'withdraw_Dublin_work_commute':['Dublin'],'withdraw_both_work_commute':['Zurich','Dublin'],'withdraw_all_submitted_commute_means':f.loc[f.commute_min.notna(),'city'].tolist()}
    for case,withdraw in cases.items():
        l,h=lo.copy(),hi.copy()
        for c in withdraw:
            i=cities.index(c);assert hi[i,j]==1 and lo[i,j]>0;l[i,j],h[i,j]=0,1
        np.testing.assert_array_equal(h,hi)
        mask=np.ones((16,10),bool)
        for c in withdraw:mask[cities.index(c),j]=False
        np.testing.assert_array_equal(l[mask],lo[mask])
        bounds.extend(dict(scenario=case,city=c,indicator=n,lower=l[i,k],upper=h[i,k]) for i,c in enumerate(cities) for k,n in enumerate(NAMES))
        for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
            table=evaluate(cities,l,h,w);rows.append(table.assign(scenario=case,weight_reference=ref))
            reports.append(dict(scenario=case,withdrawn_commute_proxies=withdraw,weight_reference=ref,conservative_recommendation=table.loc[table.decision_rank.eq(1),'city'].tolist(),possible_champions=int(table.possible_champion.sum()),necessary_champions=int(table.necessary_champion.sum()),mean_score_interval_width=float((table.score_upper-table.score_lower).mean()),minimax_regret=float(table.max_regret.min())))
    pd.concat(rows,ignore_index=True).to_csv(O/'commute_withdrawal_ranks.csv',index=False);pd.DataFrame(bounds).to_csv(O/'commute_withdrawal_bounds.csv',index=False)
    _,a,b=revised_bounds();np.testing.assert_array_equal(np.stack([a,b]),original)
    paths=[Path(__file__),SOURCE,ROOT/'design/task4_user_current_model.json',ROOT/'design/task4_user_current_extensions.json']
    for name in ['dublin_commute','zurich_commute','helsinki_teacher']:
        paths.extend(p for p in (ROOT/('data/task4_v184_'+name)).iterdir() if p.is_file())
    summary=dict(version='V184 controlled commute-proxy withdrawal',primary='V181 unchanged',paper_at_calculation='V182',primary_admissions=0,actual_baseline_width_change=0,retained_input_counts=[112,35,13],rows=160,source_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(paths))},cases=reports,scope='Diagnostic evidence-policy withdrawals only; original CSV, years, flags, all active160bounds, weights, anchors and interval rules remain fixed. Matching official records do not prove the original user source chain or historical boundary. No duration-distribution tightening.',MC_rerun=False)
    (O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(reports,indent=2))
if __name__=='__main__':main()
