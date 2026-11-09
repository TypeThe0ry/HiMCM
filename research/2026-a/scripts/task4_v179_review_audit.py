"""Audit the owned AI-only revision against frozen provenance and V176 pages."""
from pathlib import Path
from collections import Counter
import csv
import json
import re
import xml.etree.ElementTree as E
from task4_v172_review_audit import norm, pdftext, rows, read, sha

R = Path(__file__).resolve().parents[1]
P = R.parents[2] / 'HiMCM-Overleaf'
D = P / 'drafts'
O = R / 'results/task4_v179_ai_review'
T = Path('/data/scratch')


def table(name, records):
    with (O / name).open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(records)


def main():
    protected = read(O / 'protected_files.json')
    for root, mapping in [(R, protected['science']), (R.parents[1], protected['ai_provenance'])]:
        for name, expected in mapping.items(): assert sha(root / name) == expected, name
    for name, expected in protected['paper'].items():
        if name != 'drafts/task4_current_review.json': assert sha(P / name) == expected, name
    old = (D / 'task4_v154_ai.tex').read_text()
    coverage = (D / 'task4_v179_coverage.tex').read_text()
    a = old.index('\\subsection*{Recovered records and coverage}')
    b = old.index('\\subsection*{Verification associated with this draft}', a)
    expected = (old[:a] + coverage + '\n' + old[b:]).replace('all 28 saved turn contexts', 'all 74 saved root turn contexts')
    assert (D / 'task4_v179_ai.tex').read_text() == expected
    assert (D / 'task4_v179_paper.tex').read_text() == (D / 'task4_v176_paper.tex').read_text().replace('% V176 owned review;', '% V179 owned review;').replace('task4_v154_ai.tex', 'task4_v179_ai.tex')
    manifest = read(D / 'task4_v179_manifest.json')
    for path, key in [('task4_v154_ai.tex', 'base_AI_sha256'), ('task4_v179_coverage.tex', 'coverage_sha256'), ('task4_v176_paper.tex', 'base_wrapper_sha256')]: assert sha(D / path) == manifest[key]
    assert sha(P / 'mcmthesis.cls') == manifest['shared_class_sha256']
    provenance = read(R / 'data/task4_v178_ai_provenance/capture_summary.json')
    source_audit = read(R / 'data/task4_v178_ai_provenance/verification.json')
    assert provenance['full_manifest_sha256'] == source_audit['manifest_sha256'] == sha(R / 'data/task4_v178_ai_provenance/session_manifest.json')
    assert provenance['verification_sha256'] == sha(R / 'data/task4_v178_ai_provenance/verification.json')
    assert source_audit['status'] == 'pass' and not source_audit['complete_team_ai_history']
    assert provenance['selected_visible_counts'] == {'user:None': 6, 'assistant:commentary': 259, 'assistant:final_answer': 61}
    assert provenance['recorded_root_model_counts'] == {'gpt-6.1-sol': 74}
    assert provenance['call_types'] == {'custom_tool_call': 1749, 'function_call': 116}
    assert provenance['selected_visible_records'] == 326 and provenance['recorded_assistant_call_inputs'] == 1865
    assert provenance['source_prefix']['last_timestamp'] == '2026-11-09T14:31:18.850Z'
    for marker in ['14:31:18.850 UTC', '22:31 in Singapore', '326 selected', 'six selected', '259 progress', '61 complete', '125-record selection', '1,865', '1,749', '116 function-call', 'one root session', 'tool results', 'subagent response sessions', 'not included as submission transcripts', 'subsequent work is outside']:
        assert norm(marker) in norm(coverage), marker
    pdf = D / 'task4_v179_paper.pdf'
    pages = [norm(x) for x in pdftext(pdf).split('\f') if x.strip()]
    proxy = T / 'himcm_v179_proxy/task4_v179_review_entry.pdf'
    assert pages == [norm(x) for x in pdftext(proxy).split('\f') if x.strip()]
    assert len(pages) == 26
    assert pages[:24] == [norm(x) for x in pdftext(D / 'task4_v176_paper.pdf').split('\f') if x.strip()][:24]
    assert '74 saved root' in pages[24] and '326 selected' in pages[25] and '1,865' in pages[25]
    assert 'incomplete review record' in pages[24] and 'immutable serving build' in pages[24]
    aux = (O / 'direct_labels.aux').read_text()
    label = lambda name: int(re.search(r'\\newlabel\{' + name + r'\}\{\{[^}]*\}\{(\d+)\}', aux)[1])
    assert (label('news-start'), label('news-end'), label('main-end'), label('LastPage')) == (18, 19, 24, 26)
    assert len(re.findall(r'\\bibcite\{', aux)) == 50
    for name in ['direct_build.log', 'proxy_build.log']:
        log = (O / name).read_text()
        assert all(x not in log for x in ['Overfull', 'undefined', 'LaTeX Warning'])
        assert log.count('Underfull') == 2
    nodes = E.parse(T / 'himcm_v179_bbox.html').getroot().findall('.//{http://www.w3.org/1999/xhtml}page')
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
    requirements = rows(R / 'results/task4_v176_mc_paper/requirements.csv')
    statuses = {x['id']: x['status'] for x in requirements}
    for item in requirements:
        hits = []
        for marker in json.loads(item['passage_markers']):
            found = [i for i, page in enumerate(pages, 1) if norm(marker).lower() in page.lower()]
            assert found, (item['id'], marker)
            hits += found
        if hits: item['pdf_pages'] = ','.join(map(str, sorted(set(hits))))
        if item['id'] == 'CI-file': item['evidence'] = f'{pdf.stat().st_size} bytes;one current owned PDF'
        if item['id'] == 'TEAM-independent-entry': item['evidence'] = 'V179 direct/root per-page normalized text equal;26pages;0overfull/2 inherited reviewed underfull'
        if item['id'] == 'AI-tool-disclosure': item['evidence'] = 'AI25-26;V178 fixed14:31UTC window,74root labels,326visible/1865toolinputs;incomplete status retained'
        if item['id'] == 'AI-complete-record': item['scope_or_remaining_action'] = 'Expanded root-only evidence is not full-team disclosure;actual saved queries/responses and other tools/chats/team records still require reconciliation'
        if item['id'] == 'AI-verification': item['evidence'] = 'Frozen V178 per-record/filter/replay proof;V179 exactAI-only source boundary and24main/reference pages pixel-identical'
    assert len(requirements) == 47 and all(x['status'] == statuses[x['id']] for x in requirements)
    pending = [x['id'] for x in requirements if x['status'] in {'partial', 'unverified', 'awaiting_team', 'not_ready', 'not_performed'}]
    assert len(pending) == 13
    table('requirements.csv', requirements)
    fonts, counts, small = {}, Counter(), []
    for page in E.parse(T / 'v179_fonts.xml').getroot().findall('page'):
        for font in page.findall('fontspec'): fonts[font.get('id')] = font.attrib
        for span in page.findall('text'):
            value = ''.join(span.itertext()).strip()
            if not value: continue
            font = fonts[span.get('font')]
            size = int(font['size']); family = re.sub(r'^[A-Z]{6}\+', '', font['family'])
            counts[size, family] += 1
            if size < 12: small.append(dict(pdf_page=int(page.get('number')), top=int(span.get('top')), extractor_size=size, font_family=family, text=value))
    table('font_inventory.csv', [dict(extractor_size=k[0], font_family=k[1], text_spans=v, interpretation='Extractor sizes;nominal12pt body/11pt heads unchanged;no all-glyph12pt claim') for k, v in sorted(counts.items())])
    table('small_spans.csv', small)
    pixels = read(O / 'page_pixel_comparison.json')
    assert pixels['identical_pages'] == list(range(1,25)) and pixels['changed_pages'] == [25,26] and pixels['new_pdf_sha256'] == sha(pdf)
    visual = read(O / 'visual_review.json')
    assert visual['changed_AI_pages_visually_reviewed'] == [25,26] and visual['pdf_sha256'] == sha(pdf)
    reproduction = read(O / 'reproduction.json')
    assert reproduction['generated_files'] == 4 and reproduction['all_byte_identical']
    for name, expected in reproduction['files_sha256'].items(): assert sha(P / name) == expected
    registry = read(R / 'design/task4_user_current_review.json')
    assert registry == read(D / 'task4_current_review.json') and registry['version'] == 'V179' and registry['pdf_sha256'] == sha(pdf)
    report = dict(status='pass', version='V179', primary_model='V154 unchanged', total_pages=26, main_and_references_pages=24, main_page_margin=1, news_pages=[18,19], references_pages=[20,24], AI_pages=[25,26], compiled_references=50,
                  scientific_files_unchanged=187, existing_manuscript_files_unchanged=len(protected['paper'])-1, owned_pointer_files_changed=['drafts/task4_current_review.json'], shared_main_ref_class_unchanged=True,
                  AI_only_revision=True, unchanged_other_AI_sections=True, exact_full_page_pixels_identical=24, direct_root_text_equal=True, native_header_footer_checked=True, overfull_boxes=0, underfull_paragraphs_per_build=2,
                  requirements=47, prior47_statuses_preserved=True, pending_gates_preserved=pending, primary_data_admissions=0, primary_score_width_change=0, MC_rerun=False, font_or_margin_changed=False,
                  independent_agent_review='mean_rank_review:exact source boundary and V178 count/cutoff/scope checks passed read-only', AI_history_complete=False, private_content_published=False, submission_ready=False, server_compile_verified=False, default_main_setting_changed=False,
                  pdf_bytes=pdf.stat().st_size, pdf_sha256=sha(pdf), verifier_sha256=sha(Path(__file__)))
    (O / 'verification.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
