import json,math
from pathlib import Path
p=Path('research/2026-a/data/city_matrix_25_audit')
orig=json.loads((p/'original_extracted.json').read_text())[0]['rows']
sources=json.loads((p/'numbeo_comparison_sources.json').read_text())
records=[]; extract=[]
for i,r in enumerate(orig[21:],22):
 for j,kind,indicator in [(5,'cost-of-living','cli'),(7,'property-investment','pir')]:
  if r[j] is None:continue
  name='Tel Aviv-Yafo' if r[0]=='Tel Aviv' else r[0]
  versions={}
  for s in sources:
   if s['kind']!=kind:continue
   found=[a for a in s.get('rows',[]) if a['city'].split(',')[0]==name and (name!='London' or a['city'].endswith('United Kingdom'))]
   assert len(found)<=1,(r[0],kind,found)
   versions[s['version']]={'value':found[0]['value'] if found else None,'url':s['url'],'source_city':found[0]['city'] if found else None,'source_title':s['title'][0]}
  matches=[ver for ver,x in versions.items() if x['value'] is not None and math.isclose(x['value'],r[j],abs_tol=1e-8)]
  assert matches,(r[0],kind)
  version='current' if 'current' in matches else 'mid'
  val=versions[version]['value']; url=versions[version]['url']; source_city=versions[version]['source_city']
  dictionary='https://www.numbeo.com/cost-of-living/cpi_explained.jsp' if indicator=='cli' else 'https://www.numbeo.com/property-investment/indicators_explained.jsp'
  definition=('Numbeo生活成本指数，纽约=100；食品、交通、水电等商品服务价格篮子，不含租金/按揭；原始发布者为商业众包与人工采集平台。' if indicator=='cli' else 'Numbeo公式型房价收入比=90㎡×[市中心与中心外每㎡均价的平均]÷[1.5×平均税后月薪×12]；假定家庭收入，非真实家庭中位收入/成交住宅中位价。')
  issue=('原表仅写2026，未标当前滚动版本和访问日期。数字与本次当前页一致；不能标作2026全年官方统计。' if version=='current' else '原值与2026 Mid-Year快照一致；同列多数值匹配本次当前滚动版，版本混杂。与2026不带Mid-Year的历史快照不同；不宜直接判为抄错数字。')
  if r[0]=='New York' and indicator=='cli':issue+='纽约100为基准常数，单靠该值无法辨认快照版本。'
  rec={'cell':chr(65+j)+str(i),'city':r[0],'indicator':indicator,'original_value':r[j],'original_source':r[j+1],
  'status':'version_mixed' if version=='mid' else 'metadata_incomplete','numeric_match':True,'verified_value':val,
  'data_year':'2026 Mid-Year快照（非2026全年）' if version=='mid' else '当前滚动快照，访问2026-11-07；非固定日历年',
  'geography':'Numbeo城市标签：'+source_city+'；未提供行政边界一致性证明','population':'平台收集的价格/工资样本；非居民或高中生概率样本',
  'definition':definition,'primary_urls':[url,dictionary,'https://www.numbeo.com/common/motivation_and_methodology.jsp'],
  'evidence':f"发布者表 {versions[version]['source_title']}，{source_city}行，{'Cost of Living Index' if indicator=='cli' else 'Price To Income Ratio'}列={val:g}。已比较2026、Mid-Year和Current三个版本。",
  'issue':issue,'recommended_action':'保留原值及版本标记；比较分析前选定同一快照并统一重取整列，当前值仅作版本对照，不自动覆盖。',
  'access_date':'2026-11-07','comparison_values':versions,'source_level':'原始数据发布者（Numbeo），非政府统计；本次未核实平台内部每条报价/工资样本。'}
  records.append(rec)
  extract.append({'cell':rec['cell'],'city':source_city,'indicator':indicator,'original':round(r[j],5),'matches':matches,'comparison':{k:v['value'] for k,v in versions.items()}})
(p/'audit_numbeo.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
(p/'sources/numbeo_selected_cells.json').write_text(json.dumps(extract,ensure_ascii=False,indent=2))
print(len(records),'records;',sum(x['status']=='version_mixed' for x in records),'mixed,',sum(x['status']=='metadata_incomplete' for x in records),'metadata')
