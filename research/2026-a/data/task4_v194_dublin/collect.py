"""Collect two bounded official Dublin teacher-evidence routes; no model writes."""
from pathlib import Path
import datetime,hashlib,json,urllib.request
O=Path(__file__).resolve().parent
sources={
 'ncse_catalog_original.html':'https://opendata.ncse.ie/en_GB/dataset/2024-2025-school-allocations',
 'ncse_postprimary_allocations_original.csv':'https://opendata.ncse.ie/dataset/cafceebd-37ea-4350-b1c9-8017d6d751f4/resource/4b4c807b-a452-42ab-89c6-1decdcac7140/download/sna-and-set-hours-allocations-post-primary-schools.csv',
 'workforce_methodology_catalog_original.html':'https://nationaldata.ie/Standards/NationalDataMethodologyHub/DepartmentofEducationandYouth/TeacherWorkforceData/',
 'workforce_methodology_original.pdf':'https://nationaldata.ie/media/NationalDataie/MethodologyDocumentation/Department_of_Education_%26_Youth_Workforce_Data_Methodology.pdf',
}
assert not (O/'retrievals.json').exists(),'Existing raw capture must not be overwritten'
receipts=[]
for name,url in sources.items():
 row=dict(file=name,url=url,attempt_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'HiMCM-source-research/1.0'}),timeout=30) as r:
   data=r.read();row.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(data),sha256=hashlib.sha256(data).hexdigest());(O/name).write_bytes(data)
 except Exception as e:row.update(error=str(e),file=None)
 receipts.append(row)
(O/'retrievals.json').write_text(json.dumps(receipts,indent=2)+'\n')
print(json.dumps(receipts,indent=2))
