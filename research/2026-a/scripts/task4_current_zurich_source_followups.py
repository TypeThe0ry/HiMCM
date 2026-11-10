"""Apply a bounded evidence-classification overlay to the frozen V204 point ledger."""
from pathlib import Path
import collections,csv,hashlib,json
R=Path(__file__).resolve().parents[1];OLD=R/'results/task4_v204_operational_rebase/point_source_ledger';O=R/'results/current_zurich_source_followups'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
 old=list(csv.DictReader((OLD/'ledger.csv').open()));rows=[dict(r) for r in old];assert len(rows)==112
 target=[r for r in rows if r['city']=='Zurich' and r['indicator']=='research_he_density'];assert len(target)==1
 row=target[0];assert row['original_value']=='52.2' and row['classification']=='not_included_in_bounded_classification'
 row.update(classification='reviewed_lineage_unresolved',evidence='data/current_zurich_he_scope_followup/README.md',scope_detail='Submitted23/440935*1e6 rounds52.2; original23-roster not identified. Canton seven-institution analysis and eight dated accreditations do not establish municipal complete count or campus scope. ROR23 includes secondary-school and administrative records.',next_evidence_needed='Original roster/extraction, or separately defined complete municipal institution/campus inventory with dated accreditation, addresses, duplicate rules and matching geography/population; do not equate canton selection or accreditation rows with a municipal count.')
 changed=[]
 allowed={'classification','evidence','scope_detail','next_evidence_needed'}
 for before,after in zip(old,rows):
  diffs=[k for k in before if before[k]!=after[k]]
  if diffs:assert set(diffs)<=allowed;changed.append(dict(city=after['city'],indicator=after['indicator'],fields=diffs))
 assert len(changed)==1
 prior=list(csv.DictReader((OLD/'review_priority.csv').open()))
 keyed={(r['city'],r['indicator']):r for r in rows}
 priority=[keyed[(r['city'],r['indicator'])] for r in prior]
 for before,after in zip(prior,priority):
  assert all(before[k]==after[k] for k in before if k not in allowed)
 O.mkdir(exist_ok=True)
 for n,items in [('ledger.csv',rows),('review_priority.csv',priority)]:
  with (O/n).open('w') as f:
   w=csv.DictWriter(f,fieldnames=list(items[0]),lineterminator='\n');w.writeheader();w.writerows(items)
 sources=[Path(__file__),OLD/'ledger.csv',OLD/'review_priority.csv']
 for name in ['current_zurich_he_scope_followup','current_zurich_ptr_matching_followup','current_swiss_apprentice_access']:
  for n in ['verification.json','peer_review.json']:sources.append(R/'results'/name/n)
 report=dict(status='pass bounded evidence overlay',primary_model='V204 unchanged',point_records=112,changed_records=changed,numeric_values_years_flags_risk_fields_and_priority_order_unchanged=True,classification_counts=dict(collections.Counter(r['classification'] for r in rows)),source_sha256={str(p.relative_to(R)):sha(p) for p in sources},output_sha256={n:sha(O/n) for n in ['ledger.csv','review_priority.csv']},primary_admissions=0,actual_primary_width_reduction=0,changes_primary_model=False,changes_manuscript=False,scope='One reviewed-unresolved classification replaces an unclassified Zurich HE entry. New canton pupils and national apprentice context remain supporting material; no raw values or risk scores replaced.')
 (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','point_records','changed_records','classification_counts']}))
if __name__=='__main__':main()
