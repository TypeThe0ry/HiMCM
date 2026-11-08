#!/usr/bin/env python3
"""Extract five identifiable PISA2022 school populations; raw SAV stays outside Git."""
import argparse, hashlib, json
from pathlib import Path
import pyreadstat
HERE=Path(__file__).resolve().parent
BASE=['CNT','CNTRYID','CNTSCHID','CNTSTUID','REGION','STRATUM','ST001D01T','ISCEDP','AGE','W_FSTUWT']
REPS=[f'W_FSTURWT{i}' for i in range(1,81)]
PVS=[f'PV{i}{s}' for s in ['MATH','READ','SCIE'] for i in range(1,11)]
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('sav',type=Path);a=p.parse_args()
 baseline=HERE.parent/'task4_v86_bogota/manifest.json';source=json.loads(baseline.read_text())
 assert sha(a.sav)==source['member_sha256'],'Original SAV checksum mismatch'
 d,m=pyreadstat.read_sav(a.sav,usecols=BASE+REPS+PVS)
 strata=m.variable_value_labels['STRATUM']
 dubai=sorted(k for k,v in strata.items() if v.startswith('ARE -') and ': Dubai,' in v)
 london=sorted(k for k,v in strata.items() if v.startswith('QUK -') and 'Greater London' in v)
 masks={'Jakarta':d.CNT.eq('IDN')&d.STRATUM.eq('IDN01'),'Bogota':d.REGION.astype(float).eq(17001)&d.CNT.eq('COL'),'Singapore':d.CNT.eq('SGP'),'Dubai':d.CNT.eq('ARE')&d.STRATUM.isin(dubai),'Greater London':d.CNT.eq('GBR')&d.STRATUM.isin(london)}
 # PISA CNT for UK is GBR (strata retain QUK identifier).
 import pandas as pd
 out=pd.concat([d.loc[mask].assign(city=c) for c,mask in masks.items()],ignore_index=True)
 assert {k:v for k,v in out.groupby('city').size().to_dict().items() if k!='Jakarta'}=={'Bogota':1986,'Dubai':7374,'Greater London':777,'Singapore':6606}
 assert len(out[out.city.eq('Jakarta')])>0
 assert not out.duplicated(['CNT','CNTSTUID']).any()
 target=HERE/'pisa2022_city_programme_subset.csv.gz';out.to_csv(target,index=False,compression={'method':'gzip','mtime':0})
 manifest={'source_url':source['source_url'],'source_member_sha256':source['member_sha256'],'source_archive_sha256':source['archive_sha256'],'source_archive_bytes':source['archive_bytes'],'baseline_manifest_sha256':sha(baseline),'derived_file':target.name,'derived_sha256':sha(target),'derived_bytes':target.stat().st_size,'rows':len(out),'selection':{'Jakarta':['IDN01'],'Bogota':"CNT=COL and REGION=17001",'Singapore':'CNT=SGP','Dubai':dubai,'Greater London':london},'stratum_labels':{k:strata[k] for k in dubai+london+['IDN01']},'iscedp_label':m.column_names_to_labels['ISCEDP'],'iscedp_value_labels':{str(k):v for k,v in m.variable_value_labels['ISCEDP'].items() if 200<=k<400},'stage_rule':'300 <= ISCEDP < 400; official current programme classification, not a uniform grade threshold','scope':'School populations in PISA age cohort; Dubai sampling strata (emirate), Greater London region, Singapore city-state, Bogota region, DKI Jakarta capital region. Not all resident high-school ages.','raw_original':'Unmodified official SAV verified against V86 manifest; retained outside Git.'}
 (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({'rows':len(out),'bytes':target.stat().st_size,'dubai':dubai,'london':london}))
if __name__=='__main__':main()
