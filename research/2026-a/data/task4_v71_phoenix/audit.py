"""Verify a primary school-transit prioritization study; do not admit modeled minutes."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent

def text_nodes(value):
    if isinstance(value,dict):
        for key,item in value.items():
            if key=='text' and isinstance(item,str): yield item
            elif isinstance(item,(dict,list)):yield from text_nodes(item)
    elif isinstance(value,list):
        for item in value:yield from text_nodes(item)

def audit():
    for row in json.loads((ROOT/'manifest.json').read_text()):
        raw=(ROOT/row['file']).read_bytes()
        assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    meta=json.loads((ROOT/'story_metadata.json').read_text())
    org=json.loads((ROOT/'organization.json').read_text())
    assert meta['owner']=='ValleyMetro' and meta['orgId']==org['id']=='2t1927381mhTgWNC'
    assert org['name']=='Valley Metro' and 'https://www.valleymetro.org/' in org['description']
    paragraphs=list(text_nodes(json.loads((ROOT/'story_data.json').read_text())))
    text='\n'.join(paragraphs)
    for required in ['41 Schools','81,494 Students','10 minutes to/10 minutes from school per day',
                     '20 minutes x 180 days = 60 hours per school year','2019 American Community Survey',
                     'Values extracted from ACS demographics and Valley Metro system data were exported to Excel.',
                     'Number of bus stops per square mile','Miles of service per square mile',
                     'Only public high schools have been evaluated due to the attendance age.']:
        assert required in text,required
    assert meta['created']==1647532098000 and meta['modified']==1651591369000
    print('PASS: Valley Metro provenance, 2022 study, 41-school scope, ACS/supply indicators, illustrative time arithmetic; no student-duration observation admitted')

if __name__=='__main__':audit()
