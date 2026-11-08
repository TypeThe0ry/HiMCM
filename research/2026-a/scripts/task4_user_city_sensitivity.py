"""Conditional weight sensitivity for the user's 16-city interval scenario."""
import hashlib
import json
import numpy as np
import pandas as pd
from task4_user_city_indicators import SOURCE, OUT, build
from task4_v5_model import weights
from task4_ahp_mc_baseline import score_many, interval_metrics, rank_metrics


def main():
    seed, draws = 20261108, 10000
    original = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    source = pd.read_csv(SOURCE)
    lo,hi,_ = build(source)
    old_lo,old_hi = lo.copy(),hi.copy()
    rows, scenarios = [], []
    for label,center in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
        for k in (20,100,500):
            rng = np.random.default_rng(np.random.SeedSequence([seed,k]))
            sampled = rng.dirichlet(k*center,size=draws)
            assert np.allclose(sampled.sum(axis=1),1)
            lower,upper = score_many(lo,sampled),score_many(hi,sampled)
            regret,possible,necessary,_,_ = interval_metrics(lower,upper)
            ranks,recommended,_ = rank_metrics(regret,descending=False)
            assert np.allclose(recommended.sum(axis=1),1)
            assert np.all(lower<=upper+1e-10)
            for i,city in enumerate(source.city):
                rows.append(dict(city=city,weight_reference=label,concentration=k,draws=draws,
                    minimax_recommendation_frequency=float(recommended[:,i].mean()),
                    mean_decision_rank=float(ranks[:,i].mean()),
                    possible_champion_frequency=float(possible[:,i].mean()),
                    necessary_champion_frequency=float(necessary[:,i].mean())))
            scenarios.append(dict(weight_reference=label,concentration=k,
                top_minimax_recommendation=source.city.iloc[int(np.argmax(recommended.mean(axis=0)))],
                top_minimax_recommendation_frequency=float(recommended.mean(axis=0).max()),
                possible_champion_count_min=int(possible.sum(axis=1).min()),
                possible_champion_count_mean=float(possible.sum(axis=1).mean()),
                possible_champion_count_max=int(possible.sum(axis=1).max())))
    assert np.array_equal(lo,old_lo) and np.array_equal(hi,old_hi)
    assert original == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    OUT.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT/'mc_city_summary.csv',index=False)
    summary = dict(seed=seed,draws_per_scenario=draws,total_draws=draws*6,
        input_sha256=original,distribution='Dirichlet(concentration * center)',
        random_generator='numpy.default_rng(SeedSequence([20261108, concentration]))',
        interpretation='Conditional weight-scenario frequencies, not probabilities of actual city quality; missing intervals unchanged.',
        decision_rank_ties='average ranks; recommendation ties split fractionally',
        scenarios=scenarios)
    (OUT/'mc_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
