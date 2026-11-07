"""Build the audit workbook and readable report from source-specific findings.

Run with a Python that has openpyxl installed. No network access during build.
"""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import html
import json
import math
import textwrap
import unicodedata

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'deliverables'
OUT.mkdir(exist_ok=True)
original = json.loads((ROOT / 'original_extracted.json').read_text())[0]['rows']
findings = []
for name in ['audit_numbeo.json', 'audit_homicide.json',
             'audit_education_environment.json', 'audit_transport_broadband.json']:
    findings.extend(json.loads((ROOT / name).read_text()))
findings.sort(key=lambda r: (int(''.join(filter(str.isdigit, r['cell']))), r['cell'].rstrip('0123456789')))
by_cell = {r['cell']: r for r in findings}
assert len(findings) == len(by_cell) == 48
for r in findings:
    col = ord(r['cell'][0]) - 65
    row = int(r['cell'][1:]) - 1
    assert original[row][0] == r['city']
    assert math.isclose(original[row][col], r['original_value'], abs_tol=1e-10)
    assert r['primary_urls'] and r['data_year'] and r['definition']
provenance = json.loads((ROOT / 'provenance.json').read_text())
assert hashlib.sha256((ROOT / 'city_matrix_25.numbers').read_bytes()).hexdigest() == provenance['sha256']

LABEL = {'confirmed': '数值核实', 'rounding_only': '数值核实（正常舍入）',
         'metadata_incomplete': '数值匹配；须补滚动版日期',
         'version_mixed': '数值匹配年中版；同列混版',
         'year_mismatch': '年份／引文版本错配',
         'definition_mismatch': '口径需纠正／补全',
         'unverifiable': '原声明口径未完全核实', 'wrong_value': '数值错误'}
IND = {'homicide': '凶杀率', 'pm25': 'PM2.5', 'cli': '生活成本指数',
       'pir': '房价收入比', 'ptr': '学生／教师比', 'he_density': '高教机构密度',
       'pt_stops': '公交站点密度', 't10': '驾驶10km耗时', 'broadband': '固定宽带下载中位数', 'pool': '公共泳池密度'}
UNITS = {'homicide': '每10万人·年', 'pm25': 'µg/m³', 'cli': '纽约=100',
         'pir': '收入年数', 'ptr': '学生/教师', 'he_density': '所/10万人',
         'pt_stops': '站点/10万人', 't10': '分钟/10km', 'broadband': 'Mbps', 'pool': '处/10万人'}
COLS = ['homicide','pm25','cli','pir','ptr','he_density','pt_stops','t10','broadband','pool']
HIGH = {'year_mismatch', 'definition_mismatch', 'version_mixed', 'unverifiable', 'wrong_value'}
KEY = ['B26','B44','J40','J44','T27','F23','F46']

def fmt(v):
    return '未核实／不提供同口径值' if v is None else f'{v:.10g}' if isinstance(v, (int,float)) else str(v)

def short_result(r):
    return r['issue'] + '\n处理：' + r['recommended_action']

def value_label(r):
    if r['cell'] == 'B26':
        return '39.79672088（同年候选；PEP Vintage2023）'
    if r['cell'] == 'J44':
        return '15.22374164（初中；不是高中更正值）'
    return fmt(r['verified_value'])

def detail(r):
    limit = r.get('limitations', r.get('verification_limits', ''))
    if r['indicator'] in ('cli', 'pir'):
        limit = r.get('source_level', '') + ' 数字匹配发布者汇总表，不代表已审查平台每条报价或证明行政边界一致。'
    return limit

all_cells = []
for rownum, row in enumerate(original[21:], 22):
    for i, ind in enumerate(COLS):
        col = 1 + i * 2
        cell = get_column_letter(col + 1) + str(rownum)
        finding = by_cell.get(cell)
        assert (row[col] is not None) == (finding is not None)
        all_cells.append({'cell':cell,'city':row[0],'indicator':ind,
                          'original_value':row[col], 'original_source':row[col+1],
                          'status':finding['status'] if finding else 'original_blank'})
assert len(all_cells) == 250
assert sum(x['status']=='original_blank' for x in all_cells) == 202
(OUT / 'audit_all_48.json').write_text(json.dumps(findings, ensure_ascii=False, indent=2))
fields = ['cell','city','indicator','original_value','original_source','status','verified_value',
          'data_year','geography','population','definition','primary_urls','evidence','issue',
          'recommended_action','access_date']
with (OUT / '逐项核查48.csv').open('w', encoding='utf-8-sig', newline='') as f:
    writer=csv.DictWriter(f,fields);writer.writeheader()
    for r in findings:
        writer.writerow({k:'\n'.join(r[k]) if isinstance(r.get(k),list) else r.get(k,'') for k in fields})

wb = Workbook()
wb.remove(wb.active)
navy, teal, pale = '17324D', '146C73', 'E9F4F1'

def visual_width(text):
    return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in str(text))

def table(name, headers, rows, widths, statuses=None):
    ws=wb.create_sheet(name);ws.append(headers)
    for row in rows: ws.append([x if x is not None else None for x in row])
    for j,w in enumerate(widths,1):ws.column_dimensions[get_column_letter(j)].width=w
    for cell in ws[1]:
        cell.font=Font(name='Arial',size=11,color='FFFFFF',bold=True)
        cell.fill=PatternFill('solid',fgColor=navy)
        cell.alignment=Alignment(wrap_text=True,vertical='center')
    ws.row_dimensions[1].height=32
    for ri in range(2,ws.max_row+1):
        color='FFFFFF' if ri%2==0 else 'F1F6FA'
        if statuses:
            s=statuses[ri-2]
            color = 'FCE9E7' if s in HIGH else 'FFF4D6' if s=='metadata_incomplete' else 'E9F4F1'
        lines=1
        for ci,cell in enumerate(ws[ri]):
            cell.font=Font(name='Arial',size=11,color=navy)
            cell.fill=PatternFill('solid',fgColor=color)
            cell.alignment=Alignment(wrap_text=True,vertical='top')
            if cell.value is not None:
                n=sum(max(1,math.ceil(visual_width(line)/max(4,widths[ci]-2))) for line in str(cell.value).split('\n'))
                lines=max(lines,n)
            if isinstance(cell.value,str) and cell.value.startswith('https://') and '\n' not in cell.value:
                cell.hyperlink=cell.value;cell.font=Font(name='Arial',size=11,color='0869A6',underline='single')
        ws.row_dimensions[ri].height=min(390,max(30,lines*16+8))
    ws.freeze_panes='D2' if len(headers)>4 else 'A2'
    ws.auto_filter.ref=ws.dimensions
    ws.sheet_view.zoomScale=85
    ws.print_options.horizontalCentered=True
    ws.sheet_properties.pageSetUpPr.fitToPage=True
    ws.page_setup.orientation='landscape'
    ws.page_setup.paperSize=ws.PAPERSIZE_A3
    ws.page_setup.fitToWidth=1;ws.page_setup.fitToHeight=0
    ws.print_title_rows='1:1'
    return ws

overview=[
 ['核查范围','原文件1张表，25城市×10指标=250格。已填48格逐项核查；202格原始空白保留，未把缺失补零或编造。'],
 ['主要结论','4项年份/口径需处理：Detroit凶杀率、Tokyo凶杀率、Singapore师生比引文、Tokyo师生比学段；2项Numbeo生活成本混版；1项Helsinki原公共泳池/年份口径尚未核实。'],
 ['不能笼统说全部数字都错','Numbeo37项均可在发布者某一已查版本找到：35项匹配本次Current滚动版；北京37.9和Zurich123.1匹配2026 Mid-Year。保留真实匹配证据，不把缺元数据直接当捏造数字。'],
 ['数值确认6项','北京PM2.5、新加坡Murder率、London/Tokyo驾驶10km耗时、Seoul/Zurich固定宽带速度。确认仅针对相应发布口径，均已记录边界和统计期。'],
 ['待核实1项','Helsinki 2.3算术可复现；设施时点及全数符合公共/市营条件没有充分证据，同口径核实值留空。Tokyo致死凶杀率亦不提供未知更正值。'],
 ['年份规则','区分数据观测年、报告出版年、历史快照、访问日和滚动窗口；Current值匹配不能倒推整年测量或原采集日。'],
 ['候选更正规则','Detroit39.80使用252受害者/2023人口633218，固定PEP Vintage2023。Tokyo高中15.64869是另一个学段的参考值，不自动替换原初中值。'],
 ['原始来源层级','政府数据用政府原表；TomTom、Ookla、Numbeo用原始提供者。商业汇总表核对不等于逐条复核私有GPS、测速或工资报价。'],
 ['使用顺序','先看“重点问题7项”；再按城市或指标筛选“逐项结论48”和“证据与口径48”。“Numbeo版本37”提供三个版本对照；“250格台账”显示缺失。'],
 ['访问日期','2026-11-07（Asia/Singapore客户端日期）。部分网页有反爬/索引读取，访问限制逐项保留。'],
 ['原件保护','city_matrix_25.numbers字节不改；同目录有原件副本、原始提取JSON/CSV和provenance。未改论文、模型、Overleaf，也未推送。'],
 ['原件SHA256',provenance['sha256']],
 ['颜色','浅绿：相应数值/舍入核实；浅黄：匹配数值但版本日期需补；浅红：口径/年份/混版或未核实，需先处理。']]
table('阅读说明',['项目','说明'],overview,[26,110])

summary_headers=['原表格','城市','指标','原值','结论','核实值／明确口径候选','数据年份／窗口','问题与处理','原始来源（首链）']
def summary_row(r):
    return [r['cell'],r['city'],IND[r['indicator']],r['original_value'],LABEL[r['status']],value_label(r),r['data_year'],short_result(r),r['primary_urls'][0]]
table('重点问题7项',summary_headers,[summary_row(by_cell[c]) for c in KEY],[10,17,20,12,28,38,48,90,60],[by_cell[c]['status'] for c in KEY])
table('逐项结论48',summary_headers,[summary_row(r) for r in findings],[10,17,22,12,30,38,48,90,60],[r['status'] for r in findings])
table('证据与口径48',['原表格','城市','指标','年份／窗口','空间范围','分母／对象','统计定义','原表定位与复算证据','所有原始来源','核查限制','访问日期'],
      [[r['cell'],r['city'],IND[r['indicator']],r['data_year'],r['geography'],r['population'],r['definition'],r['evidence'],'\n'.join(r['primary_urls']),detail(r),r['access_date']] for r in findings],
      [10,17,22,48,55,65,85,100,95,85,14])
nums=[r for r in findings if r['indicator'] in ('cli','pir')]
table('Numbeo版本37',['原表格','城市','指标','原值','2026历史版','2026 Mid-Year','本次Current','匹配版本／处置'],
      [[r['cell'],r['city'],IND[r['indicator']],r['original_value'],r['comparison_values']['2026']['value'],r['comparison_values']['mid']['value'],r['comparison_values']['current']['value'],r['data_year']+'；'+r['recommended_action']] for r in nums],
      [10,18,20,12,16,20,20,100],[r['status'] for r in nums])
table('待核实原声明',['原表格','城市','原声明','核查所得','未知部分','处理','原始来源'],
      [[r['cell'],r['city'],str(r['original_value'])+'；'+r['original_source'],r['evidence'],r['issue'],r['recommended_action'],'\n'.join(r['primary_urls'])] for r in findings if r['status']=='unverifiable'],
      [10,18,50,90,90,90,95])
table('250格台账',['原表格','城市','指标','单位','原值','原来源','核查状态'],
      [[r['cell'],r['city'],IND[r['indicator']],UNITS[r['indicator']],r['original_value'],r['original_source'],LABEL.get(r['status'],'原表空白：未取得，不等于0；本次不补数')] for r in all_cells],
      [10,18,25,18,12,65,60])
ws=table('原始矩阵',original[20],original[21:],[19]+[14,60]*10)
for r in findings:
    cell=ws.cell(int(r['cell'][1:])-20,ord(r['cell'][0])-64)
    cell.comment=Comment(LABEL[r['status']]+'\n'+r['data_year']+'\n'+short_result(r)+'\n'+r['primary_urls'][0],'来源审计')
    cell.fill=PatternFill('solid',fgColor='FCE9E7' if r['status'] in HIGH else 'FFF4D6' if r['status']=='metadata_incomplete' else 'E9F4F1')
    cell.number_format='0.###'
wb.save(OUT/'city_matrix_25_逐项核查.xlsx')

def esc(x): return html.escape(str(x))
def links(r): return '<br>'.join(f'<a href="{esc(u)}">{esc(u)}</a>' for u in r['primary_urls'])
cards=[]
for r in findings:
    if r['indicator'] in ('cli','pir'): continue
    cards.append(f'''<article><h3>{esc(r['cell'])} · {esc(r['city'])} · {esc(IND[r['indicator']])} <span>{esc(LABEL[r['status']])}</span></h3>
<p><b>原值：</b>{esc(fmt(r['original_value']))} {esc(UNITS[r['indicator']])}　<b>核实值：</b>{esc(value_label(r))}</p>
<p><b>年份：</b>{esc(r['data_year'])}<br><b>范围：</b>{esc(r['geography'])}<br><b>分母／对象：</b>{esc(r['population'])}</p>
<p><b>定义：</b>{esc(r['definition'])}</p><p><b>证据：</b>{esc(r['evidence'])}</p>
<p class="issue"><b>判断与处理：</b>{esc(short_result(r))}</p><p><b>限制：</b>{esc(detail(r))}</p>
<p class="sources">{links(r)}</p></article>''')
numrows=[]
for r in nums:
    v=r['comparison_values']
    numrows.append('<tr>'+''.join('<td>'+esc(x)+'</td>' for x in [r['cell'],r['city'],r['indicator'],fmt(r['original_value']),fmt(v['2026']['value']) if v['2026']['value'] is not None else '未列入该榜',fmt(v['mid']['value']),fmt(v['current']['value']),'年中版' if r['status']=='version_mixed' else 'Current'])+'</tr>')
report=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>city_matrix_25 数据来源核查</title>
<style>@page{{size:A4;margin:16mm}}*{{box-sizing:border-box}}body{{font-family:"PingFang SC","Noto Sans CJK SC",sans-serif;font-size:11pt;line-height:1.65;color:#17324d;margin:30px auto;max-width:1050px;padding:0 24px}}h1{{font-size:24pt;line-height:1.3}}h2{{font-size:17pt;margin-top:30px}}h3{{font-size:13pt;line-height:1.5;margin:0 0 8px}}p{{margin:7px 0}}.lead{{font-size:13pt;background:#e9f4f1;padding:18px}}.issue{{background:#fff4d6;padding:10px;white-space:pre-line}}article{{border-top:2px solid #146c73;padding:16px 0;margin-top:18px;break-inside:avoid}}span{{display:block;font-size:11pt;color:#146c73}}a{{color:#0869a6;overflow-wrap:anywhere}}.sources{{font-size:10pt;line-height:1.5}}table{{width:100%;border-collapse:collapse;font-size:10pt;line-height:1.45}}td,th{{padding:7px 5px;text-align:left;border-bottom:1px solid #d5dfe6;overflow-wrap:anywhere}}th{{background:#17324d;color:white}}tr{{break-inside:avoid}}small{{font-size:10pt}}@media print{{body{{margin:0;padding:0;max-width:none}}a{{text-decoration:none}}article{{break-inside:auto}}h2,h3{{break-after:avoid}}thead{{display:table-header-group}}}}</style></head><body>
<h1>city_matrix_25 数据来源核查</h1><p>核查日期：2026-11-07 · 原始文件保持不变 · 只审计数据，不改模型与论文</p>
<p class="lead">25座城市×10指标共250格，其中48格有值，已逐项完成来源追溯；202格原始空白继续保留。核查发现4项年份／口径需处理、2项Numbeo混版，以及1项原声明未完全核实。</p>
<p>“完成核查”指每个已填值都有证据与判断，不表示所有数据都通过。核实范围为原始发布者表格、指标定义与复算；未检查供应商每条私有报价、GPS或测速记录。</p>
<h2>优先处理的7项</h2><ol>
<li><b>Detroit B26：</b>39.03可由2023年252名受害者÷2024人口复现，但跨年。若采用同年PEP Vintage2023人口633,218，候选为39.80/10万人。</li>
<li><b>Tokyo B44：</b>0.667由94件「殺人」÷人口复现；含未遂，不能当统一致死凶杀率。未知更正值留空。</li>
<li><b>Singapore J40：</b>12.7是2024 Secondary年度值，可引ESD2025或官方API；原引ESD2024对应2023年12.6。</li>
<li><b>Tokyo J44：</b>15.22是初中学生/本务教师。原表未写学段；若模型解释为高中则需纠正。高中另行复算15.64869，属于不同学段参考值。</li>
<li><b>Helsinki T27：</b>16/694,392×100,000≈2.3算术可复现，但设施年份与全部公共／市营准入条件未确证；同口径核实值留空。</li>
<li><b>Beijing F23、Zurich F46：</b>37.9与123.1匹配2026 Mid-Year；同列其余大多数值匹配本次Current。应先统一版本，不能把版本差异一律叫抄错。</li></ol>
<h2>Numbeo 37项：数值均找到匹配版本</h2>
<p>35项匹配本次Current滚动页；2项匹配Mid-Year。Current是访问日快照，不能标成2026全年统计。纽约100为固定基准，单独不能辨认版本。下表“未列入该榜”只描述该历史榜单，不能推断城市没有数据或值为0。</p>
<p>CLI为纽约=100的生活成本指数，不含租金／按揭。PIR采用90㎡、中心与中心外每㎡价格均值、1.5×平均税后工资的家庭收入假设，不能直接写成真实家庭中位收入与成交房价中位数之比。Numbeo为原始商业发布者，采用用户与人工采集，非政府普查；城市边界和个体价格样本未在本次审计中逐一验证。</p>
<table><thead><tr>{''.join('<th>'+x+'</th>' for x in ['格','城市','指标','原值','2026版','年中版','Current','匹配'])}</tr></thead><tbody>{''.join(numrows)}</tbody></table>
<p class="sources">成本指数：<a href="https://www.numbeo.com/cost-of-living/rankings_current.jsp">Current</a> · <a href="https://www.numbeo.com/cost-of-living/rankings.jsp">本次默认页（2026 Mid-Year）</a> · <a href="https://www.numbeo.com/cost-of-living/rankings.jsp?title=2026">2026历史版</a><br>房价收入比：<a href="https://www.numbeo.com/property-investment/rankings_current.jsp">Current</a> · <a href="https://www.numbeo.com/property-investment/rankings.jsp">本次默认页（2026 Mid-Year）</a> · <a href="https://www.numbeo.com/property-investment/rankings.jsp?title=2026">2026历史版</a><br>定义：<a href="https://www.numbeo.com/cost-of-living/cpi_explained.jsp">CLI</a> · <a href="https://www.numbeo.com/property-investment/indicators_explained.jsp">PIR</a> · <a href="https://www.numbeo.com/common/motivation_and_methodology.jsp">方法</a></p>
<p>默认rankings.jsp将来会切换版本；已保存本次页面标题、字节和哈希。显式2026-mid网址网页工具返回503，实际证据采用本次标题确为Mid-Year的默认页归档，不假称该显式网址访问成功。</p>
<h2>其余11项：原始证据与口径</h2>{''.join(cards)}
<h2>文件与保留事项</h2><p>Excel包含48项结论、7项重点问题、48项完整证据、37项版本对照、250格台账及带注释的原始矩阵。原始矩阵的数值未改；颜色和批注仅作审计标记。JSON保留全部限定、候选值与访问限制。未补齐202格空白。</p>
<p>商业指标已核对发布者汇总值，不声称自行重算全部底层数据。东京统一致死凶杀更正值、Helsinki同年公共泳池密度仍缺充分证据；不使用别国、全国或不同学段数字补齐。</p>
<p><small>原件SHA256：{provenance['sha256']}</small></p></body></html>'''
(OUT/'数据核查报告.html').write_text(report)

readme='''# city_matrix_25 数据审计\n\n核查日期2026-11-07（Asia/Singapore）。本次完整覆盖原Numbers表48个已填数值，202个原始空白保留。\n\n- `deliverables/city_matrix_25_逐项核查.xlsx`：主交付，Numbers/Excel均可打开；含逐项状态、原始来源、年份、口径、问题、复算和空白台账。\n- `deliverables/数据核查报告.html`：中文可读报告；同目录PDF为渲染版。\n- `deliverables/逐项核查48.csv`、`audit_all_48.json`：可筛选/程序读取。\n- `audit_*.json`：按来源分组的原始审计记录。`original_extracted.json`和CSV是原表逐格提取，不改写原数据。\n- `city_matrix_25.numbers`：原件字节副本；原路径和哈希见provenance.json。\n- `sources/`和`evidence_*/`：实际取得的发布者页面/表格/文本与访问清单。未取得的原PDF等限制保留在每条记录，不能冒称已归档。\n\n重点：4项年份/口径问题（Detroit凶杀、Tokyo凶杀、Singapore师生比引文、Tokyo师生比学段）；2项CLI快照混版（Beijing、Zurich）；1项原公共泳池声明未完全核实（Helsinki）。37项Numbeo数值均在已检查的某版本匹配；缺少版本日期与统计定义不等于数字本身编造。\n\nDetroit39.80为固定PEP Vintage2023同年人口的候选重算；Tokyo初中15.22不能无说明作为高中值。Helsinki的2.3只可按已知16/694392算术复现，公共设施覆盖/年份待核实。核查不自动将原表改成统一口径模型输入。未改论文、Overleaf或既有模型。\n\n复建：`python build_deliverables.py`，需openpyxl；原数据提取需numbers-parser。复建不访问网络。`fetch_numbeo.py`与`build_numbeo_audit.py`是本轮Numbeo抓取/比对脚本，以仓库根为工作目录；重新访问Current会生成不同快照，请另存新版本，勿覆盖本轮证据。\n'''
(ROOT/'README.md').write_text(readme)

# Read-back validation: every source value appears once in the audit; all 250 slots retained.
check=load_workbook(OUT/'city_matrix_25_逐项核查.xlsx')
assert check['逐项结论48'].max_row==49
assert check['250格台账'].max_row==251
assert check['重点问题7项'].max_row==8
assert check['原始矩阵'].max_row==26
for idx,row in enumerate(original[21:],2):
    for col,v in enumerate(row,1):
        got=check['原始矩阵'].cell(idx,col).value
        assert got==v or isinstance(got,(int,float)) and isinstance(v,(int,float)) and math.isclose(got,v,abs_tol=1e-10)
validation={'audited_filled_cells':48,'original_blank_cells':202,'all_slots':250,
            'unique_cells':len(by_cell),'status_counts':dict(Counter(r['status'] for r in findings)),
            'original_hash_matches':True,'xlsx_readback':True,
            'scope':'来源审计完成；保留已注明未核实口径，不代表所有数据通过'}
(OUT/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2))
print(json.dumps(validation,ensure_ascii=False))
