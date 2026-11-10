"""Add checked utility-error sensitivity to the owned historical fairness block."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent
R=D.parents[1]/'HiMCM/research/2026-a'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 old=(D/'task4_v164_core.tex').read_text()
 a=old.index("For Istanbul's retained 2012")
 b=old.index('\\AgeCase',a)
 new=r'''For Istanbul's retained 2012 high-school cohort aged 14--18, let $L_{0.2}$
be the lowest-20\% weighted mean travel utility, with fractional boundary
inclusion, and $\mu$ the overall mean. Unknown utilities lie in $[0,1]$; optional membership remains uncertain. Observed weight is $W=499950$; including all
optional members gives $N_{\max}=681503$. The sharp joint bound is
$\min(\mu-L_{0.2})=(W/N_{\max})(\mu_{\mathrm{obs}}-L_{0.2,\mathrm{obs}})=0.226686$,
where ``obs'' denotes observed trips.
Including all optional members and setting unknown trips to 45 minutes attains it.
With cohort, weights and missing-data rules fixed, allowing arbitrary utility
changes to at most 5\% or 20\% of observed weighted mass leaves sharp minimum gaps
0.200134 or 0.129091, respectively. This fractional-mass relaxation uses declared
error budgets, not estimated error rates or fractions of students.
The official-portal aggregate projection, rather than original CSV bytes,
supports these historical feasibility results, not current facility-use estimates
\cite{istanbul}.

'''
 (D/'task4_v166_core.tex').write_text(old[:a]+new+old[b:])
 paper=(D/'task4_v164_paper.tex').read_text().replace('% V164 owned review;', '% V166 owned review;').replace('task4_v164_core.tex','task4_v166_core.tex')
 (D/'task4_v166_paper.tex').write_text(paper)
 (D.parent/'task4_v166_review_entry.tex').write_text('% Independent owned review; default main setting unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v166_paper.tex}\n')
 sources=['results/task4_v162_tail_error/summary.json','results/task4_v162_tail_error/witnesses.json','results/task4_v162_tail_error/verification.json','scripts/task4_v162_tail_error.py','scripts/audit_task4_v162_tail_error.py']
 manifest={'version':'V166','primary':'V154 unchanged','base_review':'V164 frozen','changed_scope':'One owned historical fairness block; add V162 utility-error sensitivity; all other paper prose, references and template unchanged','base_core_sha256':sha(D/'task4_v164_core.tex'),'source_sha256':{n:sha(R/n) for n in sources},'project_settings_changed':False,'shared_class_sha256':sha(D.parent/'mcmthesis.cls')}
 (D/'task4_v166_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('Old/new owned block word counts:',len(old[a:b].split()),len(new.split()))
if __name__=='__main__':main()
