"""Independent raw-count and longdouble replay of source-definition scenarios."""
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
D=np.longdouble

def rows(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def score(x,a):
    w=np.full(10,(1-a)/8,dtype=D);w[[6,9]]=a/2
    positive=np.sqrt(np.sum(w*x*x,axis=1));negative=np.sqrt(np.sum(w*(1-x)*(1-x),axis=1))
    return 100*positive/(positive+negative)

def regret(l,h):return np.array([max(D(0),max(np.delete(h,i))-l[i]) for i in range(len(l))])

def main():
    source=P.parent.parent/'data/task4_v100_singapore'
    summary=json.loads((P/'summary.json').read_text())
    assert hashlib.sha256((source/'summary.json').read_bytes()).hexdigest()==summary['source_summary_sha256']
    for m in json.loads((source/'manifest.json').read_text()):
        raw=(source/m['file']).read_bytes();assert len(raw)==m['bytes'] and hashlib.sha256(raw).hexdigest()==m['sha256']
    def records(name):
        d=json.loads((source/name).read_text());assert d['success'] and len(d['result']['records'])==d['result']['total']
        return d['result']['records']
    def get(rs,name):
        hit=[r for r in rs if r['DataSeries']==name];assert len(hit)==1;return hit[0]
    victims=records('victims.json');population=records('population.json')
    n=get(victims,'Total Victims Of Murder');den=get(population,'Total Population')
    utilities={};rates=[]
    for year in [2023,2024,2025]:
        y=str(year);count=D(n[y]);total=D(den[y])
        assert count==D(get(victims,'Male Victims Of Murder')[y])+D(get(victims,'Female Victims Of Murder')[y])
        assert total==D(get(population,'Resident Population')[y])+D(get(population,'Non-Resident Population')[y])
        rate=count/total*100000;utilities['murder_'+y]=2/(2+rate)
        rates.append(dict(year=year,murder_victims=int(count),annual_total_population=int(total),rate_per_100000=float(rate)))
    wdi=json.loads((source/'wdi_homicide.json').read_text())
    assert wdi[0]['pages']==1 and len(wdi[1])==wdi[0]['total']
    current=[r for r in wdi[1] if r['date']=='2023'];assert len(current)==1
    utilities['v96_current']=2/(2+D(str(current[0]['value'])))
    raw=rows(P/'utility_bounds.csv');ranks=rows(P/'ranks.csv');labels=['v96_current','murder_2023','murder_2024','murder_2025']
    assert len(raw)==1000 and len(ranks)==100
    cities=list(dict.fromkeys(r['city'] for r in raw));names=list(dict.fromkeys(r['indicator'] for r in raw))
    assert len(cities)==25 and len(names)==10
    si,sj=cities.index('Singapore'),names.index('homicide_rate');mask=np.ones((25,10),bool);mask[si,sj]=False
    arrays={};rankvectors={};maxerr=D(0)
    for label in labels:
        rr=[r for r in raw if r['scenario']==label]
        assert [(r['city'],r['indicator']) for r in rr]==[(c,n) for c in cities for n in names]
        lo=np.array([D(r['lower']) for r in rr]).reshape(25,10);hi=np.array([D(r['upper']) for r in rr]).reshape(25,10)
        arrays[label]=(lo,hi);assert np.all((0<=lo)&(lo<=hi)&(hi<=1))
        assert abs(lo[si,sj]-utilities[label])<D('1e-15') and hi[si,sj]==lo[si,sj]
        if label=='v96_current':
            assert hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest()==summary['input_bounds_sha256']
        else:
            for x,b in zip((lo,hi),arrays['v96_current']):assert np.array_equal(x[mask],b[mask])
        l,h=score(lo,D('.1')),score(hi,D('.1'));r=regret(l,h);rv=np.array([1+sum(r<x) for x in r]);rankvectors[label]=rv
        rf=[x for x in ranks if x['scenario']==label];assert [x['city'] for x in rf]==cities
        for i,x in enumerate(rf):
            for field,val in [('score_lower',l[i]),('score_upper',h[i]),('max_regret',r[i])]:maxerr=max(maxerr,abs(val-D(x[field])))
            assert int(x['decision_rank'])==rv[i]
            assert int(x['best_rank'])==1+sum(np.delete(l,i)>h[i]+D('1e-12'))
            assert int(x['worst_rank'])==1+sum(np.delete(h,i)>l[i]+D('1e-12'))
            assert (x['possible_champion']=='True')==(h[i]>=max(np.delete(l,i))-D('1e-12'))
            assert (x['necessary_champion']=='True')==(l[i]>=max(np.delete(h,i))-D('1e-12'))
        report=next(x for x in summary['scenarios'] if x['scenario']==label)
        assert report['changed_ranks_vs_current']==sum(rv!=rankvectors['v96_current'])==0
        assert report['choice']==[cities[i] for i in np.flatnonzero(r<=r.min()+D('1e-12'))]==['Singapore']
        assert report['possible_champions']==report['continuous_possible_champions']==cities
        assert all(h[i]>=max(np.delete(l,i)) for i in range(25))
    cert=rows(P/'recommendation_certificate.csv');gaperr=D(0)
    for label in labels:
        l,h=arrays[label];last=D('.05');leaves=[r for r in cert if r['scenario']==label]
        assert leaves
        for r in leaves:
            a,b=D(r['alpha_lower']),D(r['alpha_upper']);assert a==last and a<b<=D('.2');last=b
            ls=np.array([score(l,x) for x in [a,b]]);us=np.array([score(h,x) for x in [a,b]])
            low=regret(ls.max(axis=0)+D('1e-9'),us.min(axis=0)-D('1e-9'))
            high=regret(ls.min(axis=0)-D('1e-9'),us.max(axis=0)+D('1e-9'))
            winner=int(r['winner']);gap=min(np.delete(low,winner))-high[winner]
            assert cities[winner]=='Singapore' and r['certified']=='True' and gap>D('1e-8')
            gaperr=max(gaperr,abs(gap-D(r['regret_gap_lower'])))
        assert last==D('.2')
        report=next(x for x in summary['scenarios'] if x['scenario']==label)
        assert report['continuous_recommendation']=={'unresolved':0,'winners':['Singapore']}
    assert maxerr<D('1e-11') and gaperr<D('1e-11')
    result=dict(method='Raw official JSON counts and annual population; longdouble scoring without model imports',source_hashes_verified=True,baseline_hash_verified=True,
        checked_rank_rows=len(ranks),checked_bounds=len(raw),unchanged_other_cells_each_alternative=249,
        raw_count_scenarios=rates,continuous_possible_city_witnesses=100,continuous_recommendation_leaves=len(cert),
        maximum_score_or_regret_error=float(maxerr),maximum_certificate_gap_error=float(gaperr),all_rankings_unchanged=True,
        scope='Local recorded-murder descriptors are source-definition alternatives, not a validated WDI/ICCS series update, teenage risk or main admission.')
    (P/'independent_check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
