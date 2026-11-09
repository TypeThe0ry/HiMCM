"""Read immutable official sources; produce scope facts without indicator admission."""
from pathlib import Path
import json,subprocess,zipfile,xml.etree.ElementTree as E
O=Path(__file__).resolve().parent
N={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def workbook_cells():
 with zipfile.ZipFile(O/'registration_q4_2025_original.xlsx') as z:
  strings=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',N)]
  result={}
  for name in ['xl/worksheets/sheet1.xml','xl/worksheets/sheet4.xml']:
   values={}
   for c in E.fromstring(z.read(name)).findall('.//s:c',N):
    v=c.find('s:v',N)
    if v is not None: values[c.get('r')]=strings[int(v.text)] if c.get('t')=='s' else v.text
   result[name]=values
  return result
if __name__=='__main__':
 cells=workbook_cells();a=cells['xl/worksheets/sheet1.xml'];b=cells['xl/worksheets/sheet4.xml']
 assert a['B5']=='52010' and a['B14']=='129418' and b['A34']=='Co. Dublin' and b['B34']=='5331'
 assert '24/12/2025' in a['A1'] and 'more than one route' in a['A17']
 county_sum=sum(int(b['B'+str(i)]) for i in range(4,60))
 selected=[dict(label=b['A'+str(i)],value=int(b['B'+str(i)]),label_cell='A'+str(i),value_cell='B'+str(i))
           for i in range(4,60) if 'Dublin' in b['A'+str(i)]]
 q=subprocess.check_output(['pdftotext','-layout',str(O/'quality_original.pdf'),'-'],text=True).split('\f')
 m=subprocess.check_output(['pdftotext','-layout',str(O/'methodology_original.pdf'),'-'],text=True).split('\f')
 assert 'not' in q[3] and 'published at this level' in q[3] and 'county level' in q[3]
 assert 'private schools' in q[3] and 'salary is paid' in q[3]
 assert 'microdata' in m[5] and 'do not make' in m[5]
 result=dict(version='V170',city='Dublin',indicator='upper_secondary_ptr',admitted_cells=0,
  registration=dict(reference_date='2025-12-24',national_postprimary_registered=52010,
   national_total_registered=129418,route_counts_overlap=True,
   county_sheet_postprimary_column_sum=county_sum,
   county_sum_minus_national_postprimary=county_sum-int(a['B5']),
   discrepancy='County-sheet sum and national route total differ; cause not established, no reconciliation or renormalization applied.',
   selected_geography_rows=selected,
   unit='registered people by route; not teaching FTE',geography='County-style field mixes Co. Dublin and Dublin postal labels; school workplace coverage not established in this workbook.',
   rejected='Registration does not establish active upper-secondary city teaching FTE; do not equate the 5331 county-labelled row with the complete Dublin target.'),
  payroll=dict(quality_report_pdf_page=4,reference_period_pdf_page=6,methodology_pdf_page=6,
   scope='State-funded primary and post-primary, with private-school teachers included where DEY pays their salary.',
   publication='FTE calculated at school level but not published there; DEY county/ETB aggregates and PXStat school-type aggregates.',
   microdata='Methodology states microdata are not made available to users.',
   rejected='No complete all-provider city senior-cycle FTE/student match or guaranteed enclosing denominator obtained.'),
  metadata_date_caution='Quality cover: reporting period 2025-2026, edited 06/02/2026; hub lists coverage 2015-2023. Neither metadata date is a new 2025 city observation.',
  utility_interval_before=[0,1],utility_interval_after=[0,1])
 (O/'scope_audit.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'responses':len(json.loads((O/'retrieval.json').read_text())), 'admitted_cells':0,'national_postprimary_registered':52010,'Dublin_label_rows':len(selected)}))
