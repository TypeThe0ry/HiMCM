"""Admit verified Copenhagen institution-presence lower bound; keep upper unknown."""
import hashlib,importlib.util,json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_warsaw_resource_revision import warsaw_bounds
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify

SOURCE=ROOT/'data/task4_v102_copenhagen'

def source():
    spec=importlib.util.spec_from_file_location('copenhagen102_extract',SOURCE/'extract.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    data=module.extract()
    assert data==json.loads((SOURCE/'summary.json').read_text())
    assert data['verified_count']==len(set(data['institutions']))==4
    assert data['population']>0 and data['complete_city_inventory'] is False
    density=data['verified_count']*100000/data['population']
    np.testing.assert_allclose(data['density_lower_per_100000'],density,rtol=0,atol=1e-15)
    np.testing.assert_allclose(data['utility_lower'],density/(1+density),rtol=0,atol=1e-15)
    assert data['finite_count_upper'] is None and data['utility_upper']==1
    return data

def copenhagen_bounds(withdraw=False):
    lo,hi=warsaw_bounds();i,j=CITIES.index('Copenhagen'),NAMES.index('research_he_density')
    assert (lo[i,j],hi[i,j])==(0,1)
    if not withdraw:lo[i,j],hi[i,j]=source()['utility_lower'],1.
    return lo,hi

def main():
    before=warsaw_bounds();new=copenhagen_bounds();withdrawn=copenhagen_bounds(True)
    i,j=CITIES.index('Copenhagen'),NAMES.index('research_he_density');mask=np.ones(before[0].shape,bool);mask[i,j]=False
    for old,after,back in zip(before,new,withdrawn):
        np.testing.assert_array_equal(old[mask],after[mask]);np.testing.assert_array_equal(old,back)
    baseline,_=summarize(*before,weights());frames=[];bounds=[];certs=[];reports=[]
    for label,(lo,hi) in [('v96_before',before),('v102_copenhagen_resources',new),('copenhagen_resources_withdrawn',withdrawn)]:
        frame,decision=summarize(lo,hi,weights());frames.append(frame.assign(scenario=label))
        cert=certify(lo,hi);certs.extend(dict(**r,scenario=label) for r in cert)
        reports.append(dict(scenario=label,copenhagen_resource_utility=[lo[i,j],hi[i,j]],
            copenhagen=frame.iloc[i][['decision_rank','score_lower','score_upper','max_regret']].to_dict(),
            choice=[CITIES[k] for k in decision['minimax_choices']],
            changed_ranks=int((frame.decision_rank!=baseline.decision_rank).sum()),
            kendall_tau_vs_v96=float(kendalltau(frame.decision_rank,baseline.decision_rank).statistic),
            possible_champions=frame.loc[frame.possible_champion,'city'].tolist(),
            continuous_possible_champions=[c for k,c in enumerate(CITIES) if feasible_preferences(hi[k],lo[np.arange(len(CITIES))!=k],.05,.2)['possible']],
            continuous_recommendation=dict(unresolved=sum(not r['certified'] for r in cert),winners=sorted({CITIES[r['winner']] for r in cert if r['certified']}))))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=lo[k,m],upper=hi[k,m]) for k,c in enumerate(CITIES) for m,n in enumerate(NAMES))
    out=ROOT/'results/task4_v102_copenhagen_revision';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    pd.DataFrame(certs).to_csv(out/'recommendation_certificate.csv',index=False)
    a,b=reports[0]['copenhagen'],reports[1]['copenhagen']
    result=dict(model_version='V102',baseline_model='V96',main_admitted=True,
        primary_scenario='v102_copenhagen_resources',changed_cells=1,unchanged_other_cells=249,withdrawal_restores_v96=True,
        input_bounds_sha256=hashlib.sha256(np.stack(new).astype('<f8').tobytes()).hexdigest(),
        source_summary_sha256=hashlib.sha256((SOURCE/'summary.json').read_bytes()).hexdigest(),
        score_lower_gain=b['score_lower']-a['score_lower'],score_upper_change=b['score_upper']-a['score_upper'],
        score_width_reduction_percent=100*((a['score_upper']-a['score_lower'])-(b['score_upper']-b['score_lower']))/(a['score_upper']-a['score_lower']),
        scenarios=reports,scope='Conditional same-calendar-year recognized HE institution presence: four verified distinct legal seats/central addresses in Copenhagen municipality, November2026 source snapshot and July1 population. Not student access or learning quality; incomplete inventory leaves upper unknown.',
        fixed_alpha=.1,alpha_range=[.05,.2],numerical_certificates_not_formal_interval_arithmetic=True)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['changed_cells','score_lower_gain','score_upper_change','score_width_reduction_percent','scenarios']},indent=2))

if __name__=='__main__':main()
