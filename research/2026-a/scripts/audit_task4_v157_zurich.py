"""Independent OOXML and JSON-stat checks; preserve active science and paper."""
from pathlib import Path
import hashlib,itertools,json,re,subprocess,zipfile,xml.etree.ElementTree as ET

R=Path(__file__).resolve().parents[1];D=R/'data/task4_v157_zurich_school';O=R/'results/task4_v157_zurich_school';P=Path('/data/projects/HiMCM-Overleaf')
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())

def cells(path,sheet_number,stop_row):
    """Native cached OOXML reader, independent of the openpyxl extraction."""
    with zipfile.ZipFile(path) as z:
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            root=ET.fromstring(z.read('xl/sharedStrings.xml'))
            strings=[''.join(n.itertext()) for n in root.findall('s:si',NS)]
        result={}
        with z.open(f'xl/worksheets/sheet{sheet_number}.xml') as source:
            for event,row in ET.iterparse(source,events=['end']):
                if row.tag.rsplit('}',1)[-1]!='row':continue
                number=int(row.attrib['r'])
                for cell in row.findall('s:c',NS):
                    address=cell.attrib['r'];value=cell.find('s:v',NS);kind=cell.get('t')
                    if kind=='inlineStr':value=''.join(cell.find('s:is',NS).itertext())
                    elif value is None:value=None
                    elif kind=='s':value=strings[int(value.text)]
                    else:
                        text=value.text
                        try:value=float(text);value=int(value) if value.is_integer() else value
                        except (TypeError,ValueError):value=text
                    if number<=stop_row:result[address]=value
                row.clear()
                if number>=stop_row:break
        return result


def main():
    O.mkdir(exist_ok=True);scope=read(D/'scope_audit.json')
    assert sha(D/'extract.py')==scope['extractor_sha256']
    for n,h in scope['original_sha256'].items():assert sha(D/n)==h,n
    student=R/scope['student_workbook']['file'];assert sha(student)==scope['student_workbook']['sha256']
    # Workbook order is frozen; prove it from the workbook XML before using
    # raw sheet numbers (T_2 is sheet4 and T_3 is sheet5).
    with zipfile.ZipFile(student) as z:
        sheets=ET.fromstring(z.read('xl/workbook.xml')).find('s:sheets',NS)
        names=[n.get('name') for n in sheets]
        assert names[3:5]==['T_2','T_3']
    source=cells(student,5,100);assert source['T10']==2024 and source['T11']==13426
    totals={}
    for k in range(12,101):
        value=source.get('T'+str(k))
        if isinstance(value,(int,float)):
            key=(source['A'+str(k)],source['B'+str(k)])
            totals[key]=totals.get(key,0)+value
    assert totals=={('Sekundarstufe I','öffentlich'):4443,('Sekundarstufe I','privat'):402,('Sekundarstufe II','öffentlich'):6582,('Sekundarstufe II','privat'):1999}
    assert sum(totals.values())==13426 and 4443+402==4845 and 6582+1999==8581
    school=cells(student,4,47);assert school['S10']==2024 and school['S14']==1132 and school['S21']==688
    euro=read(D/'eurostat_CH_ED3_2024_original.json')
    axes=[sorted(euro['dimension'][key]['category']['index'],key=euro['dimension'][key]['category']['index'].get) for key in euro['id']]
    decoded=[]
    for index,key in enumerate(itertools.product(*axes)):
        labels=dict(zip(euro['id'],key))
        if labels['sex']=='T' and labels['worktime']=='TOT_FTE' and labels['sector'] in ['TOT_SEC','PUB','PRV']:
            decoded.append((labels['sector'],euro['value'][str(index)],euro['status'][str(index)]))
    assert decoded==[('TOT_SEC',20904,'d'),('PUB',18446,'d'),('PRV',2459,'d')]
    note=cells(D/'eurostat_personnel_footnotes_original.xlsx',1,68495)
    assert [note[c+'68495'] for c in ['B','C','D','F','G','H','I','K']]==['TOT_SEC','TOT_FTE','NR','T','ED3','CH',2024,'educ_uoe_perp02']
    assert note['J68495']==scope['national_candidate']['matching_footnotes'][0]['text']
    assert 'includes ISCED11_4' in note['J68495']
    assert 'No data for private institutions' in scope['national_candidate']['country_personnel_metadata_context']
    assert not scope['national_candidate']['all_provider_teacher_superset_proven']
    assert scope['observations']==[] and scope['primary_data_admissions']==0
    # A blank/zero FTE cannot be manufactured from the approximate headcount.
    assert scope['valid_bound_requirements']['current_source_pairs_meet_requirements'] is False
    snapshot=read(R/'design/task4_user_v154_snapshot.json')
    for n,h in snapshot['source_sha256'].items():assert sha(R/n)==h,n
    manuscript=read(R/'results/task4_v156_readiness/summary.json')['manuscript_files_unchanged_sha256'].copy()
    manuscript.update(read(R/'results/task4_v156_readiness/delivery.json')['selected_file_sha256'])
    for n,h in manuscript.items():assert sha(P/n)==h,n
    result=dict(status='pass',iteration='V157',primary='V154 unchanged',
                source_response_bodies_verified=len(scope['original_sha256']),
                workbook_independently_read_with='Native cached OOXML; original workbook not edited or exported',
                published_student_total=13426,lower_secondary=4845,upper_secondary=8581,student_count_scope='Mittelschulen T_3 only; not the full city upper-secondary population',
                national_FTE_total=20904,national_FTE_status='d; definition differs',
                matching_footnote_cell='Footnotes!J68495',private_coverage_unresolved=True,
                stage_specific_city_teacher_FTE_identified=False,
                current_snapshot_files_unchanged=len(snapshot['source_sha256']),
                existing_manuscript_files_unchanged=len(manuscript),
                primary_data_admissions=0,primary_score_interval_width_reduction=0,
                manuscript_changed=False,PDF_authored=False,
                primary_pdf_sha256=sha(P/'drafts/task4_v154_paper.pdf'),
                source_sha256={str(p.relative_to(R)):sha(p) for p in [D/'scope_audit.json',D/'extract.py',D/'retrieval.json',D/'eurostat_retrieval.json',D/'metadata_retrieval.json']},
                verifier_sha256=sha(Path(__file__)))
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','source_response_bodies_verified','published_student_total','upper_secondary','current_snapshot_files_unchanged','existing_manuscript_files_unchanged','primary_data_admissions']},indent=2))

if __name__=='__main__':main()
