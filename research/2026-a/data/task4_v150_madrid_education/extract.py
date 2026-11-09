"""Recover the new municipal count series without relabelling it teacher FTE."""
from pathlib import Path
import csv,hashlib,json,re
D=Path(__file__).resolve().parent
CITY='https://gestiona.comunidad.madrid/desvan/AccionDatosTemaMunicipal.icm?codTema=1902424'
REPORT='https://www.comunidad.madrid/docs/assets/2025/12/17/informe_-_capitulo_b_-_2025.pdf?VersionId=xG.t7J4_kU00tSXSmvFCUBxVcNYLgOp5'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 capture=json.loads((D/'provider_capture.json').read_text());assert not capture.get('isError');text='\n'.join(x['text'] for x in capture['content'] if x['type']=='text');city,report=text.split('\n# Capítulo B\n',1)
 assert CITY in city and REPORT in report and 'Unidad: Número' in city
 assert 'en las tablas se hace referencia al último año' in city
 assert '2024 (P)' in city and '1.922 profesores impartieron exclusivamente enseñanzas en Bachillerato' in report
 assert '2023-2024' in report and 'equivalente a tiempo completo' in report and 'Comunidad de Madrid (12,6)' in report
 assert 'ensemanzas de Régimen General' in report
 records=[];level='';year_labels=None
 for line in city.splitlines():
  if not line.startswith('|'):continue
  cells=[s.strip() for s in line.strip('|').split('|')]
  if cells[0] in ['Zonas Estadísticas','Municipios']:level=cells[0];continue
  if cells[0]=='Comunidad de Madrid':level='regional'
  if cells[0]=='' and len(cells)==21 and cells[1]=='2005':year_labels=cells[1:];continue
  if len(cells)!=21 or not cells[-1] or cells[0] in ['','---']:continue
  assert all(re.fullmatch(r'(?:\d{1,3}(?:\.\d{3})+|\d+)',v) for v in cells[1:]),cells[0]
  records.append(dict(level=level,name=cells[0],values=[int(v.replace('.','')) for v in cells[1:]]))
 assert year_labels==[str(y) for y in range(2005,2024)]+['2024 (P)']
 regional=[r for r in records if r['level']=='regional'];zones=[r for r in records if r['level']=='Zonas Estadísticas'];municipal=[r for r in records if r['level']=='Municipios'];assert (len(regional),len(zones),len(municipal))==(1,11,179)
 target=next(r for r in municipal if r['name']=='Madrid');city_zone=next(r for r in zones if r['name']=='Municipio de Madrid');assert target['values']==city_zone['values']
 rows=[]
 for j,year in enumerate(range(2005,2025)):
  reg=regional[0]['values'][j];zs=sum(r['values'][j] for r in zones);ms=sum(r['values'][j] for r in municipal);assert reg==zs==ms
  rows.append(dict(source_year_label=year_labels[j],calendar_label=year,school_year=f'{year-1}/{year}',P_marker_present=(year==2024),city='Madrid',published_unit='Número',city_teacher_count=target['values'][j],region_teacher_count=reg,zone_sum=zs,municipality_sum=ms,flat_all_level_sum=reg+zs+ms,FTE_identified=False,primary_model_admitted=False))
 with (D/'candidate_city_teacher_counts.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 # Only prose and the clean HTML table are used; the PDF extraction includes
 # garbled chart/table text whose cell alignment has not been independently seen.
 markers=['Profesorado que impartió exclusivamente enseñanzas de Bachillerato','1.922 profesores impartieron exclusivamente enseñanzas en Bachillerato','La figura B4.4.4 muestra el número medio de alumnos por profesor a tiempo completo','Nota: Calculado como cociente','Comunidad de Madrid (12,6)']
 witnesses=[]
 for key,marker in zip(['exclusive_bach_heading','exclusive_bach_count','general_ratio_figure','FTE_conversion_note','region_ratio'],markers):
  p=report.index(marker);start=max(0,p-100);end=p+len(marker)+520;context=report[start:end];witnesses.append(dict(claim=key,report_text_start=start,report_text_end=end,context_sha256=hashlib.sha256(context.encode()).hexdigest()))
 result=dict(iteration='V150',primary_data_admissions=0,observations=[],city='Madrid',indicator='upper_secondary_ptr',status='not_admitted',candidate_series=dict(first_year_label=year_labels[0],last_year_label=year_labels[-1],year_columns=20,school_year_mapping='Tables use the last year of a two-year school course; 2024 refers to 2023/24',published_unit='Número',latest_city_count=target['values'][-1],latest_region_count=regional[0]['values'][-1],table_levels=dict(regional=1,statistical_zones=11,municipalities=179),count_cells=len(records)*20,all_20_hierarchy_totals_agree=True,latest_flat_all_level_sum=rows[-1]['flat_all_level_sum'],fte_established=False),report_scope=dict(publication_title='Informe 2025',school_year='2023-2024',exclusive_bachillerato_count_region=1922,all_regimen_general_FTE_ratio_region=12.6,PDF_original_downloaded=False,PDF_chart_cell_alignment_verified=False,numerical_admission_from_PDF_tables=False),scope_reasons=['Municipal teacher-count unit is Número; actual upper-stage teaching FTE is not established.','Bachillerato alone does not identify the retained whole upper-secondary teaching-resource universe or vocational allocations.','The report describes exclusive Bachillerato teaching separately; numerical agreement alone does not prove the municipal series uses the same exclusive-stage workforce definition. Its own note does establish that labels use the final school-course year.','The reported 12.6 ratio uses regional all-Régimen-General coverage, not Madrid-city upper-secondary coverage.','Repeated geographic hierarchy levels must not be summed as distinct teachers.'],representation='Exact saved Exa tool response containing provider-extracted official HTML/PDF text; not original HTTP bodies.',source_urls=[CITY,REPORT],source_sha256={n:sha(D/n) for n in ['provider_capture.json','provider_request_manifest.json','retrieval.json','versioned_attempt.json']},scope_witnesses=witnesses,extractor_sha256=sha(Path(__file__)),next_required='Matched city upper-secondary pupil universe and actual teaching FTE with provider/stage allocations. No headcount-to-FTE conversion or reference-year relabelling is assumed.')
 (D/'scope_audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print('Recovered 20 Madrid city count columns; 3,820 hierarchical count cells; 20 level reconciliations pass; zero admissions.')
if __name__=='__main__':main()
