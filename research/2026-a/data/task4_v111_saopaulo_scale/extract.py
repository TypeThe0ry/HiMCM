"""V48 cohort and paired household resampling, evaluated at five travel scales."""
from pathlib import Path
from collections import defaultdict,Counter
import csv,gzip,hashlib,importlib.util,json,math,tempfile
import numpy as np
from dbfread import DBF
P=Path(__file__).resolve().parent
V48=P.parent/'task4_v48_saopaulo_age';OLD=P.parent/'task4_v10_saopaulo'
TAUS=[15,20,30,45,60]
spec=importlib.util.spec_from_file_location('v48_saopaulo',V48/'extract.py');v48=importlib.util.module_from_spec(spec);spec.loader.exec_module(v48)
def main():
    layout=v48.layout_rows();source=json.loads((OLD/'microdata_manifest.json').read_text())
    raw=gzip.decompress((OLD/'Banco2023_divulgacao_190225.dbf.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest()==source['files'][0]['sha256']
    mapping=list(DBF(str(OLD/'Municipios_2023.dbf'),encoding='latin1'))
    assert any(r['NumeroMuni']==36 and str(r['CD_IBGE'])=='3550308' for r in mapping)
    households={};people=defaultdict(list);total=0
    with tempfile.TemporaryDirectory() as td:
        f=Path(td)/'source.dbf';f.write_bytes(raw)
        for r in DBF(str(f),encoding='latin1'):
            total+=1;hid=r['ID_DOM'];meta=r['ZONA'],r['MUNI_DOM']
            if hid in households:assert households[hid]['meta']==meta
            else:households[hid]={'meta':meta,'sums':np.zeros(15)}
            if r['ESTUDA']==4:people[r['ID_PESS']].append(r)
    hist=defaultdict(lambda:[0,0.]);status=Counter();n=0;eligible_hh=set()
    for pid,rows in people.items():
        for key in ['ID_DOM','MUNI_DOM','ESTUDA','FE_PESS','DATA','IDADE']:assert len({r[key] for r in rows})==1
        assert sum(r['F_PESS']==1 for r in rows)==1
        r=rows[0];age=r['IDADE'];w=r['FE_PESS']
        assert age is not None and math.isfinite(age) and 0<=age<=120 and int(age)==age
        assert w is not None and math.isfinite(w) and w>0
        if not(14<=age<=18 and r['MUNI_DOM']==36):continue
        lo,hi,st=v48.legacy.person_bound(rows);n+=1;status[st]+=1;eligible_hh.add(r['ID_DOM'])
        if st=='observed_direct_journey':
            t=min((x for x in rows if x['MOTIVO_D']==4),key=lambda x:x['N_VIAG'])['DURACAO'];assert math.exp(-t/30)==lo
            label=str(int(t))
        else:t=None;label='unresolved'
        hist[label][0]+=1;hist[label][1]+=w
        for k,tau in enumerate(TAUS):
            low=math.exp(-t/tau) if t is not None else 0.;high=low if t is not None else 1.
            households[r['ID_DOM']]['sums'][3*k:3*k+3]+=w*np.array([low,high,1.])
    groups=defaultdict(list)
    for r in households.values():
        zone,muni=r['meta']
        if muni==36:groups[zone].append(r['sums'])
    rng=np.random.default_rng(20261107);totals=np.zeros((2000,15))
    for zone in sorted(groups):
        array=np.asarray(groups[zone],float);nh=len(array)
        multiplicities=rng.multinomial(nh,np.full(nh,1/nh),size=2000)
        totals+=multiplicities@array
    point=np.sum([a for g in groups.values() for a in g],axis=0)
    endpoints={};result={}
    for k,tau in enumerate(TAUS):
        j=3*k;assert np.all(totals[:,j+2]>0)
        e=totals[:,j:j+2]/totals[:,j+2,None];identified=point[j:j+2]/point[j+2]
        endpoints[str(tau)]=e.tolist()
        result[str(tau)]={'point_lower':float(identified[0]),'point_upper':float(identified[1]),'sampling_lower':float(min(identified[0],np.quantile(e[:,0],.025))),'sampling_upper':float(max(identified[1],np.quantile(e[:,1],.975)))}
    ref=json.loads((V48/'summary.json').read_text());old=ref['scopes']['age14_18']
    assert n==old['students']==1690 and dict(status)==old['status_counts']
    assert sum(map(len,groups.values()))==21917
    for new,key in [('point_lower','utility_lower'),('point_upper','utility_upper'),('sampling_lower','sampling_lower'),('sampling_upper','sampling_upper')]:assert abs(result['30'][new]-old[key])<1e-12,(new,result['30'][new],old[key])
    aggregate={'raw_sha256':hashlib.sha256(raw).hexdigest(),'source':'V48 existing OD2023 mirror bytes; no new survey records','taus':TAUS,'students':n,'households_with_students':len(eligible_hh),'all_municipal_households':sum(map(len,groups.values())),'zones':len(groups),'raw_rows':total,'status_counts':dict(status),'weighted_duration_histogram':dict(hist),'point_weighted_sums':point.tolist(),'bootstrap':{'seed':20261107,'replicates':2000,'method':'V48 zone-stratified household multinomial, fixed person weights, paired across scales','interval':'min(point lower,2.5% replicate lower); max(point upper,97.5% replicate upper)','official_design_CI':False},'results':result}
    (P/'aggregate.json').write_text(json.dumps(aggregate,indent=2)+'\n')
    (P/'bootstrap_endpoints.json').write_text(json.dumps(endpoints,separators=(',',':'))+'\n')
    manifest=[]
    for file in [P/'aggregate.json',P/'bootstrap_endpoints.json',V48/'extract.py',V48/'summary.json',OLD/'extract_commute.py',OLD/'Layout_BD_OD2023_190225.xlsx',OLD/'Municipios_2023.dbf']:
        manifest.append({'file':str(file.relative_to(P)) if file.is_relative_to(P) else str(Path('..')/file.parent.name/file.name),'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
    (P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
