"""Replace an owned collection-case block with checked employment/estimation distinctions."""
from pathlib import Path
import hashlib,json,re
D=Path(__file__).resolve().parent;R=D.parents[1]/'HiMCM/research/2026-a'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 old=(D/'task4_v160_core.tex').read_text();a=old.index('For Henri-IV (Paris');z=old.index('\\textbf{Rates require',a)
 new=r'''Henri-IV (Paris, UAI 0750654D) reports 794 lyc\'ee pupils and 153.65
institution FTE for 2025, without an upper-stage allocation or complete
city-provider coverage \cite{deppmatch}. A 2026 post-baccalaureate flag cannot
recover its 2025 workloads \cite{deppdirectory}.
Dublin's school-roll payroll FTE are unpublished \cite{irelandfte}.
Its November 2025 City Of Dublin ETB post-primary vocational subgroup reports
411.8 payroll FTE against 376.1 allocated posts \cite{irelandpayroll}:
allocation is not a payroll ceiling, and this subgroup does not identify the
city's PTR. Finland's national FTE uses salary and private-provider data for
estimation, alongside register sources. Without a verified one-sided error
envelope, we do not use that estimate as a guaranteed Helsinki teacher upper
bound \cite{finlandfte}. All three city PTRs remain unknown.

'''
 core=(old[:a]+new+old[z:]).replace('\\clearpage\n\\section{Comparing cities within the same country}', '\\section{Comparing cities within the same country}')
 (D/'task4_v164_core.tex').write_text(core)
 additions=r'''\bibitem{irelandpayroll} Department of Education and Youth.
\textit{The Teaching Workforce in Ireland: Primary and Post Primary Level,
2025/26 School Year}. April 2026, Table 10, p.~14; November 2025 payroll.
\url{https://assets.gov.ie/static/documents/5935f213/Teacher_Workforce_Data_Report_2026.pdf}.
\bibitem{finlandfte} Statistics Finland / Eurostat. Finland UOE national
reference metadata, Annex III--Additional tables, sheet 15.2.2, cell F10.
National metadata updated 1 October 2026; original workbook retrieved
9 November 2026. Full-time/part-time and FTE estimation methods.
\url{https://ec.europa.eu/eurostat/cache/metadata/Annexes/educ_uoe_enr_esmsed_fi_an_Annex_III_-_Additional_tables.xlsx}.
'''
 refs=(D/'task4_v154_references.tex').read_text();assert refs.count('\\end{thebibliography}')==1
 (D/'task4_v164_references.tex').write_text(refs.replace('\\end{thebibliography}',additions+'\\end{thebibliography}'))
 front=(D/'task4_v154_front.tex').read_text()
 end_header=front.index('\\end{center}')+len('\\end{center}')
 keyword=front.index('\\textbf{Keywords:}')
 toc=front.index('\\clearpage\n\\tableofcontents',keyword)
 summary=front[end_header:keyword].strip()
 summary=re.sub(r'The resulting 160-entry matrix contains 112 point values, 34 partial\s+intervals and 14 fully missing intervals\.\s*','',summary)
 assert 'The resulting 160-entry matrix contains' not in summary
 keys=front[keyword+len('\\textbf{Keywords:}'):toc].strip()
 after_summary=front[toc:]
 owned_front='\\begin{abstract}\n'+summary+'\n\\begin{keywords}\n'+keys+'\n\\end{keywords}\n\\end{abstract}\n\\maketitle\n'+after_summary
 (D/'task4_v164_front.tex').write_text(owned_front)
 paper=r'''% V164 owned review; user-supplied mcmthesis format, shared class unchanged.
\documentclass{mcmthesis}
\mcmsetup{CTeX=false,tcn=PENDING,problem=A,sheet=true,titleinsheet=true,
keywordsinsheet=true,titlepage=false,abstract=true}
\usepackage{palatino,microtype,ragged2e,placeins,url,xurl}
\setlength{\headheight}{16pt}
\AtBeginDocument{\setlength{\parindent}{0pt}\setlength{\parskip}{0.5\baselineskip}}
\setlength{\tabcolsep}{5pt}
\widowpenalty=10000\clubpenalty=10000
\setcounter{tocdepth}{2}
\makeatletter
\renewcommand\tableofcontents{%
\centerline{\rmfamily\Large\bfseries\contentsname%
\@mkboth{\MakeUppercase\contentsname}{\MakeUppercase\contentsname}}%
\vskip 3ex\@starttoc{toc}}
\renewcommand{\l@section}{\def\@pnumwidth{2.3em}\def\@tocrmarg{2.3em}%
\bfseries\@dottedtocline{1}{1.5em}{2.3em}}
\renewcommand{\l@subsection}{\normalfont\@dottedtocline{2}{3.0em}{3.2em}}
\renewcommand{\@dotsep}{1}
\makeatother
\title{Choosing a City for High-School Life with Incomplete Evidence}
\author{}\date{}
\hypersetup{pdftitle={Choosing a City for High-School Life with Incomplete Evidence},pdfauthor={}}
\input{task4_v154_generated.tex}
\begin{document}
\input{task4_v164_front.tex}
\input{task4_v164_core.tex}
\input{task4_v154_conclusion.tex}
\clearpage
\phantomsection\addcontentsline{toc}{section}{News article}\label{news-start}
\input{task4_v154_news.tex}\label{news-end}
\clearpage
\phantomsection\addcontentsline{toc}{section}{References}
\input{task4_v164_references.tex}\label{main-end}
\clearpage
\input{task4_v154_ai.tex}
\end{document}
'''
 paper=paper.replace(r'\setlength{\headheight}{16pt}',r'\setlength{\headheight}{16pt}\urlstyle{same}\emergencystretch=3em\hyphenpenalty=500')
 paper=paper.replace('\\input{task4_v154_generated.tex}',r'\graphicspath{{./}{drafts/}}'+'\n'+r'\input{task4_v154_generated.tex}')
 conclusion="\\section{Conclusion and decision use}\nZurich minimizes maximum regret under baseline and equal weights; all sixteen\ncities remain possible champions. Education priority selects Oslo. Withholding\nZurich's unverified homicide point selects Singapore under baseline and Oslo\nunder equal weights; broader withdrawal of 28 flagged points selects Berlin and\nParis, respectively. Families should examine both their priorities and the\nsource bounds behind a recommendation.\n\nVerified supplements reduce mean score-interval width by 14.62\\% while preserving\nsubmitted values. Holding this evidence fixed, the interval revision changes\n13 decision ranks and retains completions in which another city outranks Zurich.\nBetter evidence narrows uncertainty; the decision rule makes that uncertainty\nexplicit.\n"
 (D/'task4_v164_conclusion.tex').write_text(conclusion)
 paper=paper.replace('task4_v154_conclusion.tex','task4_v164_conclusion.tex')
 (D/'task4_v164_paper.tex').write_text(paper)
 (D.parent/'task4_v164_review_entry.tex').write_text('% Independent review; default main setting unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v164_paper.tex}\n')
 sources=['results/task4_v161_dublin_scope/verification.json','data/task4_v161_dublin_scope/scope_audit.json','results/task4_v163_helsinki_envelope/verification.json','data/task4_v163_helsinki_envelope/scope_audit.json']
 manifest=dict(version='V164',primary='V154 unchanged',base_review='V160 frozen',changed_scope='Owned collection-case block, two new references, native user-template format; own summary drops repeated matrix-count sentence; remove one forced page break and tighten owned conclusion to avoid short tail page; shared class/main/ref unchanged',base_core_sha256=sha(D/'task4_v160_core.tex'),source_sha256={n:sha(R/n) for n in sources},project_settings_changed=False,format_reference_sha256=json.loads((D/'task4_v164_format_reference.json').read_text())['source_attachment_sha256'],shared_class_sha256=sha(D.parent/'mcmthesis.cls'),format_scope='Read existing mcmthesis class; native summary/banner, Team # header, Page x of y, empty footer, letterpaper1in, Palatino; tcn remains PENDING because pasted tcn18213 and author18214 conflict')
 (D/'task4_v164_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('Old/new block word counts:',len(old[a:z].split()),len(new.split()))
if __name__=='__main__':main()
