# V163 Helsinki国家包络来源核验

八份*_original.*为完整HTTP响应体，retrieval.json保存URL／方法／UTC时间／SHA；POST选择见FI_11c4_query.json。XLSX仅只读，不重导出。135h为21个地区的元数据，仅供路线筛选；学生分子来自11c4城市KU091。

extract.py需带openpyxl的Python（本机使用Codex bundled Python），生成scope_audit.json。随后以系统Python运行../../scripts/audit_task4_v163_helsinki.py，原生OOXML与JSON-stat索引独立核验。全国FTE的估算来源在15.2.2!F10，当前没有一侧误差包络，city_PTR_bound为null，observations为空。说明见../../results/task4_v163_helsinki_envelope/README.md。
