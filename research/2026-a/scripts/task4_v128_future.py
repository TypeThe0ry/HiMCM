"""Migrate fixed V125 future stresses to the frozen sixteen-city V127 inputs.

V121 reproduces V122; V124 reproduces V125; only input evidence changes for V128.
The legacy runner is a pure factory consumer and never writes older results.
"""
import hashlib
import json
from io import StringIO

import numpy as np
import pandas as pd

from task4_user_v124_revision import revised_bounds as v124_bounds
from task4_user_v127_revision import MANIFEST, revised_bounds, without_historical_proxy
from task4_v125_future import (DRAWS, FROZEN, NAMES, REFERENCES, ROOT, SCENARIOS,
                               SEED, WEIGHT_SEED, compare_control, run, v121_bounds)

OUT = ROOT/'results/task4_v128_future'
V125 = ROOT/'results/task4_v125_future'
SNAPSHOT = ROOT/'design/task4_user_v127_snapshot.json'
KEYS = {
    'ranks':['evidence_arm','scenario','weight_reference','city'],
    'utility_bounds':['evidence_arm','scenario','city','indicator'],
    'thresholds':['weight_reference','city'],
    'threshold_scan':['weight_reference','city','raw_multiplier'],
    'future_mc_city_summary':['random_source','evidence_arm','scenario','weight_reference','city'],
    'weight_mc_city_summary':['random_source','evidence_arm','scenario','weight_reference','concentration','city'],
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def serialized(frame):
    """Normalize list/object fields exactly as the frozen CSV serialization."""
    return pd.read_csv(StringIO(frame.to_csv(index=False)),float_precision='round_trip')


def v125_control(tables, summary):
    checks = {}
    for name,table in tables.items():
        frozen = pd.read_csv(V125/(name+'.csv'),float_precision='round_trip')
        pd.testing.assert_frame_equal(serialized(table),frozen,check_exact=True)
        checks[name] = dict(rows=len(frozen),all_columns_exact=True)
    old = json.loads((V125/'summary.json').read_text())
    assert summary['scenarios'] == old['scenarios']
    assert summary['thresholds'] == old['thresholds']
    return dict(factory='V124',frozen_version='V125',tables=checks,
                summary_scenarios_exact=True,summary_thresholds_exact=True)


def baseline_mc_check(table,cities):
    old = pd.read_csv(ROOT/'results/task4_user_v127_revision/mc_city_summary.csv',
                      float_precision='round_trip')
    comparisons = []
    for ref,_ in REFERENCES:
        for arm,scenario in [('conditional','after_conditional'),
                             ('withdraw_historical_stage_proxy','withdraw_historical_stage_proxy')]:
            previous = old[(old.scenario==scenario)&(old.weight_reference==ref)
                           &(old.concentration==100)].set_index('city').loc[cities]
            current = table[(table.scenario=='baseline')&(table.weight_reference==ref)
                            &(table.evidence_arm==arm)].set_index('city').loc[cities]
            for now,before in [('recommendation_frequency','minimax_recommendation_frequency'),
                               ('mean_decision_rank','mean_decision_rank'),
                               ('possible_champion_frequency','possible_champion_frequency')]:
                np.testing.assert_array_equal(current[now],previous[before])
            comparisons.append(dict(evidence_arm=arm,weight_reference=ref,
                                    cities=len(cities),three_metrics_exact=True))
    return comparisons


def matched_comparison(current,old,keys,old_suffix):
    current,old = serialized(current),serialized(old)
    assert not current.duplicated(keys).any() and not old.duplicated(keys).any()
    joined = current.merge(old,on=keys,how='outer',suffixes=('_v127',old_suffix),
                           validate='one_to_one',indicator=True)
    assert len(joined)==len(current)==len(old) and (joined['_merge']=='both').all()
    return joined.drop(columns='_merge')


def changes_between(frame,old_lo,old_hi,lo,hi):
    np.testing.assert_array_equal(hi,old_hi)
    assert np.all(lo>=old_lo)
    return [dict(city=frame.city.iloc[i],indicator=NAMES[j],
                 previous_lower=float(old_lo[i,j]),current_lower=float(lo[i,j]),
                 previous_upper=float(old_hi[i,j]),current_upper=float(hi[i,j]))
            for i,j in zip(*np.where((lo!=old_lo)|(hi!=old_hi)))]


def main():
    assert DRAWS==10000 and SEED==20261108122 and WEIGHT_SEED==[20261108,100]
    assert SCENARIOS=={
        'baseline':{},
        'resource_expansion':{'research_he_density':.1,'public_transport_density':.1,'public_pool_density':.1},
        'living_pressure':{'cost_living_index':.1,'price_income_ratio':.1,'travel':.1},
        'balanced_improvement':{'upper_secondary_ptr':-.1,'pm25':-.1,'travel':-.1}}
    snapshot_bytes = SNAPSHOT.read_bytes()
    snapshot = json.loads(snapshot_bytes)
    assert snapshot['version']=='V127'
    for path,digest in snapshot['source_sha256'].items():
        assert sha(ROOT/path)==digest,path
    old_summary = json.loads((FROZEN/'summary.json').read_text())
    previous_summary = json.loads((V125/'summary.json').read_text())
    source_paths = set(old_summary['source_sha256'])|set(previous_summary['source_sha256'])
    source_paths.update(snapshot['source_sha256'])
    source_paths.update(['scripts/task4_v128_future.py','scripts/task4_v125_future.py',
                         'scripts/task4_user_v127_revision.py',str(MANIFEST.relative_to(ROOT)),
                         str(SNAPSHOT.relative_to(ROOT))])
    source_paths.update(json.loads(MANIFEST.read_text())['source_hashes'])
    for folder in [FROZEN,V125]:
        source_paths.update(str(p.relative_to(ROOT)) for p in folder.iterdir() if p.is_file())
    protected = {p:sha(ROOT/p) for p in sorted(source_paths)}
    # Historical controls are rebuilt in memory; no legacy output is overwritten.
    control_tables,control_summary = run(v121_bounds)
    old_control = compare_control(control_tables,control_summary)
    previous_tables,previous_run = run(v124_bounds,paired_mc=True)
    previous_control = v125_control(previous_tables,previous_run)
    tables,summary = run(revised_bounds,paired_mc=True)
    frame,lo,hi = revised_bounds()
    cities = frame.city.tolist()
    assert lo.shape==hi.shape==(16,10)
    # The legacy runner's withdrawal helper and the V127 helper must be identical.
    j = NAMES.index('travel');i = cities.index('Singapore')
    expected_lo,expected_hi=lo.copy(),hi.copy();expected_lo[i,j]=0;expected_hi[i,j]=1
    l,h=without_historical_proxy(frame,lo,hi)
    np.testing.assert_array_equal(l,expected_lo);np.testing.assert_array_equal(h,expected_hi)
    baseline_checks=baseline_mc_check(tables['weight_mc_city_summary'],cities)
    _,old_lo,old_hi=v121_bounds()
    _,previous_lo,previous_hi=v124_bounds()
    changes=changes_between(frame,old_lo,old_hi,lo,hi)
    current_changes=changes_between(frame,previous_lo,previous_hi,lo,hi)
    assert len(changes)==4 and len(current_changes)==2
    assert {(r['city'],r['indicator']) for r in current_changes}=={
        ('Vienna','public_transport_density'),('Prague','public_transport_density')}
    comparisons,comparison_checks={},{}
    for name,table in tables.items():
        joined=matched_comparison(table,previous_tables[name],KEYS[name],'_v124')
        comparisons[name+'_v125_comparison']=joined
        comparison_checks[name]=dict(rows=len(joined),keys=KEYS[name],
                                    one_to_one_complete_match=True)
    for name in ['ranks','thresholds','future_mc_city_summary','weight_mc_city_summary']:
        current=tables[name]
        keys=[c for c in KEYS[name] if c in control_tables[name].columns]
        if name in ['future_mc_city_summary','weight_mc_city_summary']:
            current=current[current.evidence_arm=='conditional'].drop(columns='evidence_arm')
        comparisons[name+'_v121_comparison']=matched_comparison(current,control_tables[name],keys,'_v121')
    frequency_changes={}
    for name in ['future_mc_city_summary','weight_mc_city_summary']:
        t=comparisons[name+'_v125_comparison']
        metrics={}
        for metric in ['recommendation_frequency','possible_champion_frequency','mean_decision_rank']:
            delta=t[metric+'_v127']-t[metric+'_v124']
            metrics[metric]=dict(changed_rows=int((delta.abs()>1e-12).sum()),
                                 maximum_absolute_change=float(delta.abs().max()))
        frequency_changes[name]=metrics
    threshold_comparison=comparisons['thresholds_v125_comparison']
    threshold_changes=threshold_comparison.loc[
        (threshold_comparison.status_v127!=threshold_comparison.status_v124)|
        ((threshold_comparison.threshold_raw_multiplier_v127-
          threshold_comparison.threshold_raw_multiplier_v124).abs()>1e-12)]
    for path,digest in protected.items():assert sha(ROOT/path)==digest,path
    assert SNAPSHOT.read_bytes()==snapshot_bytes
    for path,digest in snapshot['source_sha256'].items():assert sha(ROOT/path)==digest,path
    summary.update(version='V128',baseline='16-city V127 conditional evidence',
        comparison_baseline='V125 future extension using V124 evidence; all6tables matched by complete keys',
        interpretation=old_summary['interpretation'],deterministic_raw_changes=SCENARIOS,
        future_mc={**previous_summary['future_mc']},weight_mc={**previous_summary['weight_mc']},
        travel_rule=old_summary['travel_rule'],scope=old_summary['scope'],threshold_rule=old_summary['threshold_rule'],
        threshold_evidence_arm='conditional, matching frozenV122 andV125 scope',
        weights={ref:w.tolist() for ref,w in REFERENCES},source_sha256=protected,
        v121_control_reproduction=old_control,v124_control_reproduction=previous_control,
        changed_input_bounds=changes,changed_input_bounds_since_v124=current_changes,
        source_admissions=str(MANIFEST.relative_to(ROOT)),
        primary_snapshot=str(SNAPSHOT.relative_to(ROOT)),primary_snapshot_sha256=sha(SNAPSHOT),
        no_missing_cell_imputation=True,no_calendar_prediction=True,
        v125_to_v128_matched_comparisons=comparison_checks,
        v125_to_v128_mc_metric_changes=frequency_changes,
        v125_to_v128_threshold_switch_changes=threshold_changes.astype(object).where(
            threshold_changes.notna(),None).to_dict(orient='records'))
    summary['checks'].update(weight_mc_baseline_exactly_matches_V127_both_arms_and_references=True,
        current_four_changed_cells_since_V121=True,current_two_changed_cells_since_V124=True,
        primary_snapshot_verified_before_and_after=True,all_protected_source_hashes_unchanged=True,
        v125_to_v128_all6tables_one_to_one_matched=True,
        historical_control_outputs_untouched=True)
    OUT.mkdir(parents=True,exist_ok=True)
    for name,table in tables.items():table.to_csv(OUT/(name+'.csv'),index=False)
    for name,table in comparisons.items():table.to_csv(OUT/(name+'.csv'),index=False)
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (OUT/'audit.json').write_text(json.dumps(dict(status='pass',checks=summary['checks'],
        v121_control=old_control,v124_control=previous_control,
        primary_snapshot_sha256=sha(SNAPSHOT),protected_files=len(protected),
        baseline_mc_checks=baseline_checks,matched_comparisons=comparison_checks),indent=2)+'\n')
    print(json.dumps(dict(version='V128',changed_cells_since_v121=len(changes),
        changed_cells_since_v124=len(current_changes),metric_changes=frequency_changes,
        threshold_switch_changes=summary['v125_to_v128_threshold_switch_changes']),indent=2))


if __name__=='__main__':main()
