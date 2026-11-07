"""Direct OD2023 duration revaluation with unchanged paired household draws."""
from pathlib import Path
from collections import defaultdict, Counter
import csv
import gzip
import hashlib
import json
import math
import sys
import tempfile
import numpy as np
from dbfread import DBF

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'task4_v10_saopaulo'
sys.path.insert(0,str(SOURCE))
from extract_commute import person_bound
TAUS=(15,20,30,45,60)


def bounds_for_person(rows):
    l,h,status=person_bound(rows)
    if status!='observed_direct_journey':
        assert (l,h)==(0.,1.)
        return np.tile([0.,1.],len(TAUS)),status,None
    first=min((r for r in rows if r['MOTIVO_D']==4),key=lambda r:r['N_VIAG'])
    duration=float(first['DURACAO'])
    assert abs(l-math.exp(-duration/30))<1e-14 and l==h
    return np.repeat(np.exp(-duration/np.array(TAUS)),2),status,duration


def paired_resample(groups,draws=2000,seed=20261107):
    rng=np.random.default_rng(seed);totals=np.zeros((draws,2*len(TAUS)+1))
    for key in sorted(groups):
        a=np.asarray(groups[key],float);n=len(a)
        # Same order and RNG calls as the archived resample(), across every tau.
        totals+=rng.multinomial(n,np.full(n,1/n),size=draws)@a
    assert np.all(totals[:,-1]>0)
    endpoints=totals[:,:-1]/totals[:,-1,None]
    assert np.all(endpoints[:,::2]<=endpoints[:,1::2]+1e-12)
    assert np.all(np.diff(endpoints[:,::2],axis=1)>=-1e-12)
    assert np.all(np.diff(endpoints[:,1::2],axis=1)>=-1e-12)
    return endpoints


def load():
    manifest=json.loads((SOURCE/'microdata_manifest.json').read_text())
    raw=gzip.decompress((SOURCE/'Banco2023_divulgacao_190225.dbf.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest()==manifest['files'][0]['sha256']
    for entry in manifest['files'][1:]:
        assert hashlib.sha256((SOURCE/Path(entry['path']).name).read_bytes()).hexdigest()==entry['sha256']
    mapping=list(DBF(str(SOURCE/'Municipios_2023.dbf'),encoding='latin1'))
    assert any(r['NumeroMuni']==36 and str(r['CD_IBGE'])=='3550308' for r in mapping)
    households={};people=defaultdict(list);raw_rows=0
    with tempfile.TemporaryDirectory() as td:
        f=Path(td)/'source.dbf';f.write_bytes(raw)
        for r in DBF(str(f),encoding='latin1'):
            raw_rows+=1
            hid=r['ID_DOM'];meta=(r['ZONA'],r['MUNI_DOM'])
            if hid in households:assert households[hid]['meta']==meta
            else:households[hid]={'meta':meta,'sums':np.zeros(2*len(TAUS)+1)}
            if r['ESTUDA']==4:people[r['ID_PESS']].append(r)
    audit=[]
    for pid,rows in people.items():
        for key in ['ID_DOM','MUNI_DOM','ESTUDA','FE_PESS','DATA']:
            assert len({r[key] for r in rows})==1
        assert sum(r['F_PESS']==1 for r in rows)==1
        r=rows[0];w=r['FE_PESS'];assert np.isfinite(w) and w>0
        endpoints,status,duration=bounds_for_person(rows)
        households[r['ID_DOM']]['sums']+=w*np.r_[endpoints,1.]
        if r['MUNI_DOM']==36:
            audit.append(dict(person_id=pid,household_id=r['ID_DOM'],zone=r['ZONA'],weight=w,status=status,duration_minutes=duration))
    groups=defaultdict(list)
    for row in households.values():
        z,m=row['meta']
        if m==36:groups[z].append(row['sums'])
    return groups,audit,raw_rows


def main():
    groups,audit,raw_rows=load()
    total=np.sum([row for group in groups.values() for row in group],axis=0)
    point=total[:-1]/total[-1];draws=paired_resample(groups)
    old=json.loads((SOURCE/'sampling_sensitivity.json').read_text())['scopes']['municipality_sao_paulo']
    old_point=json.loads((SOURCE/'commute_summary.json').read_text())['scopes']['municipality_sao_paulo']
    assert len(audit)==old_point['students']==1778
    assert dict(Counter(r['status'] for r in audit))==old_point['status_counts']
    assert sum(map(len,groups.values()))==old['households']==21917
    assert len(groups)==old['zones']==329
    assert sum(a[-1]>0 for group in groups.values() for a in group)==old['households_with_hs']==1648
    scenarios=[]
    for k,tau in enumerate(TAUS):
        l,h=map(float,point[2*k:2*k+2]);sl=min(l,float(np.quantile(draws[:,2*k],.025)));sh=max(h,float(np.quantile(draws[:,2*k+1],.975)))
        if tau==30:
            np.testing.assert_allclose([l,h,sl,sh],[old['point_lower'],old['point_upper'],old['utility_lower'],old['utility_upper']],atol=1e-12,rtol=0)
        scenarios.append(dict(tau_minutes=tau,utility_lower=l,utility_upper=h,sampling_lower=sl,sampling_upper=sh))
    sources=[]
    for file in ['Banco2023_divulgacao_190225.dbf.gz','Municipios_2023.dbf','microdata_manifest.json','extract_commute.py','sampling_sensitivity.py','sampling_sensitivity.json','commute_summary.json']:
        path=SOURCE/file;sources.append(dict(path='../task4_v10_saopaulo/'+file,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    out=dict(main_admitted=False,new_downloads=0,source_year=2023,scope='municipality Sao Paulo, MUNI_DOM36, current ESTUDA4 upper-secondary, all ages',
        method='Observed first direct school-trip duration revalued at each tau; missing stays [0,1]; paired zone-stratified household bootstrap with fixed weights',
        replicates=2000,seed=20261107,official_design_confidence_interval=False,raw_rows=raw_rows,students=len(audit),weighted_students=float(total[-1]),
        status_counts=dict(Counter(r['status'] for r in audit)),households=21917,households_with_hs=1648,zones=329,
        retained_source_conditions=['Public research mirror; official byte identity not verified','All-age current upper-secondary group, not exact14-18','Exploratory fixed-weight resampling, not official design-based confidence','No missing duration imputed; no changes to population, weights or journey screening'],
        sources=sources,scenarios=scenarios)
    (HERE/'summary.json').write_text(json.dumps(out,indent=2)+'\n')
    with (HERE/'student_duration_audit.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(audit[0]),lineterminator='\n');writer.writeheader();writer.writerows(audit)
    print(json.dumps(scenarios,indent=2))

if __name__=='__main__':main()
