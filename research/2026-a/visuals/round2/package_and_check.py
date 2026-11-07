from pathlib import Path
import json,hashlib,zipfile,re,shutil
import pandas as pd
import pymupdf as fitz
H=Path(__file__).resolve().parent;B=H.parents[1];ROOT=H.parents[3]
PAPER=ROOT.parent/'HiMCM-Overleaf'/H.relative_to(ROOT)
PAPER.mkdir(parents=True,exist_ok=True)
figs=json.loads((H/'figure_manifest.json').read_text());source=json.loads((H/'style_selection.json').read_text())
inputs=[B/'results/task4_access_revision'/n for n in ['point_rankings.csv','learning_access_measures.csv','matched_information_rank_bounds.csv','proxy_error_stress.json','summary.json']]+[B/'results/task4_real/normalized_indicators.csv']+[B/'data/task4_access'/f'{n}_hexes.zip' for n in ['1958','8814','2406']]
(H/'input_provenance.json').write_text(json.dumps([{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in inputs],indent=2))
# No document-class or bibliography changes; these are insertable figure environments.
tex=['% Optional figure snippets. Requires graphicx. Figures 03 and 06 are best at landscape width.\n% The included PDFs embed their fonts. These snippets are not inserted into main.tex.\n']
cap=['# Figure captions and scope\n\nLocal research figures; not inserted into the live Overleaf manuscript.\n']
for r in figs:
 name=r['name'];caption=r['caption'];caption_tex=caption.replace('%',r'\%').replace('_',r'\_').replace('&',r'\&')
 tex.append('\\begin{figure}[htbp]\n  \\centering\n  \\includegraphics[width=\\textwidth]{figures/'+name+'.pdf}\n  \\caption{'+caption_tex+'}\n  \\label{fig:revision-'+name.replace('_','-')+'}\n\\end{figure}\n')
 cap.append('## '+name+'\n\n'+caption+'\n\nStyle reference: '+r['style_reference']+'\n')
 for ext in ['png','svg','pdf']:assert (H/'figures'/f'{name}.{ext}').stat().st_size>1000
 with fitz.open(H/'figures'/f'{name}.pdf') as d:assert len(d)==1
(PAPER/'figure_inserts.tex').write_text('\n'.join(tex));(H/'CAPTIONS.md').write_text('\n'.join(cap))
(PAPER/'figures').mkdir(exist_ok=True)
for p in (H/'figures').iterdir():
 if p.is_file():shutil.copy2(p,PAPER/'figures'/p.name)
for n in ['CAPTIONS.md','figure_manifest.json']:shutil.copy2(H/n,PAPER/n)
with zipfile.ZipFile(PAPER/'overleaf_figure_pack.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in sorted((PAPER/'figures').iterdir()):z.write(p,p.relative_to(PAPER))
 for n in ['figure_inserts.tex','CAPTIONS.md','figure_manifest.json']:z.write(PAPER/n,n)
rank=pd.read_csv(B/'results/task4_access_revision/point_rankings.csv');assert len(rank)==25 and rank.city.nunique()==25
v=pd.read_csv(B/'results/task4_access_revision/matched_information_rank_bounds.csv');before=v[v.stage=='before_two_unknown'].set_index('city');after=v[v.stage!='before_two_unknown'].set_index('city').loc[before.index]
assert (after.score_lower>=before.score_lower-1e-9).all() and (after.score_upper<=before.score_upper+1e-9).all()
assert int(before.possible_champion.sum())==12 and int(after.possible_champion.sum())==3
with fitz.open(H/'redesigned_figures.pdf') as d:assert len(d)==6
with fitz.open(H/'selected_reference_book.pdf') as d:assert len(d)==8
links=re.findall(r'(?:src|href)="([^"]+)"',(H/'index.html').read_text())
for link in links:
 if '://' not in link:assert (H/link.split('#')[0]).exists(),link
print('PASS: 6 figures x 3 formats; 8 reference excerpts; 25 cities; interval nesting; 12 -> 3; all gallery links; source hashes and upload ZIP.')
