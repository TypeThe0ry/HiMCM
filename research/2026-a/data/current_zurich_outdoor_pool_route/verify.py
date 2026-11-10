"""Verify archived venue descriptions and address distinction; no model changes."""
import hashlib, json
from pathlib import Path
from bs4 import BeautifulSoup

p = Path(__file__).resolve().parent
receipts = json.loads((p / 'retrievals.json').read_text())
for r in receipts:
    assert r['status'] == 200 and r['content_type'].startswith('text/html')
    assert hashlib.sha256((p / r['file']).read_bytes()).hexdigest() == r['sha256']
old = json.loads((p.parent / 'task4_v196_zurichpool/school_candidates.json').read_text())
oldrows = old['existing_seven_addresses'] + [r for r in old['rows'] if r['slug'] != 'kuegeliloo']
assert len(oldrows) == 12
oldaddr = {(r['street'].casefold(), r['postal_code'], r['city']) for r in oldrows}
assert len(oldaddr) == 12
spec = {
 'allenmoos': ('Ringstrasse 79', '8057', 'Schwimmbecken (50 x 20 Meter)'),
 'heuried': ('Wasserschöpfi 71 (Freibad)', '8055', 'Schwimmbecken (50 x 20 Meter)'),
 'letzigraben': ('Edelweissstrasse 5', '8048', 'Schwimmbecken (50 x 25 Meter)'),
 'seebach': ('Glatttalstrasse 43', '8052', 'Schwimmbecken mit sieben Bahnen (50 x 20 Meter)'),
 'auhof': ('Luegislandstrasse 160', '8051', 'Schwimmbecken (50 x 13 Meter)'),
}
directory = BeautifulSoup((p / 'directory_original.html').read_bytes(), 'html.parser')
out=[]
for slug,(street,postcode,pool) in spec.items():
    soup = BeautifulSoup((p / (slug+'_original.html')).read_bytes(), 'html.parser')
    c = soup.select_one('stzh-contact#kontakt')
    assert c and json.loads(c['street']) == [street] and c['postal-code'] == postcode and c['location'] == 'Zürich'
    assert pool in soup.get_text(' ', strip=True)
    assert any((a.get('href') or '').endswith('/sommerbaeder/'+slug+'.html') for a in directory.find_all(href=True))
    assert (street.casefold(),postcode,'Zürich') not in oldaddr
    tables=soup.select('stzh-datatable')
    status=json.loads(soup.select_one('stzh-datatable#baederinfos')['rows'])
    hours=json.loads(tables[1]['rows'])
    text=soup.get_text(' ',strip=True)
    assert 'Öffnungszeiten 2026' in text and 'Eintrittspreise und Abonnemente' in text
    if slug == 'auhof': assert 'Wiedereröffnung ist auf die Badesaison 2029 vorgesehen' in text
    out.append({'name':c['heading'], 'street':street,'postal_code':postcode,'municipality':'Zürich','pool_description':pool,'source':slug+'_original.html','status_rows':status,'hours_2026_rows':hours,'classification':'hold_renovation' if slug=='auhof' else 'candidate_not_admitted'})
assert len({(r['street'],r['postal_code']) for r in out}) == len(out)
z=BeautifulSoup((p / 'zwischen-den-hoelzern_original.html').read_bytes(),'html.parser').select_one('stzh-contact#kontakt')
assert z['location']=='Oberengstringen'
result={'four_candidate_venues_not_admitted':out[:4], 'held_renovation':out[4], 'excluded_municipal_address':{'name':z['heading'],'street':json.loads(z['street'])[0],'postal_code':z['postal-code'],'municipality':z['location']},'old_twelve_distinct_addresses_crosschecked':True,'population_retained_as_given':440935,'population_year_as_given':2025,'primary_admissions':0}
(p/'extraction.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PASS: hashes, directory links, venue descriptions, 12 old addresses, 5 new addresses and exclusion; primary admissions 0')
