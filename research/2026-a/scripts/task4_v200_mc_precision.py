"""Bound numerical Monte Carlo mean errors; read frozen V200 exports only."""
from pathlib import Path
import csv, hashlib, json, math
R = Path(__file__).resolve().parents[1]
O = R / 'results/task4_v200_mc_precision'
PREF = ['minimax_recommendation_frequency', 'mean_decision_rank',
        'top3_decision_frequency', 'possible_champion_frequency', 'necessary_champion_frequency']
FUTURE = ['recommendation_frequency', 'possible_champion_frequency', 'mean_decision_rank']
TABLES = [
    ('preferences', 'task4_v200_preferences/mc_city_summary.csv', PREF, ['profile', 'concentration']),
    ('future_shocks', 'task4_v200_future/future_mc_city_summary.csv', FUTURE,
     ['scenario', 'weight_reference', 'evidence_arm']),
    ('weights_only', 'task4_v200_future/weight_mc_city_summary.csv', FUTURE,
     ['scenario', 'weight_reference', 'evidence_arm', 'concentration']),
]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with p.open() as f: return list(csv.DictReader(f))
def write_csv(path, records):
    with path.open('w') as f:
        w = csv.DictWriter(f, fieldnames=list(records[0]), lineterminator='\n')
        w.writeheader(); w.writerows(records)
def main():
    n, alpha = 10000, .05
    inputs, counts, records = {}, [], []
    for family, name, metrics, setting_keys in TABLES:
        source = R / 'results' / name
        inputs[str(source.relative_to(R))] = sha(source)
        data = rows(source)
        settings = {tuple(x[k] for k in setting_keys) for x in data}
        for setting in settings:
            group = [x for x in data if tuple(x[k] for k in setting_keys) == setting]
            assert len(group) == len({x['city'] for x in group}) == 16
        counts.append(dict(family=family, rows=len(data), settings=len(settings), means=len(data)*len(metrics)))
        for row in data:
            if family == 'preferences': assert int(row['draws']) == n
            for metric in metrics:
                a, b = (1, 16) if metric == 'mean_decision_rank' else (0, 1)
                estimate = float(row[metric]); assert a <= estimate <= b
                records.append(dict(family=family, setting=json.dumps({k:row[k] for k in setting_keys},sort_keys=True),
                    city=row['city'], metric=metric, draws=n, estimate=estimate, support_lower=a, support_upper=b))
    m = len(records)
    setting_count = sum(x['settings'] for x in counts)
    assert m > 0 and setting_count > 0
    epsilon = math.sqrt(math.log(2*m/alpha)/(2*n))
    for row in records:
        width = (row['support_upper']-row['support_lower'])*epsilon
        row.update(half_width=width, lower=max(row['support_lower'],row['estimate']-width),
                   upper=min(row['support_upper'],row['estimate']+width))
    # Record both current numerical exports and the actual inherited sampling chain.
    for name in ['task4_v200_extensions.py','task4_v125_preferences.py','task4_v122_preferences.py',
                 'task4_v125_future.py','task4_v122_future.py','task4_ahp_mc_baseline.py']:
        path = R/'scripts'/name; inputs[str(path.relative_to(R))] = sha(path)
    for name in ['scripts/task4_user_v200_revision.py', 'design/task4_user_v200_admissions.json']:
        path = R/name; inputs[name] = sha(path)
    O.mkdir(exist_ok=True)
    write_csv(O/'mean_bounds.csv',records)
    examples = []
    for row in records:
        s = json.loads(row['setting'])
        if (row['family']=='future_shocks' and row['city']=='Zurich'
            and s['weight_reference']=='fixed' and s['evidence_arm']=='conditional'
            and row['metric']=='recommendation_frequency') or (
            row['family']=='preferences' and row['city'] in ['Oslo','Zurich']
            and s['profile']=='baseline' and s['concentration']=='100'
            and row['metric']=='mean_decision_rank'):
            examples.append(row)
    assert len(examples) == 5
    write_csv(O/'published_examples.csv', examples)
    summary = dict(version='V200', primary_science='V200', current_paper='V198 unchanged; V200 science staged, not activated',
        familywise_alpha=alpha, draws_per_setting=n, settings=setting_count, base_means=m,
        frequency_means=sum(x['metric']!='mean_decision_rank' for x in records),
        mean_rank_means=sum(x['metric']=='mean_decision_rank' for x in records),
        normalized_half_width=epsilon, frequency_half_width_percentage_points=100*epsilon,
        mean_rank_half_width=15*epsilon, tables=counts, input_sha256=inputs,
        assumption='Independent identically distributed replications within each declared simulation setting; intended RNG design, not an empirical independence certificate for a fixed PRNG sequence.',
        dependence='Shared draws across cities and settings are permitted. The union bound does not require independence across estimated means.',
        scope='Finite-sample MC integration error around expectations under the declared simulation laws and retained evidence/model; no real-world city win probabilities, forecast calibration, source error or interval coverage.',
        excluded=['change_vs_baseline columns (derived, not counted as base means)',
                  'score-change quantiles (not sample means)', 'primary V200 10 cases and 60 MC settings (separate family)'],
        reran_monte_carlo=False, changed_scientific_inputs=False,
        changed_manuscript=False, submission_ready=False)
    (O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ['base_means','frequency_half_width_percentage_points','mean_rank_half_width']}))
if __name__=='__main__': main()
