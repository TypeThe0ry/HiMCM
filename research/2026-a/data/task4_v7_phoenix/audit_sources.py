"""Offline evidence-gap checks; never synthesize Phoenix measurements."""
from pathlib import Path
import hashlib,json,zipfile,xml.etree.ElementTree as ET,csv
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def main():
    for r in json.loads((ROOT/'manifest.json').read_text()):
        if 'sha256' in r:assert hashlib.sha256((ROOT/r['file']).read_bytes()).hexdigest()==r['sha256']
    rows=[]; inventory=[]
    with zipfile.ZipFile(ROOT/'nhts2017_codebook.xlsx') as z:
        strings=[''.join(si.itertext()) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        for sheet in range(1,5):
            var=label=''
            for r in ET.fromstring(z.read(f'xl/worksheets/sheet{sheet}.xml')).findall('.//m:sheetData/m:row',NS):
                d={}
                for cell in r.findall('m:c',NS):
                    value=cell.find('m:v',NS);v='' if value is None else value.text
                    d[cell.get('r').rstrip('0123456789')]=strings[int(v)] if cell.get('t')=='s' and v else v
                if d.get('A'):
                    var,label=d.get('A',''),d.get('B','');inventory.append(dict(sheet=sheet,variable=var,label=label))
                if var in ['HH_CBSA','HHSTATE','SCHTYP','R_AGE','TRVLCMIN','WHYTO','WHYFROM']:
                    if var=='HH_CBSA' and 'Phoenix' not in d.get('E',''):continue
                    if var=='HHSTATE' and d.get('E')!='AZ':continue
                    rows.append(dict(sheet=sheet,variable=var,label=label,code_or_range=d.get('E',''),frequency=d.get('F',''),weighted=d.get('G','')))
    with (ROOT/'nhts2017_selected_fields.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    with (ROOT/'nhts2017_variable_inventory.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=inventory[0]);w.writeheader();w.writerows(inventory)
    assert any(r['variable']=='HH_CBSA' and 'Phoenix-Mesa-Scottsdale' in r['code_or_range'] for r in rows)
    assert not any('city' in r['label'].lower() for r in inventory if r['sheet']==1)
    text=(ROOT/'nhts2022_compatibility.txt').read_text()
    assert 'HHSTATE' in text and 'HH_CBSA' in text and 'Census division' in text
    agenda=BeautifulSoup((ROOT/'trp_2026_07_agenda.html').read_bytes(),'html.parser').get_text(' ',strip=True)
    assert 'Phoenix Union High School District' in agenda and 'Brophy College Preparatory' in agenda
    summary=dict(new_admitted_measurements=0,phoenix_travel_utility_lower=0,phoenix_travel_utility_upper=1,
        nhts2017_smallest_named_local_geography='Phoenix-Mesa-Scottsdale CBSA, not Phoenix city',
        nhts2017_phoenix_cbsa_household_frequency=next(int(r['frequency']) for r in rows if r['sheet']==1 and r['variable']=='HH_CBSA'),
        nhts2017_phoenix_cbsa_person_frequency_all_ages=next(int(r['frequency']) for r in rows if r['sheet']==2 and r['variable']=='HH_CBSA'),
        nhts2022_state_cbsa_variables_omitted=True,trp_high_school_agenda_identified=True,trp_school_duration_results_acquired=False)
    (ROOT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
