"""Read-only school/country source review; no city PTR observation admitted."""
from pathlib import Path
from collections import defaultdict
from html.parser import HTMLParser
import hashlib,itertools,json,re,subprocess
import openpyxl

D=Path(__file__).resolve().parent
R=D.parents[1]
STUDENTS=R/'data/task4_v120_education/zurich_students2024.xlsx'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

class Text(HTMLParser):
    def __init__(self):super().__init__();self.parts=[]
    def handle_data(self,value):self.parts.append(value)

def plain(p):
    parser=Text();parser.feed(p.read_text());return ' '.join(' '.join(parser.parts).split())


def main():
    originals={}
    for filename in ['retrieval.json','metadata_retrieval.json']:
        for row in json.loads((D/filename).read_text()):
            assert row['status']==200
            assert sha(D/row['file'])==row['sha256'],row['file']
            originals[row['file']]=row['sha256']
    row=json.loads((D/'eurostat_retrieval.json').read_text())
    assert row['status']==200 and sha(D/row['file'])==row['sha256']
    originals[row['file']]=row['sha256']
    assert sha(STUDENTS)=='6234f5b6cf617af10db16c5930105df4183eade7df47564858cc5dfe010bc251'
    w=openpyxl.load_workbook(STUDENTS,data_only=True,read_only=True)
    stage=w['T_3'];yearcol=next(c.column for c in stage[10] if c.value==2024)
    assert yearcol==20 and 'Schuljahre' in w['Erläuterungen']['B1'].value
    totals=defaultdict(int);numeric=0;blank=0
    for values in stage.iter_rows(min_row=12,values_only=True):
        level,ownership,value=values[0],values[1],values[yearcol-1]
        if isinstance(value,(int,float)):
            assert value>=0 and value==int(value)
            totals[level,ownership]+=int(value);numeric+=1
        else:
            assert value in [None,''];blank+=1
    aggregates=[dict(stage=k[0],ownership=k[1],published_numeric_sum=v) for k,v in sorted(totals.items())]
    assert sum(totals.values())==stage['T11'].value==13426
    lower=sum(v for (level,own),v in totals.items() if level=='Sekundarstufe I')
    upper=sum(v for (level,own),v in totals.items() if level=='Sekundarstufe II')
    assert lower==4845 and upper==8581
    assert w['T_2']['S10'].value==2024 and w['T_2']['S14'].value==1132
    assert w['T_2']['S21'].value==688
    # Decode the JSON-stat mixed-radix index from categories, never infer units
    # from unit=NR alone: worktime=TOT_FTE is the required additional selector.
    euro=json.loads((D/'eurostat_CH_ED3_2024_original.json').read_text())
    dimensions=euro['id'];sizes=euro['size']
    def observation(sector,worktime):
        key=dict(freq='A',unit='NR',worktime=worktime,isced11='ED3',sector=sector,sex='T',geo='CH',time='2024')
        index=0
        for name,size in zip(dimensions,sizes):index=index*size+euro['dimension'][name]['category']['index'][key[name]]
        return dict(index=index,value=euro['value'].get(str(index)),status=euro['status'].get(str(index)))
    selected={sector:observation(sector,'TOT_FTE') for sector in ['TOT_SEC','PUB','PRV']}
    assert [selected[k]['value'] for k in ['TOT_SEC','PUB','PRV']]==[20904,18446,2459]
    assert all(x['status']=='d' for x in selected.values())
    assert euro['extension']['status']['label']['d']=='definition differs (see metadata)'
    head=observation('TOT_SEC','TOTAL');full=observation('TOT_SEC','FT')
    assert head['value']==33993 and full['value']==7663
    notes=openpyxl.load_workbook(D/'eurostat_personnel_footnotes_original.xlsx',data_only=True,read_only=True)['Footnotes']
    matched=[]
    for number,row in enumerate(notes.values,1):
        if len(row)<11:continue
        if (row[7]=='CH' and str(row[8])=='2024' and row[10]=='educ_uoe_perp02'
            and row[1] in ('*','TOT_SEC') and row[2] in ('*','TOT_FTE')
            and row[3] in ('*','NR') and row[4] in ('*','TOTAL')
            and row[5] in ('*','T') and row[6] in ('*','ED3')):
            matched.append(dict(sheet='Footnotes',row=number,range=f'A{number}:K{number}',text=row[9],selectors=list(row[:9])))
    assert len(matched)==1 and matched[0]['row']==68495
    assert 'includes ISCED11_4' in matched[0]['text']
    metadata=plain(D/'eurostat_CH_metadata_original.html')
    context=re.search(r'Personnel\s+Data not covered:\s+No data for private institutions',metadata)
    assert context, 'Country personnel scope not located'
    portrait=plain(D/'enge_portrait_original.html')
    assert re.search(r'über 150 Lehrkräfte rund 1100',portrait)
    pdf=D/'stadelhofen_2024_25_original.pdf'
    pages=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True).split('\f')[:-1]
    assert len(pages)==86
    assert sum('Vollzeit' in text for text in pages)==1
    assert 'Vollzeit-' in pages[62] and 'Vereinswart' in pages[62] and 'FKSZ' in pages[62]
    assert 'VERZEICHNISSE' in pages[80] and 'IMPRESSUM' in pages[83]
    # No public teacher names or student rows are newly extracted into outputs.
    result=dict(version='V157',status='new source review; no admission',primary='V154 unchanged',
                student_workbook=dict(file=str(STUDENTS.relative_to(R)),sha256=sha(STUDENTS),
                    population_scope='Mittelschulen table T_3 only; not all city upper-secondary pupils or resident ages14-18; separate Berufsschulen tables are not included',year_label=2024,year_scope='School year beginning in2024 per Erläuterungen!B1; not relabelled as2025',
                    total_cell='T_3!T11',total=13426,stage_aggregates=aggregates,
                    lower_secondary=lower,upper_secondary=upper,numeric_cells=numeric,blank_cells_preserved=blank,
                    enge_school_total=dict(cell='T_2!S14',value=1132,scope='All levels at that school; no school-specific stage cross-tab'),
                    stadelhofen_school_total=dict(cell='T_2!S21',value=688,scope='All levels at that school'),
                    no_upper_secondary_only_denominator_claim=True),
                school_sources=dict(enge='Approximate150-plus teacher headcount and1100 pupils; no teaching FTE denominator established',
                    stadelhofen='Public2024/25 annual report86PDF pages. The sole full-time text hit onPDF63 concerns a caretaker moving toFKSZ, not teaching FTE. Contents lists directories; public file follows chronology with imprint; no usable workload table obtained.',
                    reviewed_pdf_pages=[63,84],all_document_absence_not_claimed=True),
                national_candidate=dict(dataset='educ_uoe_perp02',geo='CH',isced11='ED3',sex='T',time_label='2024',unit='NR',worktime='TOT_FTE',
                    observations=selected,headcount=head,full_time_headcount=full,
                    published_sector_sum_difference=18446+2459-20904,
                    matching_footnotes=matched,country_personnel_metadata_context=context.group(0),
                    reference_period_match_to_city_workbook=False,
                    all_provider_teacher_superset_proven=False,
                    reason='Country metadata says private-institution personnel are not covered, despite a numerical PRV series. ED3 also includes ED4. Coverage and period cannot be silently assumed consistent; no national-to-city point substitution or upper bound admitted.'),
                valid_bound_requirements=dict(lower_PTR='Need verified student lower total and teacher upper superset for the same stage/providers/period',
                    upper_PTR='Need verified student upper superset and positive teacher lower subset for the same stage/providers/period',
                    current_source_pairs_meet_requirements=False),
                observations=[],primary_data_admissions=0,primary_score_interval_width_reduction=0,
                original_sha256=originals,extractor_sha256=sha(Path(__file__)))
    (D/'scope_audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print('Student split4845+8581=13426; EurostatFTE20904 flaggedd; matching footnote68495;0admissions')

if __name__=='__main__':main()
