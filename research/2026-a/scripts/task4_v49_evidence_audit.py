"""Recompute unchanged V48 decisions after year and journey-purpose admission checks."""
import hashlib
import json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT, CITIES, weights, summarize
from task4_saopaulo_age_revision import saopaulo_age_bounds
from task4_continuous_preferences import feasible_preferences


def main():
    source = ROOT / 'data/task4_v49_phoenix'
    for item in json.loads((source / 'manifest.json').read_text()):
        assert hashlib.sha256((source / item['file']).read_bytes()).hexdigest() == item['sha256']
    a = json.loads((source / 'hope_2023_24.json').read_text())['features'][0]['attributes']
    assert str(a['NCESSCH']) == '040386003535'
    assert sum(a[k] for k in ['G09', 'G10', 'G11', 'G12']) == a['MEMBER'] == 83
    assert a['FTE'] == 4 and a['MEMBER'] / a['FTE'] == 20.75
    chain = json.loads((ROOT / 'data/task4_v49_saopaulo_chains/summary.json').read_text())
    assert chain['examined'] == 15 and chain['recovered'] == 0
    assert chain['model_inputs_changed'] is False
    lo, hi = saopaulo_age_bounds()
    rank, decision = summarize(lo, hi, weights())
    old = pd.read_csv(ROOT / 'results/task4_v48_saopaulo_age/ranks.csv')
    old = old[old.scenario == 'v48_age14_18_sampling'].set_index('city').loc[rank.city]
    for col in ['score_lower', 'score_upper', 'max_regret', 'decision_rank']:
        np.testing.assert_allclose(rank[col], old[col], rtol=0, atol=1e-12)
    continuous = [c for i, c in enumerate(CITIES)
                  if feasible_preferences(hi[i], lo[np.arange(len(lo)) != i])['possible']]
    result = dict(baseline='V48', model_inputs_changed=0, changed_ranks=0,
                  choice=[CITIES[k] for k in decision['minimax_choices']],
                  possible_champions=int(rank.possible_champion.sum()),
                  continuous_alpha_possible=continuous, main_admitted=False,
                  historical_hope_membership=83, recovered_saopaulo_journeys=0)
    out = ROOT / 'results/task4_v49_evidence_audit'
    out.mkdir(parents=True, exist_ok=True)
    rank.to_csv(out / 'ranks.csv', index=False)
    (out / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
