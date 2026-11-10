"""Update only the owned AI record scope; retain all main scientific prose."""
from pathlib import Path
import hashlib
import json

D = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    old = (D / 'task4_v154_ai.tex').read_text()
    a = old.index('\\subsection*{Recovered records and coverage}')
    b = old.index('\\subsection*{Verification associated with this draft}', a)
    coverage = (D / 'task4_v179_coverage.tex').read_text()
    ai = old[:a] + coverage + '\n' + old[b:]
    ai = ai.replace('all 28 saved turn contexts', 'all 74 saved root turn contexts')
    (D / 'task4_v179_ai.tex').write_text(ai)
    paper = (D / 'task4_v176_paper.tex').read_text().replace('% V176 owned review;', '% V179 owned review;').replace('task4_v154_ai.tex', 'task4_v179_ai.tex')
    (D / 'task4_v179_paper.tex').write_text(paper)
    (D.parent / 'task4_v179_review_entry.tex').write_text('% Independent owned review; default main setting unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v179_paper.tex}\n')
    manifest = dict(version='V179', primary='V154 unchanged', base_review='V176 frozen',
                    changed_scope='Only owned AI coverage subsection and root model-context count;wrapper input paths/version comment',
                    base_AI_sha256=sha(D / 'task4_v154_ai.tex'), coverage_sha256=sha(D / 'task4_v179_coverage.tex'),
                    base_wrapper_sha256=sha(D / 'task4_v176_paper.tex'), shared_class_sha256=sha(D.parent / 'mcmthesis.cls'),
                    evidence='V178 fixed-prefix metadata and independent verification;private content not published',
                    main_prose_references_figures_changed=False, project_settings_changed=False)
    (D / 'task4_v179_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print('V179 owned AI scope generated; main and references retain V176 inputs')


if __name__ == '__main__':
    main()
