"""Reproducible 25-city proxy-data comparison; offline from archived Numbeo 2025 HTML."""
from pathlib import Path
import hashlib, json
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from scipy.stats import kendalltau, rankdata
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/task4_real'
OUT=ROOT/'results/task4_real'
OUT.mkdir(parents=True,exist_ok=True)
SOURCE='https://www.numbeo.com/quality-of-life/rankings.jsp?title=2025'
FIELDS=['Safety Index','Pollution Index','Property Price to Income Ratio','Traffic Commute Time Index']
BOUNDS=np.array([100.,100.,40.,90.])
DIRECTIONS=np.array([1,-1,-1,-1])

def transform(x,bounds=BOUNDS):
    a=np.clip(x/bounds,0,1)
    return np.where(DIRECTIONS>0,a,1-a)

def scores(z,w):
    # Rows=scenarios, columns=cities; weights enter squared distance once.
    dp=np.sqrt(w@((1-z)**2).T)
    dm=np.sqrt(w@(z**2).T)
    return dm/(dp+dm)

def sample(rng,n,alpha=1.,lo=.1,hi=.55):
    chunks=[];total=0
    while total<n:
        a=rng.dirichlet(np.full(4,alpha),max(5000,n))
        a=a[(a.min(axis=1)>=lo)&(a.max(axis=1)<=hi)]
        chunks.append(a);total+=len(a)
    return np.concatenate(chunks)[:n]

def grid(step=.025,lo=.1,hi=.55):
    n=round(1/step);low=int(np.ceil(lo/step-1e-9));high=int(np.floor(hi/step+1e-9))
    return np.array([(a,b,c,n-a-b-c) for a in range(low,high+1)
                     for b in range(low,high+1) for c in range(low,high+1)
                     if low<=n-a-b-c<=high],float)/n

def metrics(s):
    r=s.max(axis=1,keepdims=True)-s
    return r.max(axis=0),r

def main():
    raw=(DATA/'numbeo_quality_of_life_2025.html').read_bytes()
    soup=BeautifulSoup(raw,'html.parser')
    table=soup.find('table',id='t2')
    cols=[v.get_text(' ',strip=True) for v in table.select('thead th')]
    rows=[[v.get_text(' ',strip=True) for v in tr.find_all('td')] for tr in table.select('tbody tr')]
    all_data=pd.DataFrame(rows,columns=cols)
    candidates=pd.read_csv(ROOT/'data/city_candidates_team_25.csv')
    selected=[]
    aliases={'Phoenix':'Phoenix, AZ, United States','New York':'New York, NY, United States'}
    for _,c in candidates.iterrows():
        name=aliases.get(c.city,f'{c.city}, {c.country}')
        hit=all_data[all_data.City==name]
        assert len(hit)==1,(name,len(hit))
        row={'city':c.city,'source_city':name,'country':c.country}
        row.update({f:float(hit.iloc[0][f]) for f in FIELDS})
        row.update(source_url=SOURCE,edition='2025',accessed_local_date='2026-11-07')
        selected.append(row)
    df=pd.DataFrame(selected)
    df.to_csv(DATA/'city_indicators_2025.csv',index=False)
    x=df[FIELDS].to_numpy(); assert x.shape==(25,4) and np.isfinite(x).all()
    z=transform(x);names=df.city.to_numpy()
    pd.DataFrame(z,columns=FIELDS,index=names).to_csv(OUT/'normalized_indicators.csv',index_label='city')
    rng=np.random.default_rng(20261107)
    mc=sample(rng,20000)
    boundary=grid()
    train=np.vstack([mc,boundary])
    pd.DataFrame(train,columns=FIELDS).to_csv(OUT/'design_weights.csv',index=False)
    s=scores(z,train);R,reg=metrics(s)
    baseline=scores(z,np.full((1,4),.25))[0]
    r0=rankdata(-baseline,method='min').astype(int);r1=rankdata(R,method='min').astype(int)
    a=int(np.argmax(baseline));b=int(np.argmin(R))
    # Occupied rank positions receive equal probability mass in a numerical tie.
    mc_scores=scores(z,mc)
    first=np.zeros(25);top3=np.zeros(25)
    ranks=np.zeros((25,25))
    for row in mc_scores:
        order=np.argsort(-row);k=0
        while k<25:
            end=k+1
            while end<25 and abs(row[order[end]]-row[order[k]])<=1e-12:end+=1
            for city in order[k:end]:ranks[city,k:end]+=1/(end-k)
            k=end
    ranks/=len(mc)
    first=ranks[:,0];top3=ranks[:,:3].sum(axis=1)
    hold=sample(np.random.default_rng(20261108),20000,alpha=2.)
    hs=scores(z,hold);HR,_=metrics(hs)
    result=pd.DataFrame({'city':names,'V0_score':baseline*100,'V0_rank':r0,'V1_rank':r1,
                         'rank_gain':r0-r1,'max_tested_regret_points':R*100,
                         'holdout_max_regret_points':HR*100,'first_share':first,'top3_share':top3})
    result.sort_values('V1_rank').to_csv(OUT/'rankings.csv',index=False)
    worst=[]
    for i in range(25):
        k=int(reg[:,i].argmax());challenger=int(s[k].argmax())
        worst.append({'city':names[i],'challenger':names[challenger],
                      'regret_points':float(reg[k,i]*100),**dict(zip(FIELDS,train[k].tolist()))})
    pd.DataFrame(worst).to_csv(OUT/'worst_scenarios.csv',index=False)
    # Scaling and preference-set checks; these are explicit assumptions, not error estimates.
    stress=[]
    for label,bounds,lo,hi in [('base',BOUNDS,.1,.55),('narrow_weights',BOUNDS,.15,.45),
                             ('wide_weights',BOUNDS,.05,.75),('housing30_commute60',np.array([100,100,30,60]),.1,.55),
                             ('housing50_commute120',np.array([100,100,50,120]),.1,.55)]:
        zz=transform(x,bounds);ww=grid(lo=lo,hi=hi)
        ss=scores(zz,ww);rr,_=metrics(ss);bb=scores(zz,np.full((1,4),.25))[0]
        ia=int(bb.argmax());ib=int(rr.argmin())
        stress.append({'scenario':label,'V0_winner':names[ia],'V1_winner':names[ib],
                       'V0_winner_regret':float(rr[ia]*100),'V1_winner_regret':float(rr[ib]*100),
                       'V0_score_sacrifice':float((bb[ia]-bb[ib])*100)})
    pd.DataFrame(stress).to_csv(OUT/'assumption_sensitivity.csv',index=False)
    # Hypothetical measurement perturbation, deliberately not labelled a confidence interval.
    perturb=np.random.default_rng(91);noise_winners=np.zeros(25,int)
    for _ in range(200):
        zz=np.clip(z+perturb.uniform(-.03,.03,z.shape),0,1)
        rr,_=metrics(scores(zz,boundary));noise_winners[rr.argmin()]+=1
    # Diagnostic PCA only, no PCA reweighting. Columns are standardized directed utilities.
    standard=(z-z.mean(axis=0))/z.std(axis=0,ddof=1)
    _,sv,vt=np.linalg.svd(standard,full_matrices=False)
    eig=sv**2/(len(z)-1);expl=eig/eig.sum()
    pd.DataFrame(vt.T*np.sqrt(eig),index=FIELDS,columns=['PC1','PC2','PC3','PC4']).to_csv(OUT/'pca_loadings.csv')
    pd.DataFrame(np.corrcoef(z,rowvar=False),index=FIELDS,columns=FIELDS).to_csv(OUT/'indicator_correlations.csv')
    # A feasible observed flip is an upper bound on the unknown minimum change.
    flips=np.where(s.max(axis=1)>s[:,a]+1e-10)[0]
    certificate=None
    if len(flips):
        k=int(flips[np.argmin(.5*np.abs(train[flips]-.25).sum(axis=1))])
        challenger=int(s[k].argmax())
        certificate={'baseline_champion':names[a],'challenger':names[challenger],
                     'weights':dict(zip(FIELDS,train[k].tolist())),
                     'weight_mass_reallocated':float(.5*np.abs(train[k]-.25).sum()),
                     'challenger_score':float(s[k,challenger]*100),'champion_score':float(s[k,a]*100),
                     'claim':'smallest flip found in tested scenarios; NOT a global minimum certificate'}
    (OUT/'observed_flip.json').write_text(json.dumps(certificate,indent=2)+'\n')
    # Structural checks independent of the ranking result.
    improved=z.copy();improved[0]=np.minimum(1,improved[0]+.01)
    assert np.all(scores(improved,boundary)[:,0]>=scores(z,boundary)[:,0]-1e-12)
    augmented=np.vstack([z,np.zeros(4)])
    aug=scores(augmented,boundary)
    assert np.allclose(aug[:,:25],scores(z,boundary))
    assert np.allclose(metrics(aug)[0][:25],metrics(scores(z,boundary))[0])
    # Holdout is deliberately a different preference sampling law, not unseen city observations.
    summary={'source_url':SOURCE,'source_sha256':hashlib.sha256(raw).hexdigest(),
             'scope':'25 real cities; four Numbeo proxy indicators; not a complete high-schooler index',
             'city_count':25,'seed':20261107,'mc_count':len(mc),'grid_count':len(boundary),
             'V0_winner':names[a],'V1_winner':names[b],
             'V0_winner_baseline_score':float(baseline[a]*100),'V1_winner_baseline_score':float(baseline[b]*100),
             'max_regret_before':float(R[a]*100),'max_regret_after':float(R[b]*100),
             'holdout_regret_before':float(HR[a]*100),'holdout_regret_after':float(HR[b]*100),
             'holdout_winner':names[HR.argmin()],
             'kendall_tau_b':float(kendalltau(r0,r1).statistic),
             'cities_changed_rank':int((r0!=r1).sum()),
             'PCA_explained_variance':expl.tolist(),
             'hypothetical_noise_winner_counts':dict(zip(names,noise_winners.tolist())),
             'checks':'finite data, exact city matching, monotonicity, dominated candidate score/regret invariance passed'}
    (OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    fig,ax=plt.subplots(figsize=(10,9))
    for i in np.argsort(r0):
        ax.plot([0,1],[r0[i],r1[i]],color='#086788' if i in [a,b] else '#9aadb5',alpha=.85)
        ax.text(-.03,r0[i],f'{names[i]}  {r0[i]}',ha='right',va='center',fontsize=8)
        ax.text(1.03,r1[i],f'{r1[i]}  {names[i]}',ha='left',va='center',fontsize=8)
    ax.set_xlim(-.65,1.65);ax.set_ylim(26,0);ax.set_xticks([0,1],['V0: equal-weight TOPSIS','V1: minimum tested worst regret'])
    ax.set_yticks([]);ax.set_title('25 real cities: ranking changes\nNumbeo 2025 proxy data; not a complete youth-livability index')
    for spine in ax.spines.values():spine.set_visible(False)
    fig.tight_layout();fig.savefig(OUT/'ranking_changes.png',dpi=180);plt.close(fig)
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    print(result.sort_values('V1_rank').to_string(index=False))

if __name__=='__main__':main()
