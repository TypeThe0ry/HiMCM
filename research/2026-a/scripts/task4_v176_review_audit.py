"""Check the owned MC prose boundary, numerical claims and rendered delivery."""
from pathlib import Path
from decimal import Decimal, localcontext
from collections import Counter
import csv
import json
import re
import subprocess
import xml.etree.ElementTree as E
from task4_v172_review_audit import norm, pdftext, rows, read, sha

R = Path(__file__).resolve().parents[1]
P = R.parents[2] / 'HiMCM-Overleaf'
D = P / 'drafts'
O = R / 'results/task4_v176_mc_paper'
T = Path('/data/scratch')


def table(name, records):
    with (O / name).open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(records)


def main():
    protected = read(O / 'protected_files.json')
    for name, expected in protected['science'].items():
        assert sha(R / name) == expected, name
    for name, expected in protected['paper'].items():
        if name != 'drafts/task4_current_review.json':
            assert sha(P / name) == expected, name
    old = (D / 'task4_v173_core.tex').read_text()
    new = (D / 'task4_v176_core.tex').read_text()
    replacement = (D / 'task4_v176_mc_interpretation.tex').read_text()
    a = old.index('\\MonteCarloInterpretation')
    b = old.index('\\subsection{Within-city fairness and growth stages}', a)
    assert new == old[:a] + replacement + '\n' + old[b:]
    refs = (D / 'task4_v176_references.tex').read_text()
    original_refs = (D / 'task4_v164_references.tex').read_text()
    addition = refs[refs.index('\\bibitem{hoeffding}'):refs.index('\\end{thebibliography}')]
    assert refs.replace(addition, '') == original_refs
    # Three unchanged entries are expanded from the retained reference macro.
    assert refs.count('\\bibitem') == original_refs.count('\\bibitem') + 1 == 47
    assert (D / 'task4_v176_paper.tex').read_text() == (D / 'task4_v173_paper.tex').read_text().replace('% V173 owned review;', '% V176 owned review;').replace('task4_v173_core.tex', 'task4_v176_core.tex').replace('task4_v164_references.tex', 'task4_v176_references.tex')
    manifest = read(D / 'task4_v176_manifest.json')
    for path, key in [('task4_v173_core.tex', 'source_core_sha256'), ('task4_v164_references.tex', 'source_references_sha256'), ('task4_v176_mc_interpretation.tex', 'replacement_sha256')]:
        assert sha(D / path) == manifest[key]
    assert sha(P / 'mcmthesis.cls') == manifest['shared_class_sha256']
    source = read(R / 'results/task4_v169_mc_precision/source.json')
    assert sha(R / 'results/task4_v169_mc_precision/hoeffding_1963.pdf') == source['sha256']
    assert source['doi'] in addition
    prior = read(R / 'results/task4_v169_mc_precision/summary.json')
    assert (prior['base_means'], prior['settings'], prior['draws_per_setting']) == (2064, 37, 10000)
    for name, expected in prior['input_sha256'].items():
        assert sha(R / name) == expected, name
    with localcontext() as context:
        context.prec = 50
        epsilon = ((Decimal(4128) / Decimal('.05')).ln() / Decimal(20000)).sqrt()
        assert epsilon * 100 <= Decimal('2.38')
        assert epsilon * 15 <= Decimal('.357')
    mc = rows(R / 'results/task4_v154_preferences/mc_city_summary.csv')
    selected = {x['city']: x for x in mc if x['profile'] == 'baseline' and x['concentration'] == '100'}
    assert float(selected['Oslo']['mean_decision_rank']) == 2.1092
    assert float(selected['Zurich']['mean_decision_rank']) == 2.2620
    assert float(selected['Zurich']['minimax_recommendation_frequency']) > float(selected['Oslo']['minimax_recommendation_frequency'])
    pairs = rows(R / 'results/task4_v175_mean_rank_comparisons/pairs.csv')
    pair = next(x for x in pairs if x['family'] == 'preferences' and json.loads(x['setting']) == {'profile': 'baseline', 'concentration': '100'} and x['city_a'] == 'Oslo' and x['city_b'] == 'Zurich')
    assert Decimal('-.867') <= Decimal(pair['gap_lower']) <= 0 <= Decimal(pair['gap_upper']) <= Decimal('.561')
    assert pair['classification'] == 'unresolved'
    for marker in ['At baseline concentration 100', 'smaller sample mean', '2064', '37 settings', 'independent, identically distributed', 'shared draws across outputs', 'expected mean-rank order unresolved', 'simulation laws']:
        assert norm(marker) in norm(replacement), marker
    pdf = D / 'task4_v176_paper.pdf'
    pages = [norm(x) for x in pdftext(pdf).split('\f') if x.strip()]
    proxy = T / 'himcm_v176_proxy/task4_v176_review_entry.pdf'
    assert pages == [norm(x) for x in pdftext(proxy).split('\f') if x.strip()]
    assert len(pages) == 26 and 'Numerical precision' in pages[14] and 'Hoeffding' in pages[23]
    aux = (O / 'direct_labels.aux').read_text()
    label = lambda name: int(re.search(r'\\newlabel\{' + name + r'\}\{\{[^}]*\}\{(\d+)\}', aux)[1])
    assert (label('news-start'), label('news-end'), label('main-end'), label('LastPage')) == (18, 19, 24, 26)
    assert label('fig:identification-matrix') == 8 and label('fig:country-contrasts') == 17
    assert len(re.findall(r'\\bibcite\{', aux)) == 50
    assert len(set(re.findall(r'\\bibcite\{([^}]+)', aux))) == 50
    for name in ['direct_build.log', 'proxy_build.log']:
        log = (O / name).read_text()
        assert all(x not in log for x in ['Overfull', 'undefined', 'LaTeX Warning'])
        assert log.count('Underfull') == 2
    nodes = E.parse(T / 'himcm_v176_bbox.html').getroot().findall('.//{http://www.w3.org/1999/xhtml}page')
    assert len(nodes) == 26
    for i, node in enumerate(nodes):
        assert (float(node.get('width')), float(node.get('height'))) == (612, 792)
        words = node.findall('.//{http://www.w3.org/1999/xhtml}word')
        assert not any(float(w.get('yMin')) > 745 for w in words)
        if i:
            top = [w for w in words if float(w.get('yMin')) < 65]
            assert any(w.text == 'Team' and 70 < float(w.get('xMin')) < 74 for w in top)
            assert any(w.text == 'Page' and float(w.get('xMin')) > 450 for w in top)
            assert f'Page {i+1} of 26' in pages[i]
    requirements = rows(R / 'results/task4_v173_collection_review/requirements.csv')
    statuses = {x['id']: x['status'] for x in requirements}
    authorization = read(R / 'design/task4_publishing_authorization_20261109.json')
    assert authorization['github_research_push_authorized'] and authorization['private_overleaf_push_authorized']
    for x in requirements:
        hits = []
        for marker in json.loads(x['passage_markers']):
            found = [i for i, page in enumerate(pages, 1) if norm(marker).lower() in page.lower()]
            assert found, (x['id'], marker)
            hits += found
        if hits:
            x['pdf_pages'] = ','.join(map(str, sorted(set(hits))))
        if x['id'] == 'PA-references': x['evidence'] = 'References20-24;50 compiled entries'
        if x['id'] == 'CI-file': x['evidence'] = f'{pdf.stat().st_size} bytes;one current owned PDF'
        if x['id'] == 'TEAM-independent-entry': x['evidence'] = 'V176 direct/root per-page normalized text equal;26pages;0overfull/2 inherited reviewed underfull'
        if x['id'] == 'AI-verification': x['evidence'] = 'Frozen V154 science;V169/V175 numerical MC evidence;V176 exact prose boundary,outward rounding and full rendered review'
        if x['id'] == 'PUB-sharing':
            x['status'] = 'reviewed_scoped'
            x['evidence'] = 'Explicit user request on2026-11-09 authorizes all pending GitHub/Overleaf uploads;design/task4_publishing_authorization_20261109.json'
            x['scope_or_remaining_action'] = 'Earlier public push hold superseded for this upload;actual remote equality recorded separately in sync.json;no competition submission authorized'
    requirements.append(dict(id='U-MC-precision', authority='User Monte Carlo mean-rank comparison task', requirement='Distinguish finite-draw numerical precision from evidence and preference uncertainty', status='reviewed_scoped', pdf_pages='14-15,24', evidence='Only owned6.3 interpretation revised;Hoeffding/union-bound common95% event,m2064,n10000;outward rounded2.38pp/.357;Oslo-Zurich expected order unresolved;one theorem reference', scope_or_remaining_action='Assumes within-settingIID under declared laws;no empirical RNG independence proof,real-world winner probability or forecast calibration;no new draws', passage_markers=json.dumps(['Numerical precision', '2064 exported means', 'expected mean-rank order unresolved'])))
    assert len(requirements) == 47 and all(x['status'] == statuses[x['id']] for x in requirements if x['id'] in statuses and x['id'] != 'PUB-sharing')
    pending = [x['id'] for x in requirements if x['status'] in {'partial', 'unverified', 'awaiting_team', 'not_ready', 'not_performed'}]
    assert len(pending) == 13
    table('requirements.csv', requirements)
    xml = E.parse(T / 'v176_fonts.xml').getroot()
    fonts, counts, small = {}, Counter(), []
    for page in xml.findall('page'):
        for font in page.findall('fontspec'): fonts[font.get('id')] = font.attrib
        for span in page.findall('text'):
            value = ''.join(span.itertext()).strip()
            if not value: continue
            font = fonts[span.get('font')]
            size = int(font['size'])
            family = re.sub(r'^[A-Z]{6}\+', '', font['family'])
            counts[size, family] += 1
            if size < 12: small.append(dict(pdf_page=int(page.get('number')), top=int(span.get('top')), extractor_size=size, font_family=family, text=value))
    table('font_inventory.csv', [dict(extractor_size=k[0], font_family=k[1], text_spans=v, interpretation='Extractor glyph size;native nominal12pt body/11pt heads,unchanged figures;small math not all-glyph12pt certified') for k, v in sorted(counts.items())])
    table('small_spans.csv', small)
    visual = read(O / 'visual_review.json')
    pixels = read(O / 'body_pixel_comparison.json')
    assert visual['all26_pages_layout_reviewed'] and visual['pdf_sha256'] == sha(pdf)
    assert pixels['new_pdf_sha256'] == sha(pdf) and len(pixels['identical_body_pages']) == 22
    assert pixels['changed_body_pages'] == [14, 15, 16, 24]
    repro = read(O / 'reproduction.json')
    assert repro['all_byte_identical'] and repro['generated_files'] == 5
    for name, expected in repro['files_sha256'].items(): assert sha(P / name) == expected
    registry = read(R / 'design/task4_user_current_review.json')
    assert registry == read(D / 'task4_current_review.json') and registry['version'] == 'V176' and registry['pdf_sha256'] == sha(pdf)
    result = dict(status='pass', version='V176', primary_model='V154 unchanged', total_pages=26, main_and_references_pages=24, main_page_margin=1, news_pages=[18, 19], references_pages=[20, 24], AI_pages=[25, 26], compiled_references=50, matrix_figure_page=8, country_figure_page=17, scientific_files_unchanged=len(protected['science']), existing_manuscript_files_unchanged=len(protected['paper'])-1, owned_pointer_files_changed=['drafts/task4_current_review.json'], shared_main_ref_class_unchanged=True, unchanged_outside_MC_interpretation=True, one_reference_appended=True, numerical_claims_outward_rounded=True, independent_agent_review='mean_rank_review:math,scope,all old prose outside6.3,reference append and source hashes checked read-only;baseline wording clarified', body_pixel_identical_pages=22, all26_pages_layout_reviewed=True, direct_root_text_equal=True, native_header_footer_checked=True, overfull_boxes=0, underfull_paragraphs_per_build=2, requirements=47, prior_statuses_preserved_except_authorized_publishing_gate=True, publishing_gate_explicitly_resolved=True, pending_gates_preserved=pending, primary_data_admissions=0, primary_score_width_change=0, MC_rerun=False, font_or_margin_changed=False, submission_ready=False, AI_history_complete=False, server_compile_verified=False, default_main_setting_changed=False, pdf_bytes=pdf.stat().st_size, pdf_sha256=sha(pdf), verifier_sha256=sha(Path(__file__)))
    (O / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
