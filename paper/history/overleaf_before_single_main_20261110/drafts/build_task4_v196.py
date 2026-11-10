"""Correct only the owned Milan tariff printed month; reuse frozen V193 content."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent
R=D.parent.parent/'HiMCM/research/2026-a'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 proof=R/'data/task4_v196_milanpool/verification.json'
 v=json.loads(proof.read_text());assert v['status']=='pass' and v['printed_update_date']=='2025-09-09' and v['frozen_venue_set_identical']
 old=D/'task4_v193_references.tex';s=old.read_text();a='updated 9 October 2025.';b='updated 9 September 2025.'
 assert s.count(a)==1
 (D/'task4_v196_references.tex').write_text(s.replace(a,b))
 entry=D/'task4_v193_paper.tex';t=entry.read_text().replace('% V193 owned review;','% V196 owned review;')
 assert t.count('task4_v193_references.tex')==1
 (D/'task4_v196_paper.tex').write_text(t.replace('task4_v193_references.tex','task4_v196_references.tex'))
 (D.parent/'task4_v196_review_entry.tex').write_text('% Owned review; default Main unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v196_paper.tex}\n')
 out=dict(version='V196',science='V192 unchanged',base_review='V193',edit_scope='Only October→September in owned milanpool2025 reference; names/counts, URLs and all other manuscript inputs preserved',input_sha256={str(p.relative_to(D.parent)):sha(p) for p in [old,entry,Path(__file__)]},research_proof_sha256=sha(proof),teammate_content_changed=False,AI_history_extended=False)
 (D/'task4_v196_manifest.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
