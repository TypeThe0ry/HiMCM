"""Verify published UI definitions and endpoint binding, not an inferred test mapping."""
from pathlib import Path
import hashlib,json
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parent
for r in json.loads((P/'manifest.json').read_text()):
 b=(P/r['file']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
soup=BeautifulSoup((P/'school_page.html').read_bytes(),'html.parser')
t=' '.join(' '.join(soup.find('template',id='assessmentResultsTemplate').stripped_strings).split())
assert '“All Enrolled” displays the assessment results for all students that were tested and enrolled at the school.' in t
assert '“Partial Year Enrolled”' in t and '“Whole Year Enrolled”' in t
js=(P/'app.min.js').read_text();n=js.index('template:"#assessmentResultsTemplate"');start=js.rfind('Vue.component',0,n);end=js.find('Vue.component',n);component=js[start:end]
assert 'Assessment DetailsFAY' in component and 'store.state.fiscalYear>=2021' in component
assert 't.fayType==n.assessmentInput.fayType' in component
assert 'store.state.fiscalYear>=2025' in component and 'n.numberTested===-11' in component
result=dict(provider='Arizona Department of Education, official report-card site',observed_date='2026-11-08',
 template='assessmentResultsTemplate',component='assessment-results',endpoint_report_section='Assessment DetailsFAY',
 all_enrolled_definition='Assessment results for students both tested and enrolled at the school, not all enrolled students irrespective of participation.',
 partial_whole_definition='Partial denotes tested students enrolled part of year; Whole denotes tested students enrolled for majority of year. The tooltip does not supply exact FAY dates.',
 scope='Current frontend connects this tooltip to FY2021+ FAY endpoint and filters returned fayType, including FY2025.',
 number_tested_caution='UI handles numberTested=-11 as suppressed in FY2025+. This is not a dictionary proving valid-score denominator or unique city students.',
 test_brand_crosswalk_verified=False,legacy_type1_AzMerit_to_ACT_verified=False,science_to_AzSCI_verified=False,
 public_proficiency_denominator_fully_defined=False,main_admitted=False)
print(json.dumps(result,indent=2))
