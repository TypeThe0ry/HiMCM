"""Official city-scoped transport subsets; fixed attachment populations."""
import csv
import hashlib
import json
from pathlib import Path
from pypdf import PdfReader

HERE=Path(__file__).resolve().parent
ATTACHMENT=HERE.parent/'task4_v117_team_intake/city_indicators.csv'

def provider_text(filename):
    r=json.loads((HERE/filename).read_text())
    return '\n'.join(c.get('text','') for c in r['result']['content'])

def extract():
    source={r['city']:r for r in csv.DictReader(ATTACHMENT.open(encoding='utf-8-sig'))}
    pdf=PdfReader(HERE/'vbz_facts2025.pdf')
    text=pdf.pages[5].extract_text()
    assert 'Haltestellen auf Stadtgebiet 446' in text
    assert 'Haltestellen Agglomeration 235' in text
    unit=provider_text('zurich_stop_unit_definition.json')
    assert 'Im Normalfall weisen Haltestellen zwei Haltekanten auf' in unit
    hel=provider_text('helsinki_provider_source.json')
    assert '30 asemasta, joista 19 on Helsingin ja loput 11 Espoon puolella' in hel
    out=[]
    for city,count,year,url,scope in [
        ('Zurich',446,2025,'https://www.stadt-zuerich.ch/content/dam/vbz/de/die-vbz/zahlen-fakten/geschaeftsbericht/Z4690_VBZ_FB-2025_Web.pdf','VBZ2025 facts PDFpage6 gives446 stops on city territory, separately235agglomeration stops. Official2020 council definition distinguishes stops from usually two directional platform edges. Published aggregate stop unit accepted; no independent named-stop deduplication of2025total. Operator inventory, not all-operator completeness.'),
        ('Helsinki',19,2026,'https://kaupunkiliikenne.fi/liikennointi/metrolla/','Current official operator explicitly partitions30metro stations into19Helsinki and11Espoo. Count19unique stations once, not line memberships or platforms. November2026snapshot; not retrospectively labeled2025. Other modes unknown.')]:
        pop=int(source[city]['population']);assert pop=={'Zurich':440935,'Helsinki':694392}[city]
        density=count*100000/pop
        out.append(dict(city=city,indicator='public_transport_density',utility_before=[0,1],utility_after=[density/(50+density),1],raw_count=count,population=pop,population_year=int(source[city]['population_year']),population_source='Unchanged authoritative attachment; no external population recheck',sourceyear=year,density_per_100000_lower=density,utility_anchor=50,lower_bound_only=True,source_locator=url,scope=scope,limitations='Facility supply only, not modal share, service frequency, accessibility, equal neighborhood opportunity or teenage usage. Unknown other operators/modes keep utility upper1.'))
    return out

if __name__=='__main__':
    out=extract();(HERE/'observations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    paths=[p for p in HERE.iterdir() if p.is_file() and p.name!='manifest.json']+[ATTACHMENT]
    manifest={str(p.relative_to(HERE)) if p.parent==HERE else '../task4_v117_team_intake/city_indicators.csv':hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(out,ensure_ascii=False,indent=2))
