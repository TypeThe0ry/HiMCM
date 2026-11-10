"""Capture documented cantonal transit semantics and municipal WFS discovery."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,urllib.request,urllib.error,urllib.parse
D=Path(__file__).resolve().parent
URLS={
 'stops_metadata.html':'https://geolion.zh.ch/geodatensatz/883',
 'boundary_metadata.html':'https://geolion.zh.ch/geodatensatz/865',
 'boundary_service.html':'https://geolion.zh.ch/geodatenservice/1054',
 'boundary_capabilities.xml':'https://maps.zh.ch/wfs/GemZHWFS?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetCapabilities'}
URLS['boundary_schema.xml']='https://maps.zh.ch/wfs/GemZHWFS?SERVICE=WFS&VERSION=2.0.0&REQUEST=DescribeFeatureType&TYPENAMES=ms%3Agem_grenzen'
_FILTER='<fes:Filter xmlns:fes="http://www.opengis.net/fes/2.0"><fes:PropertyIsEqualTo><fes:ValueReference>bfs</fes:ValueReference><fes:Literal>261</fes:Literal></fes:PropertyIsEqualTo></fes:Filter>'
URLS['zurich_municipal_boundary.geojson']='https://maps.zh.ch/wfs/GemZHWFS?'+urllib.parse.urlencode(dict(SERVICE='WFS',VERSION='2.0.0',REQUEST='GetFeature',TYPENAMES='ms:gem_grenzen',OUTPUTFORMAT='application/json',FILTER=_FILTER))
_NATIONAL='https://data.oev-info.ch/api/explore/v2.1/catalog/datasets/stop-points-today/records?'
URLS['national_zurich_0.json']=_NATIONAL+urllib.parse.urlencode({'where':'fsonumber="261"','limit':100,'offset':0})
for _offset in range(0,579,100):
 URLS[f'national_ordered_{_offset}.json']=_NATIONAL+urllib.parse.urlencode({'where':'fsonumber="261"','order_by':'number','limit':100,'offset':_offset})
def fetch(item):
 name,url=item
 try:
  try:response=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'HiMCM-research/1.0'}),timeout=30)
  except urllib.error.HTTPError as e:response=e
  with response:b=response.read();status=response.status;final=response.url;ctype=response.headers.get('Content-Type')
  (D/name).write_bytes(b)
  return dict(file=name,url=url,final_url=final,status=status,content_type=ctype,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e:return dict(file=None,url=url,error=f'{type(e).__name__}: {e}',retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
def main():
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:r=list(pool.map(fetch,URLS.items()))
 (D/'retrievals.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
if __name__=='__main__':main()
