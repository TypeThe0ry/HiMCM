"""Verify one additional recognized university; keep inventory upper end unknown."""
from pathlib import Path
import hashlib,json,csv
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    manifest=json.loads((P/'manifest.json').read_text())
    for r in manifest:
        assert sha(P/r['file'])==r['sha256']
        assert (P/r['file']).stat().st_size==r['bytes']
    text=lambda f:BeautifulSoup((P/f).read_text(),'html.parser').get_text(' ',strip=True)
    about=text('uas_about.html');address=text('uas_contact.html');moe=text('moe_announcement.html')
    assert 'degrees conferred by UAS' in about
    assert 'In August 2024' in about
    assert '111 Middle Road' in address and 'Singapore 188969' in address
    assert 'Government–supported private university' in moe
    assert 'validate, confer and award degrees' in moe
    assert 'does not disaggregate the secondary school teacher data' in (P/'singstat_teacher_scope.html').read_text()
    oldpath=ROOT/'data/task4_v5_resources/sg_verified_university_inventory.csv'
    rows=list(csv.DictReader(oldpath.open()));names=[r['name'] for r in rows]
    name='University of the Arts Singapore'
    assert len(set(names))==6 and name not in names
    poppath=ROOT/'data/task4_v5_resources/sg_population_verified_web_extract.json'
    pop=json.loads(poppath.read_text());assert pop['year']==2026 and pop['unit']=='thousands'
    population=pop['value']*1000;assert population==6208500
    old=6*100000/population;new=7*100000/population
    inventory=[dict(name=n,counted_as='existing verified autonomous university',source='../task4_v5_resources/sg_verified_university_inventory.csv') for n in names]
    inventory.append(dict(name=name,counted_as='one additional degree-awarding private university; founding colleges not counted separately',source='moe_announcement.html; uas_about.html; uas_contact.html'))
    with (P/'verified_inventory.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=inventory[0].keys(),lineterminator='\n');w.writeheader();w.writerows(inventory)
    result=dict(city='Singapore',indicator='research_he_density',proposed_admission=True,
        source_snapshot='2026-11-08',commenced_degree_intake=2024,population_year=2026,population=population,
        verified_institution_count_before=6,verified_institution_count_after=7,
        density_before=old,density_after=new,utility_before=[old/(1+old),1.],utility_after=[new/(1+new),1.],
        rule='Previously declared recognized independent HE inventory lower bound; all Singapore city-state territory; institutional central address; no new university-count definition.',
        new_entity=name,central_address='111 Middle Road, National Design Centre, Singapore 188969',
        identity_scope='UAS central degree-awarding institution counted once; LASALLE and NAFA not additionally counted; incomplete inventory remains lower bound.',
        education_quality_claim=False,student_access_claim=False,travel_changed=False,teacher_interval_changed=False,
        unchanged_method='Fixed density anchor 1 institution/100000, inherited population denominator, weights and scoring.',
        inherited_source_hashes={str(oldpath.relative_to(ROOT)):sha(oldpath),str(poppath.relative_to(ROOT)):sha(poppath)},
        official_moe_confirmation='Existing ESD2025 (task4_v38_singapore/esd2025.pdf) describes UAS and AY2024 inaugural degree intake; newly downloaded MOE announcement validates degree-awarding role.',
        limitations=['Partial verified resource inventory, not complete city HE count.','June2026 denominator and November2026 source snapshot retained as such; not labeled2025.','No new highschool travel or stage-specific teacher allocation data obtained.'])
    (P/'observation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()
