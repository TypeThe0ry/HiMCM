"""Read-only Amsterdam national teacher-cap source review; no new observation."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, subprocess
from task4_audit_output import audit_parser, check_output, emit_report
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
P = G.parent / 'HiMCM-Overleaf'
D = R / 'data/current_amsterdam_teacher_bound'
O = R / 'results/current_amsterdam_teacher_review/verification.json'
a = audit_parser(__doc__).parse_args()
check_output(a, O, G)

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pages(p):
    return subprocess.check_output(['pdftotext', '-layout', str(p), '-'], text=True).split('\f')
def words(s): return ' '.join(s.split())

receipt = read(D / 'retrieval.json')
assert len(receipt['requests']) == 6
for request in receipt['requests']:
    f = D / request['file']
    assert f.stat().st_size == request['bytes'] and sha(f) == request['sha256'], f
    assert request['status'] is None and request['retrieval_utc'] is None and request['final_url'] is None

data = read(D / 'eurostat_nl_2021_fte.json')
assert all(size == 1 for dim, size in zip(data['id'], data['size']) if dim != 'isced11')
for dim, code in {'geo':'NL', 'time':'2021', 'sex':'T', 'worktime':'TOT_FTE', 'sector':'TOT_SEC', 'unit':'NR'}.items():
    assert data['dimension'][dim]['category']['index'] == {code: 0}
values = {}
for level, expected in [('ED2', 45309), ('ED3', 46539)]:
    index = str(data['dimension']['isced11']['category']['index'][level])
    values[level] = data['value'][index]
    assert values[level] == expected and index not in data.get('status', {})
assert sum(values.values()) == 91848

oecd = words(pages(D / 'oecd_eag2023_notes.pdf')[421])
assert 'Netherlands' in oecd
assert 'The number of teachers in private institutions is estimated based on the number of students in private institutions and the student-teacher ratios in public institutions.' in oecd
ipto = words(pages(D / 'duo_ipto_method.pdf')[1])
assert 'Deze PNIL telt niet mee bij Onderwijs in cijfers.' in ipto

class Text(HTMLParser):
    def __init__(self): super().__init__(); self.parts = []
    def handle_data(self, text): self.parts.append(text)
t = Text()
t.feed((D / 'duo_fte_page.html').read_text())
fte = words(' '.join(t.parts))
assert 'Om de ontbrekende gegevens aan te vullen, gebruikt DUO een weegfactor.' in fte
assert 'landelijke weegfactor: tabblad 1 t/m 3' in fte
scope = read(D / 'scope.json')
assert scope['primary_admissions'] == scope['actual_primary_width_reduction'] == 0
assert scope['teacher_cap_verified'] is False and scope['model_change'] is False
assert scope['matched_pupil_subset_verified'] is False

v = read(R / 'results/current_paper_review/current_verification.json')
core = read(R / 'design/task4_user_v203_snapshot.json')['source_sha256']
extra = {}
for name, group in v.items():
    if name.startswith('additional_') and name.endswith('_sha256'): extra.update(group)
assert len(core) == 548 and len(extra) == 77
for name, digest in {**core, **extra, **v['withdrawal_source_sha256']}.items():
    assert sha(R / name) == digest, name
for name, digest in v['current_files_sha256'].items():
    assert sha(P / name) == sha(G / 'paper/current' / name) == digest, name
frame, low, high = revised_bounds()
i = frame.city.tolist().index('Amsterdam'); j = NAMES.index('upper_secondary_ptr')
assert low[i, j] == 0 and high[i, j] == 1
sources = [*sorted(f for f in D.iterdir() if f.is_file()), Path(__file__), R / 'scripts/task4_audit_output.py']
report = {
    'status': 'pass scoped source review', 'archived_bodies_checked': 6,
    'national_FTE_values_decoded': values, 'candidate_sum_not_admitted': 91848,
    'OECD_method_PDF_page': 422, 'IPTO_scope_PDF_page': 2,
    'reference_period_alignment_verified': False, 'teacher_cap_verified': False,
    'matched_pupil_subset_verified': False, 'primary_admissions': 0,
    'actual_primary_width_reduction': 0, 'Amsterdam_PTR_utility': [0, 1],
    'core_bindings_checked': len(core), 'supplemental_bindings_checked': len(extra),
    'withdrawal_evidence_entries_checked': len(v['withdrawal_source_sha256']),
    'paper_dependencies_each_copy': len(v['current_files_sha256']),
    'source_sha256': {str(f.relative_to(R)): sha(f) for f in sources},
    'scope': 'No verified actual teacher cap or same-period pupil subset. No-status flags do not certify completeness. OECD methodology is not asserted to identify the exact Eurostat cell methodology. Workbook body integrity only; workbook contents not audited. No manuscript/model change or agency contact.'
}
emit_report(report, a, O, G)
