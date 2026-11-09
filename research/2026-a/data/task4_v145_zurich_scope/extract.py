"""Verify a bounded official metadata search; do not reconstruct suppressed counts."""
from pathlib import Path
import gzip,hashlib,html,json,re
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
    for x in read(HERE/'retrievals.json'):
        data=(HERE/x['file']).read_bytes();raw=gzip.decompress(data) if x['file'].endswith('.gz') else data
        assert len(raw)==x['raw_bytes'] and hashlib.sha256(raw).hexdigest()==x['raw_sha256']
    raw=gzip.decompress((HERE/'victim_scope_original.html.gz').read_bytes()).decode('utf-8')
    text=' '.join(html.unescape(re.sub('<[^>]+>',' ',raw)).split())
    phrases=['Opfer im Alter von 90 Jahren oder älter','Zahlen kleiner als fünf Personen','zweimal im Datensatz erfasst']
    for p in phrases:assert p in text,p
    cat=read(HERE/'city_crime_catalogue_original.json')['result'];assert 'Anzahl polizeilich registrierter Straftaten' in cat['notes'] and 'Tatbestandsgruppe' in cat['notes']
    first=read(HERE/'victim_search_original.json')['result'];rest=read(HERE/'victim_search_remaining3_original.json')['result']
    assert first['count']==rest['count']==8 and len(first['results'])==5 and len(rest['results'])==3
    matches=first['results']+rest['results'];assert len({x['name'] for x in matches})==8
    excerpts={p:text[max(0,text.index(p)-80):text.index(p)+230] for p in phrases}
    result=dict(status='pass',victim_metadata=dict(geography='Kanton Zürich',excludes_age90plus=True,suppresses_counts_below5=True,some_persons_counted_in_both_domestic_and_non_domestic_categories=True),city_crime_catalogue=dict(name=cat['name'],unit='registered criminal acts by offence group, not matched homicide victims',note=cat['notes']),bounded_search=dict(total_hits=8,all_returned_hits_reviewed=True,packages=[dict(name=x['name'],title=x['title']) for x in matches],interpretation='This exact catalogue query did not provide a matching annual city homicide-victim rate; this is not proof that no suitable data exist'),scope_excerpts=excerpts,primary_admissions=0,submitted_rate_denominator_established=False)
    (HERE/'scope_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');(HERE/'observations.json').write_text('[]\n')
    names=['retrievals.json','victim_scope_original.html.gz','city_crime_catalogue_original.json','victim_search_original.json','victim_search_remaining3_original.json','scope_audit.json','observations.json']
    receipt=dict(status='pass',source_sha256={n:sha(HERE/n) for n in names},extractor_sha256=sha(Path(__file__)),primary_admissions=0)
    dest=HERE/('recheck_verification.json' if (HERE/'verification.json').exists() else 'verification.json');dest.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
