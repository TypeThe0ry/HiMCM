"""Rebuild bounds without assigning distributions to unknown data.

AA source is archived rawHTML; TUIK and ISTKA values are transparent
manual transcriptions of official web rendering, not locally archived rawPDFs.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import csv,hashlib,json,re
P=Path(__file__).resolve().parent

def main():
    for r in json.loads((P/'manifest.json').read_text()):
        if 'sha256' in r: assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
    src=json.loads((P/'official_web_verified_values.json').read_text())
    text=BeautifulSoup((P/'homicide_aa2025.html').read_bytes(),'html.parser').get_text(' ',strip=True)
    assert '2025' in text and ('05 Ocak 2026' in text or '05.01.2026' in text)
    m=re.search(r'polisin sorumluluk bölgesinde meydana gelen (\d+) olayda (\d+) kişi hayatını kaybetti',text)
    assert m, 'Missing jurisdiction and death count statement'
    events,deaths=map(int,m.groups());assert (events,deaths)==(291,307)
    assert 'cinayet' in text and 'Geçen yıl İstanbul' in text
    pop=src['population2025']['value'];risk=deaths/pop*1e5
    url='https://www.aa.com.tr/tr/gundem/istanbul-polisi-gecen-yil-faili-mechul-cinayet-birakmadi/3789805'
    rows=[dict(city='Istanbul',indicator='homicide_rate',utility_lower=0.,utility_upper=2/(2+risk),
        raw_lower=risk,raw_upper='inf',year=2025,source_url=url+' | '+src['population2025']['source_url'],
        scope='Full2025 murder deaths in Istanbul police jurisdiction (subset of province); denominator fullprovince year-end resident population; NOT complete province homicide rate; original AA police-source reporting, not official microdata; conditional classification',
        status='conditional_partial_jurisdiction_risk_bound',numerator=deaths,denominator=pop,
        unit='deaths_per100000_residents_lower_bound',anchor=2,extraction='raw_AA_HTML_plus_manual_verified_official_population')]
    he=src['university2022'];assert he['public_universities']+he['foundation_universities']==he['universities_total']==56
    assert he['universities_total']+he['standalone_foundation_vocational_HEIs']==he['all_HEIs']==60
    density=he['all_HEIs']/he['population']*1e5;u=density/(1+density)
    rows.append(dict(city='Istanbul',indicator='research_he_density',utility_lower=u,utility_upper=u,
        raw_lower=density,raw_upper=density,year=2022,source_url=he['source_url'],
        scope='Official complete2022 Istanbul province aggregate13state+43foundation universities+4standalonefoundationvocationalHEIs; includes all three independent highereducationinstitution categories; sameyearprovince population; not2026currentcount; administrative aggregate not individually audited IDs',
        status='conditional_official_complete_he_aggregate',numerator=60,denominator=he['population'],
        unit='independent_HEIs_per100000_residents',anchor=1,extraction='manual_verified_official_pdf_web_render_not_rawPDF'))
    with (P/'bounds.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    with (P/'university_only_diagnostic.csv').open('w') as f:
        writer=csv.writer(f);writer.writerow(['city','year','university_count','standalone_vocational_HEIs','all_independent_HEIs','population','university_only_density','admitted'])
        writer.writerow(['Istanbul',2022,56,4,60,he['population'],56/he['population']*1e5,False])
    assert 0<rows[0]['utility_upper']<1 and 0<u<1
    # Decreasing cost utility: any nonnegative omitted deaths only lowers utility.
    for omitted in [0,1,100,1000,1000000]:
        assert 2/(2+(deaths+omitted)/pop*1e5)<=rows[0]['utility_upper']+1e-14
    print('PASS source hashes, murder events != deaths, subset risk monotonicity,13+43+4=60 independent HEIs;56 university-only diagnostic')
    for r in rows:print(r['indicator'],r['raw_lower'],r['utility_lower'],r['utility_upper'])
if __name__=='__main__':main()
