"""Offline source identity, dimension decoding and 2011 count checks."""
from pathlib import Path
import hashlib,json,re,subprocess
D=Path(__file__).resolve().parent

def decode(d,stat,year,sex,county):
    offset=0
    for axis,key,size in zip(d['id'],[stat,year,sex,county],d['size']):
        index=d['dimension'][axis]['category']['index']
        pos=index.index(key) if isinstance(index,list) else index[key]
        offset=offset*size+pos
    return d['value'][offset] if isinstance(d['value'],list) else d['value'].get(str(offset))

def main():
    responses=json.loads((D/'retrievals.json').read_text())
    assert len(responses)==4
    for item in responses:
        p=D/item['file'];assert item['http_status']==200
        assert p.stat().st_size==item['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256']
    d=json.loads((D/'cso_F7068_original.json').read_text())
    assert d['id']==['STATISTIC','TLIST(A1)','C02199V02655','C04104V04868'] and d['size']==[9,3,3,31]
    rows=json.loads((D/'cso2011_dublin_four_counties.json').read_text())
    stats=d['dimension']['STATISTIC']['category']['label']
    for row in rows:
        for code,label in stats.items():assert decode(d,code,'2011','-',row['geography_code'])==row['values'][label]
        vals=row['values'];assert sum(vals[label] for label in stats.values() if label.startswith('Journey time '))==vals['Total Persons']
    row=next(r for r in rows if r['geography_label']=='Dublin City')
    expected=[215384,34770,75667,57683,17420,11337,2226,16281,27.1]
    assert list(row['values'].values())==expected
    assert sum(r['values']['Total Persons'] for r in rows)==517800
    text=subprocess.check_output(['pdftotext','-f','43','-l','43','-layout',str(D/'cso2011_profile10_original.pdf'),'-'],text=True)
    assert 'excluding those who work mainly at or from home' in text
    assert 'county and city of usual residence' in ' '.join(text.split())
    line=next(x for x in text.splitlines() if re.match(r'\s*Dublin City\s+215,384',x))
    assert [int(x.replace(',','')) for x in re.findall(r'[\d,]+',line)]==expected[:8]
    geo=subprocess.check_output(['pdftotext','-f','6','-l','6',str(D/'ec_cities2012_definition_original.pdf'),'-'],text=True)
    assert 'IE001K1' in geo and 'Dublin' in geo
    print('PASS:4original identities,dimension-aware2011means/counts,originalTable6andhistoricalgreatercitycode')
if __name__=='__main__':main()
