"""Clarify the owned historical-gap paragraph; retain frozen V154 science."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent
R=Path('/data/projects/HiMCM/research/2026-a')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 s=json.loads((R/'results/task4_v158_joint_gap/summary.json').read_text());row=next(x for x in s['rows'] if x['alpha']==.2)
 assert f"{row['sharp_joint_lower']:.6f}"=='0.226686'
 old=(D/'task4_v159_core.tex').read_text();start=old.index('Citywide facilities per resident');end=old.index('\\EquityCase',start)
 intro='''Citywide facilities per resident measure supply. Student access additionally
depends on fees, opening hours, transport, disability access and location;
identifying its distribution requires matched students and qualifying facilities.

'''
 text=old[:start]+intro+old[end:]
 a=text.index("For Istanbul's retained");z=text.index('\\AgeCase',a)
 paragraph=r'''For Istanbul's retained 2012 high-school cohort aged 14--18, let $L_{0.2}$
be the lowest-20\% weighted mean travel utility, with fractional boundary
inclusion, and $\mu$ the overall mean. Keep unknown utilities in $[0,1]$ and
optional membership uncertain. Observed trips have total weight $W=499950$;
including every optional member gives maximum weight $N_{\max}=681503$.
The sharp joint bound is
$\min(\mu-L_{0.2})=(W/N_{\max})(\mu_{\mathrm{obs}}-L_{0.2,\mathrm{obs}})=0.226686$,
where ``obs'' denotes observed trips. Including all optional members and setting
every unknown trip to 45 minutes attains $\mu=0.374445$, $L_{0.2}=0.147759$.
The recovered aggregates are an official-portal projection, not original CSV
bytes; this historical feasibility result does not estimate current facility
use \cite{istanbul}.

'''
 text=text[:a]+paragraph+text[z:]
 a=text.index('Age can affect observed travel,');z=text.index('\\clearpage',a)
 ending=r'''Comparing exact ages fourteen and eighteen requires matched resident utilities
$u_{ij}^{(14)},u_{ij}^{(18)}$ and separately elicited weights
$w_j^{(14)},w_j^{(18)}$. Our analyst preference scenarios carry no age labels.

'''
 text=text[:a]+ending+text[z:]
 a=text.index('To extend the same education criterion');z=text.index("For Istanbul's retained",a)
 district=r'''For districts $d$ with pupil counts $n_d$ and pupil--teacher ratios $r_d$,
the pupil-weighted utility is
$\bar u=\sum_d n_d\,15/(15+r_d)/\sum_dn_d$.
Its difference from pooled utility reflects aggregation; school-location data
establish neither resident travel access nor policy effects.

'''
 text=text[:a]+district+text[z:]
 (D/'task4_v160_core.tex').write_text(text)
 paper=(D/'task4_v159_paper.tex').read_text().replace('V159 owned candidate','V160 owned review').replace('task4_v159_core','task4_v160_core')
 (D/'task4_v160_paper.tex').write_text(paper)
 (D.parent/'task4_v160_review_entry.tex').write_text('% Independent review; default main setting unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v160_paper.tex}\n')
 manifest=dict(version='V160',base='V159 frozen',primary_model='V154 unchanged',scope='Four prose blocks in owned section 6.4; define joint-bound weights and uncertainty, condense repeated access, aggregation and age-measurement explanations',source_sha256={n:sha(R/n) for n in ['results/task4_v158_joint_gap/summary.json','results/task4_v158_joint_gap/verification.json']},base_core_sha256=sha(D/'task4_v159_core.tex'),team_content_changed=False,project_settings_changed=False)
 (D/'task4_v160_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('V160 owned review prepared.')
if __name__=='__main__':main()
