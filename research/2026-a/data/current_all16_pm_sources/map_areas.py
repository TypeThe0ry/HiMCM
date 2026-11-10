"""Historical OECD area-code routing; no current PM observations inferred."""
from pathlib import Path
import csv,hashlib,json,unicodedata,xml.etree.ElementTree as ET
D=Path(__file__).resolve().parent;R=D.parents[1]
COUNTRY=dict(AT='AUT',CH='CHE',FI='FIN',DE='DEU',GB='GBR',NL='NLD',SE='SWE',FR='FRA',ES='ESP',IT='ITA',IE='IRL',NO='NOR',CZ='CZE',PL='POL',SG='SGP',JP='JPN')
ALIASES={'Vienna':['Wien'],'Zurich':['Zürich'],'Helsinki':['Helsinki/Helsingfors'],'Milan':['Milano'],'Prague':['Praha'],'Warsaw':['Warszawa']}
def norm(s):return ' '.join(''.join(c for c in unicodedata.normalize('NFKD',s).casefold() if not unicodedata.combining(c)).split())
def main():
    source=R/'data/current_oslo_pm_model/structure.xml';tree=ET.parse(source)
    flow=next(x for x in tree.findall('.//{*}Dataflow') if x.get('id')=='DSD_FUA_ENV@DF_POLLUTION');assert flow.get('version')=='1.2'
    cl=next(x for x in tree.findall('.//{*}Codelist') if x.get('id')=='CL_FUA_CITY');assert cl.get('version')=='1.1'
    codes={c.get('id'):c for c in cl.findall('./{*}Code')}
    def label(code):return next(n.text for n in codes[code].findall('./{*}Name') if n.get('{http://www.w3.org/XML/1998/namespace}lang')=='en')
    def chain(code):
        result=[code]
        while True:
            ref=codes[result[-1]].find('./{*}Parent/Ref')
            if ref is None:return result
            parent=ref.get('id');assert parent not in result and parent in codes;result.append(parent)
    roots={c:chain(c)[-1] for c in codes}
    raw_source=R/'data/task4_v117_team_intake/city_indicators.csv'
    with raw_source.open(encoding='utf-8-sig',newline='') as f:raw=list(csv.DictReader(f))
    result=[]
    for row in raw:
        country=COUNTRY[row['iso2']];names={norm(x) for x in [row['city']]+ALIASES.get(row['city'],[])}
        hits={c[-1]:c for c in codes if roots[c]==country and c[-1] in ['C','F'] and norm(label(c)) in names}
        if country in codes:
            assert set(hits)=={'C','F'} and codes[hits['C']].find('./{*}Parent/Ref').get('id')==hits['F']
            allowed={norm(row['country'])}
            if row['iso2']=='CZ':allowed|={norm('Czechia'),norm('Czech Republic')}
            assert norm(label(country)) in allowed
        else:assert row['city']=='Singapore' and not hits
        result.append(dict(city=row['city'],original_iso2=row['iso2'],original_country=row['country'],original_PM_value=row['pm25_ugm3'],original_year=row['pm25_ugm3_year'],original_flag=row['pm25_ugm3_flag'],
                           country_root=country,country_root_label=label(country) if country in codes else None,
                           areas=[dict(kind='CITY' if k=='C' else 'FUA',code=c,label=label(c),parent_chain=chain(c)) for k,c in sorted(hits.items())],
                           status='historical_metadata_route_only' if hits else 'country_root_absent_from_archived_codelist',
                           current_v1_5_code_validity_verified=False,numeric_original_PM_verified=False))
    assert len(result)==16 and sum(bool(x['areas']) for x in result)==15
    out=dict(metadata_flow_version='1.2',codelist='CL_FUA_CITY',codelist_version='1.1',normalization='NFKD accent removal/casefold/whitespace; exact declared alias plus country parent hierarchy',aliases=ALIASES,
             cities=result,mapped_city_pairs=15,unmapped_cities=['Singapore'],new_PM_observations=0,
             source_sha256={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,raw_source,Path(__file__)]},
             scope='Historical routing metadata only; no current version/year/value, municipal-boundary equivalence or original extraction lineage verified. Country/city labels are not original-CSV provenance.')
    (D/'area_map.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('Mapped15historical city/FUA pairs;Singapore absent;0newPMobservations')
if __name__=='__main__':main()
