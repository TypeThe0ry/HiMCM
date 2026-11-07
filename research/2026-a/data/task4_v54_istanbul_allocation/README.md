# Istanbul职业教师分配：名单完整性核查

新取得两份官方原件，尚不足以收紧V53的职业教师分配界。EBA学校介绍页列出依据2025年9月5日批复111708265开展教育的12所职业初中，其中没有Istanbul；但这份名单没有被核实为2025/26全学年27校的完整总体。不能由名单中没有Istanbul推断该省没有附设职业初中。

MTEGM《2025年度活动报告》原始PDF第47页（印刷页40）又报告2025年度在18省的20所职业技术高中内设初中。该年度口径、12校批复名单与V53学年统计27校没有经过逐校、日期和覆盖对齐，不能相加、相减或拼成完整名单。EBA页的部分其他段落保留草稿式文字，进一步说明应取得正式批复附件或完整统计名录，而非把介绍页视为排他性全名录。

因此继续保留`V∈[0,20156]`。也未取得同学年Istanbul可能受影响学校的完整教师总量，不能构造较小的教师分配上界。此次核查不改变主模型、学生计数、教师池或可能冠军范围。

## 原件与验证

- [EBA官方介绍页](https://sosyaluyum.eba.gov.tr/turkiyede-ortaokul-egitimi-genel-bilgilendirme/)：原始HTML保存为`eba_school_list.html`；逐校内容保存为`listed_schools.csv`。
- [MTEGM 2025年度活动报告](https://mtegm.meb.gov.tr/meb_iys_dosyalar/2026_04/69cd0e7080d55758688856_2025_Y%C4%B1l%C4%B1_Birim_Faaliyet_Raporu.pdf)：原始PDF1,024,991字节。

`manifest.json`记录原始URL、字节数和SHA256。运行`python3 research/2026-a/data/task4_v54_istanbul_allocation/audit.py`离线核验两份原件、12条唯一序号、批复日期及年度报告表述，输出`audit.json`。没有将搜索无结果当作零值，也没有反推受保护数据。
