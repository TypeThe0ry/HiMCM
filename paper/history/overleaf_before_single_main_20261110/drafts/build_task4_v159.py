"""Owned candidate review: add the audited joint access gap, freeze V154."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent
R=Path('/data/projects/HiMCM/research/2026-a')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    s=json.loads((R/'results/task4_v158_joint_gap/summary.json').read_text())
    row=next(x for x in s['rows'] if x['alpha']==.2)
    assert abs(row['sharp_joint_lower']-.22668552699248706)<1e-12
    old=(D/'task4_v154_core.tex').read_text()
    start=old.index('For future access measurement,')
    end=old.index('\\AgeCase',start)
    new=r'''For Istanbul's retained 2012 high-school cohort aged 14--18, let $L_{0.2}$ be
the lowest-20\% weighted mean travel utility, with fractional boundary inclusion,
and $\mu$ the overall mean. Their sharp joint gap is
$\min(\mu-L_{0.2})=(499950/681503)(\mu_{\mathrm{obs}}-L_{0.2,\mathrm{obs}})=0.226686$;
``obs'' denotes observed trips. Including all optional members and setting every
unknown trip to 45 minutes attains $\mu=0.374445$, $L_{0.2}=0.147759$.
The recovered aggregates are an official-portal projection, not original CSV
bytes; this historical feasibility result does not estimate current facility
use \cite{istanbul}.

'''
    core=old[:start]+new+old[end:]
    (D/'task4_v159_core.tex').write_text(core)
    paper=(D/'task4_v154_paper.tex').read_text().replace('task4_v154_core.tex','task4_v159_core.tex')
    (D/'task4_v159_paper.tex').write_text('% V159 owned candidate; V154 evidence and unchanged parts retained.\n'+paper)
    (D.parent/'task4_v159_review_entry.tex').write_text('% Independent candidate; project main setting unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v159_paper.tex}\n')
    manifest=dict(version='V159 candidate; not current',base_paper='V154',changed_scope='Replace future-access paragraph in owned section 6.4 with V158 sharp historical gap; all other core text exact',
                  source_sha256={'results/task4_v158_joint_gap/summary.json':sha(R/'results/task4_v158_joint_gap/summary.json'),'results/task4_v158_joint_gap/verification.json':sha(R/'results/task4_v158_joint_gap/verification.json')},
                  frozen_base_core_sha256=sha(D/'task4_v154_core.tex'),body_changes=1,current_model='V154 unchanged',project_settings_changed=False,AI_history_complete=False)
    (D/'task4_v159_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('V159 candidate prepared; one replacement block.')

if __name__=='__main__':main()
