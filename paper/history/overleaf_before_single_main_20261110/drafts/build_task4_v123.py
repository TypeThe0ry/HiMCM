#!/usr/bin/env python3
"""Build selected V123 paper material from frozen V121/V122 research."""
from pathlib import Path
import argparse, hashlib, json, re
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

p=argparse.ArgumentParser()
p.add_argument('--research-root', type=Path, required=True)
a=p.parse_args(); root=a.research_root.resolve(); here=Path(__file__).resolve().parent
out=here/'task4_v123_assets'; out.mkdir(exist_ok=True)
source=here/'task4_v122_sections.tex'; original=source.read_text()
body=original.split('\\setcounter{section}{3}\n',1)[1].split('\\section*{Reproducibility and integration note}',1)[0]
revision=(here/'task4_v123_revision.tex').read_text()
body=body.replace('\\section{Model revision and extension}',revision+'\n\\section{Model revision and extension}',1)
# Redraw the one retained figure at the actual text width and >=12 pt; omit
# the redundant preference chart because the adjacent table gives its values.
body=body.replace('task4_v122_assets/score_intervals.pdf','task4_v123_assets/score_intervals.pdf')
# Keep short tables intact rather than splitting them across pages.
for name in ['indicators','baseline']:
    table=(here/f'task4_v122_tables/{name}.tex').read_text()
    table=table.replace('\\begin{longtable}', '\\begin{table}[htbp]\\centering\n\\begin{tabular}', 1)
    # Extract caption ahead of tabular and discard the repeat-header block.
    match=re.search(r'(\\caption.*?)(?:\\\\\n)',table,flags=re.S)
    assert match
    caption=match.group(1)
    table=table[:match.start()]+table[match.end():]
    table=table.replace('\\centering\n','\\centering\n'+caption+'\n',1)
    table=re.sub(r'\\endfirsthead.*?\\endhead\n','',table,flags=re.S)
    table=table.replace('\\end{longtable}', '\\end{tabular}\n\\end{table}')
    (out/f'{name}.tex').write_text(table)
    body=body.replace(f'task4_v122_tables/{name}.tex',f'task4_v123_assets/{name}.tex')
body=body.replace('\\subsection{A significant revision:', '\\FloatBarrier\n\\subsection{A significant revision:',1)

pattern=r'\\begin\{figure\}\[htbp\]\n\\centering\n\\includegraphics\[width=\\linewidth\]\{task4_v122_assets/preference_frequencies.pdf\}.*?\\end\{figure\}'
body,n=re.subn(pattern,'',body,flags=re.S); assert n==1
(here/'task4_v123_core.tex').write_text('% Generated from the owned V122 chapter contribution; do not hand-edit.\n'+body.rstrip()+'\n')
refs='\\begin{thebibliography}{20}'+original.split('\\begin{thebibliography}{20}',1)[1].split('\\end{document}',1)[0]
refs=refs.replace('\\end{thebibliography}',r'''\bibitem{openai} OpenAI. Codex, AI-assisted research, coding, checking and writing environment. Used November 2026; exact deployed model build not retained in this draft's metadata. \url{https://openai.com/codex/}.
\end{thebibliography}''')
(here/'task4_v123_references.tex').write_text('% Generated from the owned V122 references, with an AI-tool entry.\n'+refs)
ranks=root/'results/task4_user_v121_revision/current_ranks.csv'
df=pd.read_csv(ranks); df=df[df.weight_reference.eq('fixed')].sort_values('decision_rank'); assert len(df)==16
plt.rcParams.update({'font.size':12.5,'axes.labelsize':12.5,'xtick.labelsize':12.5,'ytick.labelsize':12.5,'pdf.fonttype':42,'svg.fonttype':'none'})
fig,ax=plt.subplots(figsize=(6.45,5.6)); fig.subplots_adjust(left=.25,right=.96,bottom=.16,top=.97)
y=list(range(len(df))); lo=df.score_lower.to_numpy(); hi=df.score_upper.to_numpy()
ax.hlines(y,lo,hi,color='#526678',linewidth=2.3)
ax.scatter(lo,y,marker='|',s=100,c='#526678'); ax.scatter(hi,y,marker='|',s=100,c='#526678')
ax.hlines(0,lo[0],hi[0],color='#006c67',linewidth=4)
ax.set_yticks(y,df.city); ax.invert_yaxis(); ax.set_xlim(40,75); ax.set_xticks([40,50,60,70]); ax.set_xlabel('TOPSIS score bound (0–100)')
ax.grid(axis='x',alpha=.2); ax.set_axisbelow(True); ax.tick_params(axis='y',length=0)
for side in ['top','right','left']: ax.spines[side].set_visible(False)
for suffix in ['pdf','svg','png']: fig.savefig(out/f'score_intervals.{suffix}',dpi=300)
svg=out/'score_intervals.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
plt.close(fig)
df.to_csv(out/'score_intervals.csv',index=False)
diag=root/'results/task4_v123_revision_diagnostic/summary.json'; d=json.loads(diag.read_text())
f=d['results'][0]; assert f['changed_city_decision_ranks']==13 and f['midpoint_scenario_first']=='Zurich'
assert d['uncertain_cells_retained']==48 and len(f['possible_champions'])==16
files=[source,*[here/f'task4_v123_{name}.tex' for name in ['revision','front','conclusion','news','ai','paper']],here/'task4_v122_generated.tex',here/'task4_v122_assets/manifest.json',ranks,diag,root/'design/task4_user_current_model.json',root/'data/task4_v117_team_intake/city_indicators.csv']
manifest={'evidence':'V121 user16; V122 extensions; V123 controlled formulation diagnostic','body_source':'Owned V122 chapter, with controlled-revision subsection and one regenerated figure','figure_width_inches':6.45,'insert_width_mm':164,'minimum_figure_font_source_pt':12.5,'minimum_figure_font_inserted_pt':12.5*(164/25.4)/6.45,'sources':{str(x.relative_to(root)) if x.is_relative_to(root) else str(x.relative_to(here)):hashlib.sha256(x.read_bytes()).hexdigest() for x in files},'protected_files':{x:hashlib.sha256((here.parent/x).read_bytes()).hexdigest() for x in ['main.tex','ref.bib','mcmthesis.cls','drafts/task4_v119_sections.tex','drafts/task4_v119_sections.pdf','drafts/task4_v122_sections.tex','drafts/task4_v122_sections.pdf']}}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'status':'built','cities':len(df),'minimum_final_figure_font':manifest['minimum_figure_font_inserted_pt']}))
