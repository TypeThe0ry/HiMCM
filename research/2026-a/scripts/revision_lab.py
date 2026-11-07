"""Synthetic design experiment only. No real cities or empirical findings."""
from pathlib import Path
import math,json,random
OUT=Path(__file__).resolve().parents[1]/'design'
CITIES={
 'Synthetic-Unequal': [[.90]*5 for _ in range(4)]+[[.10]*5],
 'Synthetic-Balanced': [[.68]*5 for _ in range(5)],
 'Synthetic-Bottleneck': [[.95,.95,.95,.95,.15] for _ in range(5)]}
P=[.2]*5;W=[.2]*5

def lower_mean(values,p,alpha=.2):
    assert 0<alpha<=1 and len(values)==len(p)
    assert abs(sum(p)-1)<1e-10 and all(x>=0 for x in p)
    remaining=alpha;total=0.
    for value,prob in sorted(zip(values,p)):
        take=min(remaining,prob);total+=take*value;remaining-=take
        if remaining<1e-14:break
    return total/alpha

def score(matrix,p=P,w=W,geometric=False,lam=0.,alpha=.2,eps=.01):
    assert 0<=lam<=1 and 0<eps<1 and abs(sum(w)-1)<1e-10
    assert len(matrix)==len(p) and all(len(row)==len(w) for row in matrix)
    assert all(0<=v<=1 for row in matrix for v in row)
    if geometric:
        u=[(math.exp(sum(a*math.log(eps+(1-eps)*z) for a,z in zip(w,row)))-eps)/(1-eps) for row in matrix]
    else:u=[sum(a*z for a,z in zip(w,row)) for row in matrix]
    mean=sum(a*v for a,v in zip(p,u))
    return (1-lam)*mean+lam*lower_mean(u,p,alpha)

methods={'V0_linear_mean':dict(),'geometric_only':dict(geometric=True),'equity_only':dict(lam=.3),'V1_geometric_equity':dict(geometric=True,lam=.3)}
results={method:{name:score(matrix,**args) for name,matrix in CITIES.items()} for method,args in methods.items()}
checks={}
# Structural properties address substantive defects in ranking models.
checks['identical_inputs_tie']=score(CITIES['Synthetic-Balanced'],geometric=True,lam=.3)==score([row[:] for row in CITIES['Synthetic-Balanced']],geometric=True,lam=.3)
improved=[[min(1,x+.02) for x in row] for row in CITIES['Synthetic-Unequal']]
checks['componentwise_improvement_never_lowers_score']=score(improved,geometric=True,lam=.3)>=score(CITIES['Synthetic-Unequal'],geometric=True,lam=.3)
original={name:score(mat,geometric=True,lam=.3) for name,mat in CITIES.items()}
extended=dict(CITIES,**{'Synthetic-Dominated':[[.01]*5 for _ in range(5)]})
checks['adding_dominated_option_preserves_existing_scores']=all(abs(score(extended[name],geometric=True,lam=.3)-s)<1e-12 for name,s in original.items())
transfer=[[.85]*5 for _ in range(4)]+[[.30]*5]
checks['mean_preserving_transfer_helps_disadvantaged_in_this_example']=abs(score(transfer)-score(CITIES['Synthetic-Unequal']))<1e-12 and score(transfer,geometric=True,lam=.3)>score(CITIES['Synthetic-Unequal'],geometric=True,lam=.3)
checks['lower_tail_splits_boundary_population_mass']=abs(lower_mean([0.,1.],[.1,.9],.2)-.5)<1e-12
assert all(checks.values())
# Explicit artificial preference distribution, not estimated public preferences.
rng=random.Random(20261107);n=2000;wins={x:0 for x in CITIES};accepted=0
while accepted<n:
    e=[rng.expovariate(1) for _ in range(5)];w=[x/sum(e) for x in e]
    if not all(.05<=x<=.4 for x in w):continue
    scores={name:score(mat,w=w,geometric=True,lam=.3) for name,mat in CITIES.items()};best=max(scores.values());tied=[k for k,v in scores.items() if abs(v-best)<1e-12]
    for name in tied:wins[name]+=1/len(tied)
    accepted+=1
output={'data_status':'ALL SYNTHETIC; not empirical city rankings','assumptions':{'population_weights':P,'default_domain_weights':W,'alpha':.2,'lambda':.3,'epsilon':.01},'ablation_scores':results,'checks':checks,'artificial_preference_scenarios':{'seed':20261107,'draws':n,'distribution':'Dirichlet(1,1,1,1,1) conditioned on each weight in [0.05,0.40]','top_rank_share':{k:v/n for k,v in wins.items()},'interpretation':'Share under the declared artificial distribution only; not the probability a real city is best and not public support.'}}
(OUT/'synthetic_results.json').write_text(json.dumps(output,ensure_ascii=False,indent=2))
lines=['# 合成反例实验结果','', '**全部数据均为人为构造，不是任何真实城市的排名。**','', '| 方法 | Unequal | Balanced | Bottleneck | 首选 |','| --- | ---: | ---: | ---: | --- |']
for method,scores in results.items():lines.append('| '+method+' | '+' | '.join(f'{scores[k]:.4f}' for k in CITIES)+' | '+max(scores,key=scores.get)+' |')
lines+=['','V0被设定为更重视总体平均；几何聚合与分布关注分别解决不同的结构问题。这个反例说明两种修改可能改变推荐，不说明新偏好必然优于旧偏好，也不证明真实城市中存在同样的差异。','','五项结构检查通过：同输入并列、逐项改善不降分、加入劣势候选不影响原有得分、该例中保持均值的改善较差单元得到回应、低端人口边界按份额切分正确。','','偏好情景抽样采用明确的人为分布，仅演示名次占比的计算。默认权重与公平参数仍需团队论证；没有真实城市数据与社区分布时不可用于参赛结论。']
(OUT/'synthetic_results_notes.md').write_text('\n'.join(lines)+'\n');print(json.dumps(output,ensure_ascii=False))
