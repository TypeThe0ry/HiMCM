"""Analyst-designed preference scenarios on unchanged V118 sixteen-city evidence."""
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT, NAMES, weights
from task4_user_city_indicators import SOURCE, evaluate
from task4_user_v118_revision import revised_bounds, MANIFEST
from task4_ahp_mc_baseline import ahp_weights, score_many, interval_metrics, rank_metrics

OUT = ROOT/'results/task4_v119_preferences'
MULTIPLIERS = {'baseline': {},
    'education_priority': {'upper_secondary_ptr': 2, 'research_he_density': 2},
    'independent_living_priority': {'travel': 2, 'public_transport_density': 2}}


def profile(name, base):
    multiplier = np.array([MULTIPLIERS[name].get(n,1) for n in NAMES],float)
    w = base*multiplier
    w /= w.sum()
    matrix = w[:,None]/w[None,:]
    document = dict(source='Analyst-designed scenario: multiply designated baseline weights by 2; not respondent or expert evidence',
        respondents='None; no survey conducted', elicitation_date='Not elicited',
        judgment_method='Construct exact ratios A_ij = w_i / w_j from declared analyst multipliers',
        indicators=NAMES, matrix=matrix.tolist())
    recovered, diagnostic = ahp_weights(document,NAMES)
    np.testing.assert_allclose(recovered,w,rtol=0,atol=1e-12)
    np.testing.assert_allclose(matrix*matrix.T,1,atol=1e-12)
    assert diagnostic['CR'] < 1e-10
    return w,multiplier,matrix,document,diagnostic


def main():
    before_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    manifest_hash = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
    source,lo,hi = revised_bounds()
    original_lo,original_hi = lo.copy(),hi.copy()
    cities = source.city.tolist()
    base = weights(.1)
    old = evaluate(cities,lo,hi,base)
    baseline_saved = pd.read_csv(ROOT/'results/task4_user_v118_revision/current_ranks.csv')
    pd.testing.assert_frame_equal(old,baseline_saved[old.columns],check_exact=False,rtol=1e-12,atol=1e-12)
    OUT.mkdir(parents=True,exist_ok=True)
    ranks,weight_rows,mc_rows,reports,documents = [],[],[],[],{}
    seed,draws,k = 20261108,10000,100
    for name in MULTIPLIERS:
        w,multiplier,matrix,doc,diagnostic = profile(name,base)
        documents[name] = dict(**doc,raw_multiplier=multiplier.tolist(),weights=w.tolist(),diagnostic=diagnostic)
        pd.DataFrame(matrix,index=NAMES,columns=NAMES).rename_axis('indicator').to_csv(OUT/f'{name}_matrix.csv')
        weight_rows.extend(dict(profile=name,indicator=n,baseline_weight=float(base[j]),raw_multiplier=float(multiplier[j]),weight=float(w[j]),multiplier_source='analyst-designed') for j,n in enumerate(NAMES))
        frame = evaluate(cities,lo,hi,w)
        frame['baseline_decision_rank'] = old.decision_rank
        frame['rank_change_positive_improves'] = old.decision_rank-frame.decision_rank
        ranks.append(frame.assign(profile=name))
        rng = np.random.default_rng(np.random.SeedSequence([seed,k]))
        sampled = rng.dirichlet(k*w,size=draws)
        lower,upper = score_many(lo,sampled),score_many(hi,sampled)
        regret,possible,necessary,_,_ = interval_metrics(lower,upper)
        mc_rank,recommendation,_ = rank_metrics(regret,descending=False)
        assert np.allclose(recommendation.sum(axis=1),1)
        for i,city in enumerate(cities):
            mc_rows.append(dict(profile=name,city=city,draws=draws,concentration=k,
                minimax_recommendation_frequency=float(recommendation[:,i].mean()),
                mean_decision_rank=float(mc_rank[:,i].mean()),
                possible_champion_frequency=float(possible[:,i].mean()),
                necessary_champion_frequency=float(necessary[:,i].mean())))
        reports.append(dict(profile=name,possible_champions=frame.loc[frame.possible_champion,'city'].tolist(),
            minimax_choices=frame.loc[frame.decision_rank==1,'city'].tolist(),
            kendall_tau_b_vs_baseline=float(kendalltau(old.decision_rank,frame.decision_rank).statistic),
            mean_score_interval_width=float((frame.score_upper-frame.score_lower).mean()),
            mc_most_recommended=cities[int(np.argmax(recommendation.mean(axis=0)))],
            mc_most_recommended_frequency=float(recommendation.mean(axis=0).max()),
            consistency_ratio=diagnostic['CR']))
    pd.concat(ranks,ignore_index=True).to_csv(OUT/'ranks.csv',index=False)
    pd.DataFrame(weight_rows).to_csv(OUT/'weights.csv',index=False)
    mc = pd.DataFrame(mc_rows)
    baseline_mc = mc[mc.profile=='baseline'].set_index('city')
    for col in ['minimax_recommendation_frequency','mean_decision_rank','possible_champion_frequency']:
        mc[col+'_change_vs_baseline'] = mc[col]-mc.city.map(baseline_mc[col])
    mc.to_csv(OUT/'mc_city_summary.csv',index=False)
    (OUT/'scenario_matrices.json').write_text(json.dumps(documents,indent=2)+'\n')
    summary = dict(input_sha256=before_hash,v118_admissions_sha256=manifest_hash,
        source='Unchanged sixteen-city V118 bounds',preference_evidence='Analyst-designed scenarios, no survey, no expert elicitation, no age-based weight claims',
        ahp_interpretation='Ratio reconstruction of declared weights; CR measures internal algebraic consistency only',
        seed=seed,concentration=k,draws_per_profile=draws,total_draws=draws*len(MULTIPLIERS),
        random_generator='numpy.default_rng(SeedSequence([20261108,100])) reset for each profile',
        mc_interpretation='Conditional scenario frequencies, not population preferences or real winning probabilities',
        profiles=reports)
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    np.testing.assert_array_equal(lo,original_lo);np.testing.assert_array_equal(hi,original_hi)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==before_hash
    assert hashlib.sha256(MANIFEST.read_bytes()).hexdigest()==manifest_hash
    previous_mc=pd.read_csv(ROOT/'results/task4_user_v118_revision/mc_city_summary.csv')
    previous_mc=previous_mc[(previous_mc.weight_reference=='fixed')&(previous_mc.concentration==100)].set_index('city').loc[cities]
    for col in ['minimax_recommendation_frequency','mean_decision_rank','possible_champion_frequency']:
        np.testing.assert_allclose(baseline_mc.loc[cities,col],previous_mc[col],atol=1e-12)
    print(json.dumps(summary,indent=2))


if __name__=='__main__': main()
