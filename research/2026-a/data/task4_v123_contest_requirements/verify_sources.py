"""Offline checks on original official source captures; no manuscript changes."""
import hashlib
from html import unescape
import json
from pathlib import Path
import re
import subprocess
from datetime import datetime
from zoneinfo import ZoneInfo
import zipfile

HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE / 'source_manifest.json').read_text())
for record in manifest['sources']:
    data = (HERE / record['file']).read_bytes()
    assert len(data) == record['bytes']
    assert hashlib.sha256(data).hexdigest() == record['sha256'], record['file']
    assert record['url'].startswith('https://www.contest.comap.com/')


def normal(text):
    return re.sub(r'\s+', ' ', text).strip()


def pdf_text(name):
    assert (HERE / name).read_bytes().startswith(b'%PDF-')
    return normal(subprocess.check_output(['pdftotext', '-layout', str(HERE / name), '-'], text=True))


html = (HERE / 'instructions_2026.html').read_text(errors='strict')
instructions = normal(unescape(re.sub('<[^>]*>', ' ', html)))
for phrase in [
    'November 4-17, 2026',
    'readable font of at least 12-point type',
    'Each page of the solution must contain the team control number and the page number at the top',
    'followed by up to 24 pages',
    'Reference list, notes pages, and any appendices do count',
    'Report on Use of AI',
    'must be less than 20MB',
]:
    assert phrase in instructions, phrase
assert 'Contest_AI_Policy.pdf' in html
assert 'posting or sharing any part or all of the problem statement' in instructions
problem = pdf_text('problem_a_2026.pdf')
for phrase in [
    '2026 HiMCM', 'at least ten cities', 'at least one significant revision',
    'one-to-two-page non-technical news article', 'One-page Summary Sheet',
    'Table of Contents', 'typically ages 14-18',
]:
    assert phrase in problem, phrase
ai = pdf_text('comap_ai_policy_v102025.pdf')
for phrase in [
    'v102025', 'all aspects of student work', 'even translations',
    'which model was used and for what purpose', 'list all AI tools used in the reference section',
    'no page limit', 'not be counted as part of the 25-page solution',
    'translation purposes you are not required to include your full input query',
    'exact wording you input', 'complete output from the AI tool',
]:
    assert phrase in ai, phrase
submission = pdf_text('submission_walkthrough_v20251103.pdf')
assert 'V20251103' in submission and 'AI uses statement. Yes/No' in submission
with zipfile.ZipFile(HERE / 'official_generic_summary_sheet.docx') as archive:
    assert 'word/document.xml' in archive.namelist()
    assert b'Team Control Number' in archive.read('word/document.xml')
stop = datetime(2026, 11, 17, 20, tzinfo=ZoneInfo('America/New_York')).astimezone(ZoneInfo('Asia/Singapore'))
submit = datetime(2026, 11, 17, 21, tzinfo=ZoneInfo('America/New_York')).astimezone(ZoneInfo('Asia/Singapore'))
assert stop.isoformat() == '2026-11-18T09:00:00+08:00'
assert submit.isoformat() == '2026-11-18T10:00:00+08:00'
checks = dict(status='pass', sources=len(manifest['sources']), official_2026_entry_verified=True,
    linked_ai_policy_version='v102025', linked_submission_walkthrough_version='V20251103',
    original_byte_hashes_verified=True, format_and_problem_assertions=True,
    exact_query_complete_output_are_report_examples=True, translation_exception_verified=True,
    stop_work_asia_singapore=stop.isoformat(), submission_asia_singapore=submit.isoformat(),
    team_control_number_verified=False, complete_team_ai_history_verified=False,
    submission_readiness_claimed=False)
(HERE / 'verification.json').write_text(json.dumps(checks, indent=2) + '\n')
print(json.dumps(checks, indent=2))
