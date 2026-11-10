"""Migrate the current owned review to audited V181 evidence; preserve team files."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent
R=D.parent.parent/'HiMCM/research/2026-a'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def replace(text,old,new,count=1):
    assert text.count(old)==count,(old,text.count(old),count)
    return text.replace(old,new)
def main():
    plan=json.loads((R/'results/task4_v181_transition/paper_migration_plan.json').read_text())
    for name,h in plan['authoritative_inputs'].items():assert sha(D.parent/name)==h,name
    audit=json.loads((R/'results/task4_v181_transition/verification.json').read_text());assert audit['status']=='pass'
    for section in ['source_sha256','result_sha256']:
        for name,h in audit[section].items():assert sha(R/name)==h,name
    front=replace((D/'task4_v164_front.tex').read_text(),'twenty-two previously missing','twenty-three previously missing')
    conclusion=replace((D/'task4_v164_conclusion.tex').read_text(),'14.62\\%',r'\TotalWidthReduction\%')
    news=replace((D/'task4_v154_news.tex').read_text(),'Across twenty-two previously missing','Across twenty-three previously missing')
    core=(D/'task4_v176_core.tex').read_text()
    core=replace(core,'rebased to V154 evidence','rebased to V181 evidence')
    core=replace(core,'112 point values, 34 partial intervals and\n14 fully missing intervals: eight teacher-ratio, three transport and three','112 point values, 35 partial intervals and\n13 fully missing intervals: eight teacher-ratio, two transport and three')
    core=replace(core,'twenty-two supplements','twenty-three supplements')
    core=replace(core,'twenty-two admitted supplements','twenty-three admitted supplements')
    paragraph=r'''Amsterdam's municipal map contains 39 Metro-designated station groups.
Thirty-five lie inside both the municipal 2026 and CBS 2025 city boundaries;
a declared 100-metre nominal boundary screen omits three and retains 32
\cite{amsterdammetro2026,cbsboundary2025}. The screen defines an analyst-selected
subset, not a provider positional-error guarantee. Nearby boarding points are
already grouped by the provider. The inventory metadata specify 2026 but no
exact observation date; pairing it with the retained 2025 population of 941,927
gives a conditional lower bound, with other transport supply left unknown.

'''
    core=replace(core,"London's inventory mixes",paragraph+"London's inventory mixes")
    core=core.replace('task4_v154_assets/','task4_v182_assets/')
    core=replace(core,'task4_v168_evidence_figure.tex','task4_v182_evidence_figure.tex')
    ai=(D/'task4_v179_ai.tex').read_text()
    ai=replace(ai,'the original city CSV and the V154 primary\nevidence. The V154 validation','the original city CSV and the V181 primary\nevidence. The V181 validation')
    refs=(D/'task4_v176_references.tex').read_text()
    extra=r'''\bibitem{amsterdammetro2026} Gemeente Amsterdam.
\textit{Tram en metro: haltes}, Maps Amsterdam open geodata,
TRAMMETRO\_PUNTEN\_2026; metadata ID 649, 2026, exact observation date unreported; municipal boundary
INDELING\_GEMEENTE, March 2026.
Original GeoJSON and metadata retrieved 9 November 2026.
\url{https://maps.amsterdam.nl/open_geodata/?k=649}.
\bibitem{cbsboundary2025} Statistics Netherlands (CBS) / PDOK.
\textit{CBS Gebiedsindelingen 2025}, non-generalised municipal boundary,
GM0363 Amsterdam; retrieved 9 November 2026. CC BY 4.0.
\url{https://service.pdok.nl/cbs/gebiedsindelingen/2025/wfs/v1_0?service=WFS&request=GetCapabilities}.
'''
    refs=replace(refs,r'\end{thebibliography}',extra+r'\end{thebibliography}')
    for key,value in [('front',front),('core',core),('conclusion',conclusion),('news',news),('references',refs),('ai',ai)]:
        (D/f'task4_v182_{key}.tex').write_text(value)
    paper=(D/'task4_v179_paper.tex').read_text()
    for old,new in [('V179 owned review','V182 owned review'),('task4_v154_generated','task4_v182_generated'),('task4_v164_front','task4_v182_front'),('task4_v176_core','task4_v182_core'),('task4_v164_conclusion','task4_v182_conclusion'),('task4_v154_news','task4_v182_news'),('task4_v176_references','task4_v182_references'),('task4_v179_ai','task4_v182_ai')]:paper=replace(paper,old,new)
    (D/'task4_v182_paper.tex').write_text(paper)
    (D.parent/'task4_v182_review_entry.tex').write_text('% Independent owned review; default main setting unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v182_paper.tex}\n')
    manifest=dict(version='V182',primary='V181',base_review='V179',source_plan_sha256=sha(R/'results/task4_v181_transition/paper_migration_plan.json'),science_audit_sha256=sha(R/'results/task4_v181_transition/verification.json'),base_inputs=plan['authoritative_inputs'],shared_class_sha256=sha(D.parent/'mcmthesis.cls'),AI_capture_window_changed=False,teammate_files_changed=False,project_settings_changed=False)
    (D/'task4_v182_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('V182 owned sources generated from audited V181; old inputs preserved')
if __name__=='__main__':main()
