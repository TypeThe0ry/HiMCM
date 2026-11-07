"""Read-only intake audit of team data; no automatic scope or year substitution."""
from pathlib import Path
import csv,json,hashlib,math
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parent;D=P.parent
M=D/'city_matrix_25_audit';C=D/'homicide_2023_secondary_ratio_updated'

def table(path):
    s=BeautifulSoup(path.read_text(),'html.parser');t=s.find('table',id='t2');assert t is not None
    rows=[[c.get_text(' ',strip=True) for c in r.find_all(['th','td'])] for r in t.find_all('tr')]
    return {r[1]:dict(zip(rows[0],r)) for r in rows[1:] if len(r)==len(rows[0])},s.title.get_text()

def write(name,rows):
    with (P/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)

def main():
    raw=list(csv.reader((M/'original_sheet_1_table_1.csv').open(encoding='utf-8-sig')))
    start=next(i for i,r in enumerate(raw) if r[0]=='city');header=raw[start]
    cityrows=[r for r in raw[start+1:] if r[0]];assert len(cityrows)==25
    current=list(csv.DictReader((D/'city_candidates_team_25.csv').open(encoding='utf-8-sig')))
    currentset={r['city'] for r in current}
    cli,title=table(M/'sources/cost-of-living_2026.html');assert '2026' in title and 'Mid' not in title
    pir,title=table(M/'sources/property-investment_2026.html');assert '2026' in title and 'Mid' not in title
    names=['homicide_rate','pm25','cost_living_index','price_income_ratio','upper_secondary_ptr','research_he_density','public_transport_density','travel','fixed_broadband_mbps','public_pool_density']
    out=[]
    for row in cityrows:
        city=row[0]
        for j,name in enumerate(names):
            value=row[1+2*j];source=row[2+2*j];found=None;canonical='';match=''
            in_set=city in currentset
            if not value:decision='missing';why='Blank remains missing; not zero and no new evidence.'
            elif j in (2,3):
                tab,field=(cli,'Cost of Living Index') if j==2 else (pir,'Price To Income Ratio')
                found=[(k,v) for k,v in tab.items() if k.startswith(city+',')]
                if len(found)==1:
                    match=found[0][0];canonical=float(found[0][1][field])
                    if math.isclose(float(value),canonical,abs_tol=1e-8):
                        decision='separate_2026_scenario_only';why='Matches archived2026 edition; V5/V7 use2025, so do not intersect or replace individual cells across years.'
                    else:
                        decision='reject_claimed_2026_value';why='Original value differs from archived2026 same-city same-indicator table; version must be corrected before any temporal scenario.'
                else:decision='unresolved_city_match';why='No unique exact city prefix in archived2026 source; do not guess geography.'
            elif j==7:decision='reject_construct';why='t10 is car time for10km, not actual upper-secondary student travel time.'
            elif j==4 and city=='Tokyo':decision='reject_wrong_school_stage';why='15.22 is junior-high313944/20622; official upper-secondary302411/19325=15.6486934 already exists inV5.'
            elif j==4:decision='reject_unverified_upper_secondary_scope';why='Spot-check PTR lacks verified matched upper-secondary numerator/denominator; secondary-school aggregate is not pre-U/high-school.'
            elif j==0 and city=='Tokyo':decision='reject_homicide_definition';why='Police murder recognition/case count may include attempts; no verified fatal-victim numerator. Not admitted as homicide deaths.'
            elif j==0 and city=='Singapore':decision='retain_existing_verified_source';why='Spot-check0.068 has no archived matched denominator; existingV5WDI2023 .0690954942050905 is verified. Do not silently overwrite.'
            else:decision='unverified_spot_check';why='doc: source citation is not independently archived verification of count, scope, period and denominator.'
            if value and not in_set:why+=' City is outside current fixed25; do not change candidate set automatically.'
            out.append(dict(city=city,indicator=name,original_value=value,original_source=source,in_current_candidates=in_set,main_admit=False,
                            decision=decision,reason=why,archived_2026_value=canonical,source_city=match))
    write('matrix_cell_audit.csv',out)
    # Every country row: separate geographic acceptance of homicide from schooling scope.
    countries=list(csv.DictReader((C/'countries_2023_all.csv').open(encoding='utf-8-sig')));assert len(countries)==217
    countryaudit=[]
    old=list(csv.DictReader((D/'task4_v5_core/observations.csv').open()))
    oldsg=next(float(r['value']) for r in old if r['city']=='Singapore' and r['indicator']=='homicide_rate')
    for r in countries:
        for indicator,field in [('homicide_rate','homicide_rate_per_100k'),('upper_secondary_ptr','secondary_pupil_teacher_ratio_derived')]:
            val=r[field];sg=r['wb_country_code']=='SGP'
            if not val:decision='missing';reason='Country-year value missing; preserve missing.'
            elif indicator=='upper_secondary_ptr':decision='reject_school_stage_and_geography';reason='ISCED2+3 combined secondary; not upper-secondary-only. National geography also does not identify city values (except city-stateSG, still wrong school stage).'
            elif sg:
                assert math.isclose(float(val),oldsg,rel_tol=1e-12)
                decision='verified_duplicate';reason='Singapore city-state matches city boundary; same2023WDI value already inV5, so adds no evidence.'
            else:decision='reject_country_to_city';reason='National homicide cannot substitute for city homicide; no city-level allocation evidence.'
            countryaudit.append(dict(country=r['country_name'],country_code=r['wb_country_code'],indicator=indicator,value=val,
                year=r['homicide_year'] if indicator=='homicide_rate' else r['education_year'],main_admit=False,decision=decision,reason=reason))
    write('country_cell_audit.csv',countryaudit)
    # Useful existing originals: extract a CONSISTENT full2026 price scenario, never main.
    sourcecities={r['city']:r['source_city'] for r in csv.DictReader((D/'task4_real/city_indicators_2025.csv').open())}
    scenario=[]
    for city in sorted(currentset):
        k=sourcecities[city]
        for indicator,tab,field,slug in [('cost_living_index',cli,'Cost of Living Index','cost-of-living'),('price_income_ratio',pir,'Price To Income Ratio','property-investment')]:
            val=tab.get(k,{}).get(field,'')
            scenario.append(dict(city=city,indicator=indicator,value=val,year=2026,source_city=k,
                source_url=f'https://www.numbeo.com/{slug}/rankings.jsp?title=2026',
                status='separate_year_scenario_only' if val else 'missing_same_city_in_2026_archive',main_admit=False))
    write('price_2026_separate_scenario.csv',scenario)
    inputs=[M/'original_sheet_1_table_1.csv',M/'provenance.json',M/'sources/cost-of-living_2026.html',M/'sources/property-investment_2026.html',M/'evidence_education_environment/tokyo_2024_table17_1.csv',C/'countries_2023_all.csv',C/'method_notes.csv',C/'download_manifest.json',C/'raw/singapore_official_ptr.json']
    manifests=[]
    for f in inputs:manifests.append(dict(path=str(f.relative_to(D)),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size))
    # Verify all original raw hashes, without changing any source files.
    rawmanifest=json.loads((C/'download_manifest.json').read_text())
    for r in rawmanifest['sources']:
        f=C/r['file'];assert hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256']
    (P/'input_snapshot.json').write_text(json.dumps(manifests,indent=2)+'\n')
    summary=dict(matrix_cities=25,matrix_cells=len(out),matrix_nonmissing=sum(bool(r['original_value']) for r in out),
        same_candidate_cities=sorted(currentset & {r[0] for r in cityrows}),outside_candidates=sorted({r[0] for r in cityrows}-currentset),
        matrix_claimed_price_version_mismatches=sum(r['decision']=='reject_claimed_2026_value' for r in out),
        country_rows=len(countries),country_cell_audits=len(countryaudit),new_main_admissions=0,
        real_student_travel_observations=0,verified_duplicate_singapore_homicide=oldsg,
        separate_price_scenario_valid_cells=sum(bool(r['value']) for r in scenario),raw_hashes_verified=len(rawmanifest['sources']))
    (P/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
