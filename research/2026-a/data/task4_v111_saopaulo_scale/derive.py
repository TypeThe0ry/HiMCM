"""Nonmutating offline reconstruction from city-level sufficient aggregates."""
from pathlib import Path
import json,hashlib,math
import numpy as np
P=Path(__file__).resolve().parent
def derive():
    for entry in json.loads((P/'manifest.json').read_text()):assert hashlib.sha256((P/entry['file']).read_bytes()).hexdigest()==entry['sha256']
    a=json.loads((P/'aggregate.json').read_text());rep=json.loads((P/'bootstrap_endpoints.json').read_text());rows=[]
    for k,tau in enumerate(a['taus']):
        sums=a['point_weighted_sums'][k*3:k*3+3];lo,hi=[x/sums[2] for x in sums[:2]];e=np.asarray(rep[str(tau)])
        assert e.shape==(2000,2) and np.all(e[:,0]<=e[:,1])
        row={'city':'Sao Paulo','tau_minutes':tau,'utility_lower':float(min(lo,np.quantile(e[:,0],.025))),'utility_upper':float(max(hi,np.quantile(e[:,1],.975))),'point_lower':lo,'point_upper':hi}
        hist=a['weighted_duration_histogram'];den=sum(v[1] for v in hist.values());num=sum(v[1]*math.exp(-float(t)/tau) for t,v in hist.items() if t!='unresolved')
        assert abs(num/den-lo)<1e-12 and abs((num+hist['unresolved'][1])/den-hi)<1e-12
        power=30/tau;L=.4417949654221687;U=.6071350869515446
        jl=L**power if power>=1 else L;ju=U if power>=1 else U**power
        row.update(jensen_lower=jl,jensen_upper=ju,direct_width=row['utility_upper']-row['utility_lower'],jensen_width=ju-jl)
        rows.append(row)
    assert abs(rows[2]['utility_lower']-.4417949654221687)<1e-12
    assert abs(rows[2]['utility_upper']-.6071350869515446)<1e-12
    return {'city':'Sao Paulo','cohort':'V48 resident age14–18 current HS, unchanged membership and unresolved bounds','scenarios':rows,'bootstrap':a['bootstrap'],'scope':'Five discrete tau scenarios, not a continuous-scale certificate','new_observations':0}
if __name__=='__main__':
    result=derive();(P/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['scenarios'],indent=2))
