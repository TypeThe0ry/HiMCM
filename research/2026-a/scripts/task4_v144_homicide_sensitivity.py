"""Targeted source-information withdrawals; the submitted homicide points stay fixed."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
from task4_user_v136_revision import revised_bounds
from task4_user_city_indicators import evaluate
from task4_v5_model import ROOT,weights,NAMES
OUT=ROOT/'results/task4_v144_homicide_sensitivity'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
    frozen={}
    for name,key in [('design/task4_user_v136_snapshot.json','source_sha256'),('results/task4_v137_revision/audit.json','result_sha256'),('results/task4_v138_priority/summary.json','source_sha256'),('results/task4_v143_vintage/verification.json','result_sha256')]:frozen.update(read(ROOT/name)[key]);frozen[name]=sha(ROOT/name)
    source=ROOT/'data/task4_v144_homicide';receipt=read(source/'verification.json');assert receipt['status']=='pass' and receipt['primary_admissions']==0
    for name,digest in receipt['source_sha256'].items():assert sha(source/name)==digest;frozen[str((source/name).relative_to(ROOT))]=digest
    assert sha(source/'extract.py')==receipt['source_extractor_sha256']
    for p in [source/'extract.py',source/'verification.json',Path(__file__),ROOT/'design/task4_user_current_model.json']:frozen[str(p.relative_to(ROOT))]=sha(p)
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    frame,lo,hi=revised_bounds();cities=frame.city.tolist();assert NAMES[0]=='homicide_rate'
    selections={'retained':[],'withdraw_Amsterdam_homicide':['Amsterdam'],'withdraw_Zurich_homicide':['Zurich'],'withdraw_both_homicides':['Amsterdam','Zurich']}
    frames=[];cases=[];changes=[]
    for scenario,selected in selections.items():
        lower=lo.copy();upper=hi.copy();mask=np.zeros((16,10),bool)
        for city in selected:
            i=cities.index(city);assert lo[i,0]==hi[i,0];mask[i,0]=True;lower[i,0]=0;upper[i,0]=1
            changes.append(dict(scenario=scenario,city=city,indicator='homicide_rate',old_lower=float(lo[i,0]),old_upper=float(hi[i,0]),new_lower=0,new_upper=1))
        np.testing.assert_array_equal(lower[~mask],lo[~mask]);np.testing.assert_array_equal(upper[~mask],hi[~mask])
        for reference,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
            table=evaluate(cities,lower,upper,w);frames.append(table.assign(scenario=scenario,weight_reference=reference))
            cases.append(dict(scenario=scenario,weight_reference=reference,withdrawn_point_cells=len(selected),minimax_choices=table.loc[table.decision_rank.eq(1),'city'].tolist(),possible_champions=int(table.possible_champion.sum()),necessary_champions=int(table.necessary_champion.sum()),mean_interval_width=float((table.score_upper-table.score_lower).mean())))
    OUT.mkdir(exist_ok=True);pd.concat(frames,ignore_index=True).to_csv(OUT/'ranks.csv',index=False);pd.DataFrame(changes).to_csv(OUT/'withdrawn_cells.csv',index=False)
    summary=dict(version='V144 source-specific information withdrawal on V136',cases=cases,changes_primary_data=False,changes_primary_model=False,primary_admissions=0,source_sha256=frozen,interpretation='Withdraw the unverified utility information of named submitted homicide points to [0,1]. Original values, all supplements and other utility bounds remain. Recovered CBS victim counts and PKS offence counts are not inserted as replacement rates; source definitions and denominators remain distinct.')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    print(json.dumps(cases,indent=2))
if __name__=='__main__':main()
