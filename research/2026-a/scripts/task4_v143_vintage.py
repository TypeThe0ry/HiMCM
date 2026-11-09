"""Controlled withdrawal of submitted point information; never edit observations."""
import hashlib,json
import numpy as np
import pandas as pd
from task4_user_city_indicators import SOURCE,FIELDS,evaluate
from task4_user_v136_revision import revised_bounds
from task4_v5_model import ROOT,NAMES,weights
OUT=ROOT/'results/task4_v143_vintage'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    frozen={}
    for file,key in [('design/task4_user_v136_snapshot.json','source_sha256'),('results/task4_v137_revision/audit.json','result_sha256'),('results/task4_v138_priority/summary.json','source_sha256')]:
        frozen.update(json.loads((ROOT/file).read_text())[key]);frozen[file]=sha(ROOT/file)
    for name in ['scripts/task4_v143_vintage.py','scripts/task4_user_city_indicators.py','scripts/task4_v5_model.py','scripts/task4_interval_decision.py','design/task4_user_current_model.json']:frozen[name]=sha(ROOT/name)
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    frame,lo,hi=revised_bounds();raw=pd.read_csv(SOURCE);assert frame.city.tolist()==raw.city.tolist()
    entries=[];pre=np.zeros((16,10),bool);later=pre.copy();flag=pre.copy()
    for i,row in raw.iterrows():
        for j,field in enumerate(FIELDS):
            if field and pd.notna(row[field]) and lo[i,j]==hi[i,j]:
                year=int(row[field+'_year']);label=str(row[field+'_flag'])
                pre[i,j]=year<2020;later[i,j]=year>2025;flag[i,j]=label!='ok'
                entries.append(dict(city=row.city,indicator=NAMES[j],input_field=field,submitted_value=float(row[field]),submitted_year=year,submitted_flag=label,utility=float(lo[i,j]),before_2020=bool(pre[i,j]),after_2025=bool(later[i,j]),non_ok=bool(flag[i,j])))
    assert len(entries)==112
    masks={'baseline':np.zeros((16,10),bool),'pre2020_points':pre,'after2025_points':later,'non_ok_points':flag,'union_points':pre|later|flag}
    ranks=[];summaries=[];changes=[]
    for case,mask in masks.items():
        lower=lo.copy();upper=hi.copy();lower[mask]=0;upper[mask]=1
        assert not np.any(mask & (lo!=hi))
        np.testing.assert_array_equal(lower[~mask],lo[~mask]);np.testing.assert_array_equal(upper[~mask],hi[~mask])
        for i,j in np.argwhere(mask):changes.append(dict(scenario=case,city=raw.iloc[i].city,indicator=NAMES[j],old_lower=float(lo[i,j]),old_upper=float(hi[i,j]),new_lower=0,new_upper=1))
        for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
            table=evaluate(raw.city.tolist(),lower,upper,w);table['scenario']=case;table['weight_reference']=ref;ranks.append(table)
            summaries.append(dict(scenario=case,weight_reference=ref,withdrawn_point_cells=int(mask.sum()),points_remaining=int((lower==upper).sum()),partial_cells=int(((lower<upper)&((upper-lower)<1)).sum()),fully_unknown_cells=int(((upper-lower)==1).sum()),minimax_choices=table.loc[table.decision_rank.eq(1),'city'].tolist(),possible_champions=int(table.possible_champion.sum()),necessary_champions=int(table.necessary_champion.sum()),mean_interval_width=float((table.score_upper-table.score_lower).mean())))
    OUT.mkdir(exist_ok=True)
    pd.DataFrame(entries).to_csv(OUT/'submitted_points.csv',index=False);pd.DataFrame(changes).to_csv(OUT/'withdrawn_cells.csv',index=False);pd.concat(ranks,ignore_index=True).to_csv(OUT/'ranks.csv',index=False)
    counts=pd.DataFrame(entries);summary=dict(version='V143 controlled submitted-point withdrawal on V136',nominal_reference_year=2025,point_year_counts={str(int(k)):int(v) for k,v in counts.submitted_year.value_counts().sort_index().items()},point_flag_counts={str(k):int(v) for k,v in counts.submitted_flag.value_counts().sort_index().items()},cases=summaries,changes_primary_data=False,changes_primary_model=False,source_sha256=frozen,interpretation='One-at-a-time and union withdrawals of selected submitted POINT utility information to [0,1]; supplements and all original partial bounds remain. Categories are audit labels, not calibrated errors or probabilities. This is not a same-year-only reconstruction or empirical trend.')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    print(json.dumps(summaries,indent=2))
if __name__=='__main__':main()
