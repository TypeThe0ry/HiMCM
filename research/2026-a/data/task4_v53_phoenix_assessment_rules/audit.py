"""Offline audit of public frontend display rules; no suppressed value inference."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent

def main():
    for item in json.loads((P/'manifest.json').read_text()):
        base=P.parent if item.get('base')=='parent_data_directory' else P
        data=(base/item['file']).read_bytes()
        assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
    html=(P/'central_detail.html').read_text()
    js=(P.parent/'task4_v46_phoenix/app.min.js').read_text()
    marker='props.item[header.value]==-1||props.item[header.value]==-11'
    i=html.index(marker); table_rule=html[i:i+len(marker)+35]
    assert '"*"' in table_rule
    a=html.index('“All Enrolled” displays')
    tooltip=html[a:html.index('</',a)].strip()
    assert 'all students that were tested and enrolled at the school' in tooltip
    start=js.index('getBarChartValue:function')
    chart=js[start:js.index('}},watch:',start)+1]
    assert 'n.numberTested===-11' in chart and 'if(t===-11)return 0' in chart and 't===-1?r:' in chart
    title='store.state.fiscalYear>=2022?"Statewide Assessment Results - "'
    assert title in js
    result=dict(table_codes={'-1':'asterisk','-11':'asterisk'},
      table_rule=table_rule,all_enrolled_scope='Tested and enrolled at the school; not every testing-eligible or resident pupil',
      all_enrolled_tooltip=tooltip,chart_rule=chart,
      chart_zero_is_display_only=True,
      generic_interactive_chart_title_from_fy2022=True,
      current_brand_mapping_verified=False,ordinary_percentage_rounding_verified=False,
      assessment_participation_denominator_equivalence_verified=False,
      new_admitted_observations=0,
      consequence='Retain special codes as unknown and keep the tested cohort separate from participation and enrollment counts.')
    (P/'audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print('PASS: source hashes, table suppression display, tested-cohort tooltip and chart-only special-code behavior')
if __name__=='__main__':main()
