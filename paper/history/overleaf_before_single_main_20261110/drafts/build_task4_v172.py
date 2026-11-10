"""Replace the owned auxiliary-country table with a complete contrast figure."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 old=(D/'task4_v168_core.tex').read_text();marker='\\input{task4_v154_assets/country.tex}'
 assert old.count(marker)==1
 (D/'task4_v172_core.tex').write_text(old.replace(marker,'\\input{task4_v172_country_figure.tex}')+'\n\\FloatBarrier\n')
 caption=r'''% Owned auxiliary figure; no primary16 data or old manuscript edits.
\begin{figure}[!ht]
\centering
\includegraphics[width=\linewidth]{task4_v172_country_assets/country_contrasts.pdf}
\caption{Frozen auxiliary V117 country cases, separate from the primary sixteen cities.
Top: retained score intervals. Bottom: all twenty utility differences, first city minus second;
seven exclude zero. Positive differences favour the first city; negative differences favour
the second. Grey ranges leave direction unresolved. School resource retains
2024--25 school-location all-age XI--XII counts and nominal teacher-headcount allocation, not FTE.
Living cost and housing use 2025 Numbeo aggregates; air uses 2021 WHO monitoring means;
broadband uses the September 2026 index (July--September test window). Source years, boundaries and populations
differ. Ranges are conditional identification bounds, not confidence intervals;
neither pair identifies a necessary overall winner \cite{legacycase,numbeocase,whocase}.}
\label{fig:country-contrasts}
\end{figure}
'''
 (D/'task4_v172_country_figure.tex').write_text(caption)
 (D/'task4_v172_paper.tex').write_text((D/'task4_v168_paper.tex').read_text().replace('% V168 owned review;','% V172 owned review;').replace('task4_v168_core.tex','task4_v172_core.tex'))
 (D.parent/'task4_v172_review_entry.tex').write_text('% Independent owned review; default main setting unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v172_paper.tex}\n')
 manifest=dict(version='V172',primary='V154 unchanged',base_review='V168 frozen',
  base_core_sha256=sha(D/'task4_v168_core.tex'),shared_class_sha256=sha(D.parent/'mcmthesis.cls'),
  changed_scope='One owned auxiliary-country table input replaced by figure input, with a final FloatBarrier before the unchanged conclusion; all existing prose and template retained',
  figure_pdf_sha256=sha(D/'task4_v172_country_assets/country_contrasts.pdf'),
  figure_manifest_sha256=sha(D/'task4_v172_country_assets/figure_manifest.json'),project_settings_changed=False)
 (D/'task4_v172_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('Generated V172 owned candidate; no current-pointer change yet')
if __name__=='__main__':main()
