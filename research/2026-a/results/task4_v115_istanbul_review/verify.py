"""Verify that non-admitted source leads do not alter the selected evidence."""
from pathlib import Path
import hashlib
import json
import pandas as pd

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def run():
    for name in ['ranks.csv','utility_bounds.csv','travel_evidence.csv','recommendation_certificate.csv']:
        a=pd.read_csv(ROOT/'results/task4_current'/name)
        b=pd.read_csv(HERE/'reproduced'/name)
        pd.testing.assert_frame_equal(a,b,check_exact=True)
    audits={}
    for name in ['survey','age','reply']:
        path=ROOT/f'data/task4_v115_istanbul_{name}/audit.json'
        r=json.loads(path.read_text())
        audits[name]={'sha256':sha(path),'path':str(path.relative_to(ROOT))}
        assert not r.get('admitted',False)
    bounds=pd.read_csv(HERE/'reproduced/utility_bounds.csv')
    row=bounds[(bounds.city=='Istanbul')&(bounds.indicator=='travel')].iloc[0]
    assert row.lower==0 and row.upper==1
    ranks=pd.read_csv(HERE/'reproduced/ranks.csv')
    ist=ranks[ranks.city=='Istanbul'].iloc[0]
    for r in json.loads((ROOT/'data/task4_v115_istanbul_reply/retrieval.json').read_text()):
        assert r.get('error') and not (ROOT/'data/task4_v115_istanbul_reply'/r['file']).exists()
    summary=dict(review_round='V115',evidence_model='V114',baseline_commit='a0e4749',
        status='verified_no_new_admission',actual_changed_cells=0,actual_changed_ranks=0,
        verified_bound_cells=len(bounds),verified_city_ranks=len(ranks),
        possible_champions=int(ranks.possible_champion.sum()),
        istanbul_decision_rank=int(ist.decision_rank),istanbul_travel=[0,1],
        source_reviews=audits,
        reproduced_summary_sha256=sha(HERE/'reproduced/summary.json'),
        bounds_sha256=sha(HERE/'reproduced/utility_bounds.csv'),
        monte_carlo='Not repeated: evidence bounds and weights are unchanged; V114 results remain applicable.',
        unresolved='No verified Istanbul resident current-high-school one-way duration distribution; no observed district-by-age usable-access table.')
    (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':run()
