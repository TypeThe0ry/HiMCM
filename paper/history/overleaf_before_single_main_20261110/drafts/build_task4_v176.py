"""Revise only the owned MC interpretation and append its theorem reference."""
from pathlib import Path
import hashlib
import json

D = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    old = (D / 'task4_v173_core.tex').read_text()
    start = old.index('\\MonteCarloInterpretation')
    end = old.index('\\subsection{Within-city fairness and growth stages}', start)
    replacement = (D / 'task4_v176_mc_interpretation.tex').read_text()
    (D / 'task4_v176_core.tex').write_text(old[:start] + replacement + '\n' + old[end:])
    paper = (D / 'task4_v173_paper.tex').read_text()
    paper = paper.replace('% V173 owned review;', '% V176 owned review;')
    paper = paper.replace('task4_v173_core.tex', 'task4_v176_core.tex')
    paper = paper.replace('task4_v164_references.tex', 'task4_v176_references.tex')
    (D / 'task4_v176_paper.tex').write_text(paper)
    refs = (D / 'task4_v164_references.tex').read_text()
    addition = """\\bibitem{hoeffding} W. Hoeffding.
\\textit{Probability Inequalities for Sums of Bounded Random Variables}.
1963, Theorem 2, equation (2.6).
\\url{https://doi.org/10.1080/01621459.1963.10500830}.
"""
    (D / 'task4_v176_references.tex').write_text(refs.replace('\\end{thebibliography}', addition + '\\end{thebibliography}'))
    (D.parent / 'task4_v176_review_entry.tex').write_text(
        '% Independent owned review; default main setting unchanged.\n'
        '\\RequirePackage{import}\n\\import{drafts/}{task4_v176_paper.tex}\n')
    manifest = dict(version='V176', primary='V154 unchanged', base_review='V173 frozen',
                    changed_scope='Only owned section6.3 interpretation block and one appended reference',
                    source_core_sha256=sha(D / 'task4_v173_core.tex'),
                    source_references_sha256=sha(D / 'task4_v164_references.tex'),
                    replacement_sha256=sha(D / 'task4_v176_mc_interpretation.tex'),
                    shared_class_sha256=sha(D.parent / 'mcmthesis.cls'),
                    scientific_support=['V169 simultaneous MC bands', 'V175 derived mean-rank comparisons'],
                    project_settings_changed=False)
    (D / 'task4_v176_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('V176 candidate generated; only owned MC interpretation and theorem reference changed')


if __name__ == '__main__':
    main()
