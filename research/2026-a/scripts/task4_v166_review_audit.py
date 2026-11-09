"""Check a one-block owned revision, historical error witnesses and current delivery facts."""
from pathlib import Path
from collections import Counter
import csv, hashlib, json, math, re, subprocess, tempfile, unicodedata
import xml.etree.ElementTree as ET
import numpy as np
from scipy.optimize import linprog

R = Path(__file__).resolve().parents[1]
P = R.parents[2] / 'HiMCM-Overleaf'
O = R / 'results/task4_v166_review'
T = Path('/data/scratch')


def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):
    return ' '.join(re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)', '', unicodedata.normalize('NFKC', s)).split())
def text(p): return subprocess.check_output(['pdftotext', '-layout', str(p), '-'], text=True)
def table(name, rows):
    with (O / name).open('w') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)


def main():
    manifest = read(P / 'drafts/task4_v166_manifest.json')
    assert sha(P / 'drafts/task4_v164_core.tex') == manifest['base_core_sha256']
    for n, h in manifest['source_sha256'].items(): assert sha(R / n) == h, n
    sdir = R / 'results/task4_v162_tail_error'
    s, certificate, witnesses = [read(sdir / n) for n in ['summary.json', 'verification.json', 'witnesses.json']]
    for n, h in certificate['result_sha256'].items(): assert sha(sdir / n) == h, n
    for n, h in s['source_sha256'].items(): assert sha(R / n) == h, n
    assert sha(R / 'scripts/task4_v162_tail_error.py') == s['generator_sha256']
    assert sha(R / 'scripts/audit_task4_v162_tail_error.py') == certificate['verifier_sha256']
    assert certificate['successful_mass_LPs'] == 8589 and certificate['threshold_candidates'] == 1227
    assert s['alpha'] == .2 and not s['error_rates_estimated'] and not s['raw_record_source_upgraded']
    source = read(R / 'data/task4_v116_ibb/aggregate_results.json')
    cells = sorted((math.exp(-float(t) / 30), float(row['weight'])) for t, row in source['duration_histogram'].items())
    observed_weight = sum(w for q, w in cells)
    assert observed_weight == s['observed_weight'] == 499950
    assert source['summary']['weight_unknown'] == s['known_unknown_weight'] == 177066
    assert source['optional_membership']['weight_total'] == s['optional_weight'] == 4487
    assert sum([observed_weight, s['known_unknown_weight'], s['optional_weight']]) == s['max_denominator'] == 681503
    checks = []
    for delta in [0, .05, .2]:
        row = next(x for x in s['rows'] if x['observed_weight_error_fraction'] == delta)
        witness = next(x for x in witnesses if x['delta'] == delta)
        bins = witness['bins']
        np.testing.assert_allclose([(b['original_utility'], b['original_weight']) for b in bins], cells, atol=1e-15, rtol=0)
        kept = np.array([b['kept_weight'] for b in bins])
        edited = np.array([b['editable_weight'] for b in bins])
        np.testing.assert_allclose(kept + edited, [w for q, w in cells], atol=1e-9, rtol=0)
        assert np.all(kept >= 0) and np.all(edited >= -1e-9)
        assert abs(edited.sum() - delta * observed_weight) < 1e-6
        masses = np.r_[kept, edited.sum() + s['known_unknown_weight'] + s['optional_weight']]
        utilities = np.r_[[q for q, w in cells], witness['reassigned_utility']]
        N = masses.sum(); assert abs(N - 681503) < 1e-6
        lp = linprog(utilities, A_eq=np.ones((1, len(masses))), b_eq=[.2*N], bounds=[(0, float(w)) for w in masses], method='highs')
        assert lp.success
        gap = float(np.dot(utilities, masses)/N - lp.fun/(.2*N))
        assert abs(gap - row['sharp_gap_in_fractional_mass_set']) < 1e-11
        checks.append(dict(delta=delta, gap=gap, edited_weight=float(edited.sum())))
    snapshot = read(R / 'design/task4_user_v154_snapshot.json')['source_sha256']
    for n, h in snapshot.items(): assert sha(R / n) == h, n
    protected = read(O / 'protected_files.json')['manuscript']
    for n, h in protected.items():
        if n != 'drafts/task4_current_review.json': assert sha(P / n) == h, n
    old = (P / 'drafts/task4_v164_core.tex').read_text()
    new = (P / 'drafts/task4_v166_core.tex').read_text()
    a, b = old.index("For Istanbul's retained 2012"), old.index('\\AgeCase', old.index("For Istanbul's retained 2012"))
    c, d = new.index("For Istanbul's retained 2012"), new.index('\\AgeCase', new.index("For Istanbul's retained 2012"))
    assert old[:a] == new[:c] and old[b:] == new[d:]
    assert 'where ``obs\'\' denotes observed trips' in new[c:d]
    assert all(x in new[c:d] for x in ['0.200134', '0.129091', 'fractional-mass', 'not estimated error rates or fractions of students'])
    paper = (P / 'drafts/task4_v166_paper.tex').read_text()
    expected = (P / 'drafts/task4_v164_paper.tex').read_text().replace('% V164 owned review;', '% V166 owned review;').replace('task4_v164_core.tex', 'task4_v166_core.tex')
    assert paper == expected
    assert sha(P / 'mcmthesis.cls') == manifest['shared_class_sha256']
    pdf = P / 'drafts/task4_v166_paper.pdf'
    pdftext = text(pdf); pages = [norm(x) for x in pdftext.split('\f') if x.strip()]
    assert len(pages) == 25 and norm(pdftext) == norm(text(T / 'himcm_v166_proxy/task4_v166_review_entry.pdf'))
    assert all(x in pages[0] for x in ['Summary', 'Problem Chosen', 'Team Control Number', 'Keywords'])
    assert 'Page 1 of' not in pages[0]
    for i, page in enumerate(pages[1:], 2):
        assert re.search(r'Team\s*#\s*PENDING', page) and f'Page {i} of 25' in page
    aux = (T / 'himcm_v166_build/task4_v166_paper.aux').read_text()
    for label, page in [('news-start', 17), ('news-end', 18), ('main-end', 23), ('LastPage', 25)]:
        assert int(re.search(r'\\newlabel\{'+label+r'\}\{\{[^}]*\}\{(\d+)\}', aux)[1]) == page
    assert len(re.findall(r'\\bibcite\{', aux)) == 49
    bbox = ET.parse(T / 'himcm_v166_bbox.html').getroot().findall('.//{http://www.w3.org/1999/xhtml}page')
    assert len(bbox) == 25
    for i, page in enumerate(bbox):
        assert (float(page.get('width')), float(page.get('height'))) == (612, 792)
        words = page.findall('.//{http://www.w3.org/1999/xhtml}word')
        assert not [w for w in words if float(w.get('yMin')) > 745]
        if i:
            top = [w for w in words if float(w.get('yMin')) < 65]
            assert any(w.text == 'Team' and 70 < float(w.get('xMin')) < 74 for w in top)
            assert any(w.text == 'Page' and float(w.get('xMin')) > 450 for w in top)
    logs = [(O / n).read_text() for n in ['direct_build.log', 'proxy_build.log']]
    assert all('Overfull' not in x and 'undefined' not in x and 'LaTeX Warning' not in x for x in logs)
    assert [x.count('Underfull') for x in logs] == [2, 2]
    rows = list(csv.DictReader((R / 'results/task4_v164_review/requirements.csv').open()))
    old_status = {r['id']: r['status'] for r in rows}
    updates = {
        'PA-sample': 'Current unchanged factory verifies 16 cities x 10 indicators; primary ranking table page 10',
        'PA-data': 'Data section, source examples and 49 compiled references; 22 supplements explicitly cited',
        'PA-news': 'News occupies pages 17-18 and explains evidence ranges and common scoring yardsticks',
        'PA-references': 'Actual references follow news and occupy pages 19-23;49 compiled entries',
        'PA-ai-section': 'Appendix starts page 24 after the23 main/reference pages and is explicitly incomplete',
        'CI-budget': '23 main/reference pages; two additional provisional AI pages',
        'CI-file': f'{pdf.stat().st_size} bytes; one current owned PDF',
        'U-perturbation': 'Dirichlet preference and bounded future-shock experiments; historical utility-only fractional-mass error budgets5%/20%',
        'AI-verification': 'V154 scientific audits; V162 frozen8589-LP certificate and V166 three witness-tail LPs; V161/V163 collection-case audits; current owned content/format checks',
        'TEAM-independent-entry': 'V166 native-format direct and root-proxy builds;25 pages; normalized text equal; no overfull boxes;2 reviewed underfull paragraphs',
        'TEAM-shared-build': 'Archived V164 actual shared-entry log stops at missing framework.png; shared source/assets unchanged; not rebuilt this iteration',
    }
    for row in rows:
        hits = []
        for marker in json.loads(row['passage_markers']):
            found = [i for i, p in enumerate(pages, 1) if norm(marker).lower() in p.lower()]
            assert found, (row['id'], marker); hits += found
        if hits: row['pdf_pages'] = ','.join(map(str, sorted(set(hits))))
        if row['id'] in updates: row['evidence'] = updates[row['id']]
        if row['id'] == 'CI-budget': row['scope_or_remaining_action'] = 'Two main pages remain under the retained25-page limit; no submission readiness inferred'
    rows.append(dict(id='U-fairness-error', authority='User perturbation and fairness tasks / V162 retained historical evidence',
                     requirement='Show whether the historical lower-tail gap persists under declared utility errors', status='reviewed_scoped', pdf_pages='15',
                     evidence='Fixed cohort/weights/unknown rules; fractional observed weighted mass budgets5%/20%; sharp gaps0.200134/0.129091; three witnesses independently recomputed',
                     scope_or_remaining_action='Istanbul2012 retained aggregate set; hypothetical budgets; not whole-person sharpness, estimated error rates or current student access',
                     passage_markers=json.dumps(['0.200134', '0.129091', 'not estimated error rates or fractions of students'])))
    assert len(rows) == 43 and all(r['status'] == old_status[r['id']] for r in rows if r['id'] in old_status)
    pending = [r['id'] for r in rows if r['status'] in {'partial', 'unverified', 'awaiting_team', 'not_ready', 'not_performed'}]
    assert len(pending) == 14
    table('requirements.csv', rows)
    with tempfile.TemporaryDirectory(dir=T, prefix='himcm-v166-font-') as td:
        prefix = Path(td) / 'font'
        subprocess.run(['pdftohtml', '-xml', '-i', '-zoom', '1', '-fontfullname', str(pdf), str(prefix)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        xml = ET.parse(prefix.with_suffix('.xml')).getroot(); fonts = {}; seen = Counter(); small = []
        for page in xml.findall('page'):
            for f in page.findall('fontspec'): fonts[f.get('id')] = f.attrib
            for item in page.findall('text'):
                value = ''.join(item.itertext()).strip()
                if not value: continue
                font = fonts[item.get('font')]; size = int(font['size']); family = re.sub(r'^[A-Z]{6}\+', '', font['family']); seen[size, family] += 1
                if size < 12: small.append(dict(pdf_page=int(page.get('number')), top=int(item.get('top')), rounded_size=size, font_family=family, text=value, role='template_header' if int(item.get('top')) < 65 else 'math_script'))
    assert all(x['rounded_size'] == (11 if x['role'] == 'template_header' else 8) for x in small)
    table('font_inventory.csv', [dict(rounded_size=k[0], font_family=k[1], text_spans=v) for k, v in sorted(seen.items())]); table('small_spans.csv', small)
    visual = read(O / 'visual_review.json')
    assert visual['all25_pages_reviewed'] and visual['pdf_sha256'] == sha(pdf)
    pixels = read(O / 'pixel_comparison.json')
    assert visual['pixel_comparison_sha256'] == sha(O / 'pixel_comparison.json')
    assert pixels['current_pdf_sha256'] == sha(pdf) and pixels['base_pdf_sha256'] == sha(P / 'drafts/task4_v164_paper.pdf')
    assert [r['page'] for r in pixels['changed_pages']] == [15, 16] and len(pixels['identical_pages']) == 23
    registry = read(R / 'design/task4_user_current_review.json')
    assert registry == read(P / 'drafts/task4_current_review.json') and registry['version'] == 'V166' and registry['pdf_sha256'] == sha(pdf)
    result = dict(status='pass', version='V166', primary_model='V154 unchanged', total_pages=25, main_and_references_pages=23, news_pages=[17,18], AI_pages=[24,25], compiled_references=49,
                  scientific_files_unchanged=len(snapshot), manuscript_files_unchanged=len(protected)-1, owned_pointer_files_changed=['drafts/task4_current_review.json'],
                  shared_main_ref_class_unchanged=True, changed_prose='One owned historical fairness block', all25_pages_visually_reviewed=True, direct_root_text_equal=True,
                  native_header_footer_bbox_checked=True, overfull_boxes=0, underfull_paragraphs_per_build=2, requirements=len(rows), prior42_statuses_preserved=True, pending_gates_preserved=pending,
                  historical_witness_tail_LPs=3, historical_witness_results=checks, frozen_V162_mass_LP_certificate_verified_by_hash=True, full8589_LPs_rerun=False,
                  template_header_small_spans=sum(x['role']=='template_header' for x in small), math_script_small_spans=sum(x['role']=='math_script' for x in small),
                  primary_data_admissions=0, primary_score_width_change=0, submission_ready=False, AI_history_complete=False, server_compile_verified=False, default_main_setting_changed=False,
                  pdf_bytes=pdf.stat().st_size, pdf_sha256=sha(pdf), verifier_sha256=sha(Path(__file__)))
    (O / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
