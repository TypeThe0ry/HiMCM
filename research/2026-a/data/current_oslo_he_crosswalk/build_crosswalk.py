"""Compare Oslo-label ROR organization identities with the archived NOKUT roster."""
from pathlib import Path
from urllib.parse import urlsplit
import csv, json, unicodedata, zipfile

D = Path(__file__).resolve().parent
R = D.parents[1]

def norm(s):
    return ' '.join(''.join(c for c in unicodedata.normalize('NFKD', s).casefold()
                            if not unicodedata.combining(c)).split())

def host(s):
    return (urlsplit(s).hostname or '').lower().removeprefix('www.')

def main():
    with (D/'national_roster.csv').open(newline='') as f: national = list(csv.DictReader(f))
    with zipfile.ZipFile(R/'data/task4_v5_resources/ror_2026_10_06.zip') as z:
        records = json.loads(z.read('v2.14-2026-10-06-ror-data.json'))
    oslo = [r for r in records if r['status']=='active' and 'education' in r['types']
            and any(l['geonames_id']==3143244 and l['geonames_details']['country_code']=='NO'
                    for l in r['locations'])]
    assert len(oslo)==28
    rows=[]
    for r in sorted(oslo,key=lambda r:r['id']):
        hits=[]
        for n in national:
            names=[x['value'] for x in r['names'] if norm(x['value'])==norm(n['display_name'])]
            sites=[x['value'] for x in r['links'] if x['type']=='website' and host(x['value'])==host(n['url'])]
            if names or sites: hits.append((n,names,sites))
        assert len(hits)<=1,(r['id'],hits)
        n,names,sites=hits[0] if hits else ({},[],[])
        rows.append(dict(ror_id=r['id'],ror_display=next(x['value'] for x in r['names'] if 'ror_display' in x['types']),
                         identity_match_basis=';'.join((['exact_ROR_name'] if names else [])+(['same_official_website_host'] if sites else [])),
                         matching_ROR_names=json.dumps(names,ensure_ascii=False),matching_ROR_websites=json.dumps(sites,ensure_ascii=False),
                         nokut_name=n.get('display_name',''),nokut_category=n.get('category_heading',''),
                         nokut_accreditation_scope=n.get('accreditation_scope',''),nokut_url=n.get('url',''),
                         city_inventory_scope_verified=False,
                         decision='national_identity_match_only' if hits else 'no_match_under_declared_identity_rules'))
    with (D/'oslo_crosswalk.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    assert sum(bool(x['nokut_name']) for x in rows)==16
    print('28 Oslo-label ROR records;16 national identity matches;12 unresolved by these rules')

if __name__=='__main__':main()
