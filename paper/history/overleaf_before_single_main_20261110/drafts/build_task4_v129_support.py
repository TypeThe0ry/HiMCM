"""Copy selected V129 supporting evidence without changing the V128 paper."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--research-root', type=Path, required=True)
    args = parser.parse_args()
    research = args.research_root.resolve()
    drafts = Path(__file__).resolve().parent
    manuscript = drafts.parent
    protected = [manuscript / n for n in ['main.tex', 'ref.bib', 'mcmthesis.cls']]
    protected += [p for p in drafts.glob('task4_v128*') if p.is_file()]
    protected += [p for p in (drafts / 'task4_v128_assets').rglob('*') if p.is_file()]
    before = {str(p.relative_to(manuscript)): sha(p) for p in protected}
    primary = json.loads((research / 'design/task4_user_v127_snapshot.json').read_text())
    frozen_registry = subprocess.check_output(['git', '-C', str(research.parents[1]), 'show',
        '59edddf:research/2026-a/design/task4_user_current_model.json'])
    for p, expected in primary['source_sha256'].items():
        actual = (hashlib.sha256(frozen_registry).hexdigest()
                  if p == 'design/task4_user_current_model.json' else sha(research / p))
        assert actual == expected, p
    extension = json.loads((research / 'results/task4_v128_revision/audit.json').read_text())
    assert extension['status'] == 'pass'
    assert all(sha(research / p) == expected for p, expected in extension['result_sha256'].items())
    source_paths = {
        'ai_session_manifest.json': 'data/task4_v129_ai_provenance/session_manifest.json',
        'ai_verification.json': 'data/task4_v129_ai_provenance/verification.json',
        'berlin_source_manifest.json': 'data/task4_v129_transport/manifest.json',
        'berlin_candidate_observation.json': 'data/task4_v129_transport/observations.json',
        'berlin_stations.json': 'data/task4_v129_transport/berlin_stations.json',
        'berlin_independent_review.json': 'results/task4_v129_candidate_review/audit.json',
        'priority.csv': 'results/task4_v129_priority/priority.csv',
        'recommendation_thresholds.csv': 'results/task4_v129_priority/recommendation_thresholds.csv',
        'exclusion_thresholds.csv': 'results/task4_v129_priority/exclusion_thresholds.csv',
        'candidate_lower_only_previews.csv': 'results/task4_v129_priority/candidate_lower_only_previews.csv',
        'education_nonadmissions.json': 'data/task4_v129_education/attempts.json',
        'education_verification.json': 'data/task4_v129_education/verification.json',
    }
    for p in ['data/task4_v129_ai_provenance/verification.json',
              'data/task4_v129_education/verification.json',
              'results/task4_v129_candidate_review/audit.json',
              'results/task4_v129_priority/audit.json']:
        assert json.loads((research / p).read_text())['status'] == 'pass', p
    out = drafts / 'task4_v129_support'
    out.mkdir(exist_ok=True)
    copied = {}
    for name, rel in source_paths.items():
        source = research / rel
        shutil.copyfile(source, out / name)
        assert sha(source) == sha(out / name)
        copied[name] = dict(research_path=rel, sha256=sha(source))
    assert all(sha(manuscript / p) == expected for p, expected in before.items())
    report = dict(status='pass', scientific_basis='V127 frozen user16; V128 complete review unchanged',
        primary_admissions=0, copied_sources=copied,
        protected_manuscript_sha256=before, protected_manuscript_files=len(before),
        private_transcript_copied=False, large_original_PDF_copied=False,
        support_note_sha256=sha(drafts / 'task4_v129_support_README.md'),
        own_builder_sha256=sha(Path(__file__)),
        interpretation='Selected supporting evidence only. No new primary model, paper PDF, team control number or complete AI report is claimed.')
    (out / 'manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(status='pass', selected_files=len(copied),
                         protected_manuscript_files=len(before), primary_admissions=0)))


if __name__ == '__main__':
    main()
