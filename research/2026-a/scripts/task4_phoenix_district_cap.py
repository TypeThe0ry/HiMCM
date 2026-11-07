"""Compare the documented district cap with unknown and chart-date assumptions.

This is a separate public-school/FTE target, not a replacement for the current
all-school/headcount criterion. The district-to-school coverage remains explicit.
"""
import hashlib
import json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_saopaulo_age_revision import saopaulo_age_bounds
from task4_phoenix_public_bounds import utility_lower
from task4_continuous_preferences import feasible_preferences


def main():
    source=ROOT/'data/task4_v50_phoenix'
    for name in ['task4_v50_phoenix','task4_v50_student_travel']:
        folder=ROOT/'data'/name
        for item in json.loads((folder/'manifest.json').read_text()):
            base=folder.parent if item.get('base')=='parent_data_directory' else folder
            raw=(base/item['file']).read_bytes()
            assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
    definition=json.loads((source/'safr_definition_web_result.json').read_text())['result']
    district=json.loads((source/'safr_district_web_result.json').read_text())['result']
    assert 'October 1, 2024' in definition and 'unduplicated' in definition
    assert 'Fall 2024 Enrollment</td><td>1,180' in district
    assert 'Maricopa County Regional School District' in district
    roster=pd.read_csv(ROOT/'data/task4_v42_phoenix_coverage/phoenix_secondary_roster.csv',dtype={'NCESSCH':str,'LEAID':str})
    unknown=roster[roster.target_enrollment_upper.isna()]
    assert unknown.NCESSCH.tolist()==['040386003535']
    assert unknown.LEAID.iloc[0]=='0403860'
    non_target=['PK','KG']+[f'G{x:02d}' for x in range(1,9)]+['G13','UG','AE']
    eligible=roster.within_9_12_only & roster[non_target].isin([0,-2]).all(axis=1) & roster.FTE.ge(0)
    staff=float(roster.loc[eligible,'FTE'].sum())
    known=float(roster.target_enrollment_upper.dropna().sum())
    assert known==70678 and abs(staff-2512.97)<1e-8
    district_cap=1180
    cap=known+district_cap
    value=utility_lower(cap,staff)
    oldlo,oldhi=saopaulo_age_bounds()
    lo,hi=oldlo.copy(),oldhi.copy(); j=NAMES.index('upper_secondary_ptr'); i=CITIES.index('Phoenix')
    lo[:,j]=0;hi[:,j]=1
    baseline,_=summarize(lo,hi,weights())
    frames=[];stats=[]
    scenarios=[('same_public_target_unknown',0.),
               ('chart_1178_snapshot_assumed',utility_lower(known+1178,staff)),
               ('documented_district_1180_coverage_conditional',value)]
    for label,u in scenarios:
        l=lo.copy();l[i,j]=u
        keep=np.ones_like(lo,bool);keep[i,j]=False
        np.testing.assert_array_equal(l[keep],lo[keep])
        f,d=summarize(l,hi,weights());f['scenario']=label;frames.append(f)
        stats.append(dict(scenario=label,phoenix_education_lower=u,
            phoenix=f.iloc[i][['score_lower','score_upper','max_regret','decision_rank']].to_dict(),
            changed_ranks_vs_same_target=int((f.decision_rank!=baseline.decision_rank).sum()),
            possible_champions=int(f.possible_champion.sum()),
            continuous_possible=sum(feasible_preferences(hi[k],l[np.arange(len(l))!=k])['possible'] for k in range(len(l))),
            choice=[CITIES[k] for k in d['minimax_choices']]))
    reference,_=summarize(oldlo,oldhi,weights());reference['scenario']='current_v48_reference'
    frames.insert(0,reference)
    out=ROOT/'results/task4_v50_phoenix_cap';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    result=dict(main_model_changed=False,district_cap=district_cap,student_upper=cap,
                teacher_lower=staff,source_representation='Search extraction of official PDF; original PDF bytes unavailable',
                condition='Hope target pupils are included in the district unduplicated October 1 count; CCD school universe and snapshot are compatible',
                target='Phoenix school-location operational nonvirtual public grades9-12 with attributed teacher FTE',scenarios=stats)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
