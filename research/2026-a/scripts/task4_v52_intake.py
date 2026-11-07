"""Verify new actual school evidence without substituting incompatible populations."""
import hashlib,json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,weights,summarize,CITIES
from task4_saopaulo_age_revision import saopaulo_age_bounds


def verify_manifest(folder):
    for item in json.loads((folder/'manifest.json').read_text()):
        base=folder.parent if item.get('base')=='parent_data_directory' else folder
        raw=(base/item['file']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==item['sha256']
        if 'bytes' in item:assert len(raw)==item['bytes']


def main():
    folder=ROOT/'data/task4_v52_phoenix_outcomes';verify_manifest(folder)
    table=pd.read_csv(folder/'grade11_observations.csv')
    assert len(table)==9 and not table.duplicated(['educationOrganizationId','subject']).any()
    checks=[]
    for eid in [5439,5437,969999]:
        raw=json.loads((folder/f'{eid}_assessment.json').read_text())
        selected=[r for r in raw if r['subgroups']=='All' and str(r['grade'])=='11' and r['type']==1]
        assert len(selected)==3 and {r['subject'] for r in selected}=={'ELA','MATH','Science'}
        for row in selected:
            assert row['educationOrganizationId']==eid and row['fiscalYear']==2025
            assert row['fayType']=='ALL ENROLLED' and row['numberTested']>0
            recorded=table[(table.educationOrganizationId==eid)&(table.subject==row['subject'])].iloc[0]
            for key in ['numberTested','percentagePassed','assessmentType','fayType','fiscalYear','type','subgroups']:
                assert recorded[key]==row[key]
            assert int(recorded['grade'])==int(row['grade'])
        checks.append(dict(entity=eid,grade=11,subjects=3))
    london=ROOT/'data/task4_v52_london_travel';verify_manifest(london)
    national=json.loads((london/'audit.json').read_text())
    assert national['geography']=='England' and national['new_london_admitted_observations']==0
    lo,hi=saopaulo_age_bounds();rank,decision=summarize(lo,hi,weights())
    prior=pd.read_csv(ROOT/'results/task4_v51_evidence_withdrawal/ranks.csv')
    prior=prior[prior.scenario=='baseline'].reset_index(drop=True)
    for col in ['score_lower','score_upper','max_regret','decision_rank']:
        np.testing.assert_allclose(rank[col],prior[col],rtol=0,atol=1e-12)
    out=ROOT/'results/task4_v52_intake';out.mkdir(parents=True,exist_ok=True)
    rank.to_csv(out/'ranks.csv',index=False)
    report=dict(new_phoenix_school_subject_records=9,nonnegative_percentage_records=int(table.percentagePassed.ge(0).sum()),
                special_code_percentage_records=int(table.percentagePassed.lt(0).sum()),
                phoenix_school_checks=checks,london_city_admitted_observations=0,
                main_admitted_cells_changed=0,rank_changes=0,possible_champions=int(rank.possible_champion.sum()),
                choice=[CITIES[i] for i in decision['minimax_choices']],main_admitted=False)
    (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
