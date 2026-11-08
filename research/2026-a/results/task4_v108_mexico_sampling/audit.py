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

def verify_inference(inf):
    from scipy.stats import t
    dpath=P.parents[1]/'data/task4_v108_mexico_design'
    manifest=json.loads((dpath/'manifest.json').read_text())
    data_bytes=(dpath/manifest['file']).read_bytes()
    assert hashlib.sha256(data_bytes).hexdigest()==manifest['sha256']==inf['input_moments_sha256']
    d=json.loads(data_bytes);totals=d['weighted_totals'];cross=d['centered_crossproduct']
    df=d['diagnostics']['psu_n']-d['diagnostics']['strata_n'];assert df==inf['df']==3384
    assert d['diagnostics']['singleton_strata_n']==0 and d['diagnostics']['psus_zero_target_vector']==586
    codes=['1','2','3','4','5','6','9','blank']
    endpoints=[(math.exp(-.5),1),(math.exp(-1),math.exp(-.5)),(math.exp(-2),math.exp(-1)),(math.exp(-4),math.exp(-2)),(0,math.exp(-4)),(0,1),(0,1),(0,1)]
    checks=0
    for name in ('legacy_progression','boundary3_optional'):
        fixed={0,1} if name=='legacy_progression' else {0}
        optional={2} if name=='legacy_progression' else {1,2}
        result=inf['scenarios'][name]
        for side,col in (('lower',0),('upper',1)):
            order=sorted(range(8),key=lambda k:endpoints[k][col],reverse=bool(col))
            cs=result['candidates'][side]['candidates'];assert len(cs)==9
            ratios=[];ses=[]
            for k,c in enumerate(cs):
                selected=set(order[:k]);assert c['prefix']==k and c['optional_time_codes']==[codes[i] for i in order[:k]]
                denom=[int(g in fixed or (g in optional and j in selected)) for g in range(3) for j in range(8)]
                num=[denom[z]*endpoints[z%8][col] for z in range(24)]
                X=sum(v*w for v,w in zip(denom,totals));Y=sum(v*w for v,w in zip(num,totals));ratio=Y/X
                residual=[a-ratio*b for a,b in zip(num,denom)]
                variance=sum(residual[i]*cross[i][j]*residual[j] for i in range(24) for j in range(24))/X**2
                se=math.sqrt(max(0,variance));near(c['ratio'],ratio);near(c['taylor_se'],se);near(c['A'],Y);near(c['B'],X)
                assert c['numerator_coefficients']==num and c['denominator_coefficients']==denom
                ratios.append(ratio);ses.append(se);checks+=1
            near(result['point'][col],(min if col==0 else max)(ratios))
            for label,tail in [('outer',.025),('familywise',.05/18)]:
                critical=float(t.ppf(1-tail,df));near(result[label+'_critical'],critical)
                candidates=[r+(-1 if col==0 else 1)*critical*se for r,se in zip(ratios,ses)]
                chosen=(min if col==0 else max)(range(9),key=lambda k:candidates[k])
                assert result[label+'_prefixes'][col]==chosen
                near(result[label][col],min(1,max(0,candidates[chosen])))
        p,o,f=[result[x] for x in ('point','outer','familywise')]
        assert f[0]<=o[0]<=p[0]<=p[1]<=o[1]<=f[1]
    return {'ratios_and_taylor_standard_errors':checks,'all_nine_prefixes_per_side':True,'design_df':df,'point_outer_familywise_nesting':True,'method':'Independent coefficient and quadratic-form reconstruction from hashed public moments; raw design aggregation checked separately.'}

def audit():
    bounds=read('utility_bounds.csv');ranks=read('ranks.csv');cert=read('recommendation_certificate.csv')
    assert len(bounds)==1000 and len(ranks)==100 and len(cert)>=4
    scenarios=list(dict.fromkeys(r['scenario'] for r in bounds));assert len(scenarios)==4
    city_order=list(dict.fromkeys(r['city'] for r in bounds));assert len(city_order)==25
    matrices={s:{} for s in scenarios}
    for r in bounds:
        key=(r['city'],r['indicator']);assert key not in matrices[r['scenario']]
        lo,hi=float(r['lower']),float(r['upper']);assert 0<=lo<=hi<=1
        matrices[r['scenario']][key]=(lo,hi)
    before=matrices[scenarios[0]];withdraw=matrices[scenarios[-1]]
    assert scenarios==['v107_point','v108_outer','v108_familywise','v108_withdrawn']
    key=('Mexico City','travel')
    assert before==withdraw
    baseline=list(csv.DictReader((P.parent/'task4_v107_mexico_revision/utility_bounds.csv').open()))
    baseline_scenario='v107_2025_transition_optional'
    assert {(r['city'],r['indicator']):(float(r['lower']),float(r['upper'])) for r in baseline if r['scenario']==baseline_scenario}==before
    inf=json.loads((P/'inference.json').read_text())
    inference_check=verify_inference(inf)
    q=inf['scenarios']['boundary3_optional']
    expected=[q['point'],q['outer'],q['familywise'],q['point']]
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
        assert r['changed_ranks']==changes
        concordant=discordant=ties_a=ties_b=0
        from itertools import combinations
        for x,y in combinations(city_order,2):
            a=rank_maps[s][x]-rank_maps[s][y];b=rank_maps[scenarios[0]][x]-rank_maps[scenarios[0]][y]
            if a*b>0:concordant+=1
            elif a*b<0:discordant+=1
            elif a==0 and b!=0:ties_a+=1
            elif b==0 and a!=0:ties_b+=1
        tau=(concordant-discordant)/math.sqrt((concordant+discordant+ties_a)*(concordant+discordant+ties_b))
        near(tau,r['kendall_tau'])
        for field,value in [('score_lower',ls['Mexico City']),('score_upper',us['Mexico City']),('max_regret',regret['Mexico City']),('decision_rank',rank_maps[s]['Mexico City'])]:near(r['mexico'][field],value)
    import struct
    primary=matrices['v108_outer']
    keys=list(primary)
    digest=hashlib.sha256(b''.join(struct.pack('<d',primary[k][side]) for side in (0,1) for k in keys)).hexdigest()
    assert digest==summary['input_bounds_sha256']
    return {'passed':True,'independent_scoring':True,'core_scoring_functions_imported':False,'bounds_verified':1000,'rank_rows_verified':100,'unchanged_other_cells_per_case':249,'withdrawal_exactly_restores_v107':True,'baseline_matches_v107':True,'source_endpoints_verified':True,'inference_verified':inference_check,'primary_binary_input_hash_verified':True,'scenarios':checks,'certificate_scope':'Independent scalar TOPSIS; monotonic endpoint enclosures over continuous alpha [0.05,0.2]. Floating-point numerical certificate, not directed-rounding formal arithmetic. All25 possible champions have the shared-alpha0.1 witness.','interpretation':'Approximate Taylor sampling outer envelope around conditional identification bounds; not a finite-sample coverage guarantee or unconditional population claim.','input_sha256':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['utility_bounds.csv','ranks.csv','recommendation_certificate.csv','summary.json','inference.json']}}
if __name__=='__main__':
    result=audit();(P/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
