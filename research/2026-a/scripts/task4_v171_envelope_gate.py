"""Trace a potential one-sided school-resource bound without changing the model."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];O=R/'results/task4_v171_envelope_gate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
 student=read(R/'data/task4_v171_student_scope/student_scope.json')
 method=read(R/'data/task4_v171_bfs_scope/source_scope.json')
 assert student['admissions']==method['admitted_cells']==0
 source_files=['data/task4_v171_student_scope/student_scope.json',
  'data/task4_v171_bfs_scope/source_scope.json','data/task4_v170_zurich/source_scope.json',
  'data/task4_v170_zurich/bfs_staff_2024_25_original.xlsx']
 gates=[
  dict(id='teaching_FTE_definition',status='supported',evidence='2024/25 manual PDF19-20: activity workload C.7 / matching full-time basis C.8; category split PDF15/31.',meaning='Published SSP teaching FTE is distinct from persons, school leadership and the separate STATENT wage-model estimate.'),
  dict(id='public_private_collection_frame',status='supported',evidence='Manual PDF6-8 and23: compulsory public/private census and expected-school controls; unresolved collection gaps should be flagged (PDF7).',meaning='Positive population/control evidence; not an empirical certificate of every actual target workload.'),
  dict(id='gymnasium_stage_coding',status='supported',evidence='Manual PDF21: compulsory/post-compulsory gymnasium years separately coded.',meaning='Mixed-stage school headcounts need not be used as the teacher denominator.'),
  dict(id='city_student_target_subset_and_date',status='not_established',evidence='Re-fetched city workbook is exactly the frozen V120 source; existing V157 public upper6582/private upper1999 reused. School year2024 means2024/25, not an exact census-date certificate.',meaning='No certified lower pupil total has been selected after adult/bridging/remote and programme/date compatibility checks.'),
  dict(id='numerical_upper_teacher_enclosure',status='not_established',evidence='V170 workbook T8/T10 has one-decimal values; inspected manual/profile supply no explicit one-sided rounding/adjustment envelope.',meaning='No reported aggregate has been promoted to a guaranteed upper teacher total.'),
 ]
 gate=dict(version='V171',primary_science='V154',current_paper='V168',gates=gates,
  sufficient_relation='If 0 <= S_lower <= S_city and 0 < T_city <= T_upper for the same target activities/date, then PTR_city >= S_lower/T_upper and cost utility <= 15*T_upper/(15*T_upper+S_lower).',
  subset_rule='A certified pupil subset and teacher superset can suffice; complete exact city totals and individual personnel records are not required by this argument.',
  national_dates_rule='Other cantons may have different census dates in a nonnegative nationwide private sum; that alone does not invalidate a cover. The Zurich component must contain the target Zurich activities at the matched local date.',
  note_on_existing_data='These gates concern the proposed one-sided covering bound; they do not change the existing user point-value assumptions or adopt a new generic admission rule.',
  raw_indicator_replaced=False,pupil_lower_bound_admitted=False,teacher_upper_bound_admitted=False,
  city_PTR_computed=False,utility_interval_before=[0,1],utility_interval_after=[0,1],admitted_cells=0,
  source_sha256={n:sha(R/n) for n in source_files},
  next_action='Use a genuinely matched local pupil subset and an explicit numerical enclosure before computing a candidate. Do not repeat the public-funded chart, STATENT or registry-count substitution routes.')
 (O/'admission_gate.json').write_text(json.dumps(gate,indent=2)+'\n')
 reference=R/'results/task4_v170_staff_coverage/comparison.json'
 (O/'model_comparison_reference.json').write_text(json.dumps(dict(
  referenced_file=str(reference.relative_to(R)),sha256=sha(reference),
  source_checks='V170 recomputed160 utility cells and32 deterministic city/weight cases; reused here after unchanged V154 snapshot hashes, not rerun in V171.',
  admissions_this_iteration=0,score_width_reduction=0,comparison=read(reference)),indent=2)+'\n')
 receipts=[]
 for folder in ['task4_v171_student_scope','task4_v171_bfs_scope']:
  for row in read(R/'data'/folder/'retrieval.json'):receipts.append(dict(research_directory='data/'+folder,**row))
 (O/'source_manifest.json').write_text(json.dumps(receipts,indent=2)+'\n')
 print('V171 admission gate generated; zero numerical city bounds admitted')
if __name__=='__main__':main()
