"""Acquire official NCES directory bridges and ADE responses without name-only matches."""
import csv,json,subprocess,hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
P=Path(__file__).resolve().parent;D=P.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def get(job):
 name,url=job;f=P/name;f.parent.mkdir(parents=True,exist_ok=True)
 if not f.exists():
  r=subprocess.run(['curl','-fsSL','--max-time','35',url],capture_output=True)
  if r.returncode:return dict(file=name,url=url,error=r.stderr.decode()[:200])
  f.write_bytes(r.stdout)
 return dict(file=name,url=url,bytes=f.stat().st_size,sha256=sha(f))
def main():
 roster=list(csv.DictReader((D/'task4_v93_phoenix/roster_coverage.csv').open()))
 missing=[r for r in roster if r['grade11_category']=='positive' and r['identity_verified']=='False']
 jobs=[(f'nces/{r["nces_id"]}.html',f'https://nces.ed.gov/ccd/schoolsearch/school_detail.asp?ID={r["nces_id"]}') for r in missing]
 ids=[87322,92189,93018,1000083,80385,79929,85749,80006,85750,90907,6395,6250,92248,1002102,1002105]
 jobs += [(f'responses/{i}_entity.json',f'https://azreportcards.azed.gov/api/Entity/GetEntity?id={i}&fiscalYear=2025') for i in ids]
 jobs += [(f'responses/{i}_assessment.json',f'https://azreportcards.azed.gov/api/DataApi/Assessment%20DetailsFAY?reportSection=Assessment+DetailsFAY&fiscalYear=2025&educationOrganizationId={i}') for i in ids if i not in [79929,85749]]
 jobs += [('ccd_sch_029_2425_w_1a_073025.zip','https://nces.ed.gov/ccd/Data/zip/ccd_sch_029_2425_w_1a_073025.zip'),('ccd_downloads_2024_25.json','https://nces.ed.gov/ccd/datatables/api/File/2/7/39/0/0/0'),('ccd_files.html','https://nces.ed.gov/ccd/files.asp'),('ccd_file_controller.js','https://nces.ed.gov/ccd/datatables/Scripts/app/file-controller.js')]
 with ThreadPoolExecutor(6) as pool:manifest=list(pool.map(get,jobs))
 (P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps([m for m in manifest if 'error' in m],indent=2));print('downloaded',sum('sha256'in m for m in manifest))
if __name__=='__main__':main()
