"""Check primary source bytes and the scope of the rejected city transfer."""
from pathlib import Path
import hashlib,json
from pypdf import PdfReader
P=Path(__file__).resolve().parent

def audit():
    for r in json.loads((P/'manifest.json').read_text()):
        assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
    e=PdfReader(P/'eud.pdf');r=PdfReader(P/'rysensteen.pdf')
    def t(pdf,page):return ' '.join(pdf.pages[page-1].extract_text().split())
    assert '1.732' in t(e,36) and '2024' in t(e,36)
    assert 'Hovedstaden' in t(e,38) and '8,1' in t(e,38)
    assert 'regioner' in t(e,37)
    fig=t(e,85)
    for label in ['4%','18%','29%','33%','17%','Mindre end 5','16-30 minutter','Mere end 1 time']:
        assert label in fig,label
    assert 'Transport til og fra gymnasiet' in t(r,34)
    assert '2010' in t(r,18)
    s=json.loads((P/'summary.json').read_text())
    assert sum(s['new_actual_travel_source']['rounded_percentages'])==101
    assert not s['admitted'] and s['utility_interval']==[0,1]
    return {'passed':True,'primary_files_verified':2,'city_travel_cells_admitted':0,'rounding_not_renormalized':True,'source_scope_reviewed':True,'visual_figure_review_recorded':s['visual_checks']}
if __name__=='__main__':
    out=audit();(P/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
