"""Integrate the checked identification matrix into the owned data section."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent
R=D.parents[1]/'HiMCM/research/2026-a'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 old=(D/'task4_v166_core.tex').read_text()
 marker='The current 160 cells comprise 112 point values, 34 partial intervals and'
 assert old.count(marker)==1
 core=old.replace(marker,'Figure~\\ref{fig:identification-matrix} locates the remaining uncertainty.\n'+marker)
 boundary='\\section{Establishing the baseline evaluation model}'
 assert core.count(boundary)==1
 core=core.replace(boundary,'\\input{task4_v168_evidence_figure.tex}\n\n'+boundary)
 (D/'task4_v168_core.tex').write_text(core)
 snippet=(D/'task4_v167_evidence_assets/figure.tex').read_text()
 snippet=snippet.replace('task4_v167_evidence_assets/identification_matrix.pdf','task4_v168_evidence_assets/identification_matrix.pdf')
 snippet=snippet.replace('confidence intervals. Cities follow','confidence intervals. Travel entries retain school-travel and general-commute proxy scopes. Cities follow')
 snippet=snippet.replace('% Optional owned figure; not input by the current V166 review.','% Owned identification figure integrated in V168.')
 (D/'task4_v168_evidence_figure.tex').write_text(snippet)
 paper=(D/'task4_v166_paper.tex').read_text().replace('% V166 owned review;','% V168 owned review;').replace('task4_v166_core.tex','task4_v168_core.tex')
 (D/'task4_v168_paper.tex').write_text(paper)
 (D.parent/'task4_v168_review_entry.tex').write_text('% Independent owned review; default main setting unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v168_paper.tex}\n')
 manifest={'version':'V168','primary':'V154 unchanged','base_review':'V166 frozen','changed_scope':'One owned data-paragraph figure reference and figure input; new caption and Travel burden label retain commute-proxy scope; other existing prose and template retained','base_core_sha256':sha(D/'task4_v166_core.tex'),'figure_pdf_sha256':sha(D/'task4_v168_evidence_assets/identification_matrix.pdf'),'figure_source_manifest_sha256':sha(D/'task4_v168_evidence_assets/figure_manifest.json'),'figure_verification_sha256':sha(R/'results/task4_v167_evidence/verification.json'),'shared_class_sha256':sha(D.parent/'mcmthesis.cls'),'project_settings_changed':False}
 (D/'task4_v168_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('Generated owned V168 candidate; science and previous files unchanged')
if __name__=='__main__':main()
