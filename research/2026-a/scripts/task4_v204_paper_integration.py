"""Bind the reviewed V204 single manuscript without rewriting frozen evidence."""
from pathlib import Path
import hashlib, json, re, shutil, subprocess
import task4_v198_reproduce as base

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
P = G.parent / 'HiMCM-Overleaf'
O = R / 'results/task4_v204_paper_integration'
C = R / 'results/current_paper_review'
BUILD = Path('/data/scratch/himcm-v204-paper-build')
sha = base.sha
read = base.read

def write(p, value):
    p.write_text(json.dumps(value, indent=2) + '\n')

def main():
    O.mkdir(exist_ok=True)
    proof = read(C / 'current_verification.json')
    archive = O / 'previous_v203_current_verification.json'
    if not archive.exists():
        assert proof['primary_model'] == 'V203'
        shutil.copyfile(C / 'current_verification.json', archive)
    old = read(archive)
    independent = O / 'independent_review.json'
    assert independent.is_file()
    for name in old['current_files_sha256']:
        assert sha(P / name) == sha(G / 'paper/current' / name), name
    for name in ['mcmthesis.cls', 'ref.bib', 'figures/country_contrasts.pdf', 'figures/walktime_context.pdf']:
        assert sha(P / name) == old['current_files_sha256'][name], name
    source = (P / 'main.tex').read_text()
    assert len(re.findall(r'\\bibitem\{', source)) == 63
    for line in subprocess.check_output(['git', 'show', '1cbec98:main.tex'], cwd=P, text=True).splitlines():
        if 'We define' in line or '\\mcmsetup' in line or 'tcn=18213' in line:
            assert line in source, line
    for n in ['score_intervals.pdf', 'identification_matrix.pdf']:
        assert sha(P / 'figures' / n) == sha(R / 'results/task4_v204_paper_assets' / n)
    pdf = G / 'paper/current/main.pdf'
    assert sha(pdf) == sha(BUILD / 'main.pdf')
    pages = base.text_pages(pdf)
    assert len(pages) == 27
    aux = (BUILD / 'main.aux').read_text()
    label = lambda n: int(re.search(r'\\newlabel\{' + n + r'\}\{\{[^}]*\}\{(\d+)\}', aux)[1])
    assert label('main-end') == 25 and label('LastPage') == 27
    assert len(re.findall(r'\\bibcite\{', aux)) == 63
    layout = base.layout(pdf, O, pages)
    log = (BUILD / 'main.log').read_text()
    assert 'Overfull' not in log and 'undefined' not in log and 'LaTeX Warning' not in log
    snapshot = read(R / 'design/task4_user_v204_snapshot.json')
    science = dict(snapshot['source_sha256'])
    for n in ['design/task4_user_v204_snapshot.json', 'design/task4_user_v204_admissions.json']:
        science[n] = sha(R / n)
    for n, h in science.items():
        assert sha(R / n) == h, n
    inputs = {str(Path(__file__).relative_to(R)): sha(Path(__file__))}
    for folder in ['task4_v204_paper_assets', 'task4_v204_operational_rebase']:
        for p in sorted((R / 'results' / folder).rglob('*')):
            if p.is_file(): inputs[str(p.relative_to(R))] = sha(p)
    for p in [independent, R / 'scripts/task4_v204_paper_assets.py', R / 'scripts/task4_apply_v204_current_paper.py', R / 'scripts/task4_v204_reproduce.py']:
        inputs[str(p.relative_to(R))] = sha(p)
    write(O / 'verification.json', dict(status='pass', primary_model='V204',
        source_sha256=inputs, pdf_sha256=sha(pdf), main_sha256=sha(P / 'main.tex'),
        total_pages=27, main_and_references_pages=25, reference_keys=63,
        preserved_shared_class_bib_and_auxiliary_figures=True,
        approved_definition_preserved=True, **layout,
        minimum_new_figure_font_pt=10,
        visual_review='independent_review.json',
        scope='Source and local layout binding; independent scalar science and clean-HEAD rendering are checked by task4_v204_reproduce.py. No online preview or submission claim.'))
    delivery = read(C / 'delivery_verification.json')
    assert delivery['primary_model'] == 'V204' and delivery['pdf_sha256'] == sha(pdf)
    proof.update(primary_model='V204', pdf_sha256=sha(pdf), main_source_sha256=sha(P / 'main.tex'),
        total_pages=27, main_and_references_pages=25, underfull_counts=[log.count('Underfull')]*2,
        current_files_sha256={n:sha(P/n) for n in old['current_files_sha256']},
        independent_audit_sha256=sha(independent), delivery_audit_sha256=sha(C/'delivery_verification.json'),
        visual_review_sha256=sha(independent), science_bindings_verified=658,
        v204_science_sha256=science,
        scope='V204 Vienna scheduled-supply refinement; 27 pages/63 references. Shared class, bibliography, auxiliary figures and approved definition preserved. Full clean-HEAD reproduction is recorded separately.',
        vienna_378_scheduled_supply_lower_admitted=True,
        v204_integration_verification='results/task4_v204_paper_integration/verification.json',
        v204_integration_verification_sha256=sha(O/'verification.json'))
    write(C/'current_verification.json', proof)
    review_path = R/'design/task4_user_current_review.json'
    review = read(review_path)
    review.update(primary_model='V204', pdf_sha256=sha(pdf),
        scope='Single V204 main; 27 pages/63 references; fixed Oslo/equal Zurich; 16 possible and zero necessary champions.',
        revision='Owned source, numerical figures and necessary method/source explanations synchronized to V204; unrelated team content preserved.',
        target_status='V204 integrated; local reviewed PDF bound; clean-HEAD reproduction and remote synchronization recorded separately.',
        v204_integration_verification='research/2026-a/results/task4_v204_paper_integration/verification.json',
        v204_integration_verification_sha256=sha(O/'verification.json'))
    write(review_path, review)
    fixed = 15.82232695332216 - 15.776782727425475
    equal = 18.39181162388826 - 18.30212083359472
    activation = read(C/'activation.json')
    activation.update(primary='V204', core_bindings=658, primary_admissions=1,
        newly_filled_cells=0, refined_existing_partial_cells=1,
        actual_active_width_reduction=fixed, equal_weight_width_reduction=equal,
        pdf_sha256=sha(pdf), source_sha256=sha(P/'main.tex'),
        change='Vienna transport lower subset replaces 99 metro areas with 378 source-defined scheduled passenger DIVA areas; original values, weights, population and interval rules preserved.',
        condition_withholding_areas=342, possible_champions=16, necessary_champions=0,
        clean_head_reproduction='pending separate receipt', remote_synchronization='pending separate receipt')
    write(C/'activation.json', activation)
    print(json.dumps(dict(status='pass', pages=27, main_pages=25, core_bindings=658, new_science_proof_bindings=len(science))))

if __name__ == '__main__': main()
