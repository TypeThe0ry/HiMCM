"""Audit observed public-use PISA geography codes; do not infer city IDs.
Usage: /tmp/task4_pisa_venv/bin/python audit.py /path/to/CY08MSP_STU_QQQ.SAV
"""
import argparse, hashlib, json
from pathlib import Path
import pandas as pd
import pyreadstat
HERE=Path(__file__).resolve().parent
FIELDS=['REGION','STRATUM','SUBNATIO']
TARGETS={
'Toronto':('CAN','Ontario province; strata province/language/school size, not Toronto'),
'Phoenix':('USA','US census region and school sector, not Phoenix'),
'New York':('USA','US census region and school sector, not New York'),
'Mexico City':('MEX','National region; strata school stage/sector/size, not CDMX'),
'Sao Paulo':('BRA','Brazil macroregions and school sector, not Sao Paulo municipality'),
'Santiago':('CHL','National region; strata ownership/stage/programme, not Santiago'),
'Copenhagen':('DNK','Minority composition/Faroe strata, not Copenhagen'),
'Barcelona':('ESP','Cataluna autonomous community, not Barcelona'),
'Warsaw':('POL','National region and school programmes, not Warsaw'),
'Athens':('GRC','Urbanicity strata, not Athens'),
'Nairobi':('KEN','No country records in this release'),
'Lagos':('NGA','No country records in this release'),
'Cape Town':('ZAF','No country records in this release'),
'Istanbul':('TUR','School type and opaque letters, no verified Istanbul mapping'),
'Mumbai':('IND','No country records in this release'),
'Delhi':('IND','No country records in this release'),
'Dhaka':('BGD','No country records in this release'),
'Tokyo':('JPN','National region; strata sector/programme, not Tokyo'),
'Shanghai':('CHN','No mainland China records in this release; HKG/MAC are different populations'),
'Melbourne':('AUS','Victoria state and school sector, not Melbourne')}

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()

def main():
 p=argparse.ArgumentParser();p.add_argument('sav',type=Path);a=p.parse_args()
 baseline=HERE.parent/'task4_v86_bogota/manifest.json';manifest=json.loads(baseline.read_text())
 assert sha(a.sav)==manifest['member_sha256'],'Original SAV mismatch'
 d,m=pyreadstat.read_sav(a.sav,usecols=['CNT']+FIELDS)
 assert len(d)==manifest['international_rows']
 evidence={};rows=[]
 for city,(country,reason) in TARGETS.items():
  sub=d.loc[d.CNT.eq(country)]
  if country not in evidence:
   evidence[country]={'rows':len(sub),'fields':{}}
   for field in FIELDS:
    counts=sub[field].value_counts(dropna=False)
    evidence[country]['fields'][field]=[{'code':str(code),'label':m.variable_value_labels[field].get(code,'UNLABELLED_OR_MISSING'),'records':int(n)} for code,n in counts.items()]
  rows.append(dict(city=city,country=country,country_records=len(sub),status='country_absent' if sub.empty else 'city_not_identified_by_audited_fields',reason=reason,main_admitted=False))
 pd.DataFrame(rows).to_csv(HERE/'candidate_audit.csv',index=False)
 (HERE/'observed_code_labels.json').write_text(json.dumps(evidence,indent=2,ensure_ascii=False)+'\n')
 result={'source_url':manifest['source_url'],'source_member_sha256':manifest['member_sha256'],'baseline_manifest_sha256':sha(baseline),'audited_fields':FIELDS,'international_rows':len(d),'candidate_count':len(rows),'country_absent_candidates':sum(r['status']=='country_absent' for r in rows),'city_unidentified_candidates':sum(r['status']!='country_absent' for r in rows),'additional_city_admissions':0,'scope':'Observed REGION/STRATUM/SUBNATIO labels in official student SAV. Does not prove that no restricted or domestic city linkage exists; anonymous school IDs are not guessed as public school codes.'}
 (HERE/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
