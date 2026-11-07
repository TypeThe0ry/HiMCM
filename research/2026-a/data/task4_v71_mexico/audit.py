"""Verify official questionnaires; do not merge unlinked survey respondents."""
import hashlib,json
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent

def audit():
    for r in json.loads((ROOT/'manifest.json').read_text()):
        b=(ROOT/r['file']).read_bytes()
        assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
    def page(file,n):return ' '.join(PdfReader(ROOT/file).pages[n-1].extract_text().split())
    e=page('enut2024_questionnaire.pdf',10)
    assert 'aprobó usted en la escuela' in e
    travel=page('enut2024_questionnaire.pdf',14)
    assert 'se trasladó de ida y vuelta' in travel and 'lunes a' in travel and 'sábado y' in travel
    dictionary=page('enigh2024_dictionary.pdf',23)
    assert 'Nivel escolar al que asiste' in dictionary and 'Nivel de instrucción aprobado' in dictionary
    manual=page('enigh2024_interviewer.pdf',261)
    assert 'Ir a la escuela (tiempo de traslado)' in manual and 'Hacer tareas' in manual
    print('Verified: ENUT attained grade / weekly round-trip time; ENIGH current level / bundled study time. No city observation admitted.')

if __name__=='__main__':audit()
