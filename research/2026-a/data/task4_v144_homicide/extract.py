"""Read original CBS workbook/HTML and PKS report; no submitted value replaced."""
from pathlib import Path
from html.parser import HTMLParser
import csv,gzip,hashlib,json,re,subprocess,tempfile,zipfile
import xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
class Tables(HTMLParser):
    def __init__(self):super().__init__();self.tables=[];self.table=None;self.row=None;self.cell=None
    def handle_starttag(self,t,a):
        if t=='table':self.table=[]
        elif t=='tr' and self.table is not None:self.row=[]
        elif t in ['td','th'] and self.row is not None:self.cell=[]
    def handle_data(self,s):
        if self.cell is not None:self.cell.append(s)
    def handle_endtag(self,t):
        if t in ['td','th'] and self.cell is not None:self.row.append(' '.join(''.join(self.cell).split()));self.cell=None
        elif t=='tr' and self.row is not None:self.table.append(self.row);self.row=None
        elif t=='table' and self.table is not None:self.tables.append(self.table);self.table=None

def main():
    source=ROOT/'data/task4_v117_team_intake/city_indicators.csv';before=sha(source)
    raw={}
    for meta in read(HERE/'retrievals.json'):
        name=meta['file'];data=(HERE/name).read_bytes();data=gzip.decompress(data) if name.endswith('.gz') else data
        assert len(data)==meta['raw_bytes'] and hashlib.sha256(data).hexdigest()==meta['raw_sha256'];raw[name]=data
    n={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(HERE/'cbs2022_original.xlsx') as z:
        strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        workbook=ET.fromstring(z.read('xl/workbook.xml'));sheets={x.get('name'):x.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id') for x in workbook.find('m:sheets',n)}
        rels={x.get('Id'):x.get('Target') for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        extracted={}
        for title in ['Tabel 7. Regio','Toelichting']:
            target='xl/'+rels[sheets[title]];cells={}
            for cell in ET.fromstring(z.read(target)).findall('.//m:c',n):
                v=cell.find('m:v',n);text=v.text if v is not None else ''
                if cell.get('t')=='s':text=strings[int(text)]
                if text:cells[cell.get('r')]=text
            extracted[title]=dict(xml_part=target,cells=cells)
    regional=extracted['Tabel 7. Regio']['cells'];assert regional['A24']=='Amsterdam' and regional['B24']=='68' and regional['F24']=='1.55' and '2018-2022*' in regional['A1']
    parser=Tables();parser.feed(raw['cbs_news2022_original.html.gz'].decode('utf-8'))
    city_tables=[x for x in parser.tables if x and x[0]==['Jaar','Amsterdam','Rotterdam','Den Haag']];assert len(city_tables)==2 and city_tables[0]==city_tables[1]
    city_table=city_tables[0];annual=next(x for x in city_table if x[0]=='2022*');assert annual==['2022*','10','16','3']
    series={int(x[0].replace('*','')):int(x[1]) for x in city_table[1:] if x and re.fullmatch(r'\d{4}\*?',x[0])}
    assert sum(series[y] for y in range(2018,2023))==68
    (HERE/'cbs_cells_extracted.json').write_text(json.dumps(extracted,ensure_ascii=False,indent=2)+'\n');(HERE/'cbs_annual_table_extracted.json').write_text(json.dumps(city_table,ensure_ascii=False,indent=2)+'\n')
    with tempfile.TemporaryDirectory(prefix='himcm_v144_source_',dir='/data/scratch') as temp:
        p=Path(temp)/'report.pdf';p.write_bytes(raw['zurich2025_original.pdf.gz'])
        for page in [117,118,120]:
            result=subprocess.check_output(['pdftotext','-f',str(page),'-l',str(page),'-layout',str(p),'-']);(HERE/f'zurich_page_{page:03d}_extracted.txt').write_bytes(result)
    text=(HERE/'zurich_page_117_extracted.txt').read_text();assert '5.1.26 Stadt Zürich gesamt' in text and re.search(r'2021\s+2022\s+2023\s+2024\s+2025',text)
    completed=re.search(r'Tötungsdelikte vollendet\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)',text);attempted=re.search(r'Tötungsdelikte versucht\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)',text)
    assert list(map(int,completed.groups()))==[3,4,4,1,2] and list(map(int,attempted.groups()))==[14,14,18,17,20]
    glossary=' '.join((HERE/'zurich_page_118_extracted.txt').read_text().split());assert 'ungeachtet der Anzahl geschädigter Personen' in glossary
    with source.open(encoding='utf-8-sig',newline='') as f:submitted={x['city']:x for x in csv.DictReader(f)}
    am=submitted['Amsterdam'];zh=submitted['Zurich'];assert am['homicide_numerator']=='340.0' and zh['homicide_numerator']=='1.0'
    scope=dict(version='V144 source-definition verification, no primary numerical admission',amsterdam=dict(source='CBS release 29 August 2023',annual_year=2022,provisional=True,annual_victims=10,regional_period=[2018,2022],regional_period_victims=68,regional_published_rate_per100000=1.55,regional_rate_is_not_annual_2022=True,includes_resident_and_nonresident_victims=True,submitted_numerator=float(am['homicide_numerator']),submitted_rate=float(am['homicide_per_100k']),submitted_population=int(am['population']),submitted_population_year=int(am['population_year']),same_definition_match=False,original_submitted_source_not_traced=True),zurich=dict(source='PKS 2025, PDF page 117',geography='Stadt Zürich gesamt',statistical_unit='registered criminal acts, independent of the number of injured persons',completed_offences_2024=1,completed_offences_2025=2,attempted_offences_2024=17,attempted_offences_2025=20,offence_counts_are_not_victim_counts=True,submitted_numerator=float(zh['homicide_numerator']),submitted_rate=float(zh['homicide_per_100k']),submitted_population=int(zh['population']),submitted_population_year=int(zh['population_year']),submitted_rate_denominator_not_established=True),primary_admissions=0,original_values_replaced=0,interpretation='Independent source scope checks; no corrected victim rate, no empirical trend and no inference that every source flag denotes an error')
    (HERE/'scope_audit.json').write_text(json.dumps(scope,ensure_ascii=False,indent=2)+'\n');(HERE/'observations.json').write_text('[]\n')
    assert sha(source)==before
    files=['retrievals.json','cbs_news2022_original.html.gz','cbs_landing2022_original.html.gz','cbs2022_original.xlsx','zurich2025_original.pdf.gz','cbs_cells_extracted.json','cbs_annual_table_extracted.json','zurich_page_117_extracted.txt','zurich_page_118_extracted.txt','zurich_page_120_extracted.txt','scope_audit.json','observations.json']
    receipt=dict(status='pass',source_sha256={n:sha(HERE/n) for n in files},original_csv_sha256=before,source_extractor_sha256=sha(Path(__file__)),cbs_2018_2022_annual_sum_matches_regional_68=True,cbs_2022_annual_victims=10,zurich_city_completed_offences_2024_2025=[1,2],primary_admissions=0)
    dest=HERE/('recheck_verification.json' if (HERE/'verification.json').exists() else 'verification.json');dest.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
