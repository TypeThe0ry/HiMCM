"""Verify the archived instrument and the retained source-scope decisions."""
import hashlib,json,subprocess
from pathlib import Path

P=Path(__file__).resolve().parent
for row in json.loads((P/'manifest.json').read_text()):
    data=(P/row['file']).read_bytes()
    assert len(data)==row['bytes']
    assert hashlib.sha256(data).hexdigest()==row['sha256']
text=subprocess.check_output(['pdftotext','-layout',str(P/'eod2017_questionnaire.pdf'),'-']).decode()
assert '¿Hasta qué año o grado' in text and 'aprobó' in text
start=text.index('CONDICIÓN DE ACTIVIDAD')
section=text[start:start+6000]
assert section.index('trabajó?')<section.index('¿Es estudiante?')
assert 'REGISTRE UN SOLO CÓDIGO' in section
j=json.loads((P/'jakarta_reader_audit.json').read_text())
assert j['current_stage_table']['number']==55 and j['duration_table']['number']==20
assert not j['admission'] and not j['microdata_obtained']
result=dict(original_instrument_verified=True,mexico_current_stage_identified=False,
            jakarta_stage_duration_joint_obtained=False,changed_model_cells=0)
(P/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
