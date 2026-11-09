"""Independently index year columns and reconcile hierarchy; do not admit counts."""
from pathlib import Path
import csv,hashlib,json,re
from task4_user_v136_revision import revised_bounds
from task4_v5_model import NAMES
R=Path(__file__).resolve().parents[1];D=R/'data/task4_v150_madrid_education';O=R/'results/task4_v150_madrid_education';P=R.parents[2]/'HiMCM-Overleaf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
 O.mkdir(exist_ok=True);s=read(D/'scope_audit.json');assert s['observations']==[] and s['primary_data_admissions']==0
 for n,h in s['source_sha256'].items():assert sha(D/n)==h,n
 assert sha(D/'extract.py')==s['extractor_sha256'];capture=read(D/'provider_capture.json');text='\n'.join(x['text'] for x in capture['content'] if x['type']=='text');city,report=text.split('\n# Capítulo B\n',1)
 assert 'en las tablas se hace referencia al último año' in city and 'Unidad: Número' in city
 header=next(l for l in city.splitlines() if l.startswith('| | 2005 |'));labels=[v.strip() for v in header.split('|')[2:-1]];assert len(labels)==20 and labels[-1]=='2024 (P)'
 def read_rows(section):
  result={}
  for line in section.splitlines():
   cells=[v.strip() for v in line.split('|')[1:-1]]
   if len(cells)==21 and cells[0] and all(re.fullmatch(r'[\d.]+',v) for v in cells[1:]):
    assert cells[0] not in result;result[cells[0]]={y:int(v.replace('.','')) for y,v in zip(labels,cells[1:])}
  return result
 top,rest=city.split('| Zonas Estadísticas |',1);zpart,mpart=rest.split('| Municipios |',1);top=read_rows(top);zones=read_rows(zpart);towns=read_rows(mpart)
 assert (len(top),len(zones),len(towns))==(1,11,179)
 rows=list(csv.DictReader((D/'candidate_city_teacher_counts.csv').open()));assert len(rows)==20
 for row in rows:
  y=row['source_year_label'];i=int(row['calendar_label']);assert y in labels and row['school_year']==f'{i-1}/{i}'
  region=top['Comunidad de Madrid'][y];municipality=towns['Madrid'][y];zone=zones['Municipio de Madrid'][y];assert municipality==zone==int(row['city_teacher_count'])
  z=sum(v[y] for v in zones.values());m=sum(v[y] for v in towns.values());assert region==z==m==int(row['region_teacher_count'])==int(row['zone_sum'])==int(row['municipality_sum'])
  assert int(row['flat_all_level_sum'])==region+z+m==3*region
  assert row['P_marker_present']==str(i==2024) and row['published_unit']=='Número' and row['FTE_identified']==row['primary_model_admitted']=='False'
 assert rows[-1]['city_teacher_count']=='1008' and rows[-1]['region_teacher_count']=='1922' and rows[-1]['flat_all_level_sum']=='5766'
 assert '1.922 profesores impartieron exclusivamente enseñanzas en Bachillerato' in report and 'equivalente a tiempo completo' in report and 'Comunidad de Madrid (12,6)' in report
 for item in s['scope_witnesses']:assert hashlib.sha256(report[item['report_text_start']:item['report_text_end']].encode()).hexdigest()==item['context_sha256']
 # Failed acquisition names are intended paths, not downloaded files.
 failures=read(D/'retrieval.json');assert len(failures)==5 and all(x.get('error_type') for x in failures) and all(not (D/x['file']).exists() for x in failures)
 assert read(D/'versioned_attempt.json')['error_type']=='TimeoutError' and not (D/'chapter_b_versioned_original.pdf').exists()
 manifest=read(D/'provider_request_manifest.json');assert manifest['saved_response_sha256']==sha(D/'provider_capture.json') and manifest['saved_response_bytes']==(D/'provider_capture.json').stat().st_size
 assert not manifest['is_error'] and manifest['text_characters']==sum(len(x.get('text','')) for x in capture['content'])
 frozen={}
 for n,k in [('design/task4_user_v136_snapshot.json','source_sha256'),('results/task4_v137_revision/audit.json','result_sha256'),('results/task4_v138_priority/summary.json','source_sha256')]:frozen.update(read(R/n)[k])
 for n,h in frozen.items():assert sha(R/n)==h,n
 frame,lo,hi=revised_bounds();j=NAMES.index('upper_secondary_ptr');i=list(frame.city).index('Madrid');assert (lo[i,j],hi[i,j])==(0,1)
 counts=dict(point=int((lo==hi).sum()),unknown=int(((lo==0)&(hi==1)).sum()));counts['partial']=160-counts['point']-counts['unknown'];assert counts==dict(point=112,unknown=15,partial=33)
 qa=read(P/'drafts/task4_v137_assets/qa.json');paper=read(P/'drafts/task4_v137_assets/manifest.json');assert qa['documentation_revision']==paper['documentation_revision']=='V148'
 protected={**paper['protected_files'],**{str(Path('drafts')/n):h for n,h in paper['manuscript_source_sha256'].items()},'drafts/task4_v137_paper.pdf':qa['pdf_sha256']}
 for n,h in protected.items():assert sha(P/n)==h,n
 result=dict(status='pass',iteration='V150',candidate_years=20,hierarchical_count_cells=3820,geographic_level_reconciliations=20,municipal_rows=179,statistical_zone_rows=11,city_count_2023_24=1008,region_count_2023_24=1922,incorrect_all_level_sum=5766,school_year_mapping_verified=True,published_unit='Número',FTE_identified=False,provider_extraction_not_original_HTTP=True,PDF_table_alignment_verified=False,primary_data_admissions=0,primary_score_interval_width_reduction=0,current_counts=counts,protected_scientific_files=len(frozen),scientific_file_sha256=frozen,unchanged_manuscript_files=len(protected),manuscript_files_unchanged_sha256=protected,paper_documentation_revision='V148',source_sha256={str(p.relative_to(R)):sha(p) for p in D.iterdir() if p.is_file() and p.name not in ['verification.json','README.md']},verifier_sha256=sha(Path(__file__)),scope='Structure and year mapping of saved provider text checked; no raw teacher FTE, all-provider upper-stage workforce or city PTR certified. No inference that matching sources are absent elsewhere.')
 (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');small={k:v for k,v in result.items() if k not in ['scientific_file_sha256','manuscript_files_unchanged_sha256','source_sha256']};(D/'verification.json').write_text(json.dumps(small,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','candidate_years','hierarchical_count_cells','geographic_level_reconciliations','primary_data_admissions','protected_scientific_files','unchanged_manuscript_files']},indent=2))
if __name__=='__main__':main()
