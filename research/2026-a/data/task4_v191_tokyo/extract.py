"""Extract a named Oedo station subset; preserve the supplied Tokyo population."""
from pathlib import Path
import csv,hashlib,io,json,math,re
D=Path(__file__).resolve().parent;R=D.parents[1]
SOURCE=R/'data/task4_v117_team_intake/city_indicators.csv'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    receipts=json.loads((D/'retrievals.json').read_text())
    for rec in receipts:
        if rec['file']:
            p=D/rec['file'];assert p.stat().st_size==rec['bytes'] and sha(p)==rec['sha256']
    original=sha(SOURCE);assert original=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
    team=list(csv.DictReader(io.StringIO(SOURCE.read_text(encoding='utf-8-sig'))));tokyo=next(x for x in team if x['city']=='Tokyo')
    assert tokyo['population']=='9983365' and tokyo['population_year']=='2026' and not tokyo['transit_share_pct']
    rows=list(csv.DictReader(io.StringIO((D/'stationlist_original.csv').read_bytes().decode('cp932'))))
    assert len(rows)==38 and set(rows[0])=={'定','自','駅名','住所','緯度','経度','座標系','電話番号/Tel',''}
    wards={'千代田区','中央区','港区','新宿区','文京区','台東区','墨田区','江東区','品川区','目黒区','大田区','世田谷区','渋谷区','中野区','杉並区','豊島区','北区','荒川区','板橋区','練馬区','足立区','葛飾区','江戸川区'}
    selected=[]
    for k,row in enumerate(rows,2):
        ward=re.match(r'^(.+?区)',row['住所'])[1];assert ward in wards and row['座標系']=='JGD2011'
        assert row['自']=='●' and row['定'] in {'','○'}
        selected.append(dict(source_data_row=k,station_name=row['駅名'],address=row['住所'],ward=ward,latitude=row['緯度'],longitude=row['経度'],coordinate_reference=row['座標系']))
    assert len({x['station_name'] for x in selected})==len({x['address'] for x in selected})==len({(x['latitude'],x['longitude']) for x in selected})==38
    assert sum(x['station_name']=='都庁前' for x in selected)==1
    def distance(a,b):
        p,q=math.radians(float(a['latitude'])),math.radians(float(b['latitude']));dp=q-p;dl=math.radians(float(b['longitude'])-float(a['longitude']))
        return 2*6371000*math.asin(math.sqrt(math.sin(dp/2)**2+math.cos(p)*math.cos(q)*math.sin(dl/2)**2))
    nearest=min((distance(a,b),a['station_name'],b['station_name']) for i,a in enumerate(selected) for b in selected[i+1:])
    assert nearest[0]>200 # separation diagnostic only; no clustering threshold changes station identities.
    metadata=(D/'api_catalog_original.html').read_text()
    for value in ['subway_branch_o_stationlist.csv','東京都交通局','2026/09/01 11:44:00','2026/09/04 15:00:00','クリエイティブ・コモンズ 表示（CC BY）','自動定期券発売機','定期券発売所']:assert value in metadata,value
    with (D/'named_stations.csv').open('w') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(selected[0]),lineterminator='\n');writer.writeheader();writer.writerows(selected)
    n=len(selected);population=int(tokyo['population']);density=n*100000/population;lower=density/(50+density)
    obs=dict(city='Tokyo',indicator='public_transport_density',raw_count=n,population=population,population_year=2026,population_basis='Retained user cityproper population; existing V117/V124 scope is23specialwards',density_per100000=density,utility_lower=lower,utility_upper=1,source_scope='Named Oedo-line station directory subset, all38addresses inTokyo23specialwards; distinct station names/addresses, not platforms or ticket-machine counts; other rail lines/operators/modes uncounted',source_file='stationlist_original.csv',inventory_reference_year=None,inventory_reference_date='unknown; catalogue metadata is not an inventory observation date',catalogue_created='2026/09/01 11:44:00',catalogue_last_updated='2026/09/04 15:00:00',catalogue_timezone='not stated on page',access_date_utc='2026-11-09',status='candidate_conditional_catalogue_lower_bound_not_primary_admission',no_current_opening_status_claim=True)
    (D/'observations.json').write_text(json.dumps([obs],ensure_ascii=False,indent=2)+'\n')
    report=dict(version='V191 Tokyo candidate',provider='Tokyo Metropolitan Government Bureau of Transportation',raw_csv_encoding='cp932',count=n,named_stations_unique=True,addresses_unique=True,coordinate_pairs_unique=True,Tochomae_occurrences=1,observed_ward_count=len({x['ward'] for x in selected}),observed_wards=sorted({x['ward'] for x in selected}),minimum_station_separation_m=nearest[0],nearest_pair=list(nearest[1:]),utility_lower=lower,utility_upper=1,inventory_reference_year=None,catalogue_date_not_observation_date=True,primary_admissions=0,original_CSV_sha256=original,source_hashes={rec['file']:rec['sha256'] for rec in receipts if rec['file']},not_used=[dict(url=x['url'],status=x['http_status'],reason=x.get('payload_classification',x.get('error'))) for x in receipts if x.get('payload_classification') or not x['file']],license_catalogue_literal='クリエイティブ・コモンズ 表示（CC BY）',limitations='Static directory infrastructure subset; no full inventory, current operational state, actual student access, travel time, population replacement or observation-year inference. Map/2026 media-guide source requests returned access shells and supply no counts.')
    (D/'findings.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');assert sha(SOURCE)==original
    print(json.dumps(dict(count=n,wards=report['observed_ward_count'],density=density,utility_lower=lower,minimum_separation_m=nearest[0]),indent=2))
if __name__=='__main__':main()
