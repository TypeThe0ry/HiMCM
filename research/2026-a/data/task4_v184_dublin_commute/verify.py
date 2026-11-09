"""Verify archived response identities and the exact Dublin2011JSONstat cell."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    receipts=json.loads((D/'retrievals.json').read_text())
    for row in receipts:
        p=D/row['file'];assert row['http_status']==200
        assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],p.name
    d=json.loads((D/'eurostat_dublin2011_original.json').read_text())
    selection={'freq':'A','indic_ur':'TT1019V','cities':'IE001C','time':'2011'};position=0
    for name,size in zip(d['id'],d['size']):
        position=position*size+d['dimension'][name]['category']['index'][selection[name]]
    assert d['value'][str(position)]==28.8
    assert d['dimension']['cities']['category']['label']['IE001C']=='Dublin (greater city)'
    assert d['dimension']['indic_ur']['category']['label']['TT1019V']=='Average time of journey to work - minutes'
    findings=json.loads((D/'findings.json').read_text())
    assert findings['official_match']['flattened_JSONstat_index']==position==6
    assert findings['official_match']['value_minutes']==28.8 and findings['official_match']['time']==2011
    assert findings['primary_admissions']==0 and findings['methodological_reference']['edition']==2004
    assert set(d['id'])=={'freq','indic_ur','cities','time'}
    print('TwooriginalidentitiesandDublin28.8/2011workjourneygreatercitycellverified;noage/binidentification')
if __name__=='__main__':main()
