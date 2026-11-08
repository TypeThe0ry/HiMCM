from pathlib import Path
import json,hashlib,re
from pypdf import PdfReader
P=Path(__file__).resolve().parent

def extract():
    item=json.loads((P/'manifest.json').read_text())[0]
    assert hashlib.sha256((P/item['file']).read_bytes()).hexdigest()==item['sha256']
    pdf=PdfReader(P/item['file'])
    table=' '.join(pdf.pages[73].extract_text().split())
    method=' '.join(pdf.pages[14].extract_text().split())
    assert '10.3' in table and 'one direction' in table
    assert 'Mother\'s/caregiver\'s education' in table
    row=re.search(r'15-17\s+(\d+,\d+)\s+100,0\s+(\d+,\d+)\s+(\d+,\d+)',table)
    assert row
    accompaniment,le30,gt30=[float(v.replace(',','.')) for v in row.groups()]
    assert le30+gt30==100 and le30==80.7 and gt30==19.3
    assert 'At the national level of Türkiye' in method
    assert 'design weights' in method and 'calibration' in method
    return {'city':'Istanbul','main_admitted':False,'new_admitted_cells':0,'travel_interval':[0,1],'source_year':2022,'table':'10.3','printed_page':56,'pdf_page':74,'source_geography':'Türkiye national','stratum':'children aged15-17; not a verified currently-enrolled-high-school subgroup','reported_one_direction_minutes_percent':{'at_most30':le30,'over30':gt30},'separate_accompanied_by_adult_percent':accompaniment,'respondent':'mother or primary caregiver','direction':'one direction, either outbound or return; not guaranteed first home-to-school outbound trip','sampling':'national estimates; multistage sample; design weights, nonresponse adjustment, calibration, trimming, inflation','city_identifier_verified':False,'current_high_school_identifier_verified':False,'microdata_acquired':False,'visual_table_checked':True,'do_not_misread':'High school/vocational high school label in this table is maternal/caregiver education, not child school attendance.'}
if __name__=='__main__':
    x=extract();(P/'summary.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x,indent=2))
