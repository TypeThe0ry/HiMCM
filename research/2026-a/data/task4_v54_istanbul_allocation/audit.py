"""Check partial school-list coverage without interpreting absence as zero."""
from pathlib import Path
import csv,hashlib,html,json,re,subprocess
P=Path(__file__).resolve().parent

def main():
    for item in json.loads((P/'manifest.json').read_text()):
        b=(P/item['file']).read_bytes()
        assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
    source=(P/'eba_school_list.html').read_text()
    rows=[]
    for tr in re.findall(r'<tr\b[^>]*>(.*?)</tr>',source,re.S|re.I):
        cells=[re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',x))).strip() for x in re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>',tr,re.S|re.I)]
        if len(cells)==4 and cells[0].isdigit() and 'Ortaokulu' in cells[3]:
            rows.append(dict(number=int(cells[0]),province=cells[1],district=cells[2],school=cells[3]))
    assert len(rows)==12 and [r['number'] for r in rows]==list(range(1,13))
    assert not any(r['province'].casefold() in ('istanbul','i̇stanbul') for r in rows)
    assert '111708265' in source and '05.09.2025' in source
    report=subprocess.check_output(['pdftotext','-layout',str(P/'mtegm_2025_activity.pdf'),'-']).decode()
    pages=report.split('\f')
    matches=[i+1 for i,text in enumerate(pages) if re.search(r'18 ilde 20 mesleki ve teknik Anadolu lisesi',text)]
    assert len(matches)==1
    with (P/'listed_schools.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    result=dict(approval_date='2025-09-05',approval_reference='111708265',listed_schools=12,
                listed_istanbul_schools=0,list_is_verified_complete_2025_26_universe=False,
                calendar2025_report_national_schools=20,calendar2025_report_provinces=18,
                report_pdf_page=matches[0],v53_academic2025_26_national_schools=27,
                decision='No Istanbul zero or affected-teacher ceiling inferred from this partial list; retain V in [0,20156]',
                new_model_observations=0)
    (P/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
