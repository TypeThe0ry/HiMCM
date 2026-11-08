"""Verify seven dated public swimming venues; no completeness assertion."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def extract():
    source = json.loads((HERE/'provider_pool_sources.json').read_text())
    text = '\n'.join(c.get('text','') for c in source['result']['content'])
    article = text.split('URL: https://www.activesgcircle.gov.sg/read/editors-pick-must-hit-pools-in-singapore', 1)[1]
    assert 'Published on April 23, 2025' in article
    detail = json.loads((HERE/'provider_pool_details.json').read_text())
    details = '\n'.join(c.get('text','') for c in detail['result']['content'])
    venues = [
        ('Bukit Canberra Swimming Complex','bukit-canberra-swimming-complex','756973'),
        ('Sengkang Swimming Complex','sengkang-swimming-complex','544964'),
        ('Our Tampines Hub Swimming Complex','tampines-swimming-complex','528523'),
        ('Heartbeat @ Bedok ActiveSG Pool','heartbeat-bedok-activesg-swimming-complex','469662'),
        ('Jurong West Swimming Complex','jurong-west-swimming-complex','648965'),
        ('Jurong East Swimming Complex','jurong-east-swimming-complex','609517'),
        ('Delta Swimming Complex','delta-swimming-complex','158790')]
    assert len({v[2] for v in venues}) == 7
    for name, slug, postal in venues:
        assert name in article
        assert f'URL: https://www.activesgcircle.gov.sg/facilities/{slug}' in details
        assert postal in details
    population_path = HERE.parent/'task4_v100_singapore/population.json'
    population = json.loads(population_path.read_text())
    rows = population['result']['records']
    matches = [r for r in rows if r['DataSeries']=='Total Population']
    assert len(matches)==1
    denominator = float(matches[0]['2025'])
    assert denominator == 6111175
    density = len(venues)*100000/denominator
    result = dict(city='Singapore',indicator='public_pool_density',year=2025,
        count_lower=7,count_upper=None,population=denominator,
        population_scope='2025 total population of Singapore city-state, residents plus nonresidents',
        density_lower=density,density_unit='physical public swimming venues per100000 total population',
        utility_anchor=1,utility_lower=density/(1+density),utility_upper=1,
        status='verified_partial_public_venue_inventory_lower_bound',
        observation_date='2025-04-23 article; public venue identities crosschecked against current official pages',
        source_url='https://www.activesgcircle.gov.sg/read/editors-pick-must-hit-pools-in-singapore',
        venues=[dict(name=n,url='https://www.activesgcircle.gov.sg/facilities/'+s,postal_code=p) for n,s,p in venues],
        excluded=['SAFRA Yishun membership/guest venue','SAFRA Toa Payoh membership/guest venue','Splash @ Kidz Amaze under12 waterplay'],
        limitations=['Dated selected inventory, not complete city inventory or year-end open census.',
                    'Count one physical venue, not water basins, lanes or users.',
                    'No inference about teenage accessibility, school travel or neighborhood equity.',
                    'Current facility pages corroborate identity; their hours are not substituted for 2025 hours.',
                    'Main registry and existing bounds not edited by this extraction.'],
        sha256={str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'provider_pool_sources.json',HERE/'provider_pool_details.json',population_path]})
    assert 0 < result['utility_lower'] < result['utility_upper'] == 1
    return result

if __name__=='__main__':
    result=extract()
    (HERE/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['count_lower','population','density_lower','utility_lower','utility_upper']},indent=2))
