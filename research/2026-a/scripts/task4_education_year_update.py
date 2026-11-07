"""Same-scope Jakarta SMA year substitution; never intersect different years."""
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_roster_coverage_comparison import current_bounds
from task4_continuous_preferences import feasible_preferences

SOURCE=ROOT/'data/task4_v29_jakarta_education'


def updated_bounds(strict_source=False):
    manifest=json.loads((SOURCE/'manifest.json').read_text())
    for item in manifest['files']:
        assert hashlib.sha256((SOURCE/item['file']).read_bytes()).hexdigest()==item['sha256'],item['file']
    rows=pd.read_csv(SOURCE/'observations.csv')
    assert len(rows)==1
    r=rows.iloc[0]
    assert r.city=='Jakarta' and r.indicator=='upper_secondary_ptr'
    assert r.status=='observed_general_upper_secondary_indexed_source_scope_conditional'
    assert r.academic_year=='2025/2026' and r.unit=='students_per_headmaster_and_teacher_headcount'
    assert r.denominator>0 and r.numerator>=0
    np.testing.assert_allclose(r.value,r.numerator/r.denominator,rtol=0,atol=1e-12)
    lo,hi=current_bounds();i=CITIES.index('Jakarta');j=NAMES.index('upper_secondary_ptr')
    old=15/(15+190143/12114)
    np.testing.assert_allclose([lo[i,j],hi[i,j]],[old,old],rtol=0,atol=1e-12)
    lo[i,j],hi[i,j]=(0.,1.) if strict_source else (15/(15+r.value),)*2
    return lo,hi


def main():
    base_lo,base_hi=current_bounds();base,_=summarize(base_lo,base_hi,weights())
    i=CITIES.index('Jakarta');j=NAMES.index('upper_secondary_ptr')
    out=ROOT/'results/task4_v29_education_year';out.mkdir(parents=True,exist_ok=True)
    frames=[];bounds=[];summary=[]
    for label,(lo,hi) in [('baseline_2024_25',(base_lo,base_hi)),('updated_2025_26',updated_bounds()),('jakarta_indexed_source_withdrawn',updated_bounds(True))]:
        keep=np.ones(lo.shape,dtype=bool);keep[i,j]=False
        np.testing.assert_array_equal(lo[keep],base_lo[keep]);np.testing.assert_array_equal(hi[keep],base_hi[keep])
        assert np.all((0<=lo)&(lo<=hi)&(hi<=1))
        frame,d=summarize(lo,hi,weights());frame['scenario']=label;frames.append(frame)
        possible=[city for k,city in enumerate(CITIES) if feasible_preferences(hi[k],lo[np.arange(len(lo))!=k])['possible']]
        summary.append(dict(scenario=label,decision_choices=[CITIES[k] for k in d['minimax_choices']],
            possible_champions=int(frame.possible_champion.sum()),continuous_alpha_possible_champions=possible,
            changed_ranks_vs_baseline=int((frame.decision_rank!=base.decision_rank).sum()),
            kendall_tau_vs_baseline=float(kendalltau(frame.decision_rank,base.decision_rank).statistic),
            mean_score_width=float((frame.score_upper-frame.score_lower).mean()),
            jakarta={key:float(frame.iloc[i][key]) for key in ['score_lower','score_upper','max_regret','decision_rank']},
            jakarta_education_utility=[float(lo[i,j]),float(hi[i,j])],
            phoenix_rank=int(frame.iloc[CITIES.index('Phoenix')].decision_rank)))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=float(lo[k,m]),upper=float(hi[k,m])) for k,c in enumerate(CITIES) for m,n in enumerate(NAMES))
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    (out/'summary.json').write_text(json.dumps(dict(main_admitted=False,new_city_indicator_cells=0,updated_year_cells=1,
        alpha_fixed=.1,alpha_range=[.05,.2],method='Replace Jakarta SMA 2024/25 by 2025/26; identical score model and all other inputs. Indexed-source withdrawal changes only Jakarta PTR; it is not a global provenance-clean analysis.',
        input_manifest_sha256=hashlib.sha256((SOURCE/'manifest.json').read_bytes()).hexdigest(),scenarios=summary),indent=2)+'\n')
    print(json.dumps([{k:v for k,v in r.items() if k!='continuous_alpha_possible_champions'} for r in summary],indent=2))

if __name__=='__main__':main()
