"""Independent scalar TOPSIS and continuous regret audit; no scoring imports."""
from pathlib import Path
import csv,json,math,hashlib
P=Path(__file__).resolve().parent
AUX={'public_transport_density','public_pool_density'}
def read(name):return list(csv.DictReader((P/name).open()))
def near(a,b):assert math.isclose(float(a),float(b),abs_tol=1e-10,rel_tol=0),(a,b)
def score(row,alpha):
    plus=math.sqrt(sum(((1-u)**2)*(alpha/2 if j in AUX else (1-alpha)/8) for j,u in row.items()))
    minus=math.sqrt(sum(u*u*(alpha/2 if j in AUX else (1-alpha)/8) for j,u in row.items()))
    return 100*minus/(plus+minus)
def audit():
    bounds=read('utility_bounds.csv');ranks=read('ranks.csv');cert=read('recommendation_certificate.csv')
    assert len(bounds)==1250 and len(ranks)==125 and len(cert)>=5
    scenarios=list(dict.fromkeys(r['scenario'] for r in bounds));assert len(scenarios)==5
    city_order=list(dict.fromkeys(r['city'] for r in bounds));assert len(city_order)==25
    matrices={s:{} for s in scenarios}
    for r in bounds:
        key=(r['city'],r['indicator']);assert key not in matrices[r['scenario']]
        lo,hi=float(r['lower']),float(r['upper']);assert 0<=lo<=hi<=1
        matrices[r['scenario']][key]=(lo,hi)
    before=matrices[scenarios[0]];withdraw=matrices[scenarios[-1]]
    assert scenarios==['v102_2020_progression','2020_transition_optional','2025_progression','v107_2025_transition_optional','v107_withdrawn']
    key=('Mexico City','travel')
    assert before==withdraw
    baseline=list(csv.DictReader((P.parent/'task4_v102_copenhagen_revision/utility_bounds.csv').open()))
    baseline_scenario=list(dict.fromkeys(r['scenario'] for r in baseline))[1]
    assert {(r['city'],r['indicator']):(float(r['lower']),float(r['upper'])) for r in baseline if r['scenario']==baseline_scenario}==before
    s20=json.loads((P.parents[1]/'data/task4_v107_mexico_membership/summary.json').read_text())
    s25=json.loads((P.parents[1]/'data/task4_v107_mexico/aggregate_bounds.json').read_text())
    expected=[s20['old_utility'],s20['revised_utility'],s25['legacy_progression'],s25['boundary3_optional'],s20['old_utility']]
    for scenario,interval in zip(scenarios,expected):
        m=matrices[scenario]
        assert set(m)==set(before)
        assert all(m[k]==before[k] for k in before if k!=key)
        for actual,want in zip(m[key],interval):near(actual,want)
    scores={};checks=[]
    for scenario,m in matrices.items():
        assert len(m)==250
        lows={c:{j:v[0] for (cc,j),v in m.items() if cc==c} for c in city_order}
        highs={c:{j:v[1] for (cc,j),v in m.items() if cc==c} for c in city_order}
        def calc(alpha):return ({c:score(lows[c],alpha) for c in city_order},{c:score(highs[c],alpha) for c in city_order})
        ls,us=calc(.1)
        regret={c:max(0,max(us[k] for k in city_order if k!=c)-ls[c]) for c in city_order}
        for r in [r for r in ranks if r['scenario']==scenario]:
            c=r['city'];near(r['score_lower'],ls[c]);near(r['score_upper'],us[c]);near(r['max_regret'],regret[c])
            best=1+sum(ls[k]>us[c] for k in city_order if k!=c)
            worst=1+sum(us[k]>ls[c] for k in city_order if k!=c)
            assert int(r['best_rank'])==best and int(r['worst_rank'])==worst
            assert (r['possible_champion']=='True')==(best==1)
            assert (r['necessary_champion']=='True')==(worst==1)
            assert int(r['decision_rank'])==1+sum(v<regret[c] for v in regret.values())
        leaves=sorted([r for r in cert if r['scenario']==scenario],key=lambda r:float(r['alpha_lower']))
        end=.05;gaps=[]
        for leaf in leaves:
            a,b=float(leaf['alpha_lower']),float(leaf['alpha_upper']);near(a,end);assert a<b;end=b
            l0,u0=calc(a);l1,u1=calc(b)
            # Scores have affine squared distances in alpha; each endpoint utility
            # score is monotone, so endpoint extrema enclose the whole interval.
            lower={c:max(0,max(min(u0[k],u1[k])-1e-9 for k in city_order if k!=c)-max(l0[c],l1[c])-1e-9) for c in city_order}
            upper={c:max(0,max(max(u0[k],u1[k])+1e-9 for k in city_order if k!=c)-min(l0[c],l1[c])+1e-9) for c in city_order}
            winner=city_order[int(leaf['winner'])];gap=min(lower[k] for k in city_order if k!=winner)-upper[winner]
            near(leaf['regret_gap_lower'],gap);assert gap>1e-8 and leaf['certified']=='True' and winner=='Singapore';gaps.append(gap)
        near(end,.2)
        assert all(us[c]>=max(ls[k] for k in city_order if k!=c) for c in city_order)
        # A single fixed-alpha witness in the allowed range certifies each city
        # is a possible champion somewhere in that continuous preference range.
        checks.append({'scenario':scenario,'rank_rows_verified':25,'possible_champions_fixed':25,'continuous_possible_champion_witness_alpha':.1,'certified_leaves':len(leaves),'minimum_certified_gap':min(gaps),'winner':'Singapore'})
        scores[scenario]=(ls,us,regret)
    assert scores[scenarios[0]]==scores[scenarios[-1]]
    summary=json.loads((P/'summary.json').read_text())
    rank_maps={s:{r['city']:int(r['decision_rank']) for r in ranks if r['scenario']==s} for s in scenarios}
    for r in summary['scenarios']:
        s=r['scenario'];ls,us,regret=scores[s]
        assert r['choice']==['Singapore'] and r['possible_champions']==25
        assert set(r['continuous_possible_champions'])==set(city_order)
        assert r['continuous_recommendation']=={'unresolved':0,'winners':['Singapore']}
        changes=sum(rank_maps[s][c]!=rank_maps[scenarios[0]][c] for c in city_order)
        assert r['changed_ranks_vs_v102']==changes
        concordant=discordant=ties_a=ties_b=0
        from itertools import combinations
        for x,y in combinations(city_order,2):
            a=rank_maps[s][x]-rank_maps[s][y];b=rank_maps[scenarios[0]][x]-rank_maps[scenarios[0]][y]
            if a*b>0:concordant+=1
            elif a*b<0:discordant+=1
            elif a==0 and b!=0:ties_a+=1
            elif b==0 and a!=0:ties_b+=1
        tau=(concordant-discordant)/math.sqrt((concordant+discordant+ties_a)*(concordant+discordant+ties_b))
        near(tau,r['kendall_tau_vs_v102'])
        for field,value in [('score_lower',ls['Mexico City']),('score_upper',us['Mexico City']),('max_regret',regret['Mexico City']),('decision_rank',rank_maps[s]['Mexico City'])]:near(r['mexico'][field],value)
    import struct
    primary=matrices['v107_2025_transition_optional']
    keys=list(primary)
    digest=hashlib.sha256(b''.join(struct.pack('<d',primary[k][side]) for side in (0,1) for k in keys)).hexdigest()
    assert digest==summary['input_bounds_sha256']
    return {'passed':True,'independent_scoring':True,'core_scoring_functions_imported':False,'bounds_verified':1250,'rank_rows_verified':125,'unchanged_other_cells_per_case':249,'withdrawal_exactly_restores_v102':True,'baseline_matches_v102':True,'source_endpoints_verified':True,'primary_binary_input_hash_verified':True,'scenarios':checks,'certificate_scope':'Independent scalar TOPSIS; monotonic endpoint enclosures over continuous alpha [0.05,0.2]. Floating-point numerical certificate, not directed-rounding formal arithmetic. All25 possible champions have the shared-alpha0.1 witness.','interpretation':'Conditional weighted-sample identification bounds, not an unconditional population bound or sampling CI.','input_sha256':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['utility_bounds.csv','ranks.csv','recommendation_certificate.csv','summary.json']}}
if __name__=='__main__':
    result=audit();(P/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
