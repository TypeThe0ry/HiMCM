"""Insert the verified one-mean threshold in the owned sensitivity paragraph."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent
R=D.parent.parent/'HiMCM/research/2026-a'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    folder=R/'results/task4_v185_commute_candidate'
    proof=json.loads((folder/'verification.json').read_text());assert proof['status']=='pass'
    rows=json.loads((folder/'mean_thresholds.json').read_text())
    fixed=next(x for x in rows if x['weight_reference']=='fixed')
    equal=next(x for x in rows if x['weight_reference']=='equal')
    assert fixed['status']=='one_finite_mean_tie' and equal['status']=='Zurich_unique_for_all_nonnegative_means'
    value=f"{fixed['tie_mean_minutes']:.2f}"
    old=(D/'task4_v184_vintage.tex').read_text()
    start=old.index('Separately withdraw commute proxies')
    paragraph=r"""Replace selected commute intervals by $[0,1]$, holding other entries fixed.
Withdrawing Zurich's alone, both identified proxies or all twelve supplied
means selects Singapore under baseline weights; equal weights retain Zurich.
Dublin alone changes neither choice; all withdrawals retain sixteen possible
champions. Separately vary only Zurich's mean with Jensen bounds: baseline
weights give a regret tie near VALUE minutes, selecting Zurich below and
Singapore above. Equal weights retain Zurich for all nonnegative means,
with other data fixed.
""".replace('VALUE',value)
    (D/'task4_v186_vintage.tex').write_text(old[:start]+paragraph)
    core=(D/'task4_v184_core.tex').read_text()
    assert core.count('task4_v184_vintage.tex')==1
    (D/'task4_v186_core.tex').write_text(core.replace('task4_v184_vintage.tex','task4_v186_vintage.tex'))
    paper=(D/'task4_v184_paper.tex').read_text()
    assert paper.count('task4_v184_core.tex')==1
    (D/'task4_v186_paper.tex').write_text(paper.replace('% V184 owned review;','% V186 owned review;').replace('task4_v184_core.tex','task4_v186_core.tex'))
    (D.parent/'task4_v186_review_entry.tex').write_text('% Owned independent review; default main setting unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v186_paper.tex}\n')
    manifest=dict(version='V186',primary='V181 unchanged',base_review='V184',
        edited_scope='Only final owned5.5sensitivityparagraph and two inputpaths/versioncomment',
        threshold_mean_minutes=fixed['tie_mean_minutes'],rounded_threshold_minutes=value,
        baseline_data_changed=False,figures_references_AI_changed=False,project_settings_changed=False,
        source_sha256={str(p.relative_to(R)):sha(p) for p in [folder/'verification.json',folder/'mean_thresholds.json',R/'scripts/task4_v185_commute_candidate.py']},
        paper_input_sha256={str(p.relative_to(D.parent)):sha(p) for p in [D/'task4_v184_vintage.tex',D/'task4_v184_core.tex',D/'task4_v184_paper.tex',Path(__file__)]})
    (D/'task4_v186_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('V186 generated; threshold',value,'old/new lastparagraph words',len(old[start:].split()),len(paragraph.split()))
if __name__=='__main__':main()
