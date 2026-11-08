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
    assert len(bounds)==750 and len(ranks)==75 and len(cert)==6
    scenarios=list(dict.fromkeys(r['scenario'] for r in bounds));assert len(scenarios)==3
    city_order=list(dict.fromkeys(r['city'] for r in bounds));assert len(city_order)==25
    matrices={s:{} for s in scenarios}
    for r in bounds:
        key=(r['city'],r['indicator']);assert key not in matrices[r['scenario']]
        lo,hi=float(r['lower']),float(r['upper']);assert 0<=lo<=hi<=1
        matrices[r['scenario']][key]=(lo,hi)
    before,after,withdraw=[matrices[s] for s in scenarios]
    changed=[k for k in before if before[k]!=after[k]]
    assert changed==[('Copenhagen','research_he_density')]
    assert before==withdraw
    baseline=list(csv.DictReader((P.parent/'task4_v96_intake/utility_bounds.csv').open()))
    assert {(r['city'],r['indicator']):(float(r['lower']),float(r['upper'])) for r in baseline}==before
    source=json.loads((P.parents[1]/'data/task4_v102_copenhagen/summary.json').read_text())
    near(after[changed[0]][0],source['utility_lower']);assert after[changed[0]][1]==1
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
    rank_maps={s:{r['city']:int(r['decision_rank']) for r in ranks if r['scenario']==s} for s in scenarios}
    assert rank_maps[scenarios[0]]==rank_maps[scenarios[1]]==rank_maps[scenarios[2]]
    assert scores[scenarios[0]]==scores[scenarios[2]]
    summary=json.loads((P/'summary.json').read_text());b0,b1=scores[scenarios[0]],scores[scenarios[1]]
    gain=b1[0]['Copenhagen']-b0[0]['Copenhagen'];near(summary['score_lower_gain'],gain)
    near(summary['score_upper_change'],b1[1]['Copenhagen']-b0[1]['Copenhagen'])
    near(summary['score_width_reduction_percent'],100*gain/(b0[1]['Copenhagen']-b0[0]['Copenhagen']))
    for s in summary['scenarios']:
        assert s['choice']==['Singapore'] and s['changed_ranks']==0
        near(s['kendall_tau_vs_v96'],1)
        assert set(s['possible_champions'])==set(city_order)==set(s['continuous_possible_champions'])
    return {'passed':True,'independent_scoring':True,'core_scoring_functions_imported':False,'bounds_verified':750,'rank_rows_verified':75,'changed_cells':1,'unchanged_other_cells':249,'withdrawal_exactly_restores_v96':True,'baseline_matches_v96_intake':True,'score_lower_gain':gain,'scenarios':checks,'certificate_scope':'Endpoint monotonicity enclosures over [0.05,0.2]; floating-point numerical certificate, not directed-rounding formal interval arithmetic.','input_sha256':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['utility_bounds.csv','ranks.csv','recommendation_certificate.csv','summary.json']}}
if __name__=='__main__':
    result=audit();(P/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
