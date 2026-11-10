import urllib.request,urllib.error,hashlib,json,datetime,pathlib
p=pathlib.Path(__file__).resolve().parent
urls={'toi_2009_key_report.pdf':'https://www.toi.no/getfile.php/1316282-1299139177/Publikasjoner/T%C3%98I%20rapporter/2011/1130-2011/1130-2011-el.pdf','toi_2009_commute_factsheet.pdf':'https://www.toi.no/getfile.php/1324284-1344948842/mmarkiv/Forskningsprogram/RVU/Faktaark-RVU%202009-Arbeidsreiser.pdf'}
for name,url in urls.items():
 req=urllib.request.Request(url,headers={'User-Agent':'HiMCM-research'})
 try:
  r=urllib.request.urlopen(req,timeout=45);b=r.read();(p/name).write_bytes(b);meta={'url':url,'status':r.status,'headers':dict(r.headers),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 except (urllib.error.URLError,TimeoutError) as e:meta={'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'error':repr(e)}
 (p/(name+'.metadata.json')).write_text(json.dumps(meta,indent=2)+'\n');print(name,meta.get('status'),meta.get('bytes'),meta.get('sha256'),meta.get('error'))
