"""Audit actual Barcelona study-trip means without assigning high-school scope."""
import gzip,hashlib,json,subprocess
from pathlib import Path
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parent

def main():
    for item in json.loads((P/'manifest.json').read_text()):
        raw=(P/item['file']).read_bytes()
        assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
        if item.get('compression')=='gzip':
            decoded=gzip.decompress(raw)
            assert len(decoded)==item['original_bytes'] and hashlib.sha256(decoded).hexdigest()==item['original_sha256']
    raw=gzip.decompress((P/'11_durada_distancia_mitjana.html.gz').read_bytes()).decode('utf-8')
    soup=BeautifulSoup(raw,'html.parser')
    chosen=[t for t in soup.find_all('table') if 'Total Barcelona' in t.get_text() and 'Estudis' in t.get_text()]
    assert len(chosen)==1
    rows=[[c.get_text(' ',strip=True) for c in r.find_all(['td','th'])] for r in chosen[0].find_all('tr')]
    studies=[r for r in rows if r and r[0]=='Estudis']
    assert studies==[['Estudis','28 mins','4,7 kms']]
    questionnaire=subprocess.check_output(['pdftotext','-layout',str(P/'questionnaire2024.pdf'),'-'],text=True)
    assert 'NIVELL D’ESTUDIS FINALITZATS' in questionnaire
    assert '6. Estudiant' in questionnaire and 'TEMPS EN' in questionnaire and 'MINUTS' in questionnaire
    segments=BeautifulSoup(gzip.decompress((P/'12_mobilitat_segons_segments_poblacio.html.gz').read_bytes()).decode(),'html.parser').get_text(' ',strip=True)
    assert '16 – 29 anys' in segments and 'nivell d’estudis acabats' in segments
    result=dict(survey='EMEF 2024',geography='Barcelona resident trip table',reference_population='Residents aged16+; all study purposes/stages',
                published_study_trip_mean_minutes=28,published_mean_distance_km=4.7,
                statistic='Published rounded mean per study trip, not pupil-level exponential utility',
                questionnaire_current_status='Generic Estudiant; no current upper-secondary category established',
                questionnaire_education_variable='S04: completed education, not current enrolment stage',
                published_age_group='16–29',new_admitted_city_observations=0,
                decision='Do not assign the broad study-trip mean to current14–18 high-school students; preserve Barcelona travel bounds')
    (P/'audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
