"""Offline extraction of WHO V8 urban PM2.5 observations; no imputation.

The published XLSX has CSV records in cells separated at embedded semicolons.
Rejoin those cell fragments before CSV parsing; validate the whole 21-field schema.
WHO explicitly cautions against unqualified cross-city/country ranking.
"""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import csv
import io
import hashlib
import json
import pandas as pd

P=Path(__file__).resolve().parent
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
SOURCE='https://www.who.int/publications/m/item/who-ambient-air-quality-database-(update-jun-2026)'
# Aliases were inspected alongside source country codes and coordinates.
MAP={
'Toronto':('CAN',['Toronto/CAN']),
'Phoenix':('USA',['Phoenix Mesa Scottsdale AZ/USA']),
'New York':('USA',['New York Newark Jersey City NY NJ PA/USA']),
'Mexico City':('MEX',[]),
'Bogota':('COL',['Bogota/COL']),
'Sao Paulo':('BRA',['Sao Paulo/BRA']),
'Santiago':('CHL',['Santiago/CHL']),
'Copenhagen':('DNK',['Copenhagen/DNK','Kobenhavn/DNK']),
'London':('GBR',['London/GBR']),
'Barcelona':('ESP',['Barcelona/ESP']),
'Warsaw':('POL',['Warszawa/POL']),
'Athens':('GRC',['Athens/GRC','Athina/GRC']),
'Nairobi':('KEN',['Nairobi/KEN']),
'Lagos':('NGA',['Lagos/NGA']),
'Cape Town':('ZAF',['Cape Town/ZAF']),
'Dubai':('ARE',['Dubai/ARE']),
'Istanbul':('TUR',['Istanbul/TUR']),
'Mumbai':('IND',['Mumbai/IND']),
'Delhi':('IND',['Delhi/IND']),
'Dhaka':('BGD',['Dhaka/BGD']),
'Tokyo':('JPN',['Tokyo/JPN']),
'Shanghai':('CHN',['Shanghai/CHN']),
'Singapore':('SGP',['Singapore/SGP']),
'Jakarta':('IDN',['DKI Jakarta/IDN','Jakarta/IDN']),
'Melbourne':('AUS',['Melbourne/AUS'])}

def main():
    manifest=json.loads((P/'manifest.json').read_text())
    src=next(r for r in manifest if r['file']=='who2026_v8.xlsx')
    assert hashlib.sha256((P/src['file']).read_bytes()).hexdigest()==src['sha256']
    with ZipFile(P/src['file']) as z:
        ss=[''.join(si.itertext()) for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',NS)]
        records=[]
        for row in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//m:row',NS):
            vals=[]
            for c in row:
                v=c.find('m:v',NS)
                if v is not None:
                    vals.append(ss[int(v.text)] if c.get('t')=='s' else v.text)
            records.append(';'.join(vals))
    parsed=list(csv.reader(io.StringIO('\n'.join(records))))
    assert len(parsed[0])==21 and all(len(r)==21 for r in parsed)
    d=pd.DataFrame(parsed[1:],columns=parsed[0]);d.insert(0,'source_record_number',range(1,len(d)+1))
    for col in ['year','pm25_concentration','pm25_tempcov','number_stations','latitude','longitude']:
        d[col]=pd.to_numeric(d[col],errors='coerce')
    result=[];selected=[]
    for name,(iso,aliases) in MAP.items():
        hit=d[(d.iso3==iso)&d.city.isin(aliases)&d.pm25_concentration.notna()&(d.year<=2025)].sort_values('year')
        row=dict(city=name,indicator='pm25',value=None,year=None,unit='ug/m3',source_url=SOURCE,
                 scope='not_available',status='missing_city_aggregate',source_city=None,
                 temporal_coverage_percent=None,number_stations=None,flags='')
        if len(hit):
            latest=hit[hit.year==hit.year.max()]
            assert len(latest)==1,(name,latest.to_dict('records'))
            s=latest.iloc[0];selected.append(dict(target_city=name,**s.to_dict()))
            flags=['WHO_warns_against_unqualified_cross_city_ranking']
            metro=name in ['New York','Phoenix']
            row.update(value=float(s.pm25_concentration),year=int(s.year),
                scope='metropolitan_area_not_city' if metro else 'WHO_named_urban_settlement_monitor_average',
                status='scope_mismatch_metro' if metro else 'conditional_monitoring_comparability',
                source_city=s.city,temporal_coverage_percent=s.pm25_tempcov,number_stations=int(s.number_stations))
            if metro:flags.append('not_admitted_to_strict_city_model')
            if s.year<2023:flags.append('observation_more_than_3_years_old_at_2026')
            if pd.isna(s.pm25_tempcov):flags.append('temporal_coverage_unknown')
            elif s.pm25_tempcov<75:flags.append('temporal_coverage_below_75pct_sensitivity_flag_not_WHO_rule')
            if s.number_stations==1:flags.append('single_source_station')
            if s.year==2025:flags.append('2025_row_despite_landing_page_says_through2024')
            row['flags']=';'.join(flags)
        else:
            row['flags']='WHO_has_Mexico_City_boroughs_but_no_city_aggregate;do_not_average_without_matching_weights'
        result.append(row)
    pd.DataFrame(result).to_csv(P/'observations.csv',index=False)
    pd.DataFrame(selected).to_csv(P/'source_selected_rows.csv',index=False)
    assert len(result)==25
    print(pd.DataFrame(result)[['city','value','year','status']].to_string(index=False))
    print('Parsed',len(d),'source rows; 24 observed matches, including two metropolitan mismatches; one missing city aggregate.')

if __name__=='__main__':main()
