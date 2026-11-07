import gzip,json,math,hashlib,struct
import numpy as np
from pathlib import Path
from collections import defaultdict,Counter
base=Path('research/2026-a/data/task4_v10_saopaulo');raw=gzip.decompress((base/'Banco2023_divulgacao_190225.dbf.gz').read_bytes());assert hashlib.sha256(raw).hexdigest()=='6cc3d71c8665900c296b6732cf038d3b4142872e82d74f063c8e75e270e9f425'
n=struct.unpack_from('<I',raw,4)[0];head,size=struct.unpack_from('<HH',raw,8);fields=[];offset=1
for at in range(32,head,32):
 if raw[at]==13:break
 name=raw[at:at+11].split(b'\0')[0].decode();typ=chr(raw[at+11]);length=raw[at+16];fields.append((name,typ,offset,length));offset+=length
assert offset==size
wanted={'ID_DOM','ZONA','ID_PESS','IDADE','ESTUDA','MUNI_DOM','FE_PESS','N_VIAG','MOTIVO_D','MOTIVO_O','H_SAIDA','MIN_SAIDA','H_CHEG','MIN_CHEG','DURACAO','DIA_SEM'}
fields=[x for x in fields if x[0] in wanted];assert len(fields)==len(wanted)
people=defaultdict(list)
households={}
for at in range(head,head+n*size,size):
 if raw[at]==42:continue
 r={}
 for name,typ,pos,length in fields:
  v=raw[at+pos:at+pos+length].decode('latin1').strip()
  r[name]=None if not v else float(v) if typ in ['N','F'] else v
 hid=r['ID_DOM'];meta=(r['ZONA'],r['MUNI_DOM'])
 if hid not in households:households[hid]=[meta,np.zeros(6)]
 else:assert households[hid][0]==meta
 if r['ESTUDA']==4:people[r['ID_PESS']].append(r)
results={}
for scope,check in [('all_age',lambda age:True),('age14_18',lambda age:age is not None and 14<=age<=18)]:
 total=lower=upper=0.;count=0;statuses=Counter();ages=Counter()
 for pid,rs in people.items():
  r=rs[0];assert len({x['IDADE'] for x in rs})==1
  if r['MUNI_DOM']!=36 or not check(r['IDADE']):continue
  count+=1;w=r['FE_PESS'];total+=w;ages[r['IDADE']]+=1
  schools=[x for x in rs if x['MOTIVO_D']==4];t=None;status='no_school'
  if schools:
   ordered=all(x['N_VIAG'] is not None and x['N_VIAG']>0 for x in schools)
   first=[x for x in schools if x['N_VIAG']==min(y['N_VIAG'] for y in schools)] if ordered else []
   status='bad_order'
   if len(first)==1:
    x=first[0];status='not_home'
    if x['MOTIVO_O']==8:
     hh,mm,ah,am=(x[k] for k in ['H_SAIDA','MIN_SAIDA','H_CHEG','MIN_CHEG']);status='bad_time'
     if all(y is not None for y in [hh,mm,ah,am]) and 0<=hh<24 and 0<=ah<24 and 0<=mm<60 and 0<=am<60:
      dt=(ah*60+am-hh*60-mm)%1440
      if x['DURACAO'] is not None and x['DURACAO']>0 and x['DURACAO']==dt and x['DIA_SEM'] in [2,3,4,5,6]:t=dt;status='observed'
  off=0 if scope=='all_age' else 3
  lv=0. if t is None else math.exp(-t/30);uv=1. if t is None else lv
  households[r['ID_DOM']][1][off:off+3]+=w*np.array([lv,uv,1.])
  statuses[status]+=1
  if t is None:upper+=w
  else:v=math.exp(-t/30);lower+=w*v;upper+=w*v
 results[scope]={'n':count,'weight':total,'lower':lower/total,'upper':upper/total,'status':dict(statuses),'ages':dict(ages)}
groups=defaultdict(list)
for (zone,muni),vals in households.values():
 if muni==36:groups[zone].append(vals)
rng=np.random.default_rng(20261107);reps=np.zeros((2000,6))
for z in sorted(groups):
 a=np.array(groups[z]);n=len(a);m=rng.multinomial(n,np.ones(n)/n,size=2000);reps+=np.einsum('ij,jk->ik',m,a)
for scope,off in [('all_age',0),('age14_18',3)]:
 eps=reps[:,off:off+2]/reps[:,off+2,None]
 results[scope]['sampling_lower']=min(results[scope]['lower'],float(np.quantile(eps[:,0],.025)))
 results[scope]['sampling_upper']=max(results[scope]['upper'],float(np.quantile(eps[:,1],.975)))
results['bootstrap_households']=sum(map(len,groups.values()));results['bootstrap_zones']=len(groups)
p=Path('research/2026-a/data/task4_v48_saopaulo_source');(p/'independent_age_check.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
