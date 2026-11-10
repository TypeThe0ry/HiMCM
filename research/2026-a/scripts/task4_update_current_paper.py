#!/usr/bin/env python3
"""Apply audited V202 assets to the exact current Overleaf manuscript."""
from pathlib import Path
import hashlib, re, shutil
R = Path(__file__).resolve().parents[1]
P = R.parents[2] / 'HiMCM-Overleaf'
p = P / 'main.tex'
s = p.read_text()
assert hashlib.sha256(s.encode()).hexdigest() == '7abf9e3e550583dc70b39d6b11b015fac94edb4cef6b06d97645d90faf20a200', 'Unexpected source; inspect changes before applying'
a = R / 'results/current_paper_assets'
generated = (a / 'generated.tex').read_text()
for name in ['CurrentMeanWidth','TotalWidthReduction','LatestEvidenceChange','RevisionRankChanges','SummaryWeightMC','MethodComparison','FutureDeterministic','FutureThresholds','FutureMonteCarlo','ProxyWithdrawalMC','PreferenceResults','PreferenceEvidenceChange','EvidenceThresholdCheck','MonteCarloInterpretation','MCBaseMeans','MCSettings','MCPairComparisons','MCCertifiedPairs','MCUnresolvedPairs','MCUniqueMinSettings','MCFrequencyHalfWidthPP','MCRankHalfWidth']:
    pat = r'^\\newcommand\{\\' + name + r'\}.*$'
    new = re.search(pat, generated, re.M).group()
    s, n = re.subn(pat, lambda _: new, s, flags=re.M)
    assert n == 1, name

def replace(old, new):
    global s
    assert s.count(old) == 1, (old, s.count(old))
    s = s.replace(old, new)
replace('Under uniform ten-per-cent development changes, resource expansion selects\nSingapore under baseline weights; other scenarios retain Zurich.', 'Under uniform ten-per-cent development changes, Singapore is selected\nunder baseline weights for resource expansion and living pressure;\nbalanced improvement retains Zurich.')
replace('Named subsets include 25 Singapore venues in the ActiveSG directory captured\n10 November 2026, twelve Zurich venues and seventeen Milan indoor venues under\nthe June 2025 tariff \\cite{sgpool_directory,sgpool_2025,zurichpool,milanpool2025}.\nThe Singapore inventory counts physical venues, not currently open pools or\nteen access; four pool-specific temporary notices affect three venues. Withholding\nthose three venues leaves 22 and retains Zurich under both weight references.', 'Named subsets include 25 Singapore venues in the ActiveSG directory and one\nOCBC Aquatic Centre at 7 Stadium Drive, Singapore 397632, counted once despite\nits multiple basins; operator pages were captured 10 November 2026 and their\ninventory date is unstated. The denominator is the 2024 population of 6,036,900.\nTwelve Zurich venues and seventeen Milan indoor venues under the June 2025 tariff\nare also retained \\cite{sgpool_directory,sgpool_2025,sgocbc,zurichpool,milanpool2025}.\nThe Singapore count does not establish opening or teen access. Four earlier\npool-specific notices affect three ActiveSG venues: withholding them leaves 23\nvenues; also withholding OCBC leaves 22. At OCBC, competition-pool booking is\nfor ages 16 and above, training-pool booking is for all ages, and supervisory rules\napply for ages 15 and below. Individual per-entry prices are offered; normal hours\nare 07:00--21:30 Monday and Wednesday--Sunday. Tuesday maintenance, the 30 October--1 November\n2026 event and 5--28 December competition-pool closure with limited training\navailability constrain access \\cite{sgocbc}.')
replace('Source: V200 utility bounds.', 'Source: V202 utility bounds.')
replace('2 & Singapore & 55.19--63.53 & 16.99', '2 & Singapore & 55.23--63.53 & 16.95')
replace('smallest lead is 4.188 score', 'smallest lead is 4.153 score')
replace('Before 2020 & 13 & Singapore & Zurich & 21.04', 'Before 2020 & 13 & Singapore & Zurich & 21.03')
replace('0.14951 and 1.03432', '0.14257 and 1.01449')
replace('near 40.53 minutes', 'near 40.07 minutes')
replace('1.57080\\% (baseline)', '0.42205\\% (baseline)')
replace('Baseline & 43.62 & 18.18 & 37.80', 'Baseline & 43.18 & 18.01 & 38.41')
replace('Education priority & 6.59 & 31.88 & 55.06', 'Education priority & 6.47 & 31.47 & 55.70')
replace('Independent living & 58.54 & 9.66 & 31.45', 'Independent living & 58.21 & 9.58 & 31.86')
replace('decision ranks 2.0764, 2.1586 and 2.3354', 'decision ranks 2.0515, 2.1651 and 2.3425')
replace('resolves 4,259 of 4,440', 'resolves 4,260 of 4,440')
replace('leaves 181 unresolved', 'leaves 180 unresolved')
replace('rank in 17 of 37 settings', 'rank in 18 of 37 settings')
replace('The research calculations preserve the original city CSV and the V200 primary\nevidence. The V200 validation', 'The research calculations preserve the original city CSV and the V202 primary\nevidence. The V202 validation')
replace('% V201 manuscript assets from V200 evidence and controlled extensions; historical cases retained.', '% Current manuscript assets from V202 evidence and controlled extensions; historical cases retained.')
replace('\\bibitem{sgpool_2025}', '\\bibitem{sgocbc} The Kallang. OCBC Aquatic Centre and swimming information, captured 10 November 2026; inventory date unstated. \\url{https://www.thekallang.com.sg/en/plan-your-visit/venues-and-amenities/ocbc-aquatic-centre.html}; \\url{https://www.thekallang.com.sg/en/things-to-do/sports/swimming.html}.\n\\bibitem{sgpool_2025}')
replace('\\begin{table}[!ht]\\centering\n\\caption{Conservative baseline decision ranks with unchanged weights.}\\label{tab:baseline}\n\\begin{tabular}{rlrr}\\toprule\nRank & City & Score interval & Maximum regret\\\\\\midrule\n1 & Zurich & 53.97--72.18 & 16.94 \\\\\n2 & Singapore & 55.23--63.53 & 16.95 \\\\\n3 & Oslo & 54.30--63.90 & 17.89 \\\\\n4 & Stockholm & 52.12--64.54 & 20.06 \\\\\n5 & Prague & 51.97--62.78 & 20.21 \\\\\n6 & Dublin & 51.13--70.90 & 21.05 \\\\\n7 & Berlin & 50.73--61.54 & 21.45 \\\\\n8 & Helsinki & 49.41--69.84 & 22.78 \\\\\n9 & Paris & 49.11--69.04 & 23.08 \\\\\n10 & Madrid & 49.00--68.22 & 23.18 \\\\\n11 & Warsaw & 47.64--63.99 & 24.54 \\\\\n12 & Vienna & 47.52--61.03 & 24.66 \\\\\n13 & Milan & 46.07--65.99 & 26.11 \\\\\n14 & London & 45.22--66.12 & 26.97 \\\\\n15 & Tokyo & 43.98--61.12 & 28.20 \\\\\n16 & Amsterdam & 42.48--60.43 & 29.70 \\\\\n\\bottomrule\\end{tabular}\\end{table}', '\\begin{table}[!ht]\\centering\n\\caption{Conservative baseline decision ranks with unchanged weights.}\\label{tab:baseline}\n\\begingroup\\setlength{\\tabcolsep}{2pt}\n\\begin{tabular}{rlrr@{\\quad}rlrr}\\toprule\nRank & City & Score interval & Regret & Rank & City & Score interval & Regret\\\\\\midrule\n1 & Zurich & 53.97--72.18 & 16.94 & 9 & Paris & 49.11--69.04 & 23.08 \\\\\n2 & Singapore & 55.23--63.53 & 16.95 & 10 & Madrid & 49.00--68.22 & 23.18 \\\\\n3 & Oslo & 54.30--63.90 & 17.89 & 11 & Warsaw & 47.64--63.99 & 24.54 \\\\\n4 & Stockholm & 52.12--64.54 & 20.06 & 12 & Vienna & 47.52--61.03 & 24.66 \\\\\n5 & Prague & 51.97--62.78 & 20.21 & 13 & Milan & 46.07--65.99 & 26.11 \\\\\n6 & Dublin & 51.13--70.90 & 21.05 & 14 & London & 45.22--66.12 & 26.97 \\\\\n7 & Berlin & 50.73--61.54 & 21.45 & 15 & Tokyo & 43.98--61.12 & 28.20 \\\\\n8 & Helsinki & 49.41--69.84 & 22.78 & 16 & Amsterdam & 42.48--60.43 & 29.70 \\\\\n\\bottomrule\\end{tabular}\\endgroup\\end{table}')
replace('\\FloatBarrier\n\\subsection{A significant revision:', '\\subsection{A significant revision:')
replace('resource expansion selects Singapore under baseline priorities; Zurich remains the recommendation in the living-pressure and balanced-improvement scenarios and under equal priorities.', 'resource expansion and living pressure select Singapore under baseline priorities; Zurich remains the recommendation for balanced improvement and under equal priorities.')
p.write_text(s)
for name in ['identification_matrix.pdf', 'score_intervals.pdf']:
    shutil.copyfile(a / name, P / 'figures' / name)
print('Updated', p)
