"""Independent source arithmetic and full before/after interval decision audit."""
from pathlib import Path
import hashlib,json,sys,subprocess,re
import numpy as np,pandas as pd
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from task4_mexico_sampling_revision import mexico_sampling_bounds
from task4_v5_model import CITIES,NAMES,weights
OUT=Path(__file__).resolve().parent

def scores(z,w):
    # Equivalent odds form, independent of production score function.
    a=np.einsum('ij,j->i',z*z,w);b=np.einsum('ij,j->i',(1-z)**2,w)
    return 100/(1+np.sqrt(b/a))

def run():
    raw=ROOT/'data/task4_v113_tokyo/R07_05_2.pdf'
    txt=subprocess.check_output(['/usr/bin/arch','-arm64','/opt/homebrew/bin/pdftotext','-f','1','-l','1','-layout',str(raw),'-']).decode()
    assert re.search(r'27,823\s+10,425\s+631\s+265',txt)
    assert '死' in txt and '53' in txt
    tokyo_n=631
    original_population=json.loads((ROOT/'data/task4_v46_tokyo/summary.json').read_text())['higher_education']['population']
    tokyo_lower=2/(2+tokyo_n/original_population*100000)
    sgdir=ROOT/'data/task4_v113_singapore'
    read=lambda f:BeautifulSoup((sgdir/f).read_text(),'html.parser').get_text(' ',strip=True)
    assert 'validate, confer and award degrees' in read('moe_announcement.html')
    assert 'In August 2024' in read('uas_about.html') and 'degrees conferred by UAS' in read('uas_about.html')
    assert '111 Middle Road' in read('uas_contact.html')
    previous=pd.read_csv(ROOT/'data/task4_v5_resources/sg_verified_university_inventory.csv')
    assert previous.name.nunique()==6 and 'University of the Arts Singapore' not in previous.name.tolist()
    sg_pop=json.loads((ROOT/'data/task4_v5_resources/sg_population_verified_web_extract.json').read_text())['value']*1000
    sg_lower=7*100000/(sg_pop+7*100000)
    for city,new in [('tokyo',tokyo_lower),('singapore',sg_lower)]:
        obs=json.loads((ROOT/f'data/task4_v113_{city}/observation.json').read_text())
        np.testing.assert_allclose(obs['utility_after'],[new,1],rtol=0,atol=1e-15)
        for f in json.loads((ROOT/f'data/task4_v113_{city}/manifest.json').read_text()):
            b=(ROOT/f'data/task4_v113_{city}'/f['file']).read_bytes()
            assert hashlib.sha256(b).hexdigest()==f['sha256'] and len(b)==f['bytes']
    base_lo,base_hi=mexico_sampling_bounds()
    stored=pd.read_csv(ROOT/'results/task4_v113_evidence_revision/utility_bounds.csv',float_precision='round_trip')
    ranks=pd.read_csv(ROOT/'results/task4_v113_evidence_revision/ranks.csv',float_precision='round_trip')
    checks=[]
    for scenario in stored.scenario.unique():
        sub=stored[stored.scenario==scenario]
        assert sub.city.tolist()==[c for c in CITIES for _ in NAMES]
        assert sub.indicator.tolist()==NAMES*len(CITIES)
        lo,hi=base_lo.copy(),base_hi.copy()
        if scenario in ['singapore_only_strict_tokyo','v113_conditional']:lo[CITIES.index('Singapore'),NAMES.index('research_he_density')]=sg_lower
        if scenario in ['tokyo_only_conditional','v113_conditional']:lo[CITIES.index('Tokyo'),NAMES.index('homicide_rate')]=tokyo_lower
        np.testing.assert_allclose(sub.lower.to_numpy().reshape(25,10),lo,atol=1e-15,rtol=0)
        np.testing.assert_array_equal(sub.upper.to_numpy().reshape(25,10),hi)
        assert np.all(lo>=base_lo) and np.all(hi==base_hi)
        for weight_name,w in [('inherited',weights(.1)),('equal',np.ones(10)/10)]:
            low,high=scores(lo,w),scores(hi,w)
            rr=ranks[(ranks.scenario==scenario)&(ranks.weight_reference==weight_name)]
            regret=np.array([max(0,np.delete(high,i).max()-low[i]) for i in range(25)])
            decision=1+np.sum(regret[:,None]>regret[None,:],axis=1)
            possible=[high[i]>=np.delete(low,i).max()-1e-12 for i in range(25)]
            necessary=[low[i]>=np.delete(high,i).max()-1e-12 for i in range(25)]
            for col,arr in [('score_lower',low),('score_upper',high),('max_regret',regret),('decision_rank',decision),('possible_champion',possible),('necessary_champion',necessary)]:
                np.testing.assert_allclose(rr[col],arr,atol=5e-13,rtol=0)
            assert np.all(low>=scores(base_lo,w)-1e-12)
            checks.append(dict(scenario=scenario,weights=weight_name,possible=int(sum(possible)),recommendation=CITIES[int(np.argmin(regret))]))
    result=dict(status='passed',independent_source_arithmetic=True,pdf_death_victims_verified=631,sg_verified_inventory_count=7,
       source_scope='Tokyo recorded-criminal-death superset conditional, strict withdrawal retained; Singapore recognized-institution supply only.',
       endpoint_cells_per_scenario=250,ablation_scenarios=4,weight_scenarios=2,all_unchanged_except_declared_two_lower_endpoints=True,
       checks=checks,source_bound_sha256=hashlib.sha256(np.stack([base_lo,base_hi]).astype('<f8').tobytes()).hexdigest())
    (OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':run()
