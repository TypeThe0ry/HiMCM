"""Exploratory zone-stratified household resampling, preserving unknown outcomes.
Not official replicate weights and not a design-valid confidence interval.
"""
from pathlib import Path
from collections import defaultdict
import gzip, hashlib, json, tempfile
import numpy as np
from dbfread import DBF
from extract_commute import P, person_bound


def resample(groups, draws=2000, seed=20261107):
    rng=np.random.default_rng(seed); totals=np.zeros((draws,3))
    for key in sorted(groups):
        a=np.asarray(groups[key],float);n=len(a)
        totals += rng.multinomial(n,np.full(n,1/n),size=draws) @ a
    assert np.all(totals[:,2]>0)
    endpoints=totals[:,:2]/totals[:,2,None]
    assert np.all(endpoints[:,0]<=endpoints[:,1]+1e-12)
    return endpoints


def main():
    raw=gzip.decompress((P/'Banco2023_divulgacao_190225.dbf.gz').read_bytes())
    manifest=json.loads((P/'microdata_manifest.json').read_text())
    assert hashlib.sha256(raw).hexdigest()==manifest['files'][0]['sha256']
    households={};people=defaultdict(list)
    with tempfile.TemporaryDirectory() as td:
        f=Path(td)/'data.dbf';f.write_bytes(raw)
        for r in DBF(str(f),encoding='latin1'):
            hid=r['ID_DOM'];meta=(r['ZONA'],r['MUNI_DOM'])
            if hid in households:assert households[hid]['meta']==meta
            else:households[hid]={'meta':meta,'sums':np.zeros(3)}
            if r['ESTUDA']==4:people[r['ID_PESS']].append(r)
    weights=defaultdict(list)
    for rows in people.values():
        assert len({r['ID_DOM'] for r in rows})==1
        assert len({r['FE_PESS'] for r in rows})==1
        r=rows[0];w=r['FE_PESS'];assert np.isfinite(w) and w>0
        l,h,_=person_bound(rows);households[r['ID_DOM']]['sums']+=w*np.array([l,h,1])
        weights[r['MUNI_DOM']].append(w)
    result={'method':'exploratory zone-stratified household bootstrap with fixed final person weights','replicates':2000,'seed':20261107,'main_admitted':False,'design_valid_confidence_interval':False,'scopes':{}}
    for scope,mun in [('metro',None),('municipality_sao_paulo',36)]:
        groups=defaultdict(list)
        for row in households.values():
            z,m=row['meta']
            if mun is None or m==mun:groups[z].append(row['sums'])
        point=np.sum([a for g in groups.values() for a in g],axis=0);point=point[:2]/point[2]
        expected=json.loads((P/'commute_summary.json').read_text())['scopes'][scope]
        assert np.allclose(point,[expected['utility_lower'],expected['utility_upper']],rtol=0,atol=1e-12)
        endpoints=resample(groups)
        # Outer envelope includes the original sample identification interval.
        lo=min(point[0],float(np.quantile(endpoints[:,0],.025)))
        hi=max(point[1],float(np.quantile(endpoints[:,1],.975)))
        w=np.array([v for m,vs in weights.items() if mun is None or m==mun for v in vs])
        result['scopes'][scope]=dict(utility_lower=lo,utility_upper=hi,point_lower=point[0],point_upper=point[1],households=sum(map(len,groups.values())),zones=len(groups),singleton_zones=sum(len(g)==1 for g in groups.values()),households_with_hs=int(sum(a[2]>0 for g in groups.values() for a in g)),kish_weight_effective_n=float(w.sum()**2/(w*w).sum()),endpoint_standard_deviation=endpoints.std(axis=0,ddof=1).tolist())
    (P/'sampling_sensitivity.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
