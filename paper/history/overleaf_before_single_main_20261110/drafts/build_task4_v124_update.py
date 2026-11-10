#!/usr/bin/env python3
"""Build the V124 evidence-update tables without changing the frozen V123 paper."""
from pathlib import Path
import argparse,hashlib,json
import pandas as pd
p=argparse.ArgumentParser();p.add_argument('--research-root',type=Path,required=True);a=p.parse_args();r=a.research_root.resolve();here=Path(__file__).resolve().parent;out=here/'task4_v124_assets';out.mkdir(exist_ok=True)
base=r/'results/task4_user_v124_revision';s=json.loads((base/'summary.json').read_text());assert s['changed_cells']==2 and s['protected_nonmissing_cells']==139
rows=pd.read_csv(base/'all_ranks.csv');before=rows[(rows.scenario=='before')&(rows.weight_reference=='fixed')];after=rows[(rows.scenario=='after_conditional')&(rows.weight_reference=='fixed')];assert len(before)==len(after)==16
bs=next(x for x in s['results'] if x['scenario']=='before' and x['weight_reference']=='fixed');ns=next(x for x in s['results'] if x['scenario']=='after_conditional' and x['weight_reference']=='fixed');reduction=100*(bs['mean_width']-ns['mean_width'])/bs['mean_width']
tex='\\newcommand{\\WidthBefore}{'+f"{bs['mean_width']:.5f}"+'}\n\\newcommand{\\WidthAfter}{'+f"{ns['mean_width']:.5f}"+'}\n\\newcommand{\\WidthReduction}{'+f'{reduction:.3f}'+'}\n'
tex+=r'''\begin{table}[htbp]\centering
\caption{Two facility lower bounds improve score precision. Fixed weights and all other evidence stay fixed.}
\begin{tabular}{lrrrr}\toprule
City & Old lower & New lower & Upper & Decision rank\\\midrule
'''
for c in ['Madrid','Tokyo']:
 b=before[before.city==c].iloc[0];n=after[after.city==c].iloc[0];assert b.decision_rank==n.decision_rank
 tex+=f'{c} & {b.score_lower:.5f} & {n.score_lower:.5f} & {n.score_upper:.5f} & {int(n.decision_rank)} \\\\\n'
tex+='\\bottomrule\\end{tabular}\\end{table}\n';(out/'numbers.tex').write_text(tex)
files=[base/'summary.json',base/'all_ranks.csv',base/'revision_audit.json',r/'design/task4_user_v124_admissions.json',r/'results/task4_v124_priority/summary.json']
protected=['main.tex','ref.bib','mcmthesis.cls','drafts/task4_v123_paper.tex','drafts/task4_v123_paper.pdf','drafts/task4_v122_sections.tex','drafts/task4_v122_sections.pdf']
m={'version':'V124 standalone evidence update; V123 full review remains frozen on V121','research_sources':{str(x.relative_to(r)):hashlib.sha256(x.read_bytes()).hexdigest() for x in files},'protected_manuscript_files':{x:hashlib.sha256((here.parent/x).read_bytes()).hexdigest() for x in protected},'fixed_width_reduction_percent':reduction,'current_registry_version':json.loads((r/'design/task4_user_current_model.json').read_text())['version']}
assert m['current_registry_version']=='V124';(out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print('V124 update numbers generated')
