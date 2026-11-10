"""Staged Vienna scheduled-bus refinement. No activation or manuscript changes."""
import hashlib
import json
from functools import lru_cache
import numpy as np
import pandas as pd
from task4_user_v203_revision import revised_bounds as previous_bounds
from task4_user_v136_revision import without_historical_proxy
from task4_user_city_indicators import SOURCE, evaluate
from task4_v5_model import ROOT, NAMES, SPEC, weights
from task4_ahp_mc_baseline import score_many, interval_metrics, rank_metrics

OUT = ROOT / 'results/task4_user_v204_revision'
MANIFEST = ROOT / 'design/task4_user_v204_admissions.json'
WITNESSES = ROOT / 'results/current_vienna_gtfs_candidate/station_witnesses.csv'
CONDITION_ROUTES = ('41A','43A','56A','58A','73A','74A','86A','89A','92A')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

@lru_cache(maxsize=1)
def admission():
    m = json.loads(MANIFEST.read_text())
    assert m['input_sha256'] == sha(SOURCE)
    for name, expected in m['source_hashes'].items():
        assert sha(ROOT / name) == expected, name
    # This exact CSV contains one selected witness per native DIVA group.
    witness_path = str(WITNESSES.relative_to(ROOT))
    assert witness_path in m['source_hashes']
    w = pd.read_csv(WITNESSES, dtype=str, keep_default_na=False)
    assert len(w) == w.DIVA.nunique() == 378
    assert m['version']=='V204' and m['activation_status']=='staged_not_active'
    assert len(m['observations'])==1
    row=m['observations'][0]
    for key,value in dict(city='Vienna',indicator='public_transport_density',raw_count_before=99,raw_count=378,population=2028399,population_year=2025,anchor=50,service_day='20261110',counts_not_added=True,public_passenger_nature_supported=True,source_defined_scheduled_supply_supported=True,trip_level_PDF_conditions_verified=False,actual_operation_verified=False).items():
        assert row[key]==value, key
    assert set(row['native_root_ids'])==set(w.DIVA) and len(row['native_root_ids'])==378
    assert set(m['condition_routes'])==set(CONDITION_ROUTES)
    for route in CONDITION_ROUTES:
        assert set(m['condition_route_DIVA_ids'][route])==set(w.loc[w.route_short_name.eq(route),'DIVA'])
    assert set(m['condition_selected_DIVA_ids'])==set(w.loc[w.route_short_name.isin(CONDITION_ROUTES),'DIVA'])
    assert len(m['condition_selected_DIVA_ids'])==36
    assert sha(ROOT/m['qualification_verification'])==m['qualification_verification_sha256']
    return m, w

def revised_bounds(include_vienna_bus=True, withhold_condition_routes=False, withhold_witness_routes=(), **kwargs):
    f, lo, hi = previous_bounds(**kwargs)
    before_lo, before_hi = lo.copy(), hi.copy()
    routes = set(withhold_witness_routes)
    if not routes.issubset(CONDITION_ROUTES):
        raise ValueError("Unknown condition route")
    if withhold_condition_routes: routes.update(CONDITION_ROUTES)
    if routes and not include_vienna_bus:
        raise ValueError('Withholding requires the Vienna candidate')
    if include_vienna_bus:
        m, w = admission()
        i = f.city.tolist().index('Vienna'); j = NAMES.index('public_transport_density')
        assert f.iloc[i].population == 2028399 and f.iloc[i].population_year == 2025
        assert SPEC[j][2] == 50 and hi[i,j] == 1
        n = len(w) - int(w.route_short_name.isin(routes).sum())
        density = n * 100000 / 2028399
        lo[i,j] = density / (50 + density)
        assert lo[i,j] >= before_lo[i,j]
        mask = np.ones(lo.shape, dtype=bool); mask[i,j] = False
        np.testing.assert_array_equal(lo[mask], before_lo[mask])
    np.testing.assert_array_equal(hi, before_hi)
    return f, lo, hi

def main():
    if OUT.exists() and any(OUT.iterdir()):
        raise ValueError('Choose an absent or empty staged output directory')
    m,witness = admission()
    f,l0,h0 = previous_bounds(); _,lo,hi = revised_bounds(); cities=f.city.tolist()
    _,off,offhi = revised_bounds(include_vienna_bus=False)
    np.testing.assert_array_equal(off,l0); np.testing.assert_array_equal(offhi,h0)
    def lower(**kwargs): return revised_bounds(**kwargs)[1]
    amsterdam=lo.copy(); amsterdam[cities.index('Amsterdam'),NAMES.index('public_transport_density')]=0
    cases=[('before_V203',l0,h0),('after_conditional',lo,hi),('withdraw_Vienna_bus_refinement',off,hi),
      ('withdraw_Oslo_bus_refinement',lower(include_oslo_bus=False),hi),
      ('withdraw_OCBC_venue',lower(include_sportshub=False),hi),
      ('withdraw_Singapore_directory_refinement',lower(include_sg_pool=False),hi),
      ('withdraw_all_Singapore_pool_supplements',lower(include_sportshub=False,include_sg_pool=False),hi),
      ('withhold_existing_three_notice_venues',lower(withhold_existing_notice_venues=True),hi),
      ('withhold_all_four_notice_venues',lower(withhold_notice_venues=True),hi),
      ('withdraw_Zurich_pool_refinement',lower(include_zurich_pool=False),hi),
      ('withdraw_Tokyo_inventory',lower(include_tokyo=False),hi),
      ('withdraw_Warsaw_inventory',lower(include_warsaw=False),hi),
      ('withdraw_both_inventory',lower(include_tokyo=False,include_warsaw=False),hi),
      ('withdraw_historical_stage_proxy',*without_historical_proxy(f,lo,hi)),
      ('withdraw_Amsterdam_mapped_inventory',amsterdam,hi),
      ('withhold_two_rail_replacement_stops',lower(withhold_rail_replacement=True),hi),
      ('withhold_no_calls_Midtstuen_bus',lower(withhold_no_calls_bus=True),hi),
      ('withhold_all_three_service_flags',lower(withhold_rail_replacement=True,withhold_no_calls_bus=True),hi),
      ('include_questioned_Tveten_bru',lower(include_questioned_stop=True),hi),
      ('conservative_withhold_selected_nine_route_witnesses',lower(withhold_condition_routes=True),hi)]
    cases.extend((f'conservative_withhold_selected_{route}_witnesses', lower(withhold_witness_routes=(route,)), hi) for route in CONDITION_ROUTES)
    ranks=[]; bounds=[]; reports=[]; mc=[]
    for label,a,b in cases:
        for ref,weight in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
            t=evaluate(cities,a,b,weight); ranks.append(t.assign(scenario=label,weight_reference=ref))
            reports.append(dict(scenario=label,weight_reference=ref,possible_champions=t.loc[t.possible_champion,'city'].tolist(),necessary_champions=t.loc[t.necessary_champion,'city'].tolist(),minimax_choices=t.loc[t.decision_rank.eq(1),'city'].tolist(),mean_width=float((t.score_upper-t.score_lower).mean())))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=a[i,j],upper=b[i,j]) for i,c in enumerate(cities) for j,n in enumerate(NAMES))
    for ref,center in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
        for concentration in [20,100,500]:
            draws=np.random.default_rng(np.random.SeedSequence([20261108,concentration])).dirichlet(concentration*center,10000)
            for label,a,b in cases:
                lower_scores,upper=score_many(a,draws),score_many(b,draws)
                regret,possible,_,_,_=interval_metrics(lower_scores,upper); rank,recommended,_=rank_metrics(regret,descending=False)
                for i,c in enumerate(cities): mc.append(dict(scenario=label,weight_reference=ref,concentration=concentration,city=c,minimax_recommendation_frequency=float(recommended[:,i].mean()),mean_decision_rank=float(rank[:,i].mean()),possible_champion_frequency=float(possible[:,i].mean())))
    OUT.mkdir(parents=True,exist_ok=True)
    table=pd.concat(ranks,ignore_index=True);table.to_csv(OUT/'all_ranks.csv',index=False)
    table[table.scenario.eq('after_conditional')].to_csv(OUT/'current_ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(OUT/'utility_bounds.csv',index=False); pd.DataFrame(mc).to_csv(OUT/'mc_city_summary.csv',index=False)
    route_counts={route:int(witness.route_short_name.eq(route).sum()) for route in CONDITION_ROUTES}
    report=dict(version='V204',activation_status='staged_not_active',baseline='V203',results=reports,changed_cells=1,unchanged_cells=159,all_upper_bounds_unchanged=True,point_cells=112,partial_cells=37,fully_missing_cells=11,refined_existing_partial_cells=1,newly_filled_cells=0,input_sha256=sha(SOURCE),admissions_sha256=sha(MANIFEST),mc_seed=20261108,mc_draws_per_setting=10000,primary_mc_settings=len(cases)*6,condition_witness_counts=route_counts,condition_witnesses_withheld=sum(route_counts.values()),condition_remaining_groups=378-sum(route_counts.values()),scope='378 selected DIVA groups replace, not add to, 99 metro groups. Condition case conservatively withholds groups with selected witnesses on nine named routes; no search for alternative witnesses. Scheduled service-day evidence is not a census, real-time service or access measure. Simulations are conditional sensitivity analyses, not empirical probabilities.')
    (OUT/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print('V204 staged primary complete:',len(cases),'cases',len(cases)*6,'MC settings')
if __name__=='__main__': main()
