import datetime,hashlib,json,pathlib,urllib.request,urllib.error
p=pathlib.Path(__file__).resolve().parent
url='https://api.entur.io/journey-planner/v3/graphql'
ids=['5677','6197','6302','6313']
fields='id name estimatedCalls(timeRange: 72100, numberOfDepartures: 10) { realtime aimedDepartureTime expectedDepartureTime forBoarding forAlighting destinationDisplay { frontText } quay { id } serviceJourney { journeyPattern { line { id name transportMode } } } }'
query='{ '+' '.join('s'+i+': stopPlace(id: "NSR:StopPlace:'+i+'") { '+fields+' }' for i in ids)+' }'
body=json.dumps({'query':query},separators=(',',':')).encode(); headers={'Content-Type':'application/json','ET-Client-Name':'himcm-research'}
(p/'request.json').write_bytes(body);req=urllib.request.Request(url,data=body,headers=headers,method='POST')
try:r=urllib.request.urlopen(req,timeout=30)
except urllib.error.HTTPError as e:r=e
except Exception as e:
 (p/'failure.json').write_text(json.dumps({'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exception':repr(e)},indent=2)+'\n');raise
b=r.read();(p/'response.json').write_bytes(b);(p/'metadata.json').write_text(json.dumps({'url':url,'method':'POST','request_headers':headers,'request_sha256':hashlib.sha256(body).hexdigest(),'response_status':r.status,'response_headers':dict(r.headers),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'response_bytes':len(b),'response_sha256':hashlib.sha256(b).hexdigest()},indent=2)+'\n');print(r.status,b.decode()[:12000])
