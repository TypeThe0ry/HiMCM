"""Extract published Bogotá learning estimates and verify public geography fields."""
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as E
import hashlib,json,re,csv
P=Path(__file__).resolve().parent
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def sheet_rows(path,name):
    with ZipFile(path) as z:
        assert z.testzip() is None
        ss=[''.join(n.itertext()) for n in E.fromstring(z.read('xl/sharedStrings.xml'))]
        wb=E.fromstring(z.read('xl/workbook.xml'))
        rel={n.attrib['Id']:n.attrib['Target'] for n in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        sheet=next(x for x in wb.findall('m:sheets/m:sheet',NS) if x.attrib['name']==name)
        target=rel[sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
        if target.startswith('/'):target=target.lstrip('/')
        else:target='xl/'+target
        out=[]
        for row in E.fromstring(z.read(target)).findall('.//m:row',NS):
            d={}
            for c in row.findall('m:c',NS):
                v=c.find('m:v',NS);t='' if v is None else v.text
                d[re.sub('[0-9]','',c.attrib['r'])]=ss[int(t)] if c.attrib.get('t')=='s' and t else t
            out.append((int(row.attrib['r']),d))
        return out

def extract():
    for r in json.loads((P/'manifest.json').read_text()):
        raw=(P/r['file']).read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
    records=[];proficiency=[]
    for subject,n,prof in [('mathematics',1,12),('reading',2,13),('science',3,14)]:
        name=f'Table I.B2.{n}';rows=sheet_rows(P/'annex_b2.xlsx',name)
        row_id,d=next((i,d) for i,d in rows if d.get('A','').strip()=='Bogotá')
        assert dict(rows)[9]['B']=='Mean score' and dict(rows)[9]['C']=='S.E.'
        mean,se=float(d['B']),float(d['C'])
        records.append(dict(city='Bogotá',year=2022,subject=subject,table=name,row=row_id,mean=mean,standard_error=se,normal_approx_95_lower=mean-1.96*se,normal_approx_95_upper=mean+1.96*se))
        p_rows=sheet_rows(P/'annex_b2.xlsx',f'Table I.B2.{prof}');headers=dict(p_rows)[8]
        _,pd=next((i,d) for i,d in p_rows if d.get('A','').strip()=='Bogotá')
        levels={}
        for col,label in headers.items():
            if col=='A' or not label:continue
            levels[label.split('\n')[0]]=float(pd[col])
        assert abs(sum(levels.values())-100)<1e-8
        proficiency.append(dict(subject=subject,published_level_percentages=levels,at_least_level2_percent=sum(v for k,v in levels.items() if k in ['Level 2','Level 3','Level 4','Level 5','Level 6']),aggregate_standard_error=None))
    source=P.parent/'task4_v8_istanbul/pisa2022_codebook.xlsx'
    current='';selected=[]
    for row_id,d in sheet_rows(source,'CY08MSP_STU_QQQ'):
        if d.get('A'):current=d['A']
        if (current=='REGION' and d.get('G')=='17001') or (current=='STRATUM' and d.get('G') in ['COL01','COL02','COL03']) or (current=='ST001D01T' and d.get('G') in ['10','11']):
            selected.append(dict(row=row_id,variable=current,code=d.get('G'),label=d.get('H'),unweighted_codebook_frequency=int(d['I']),frequency_scope='International student file' if current=='ST001D01T' else 'Bogota regional records'))
    region=next(x for x in selected if x['variable']=='REGION');strata=[x for x in selected if x['variable']=='STRATUM']
    assert region['label']=='Colombia: Bogota' and region['unweighted_codebook_frequency']==1986
    assert len(strata)==3 and sum(x['unweighted_codebook_frequency'] for x in strata)==1986
    assert len([x for x in selected if x['variable']=='ST001D01T'])==2
    with (P/'bogota_outcomes.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,records[0].keys(),lineterminator='\n');w.writeheader();w.writerows(records)
    result=dict(city='Bogotá',year=2022,outcomes=records,proficiency=proficiency,geography_and_grade_codebook=selected,main_admitted=False,scope='Published PISA age15 regional cohort, including lower-secondary grades; not a grade10-11-only or all14-18 estimate. Codebook frequencies are record counts, not weighted population totals. Current-grade-specific learning estimates require the joint microdata plus plausible values and replicate weights.',uncertainty='Individual normal-approximate95% intervals derived from OECD published mean and SE; not simultaneous intervals or student score ranges. Proficiency aggregates have no derived SE because cross-level covariance is unavailable.')
    (P/'summary.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');return result
if __name__=='__main__':print(json.dumps(extract(),indent=2,ensure_ascii=False))
