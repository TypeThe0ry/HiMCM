# V196 Zurich：原始泳池目录核验与五处学校泳池候选

本轮取得市府[室内泳池目录](https://www.stadt-zuerich.ch/de/stadtleben/sport-und-erholung/sport-und-badeanlagen/hallenbaeder.html)原始HTML，逐名确认V118保留的七个设施及七个独立目录目标。相对旧provider提取文本，新原件可直接复核页面结构和来源字节；旧捕获保持。

目录的`stzh-card-navigation`组件另列六个学校泳池，均标注`Mit öffentlichem Schwimmen`：Aemtler、Altweg、Borrweg、Kügeliloo、Riedtli、Tannenrauch。按父agent授权取得六个新场所及七个原场所的官方详情原HTML，均HTTP200。十三个`stzh-contact#kontakt`地址全部不同、城市字段均为Zürich，完成跨组地址去重。页面是真实目录及详情内容，而非HTTP200挑战壳。

保守候选为原七处加五处学校泳池，共十二处；Kügeliloo简介明确只提供成人公共游泳，排除于本候选。Aemtler和Riedtli部分时段仅供女性／女孩；五处新增候选均在学校假期及非上课日关闭，仅在具体时段提供公共游泳。目录供给不证明所有14—18岁学生能够使用、持续开放或实际个人可达性。十三处只是包含成人场所的描述性目录总数，不作为本候选计数。

`school_candidates.json`保存十二处候选名集合、十三处地址去重、六处学校场所的公共时段／年龄／性别限制及旧七处页面中的运营提示。旧七处部分页面同时出现八月检修及具体月份临时关闭提示，年份未全部说明，因此不据此声称当前持续开放，也不把设施存在转成全年可使用。原用户人口440935／2025保持，未独立重新核定；本包不改变模型输入或评分。

`retrieval.json`、`school_retrievals.json`、`existing_retrievals.json`记录原件URL、实际UTC、状态、内容类型、字节和SHA。访问日期为2026-11-10；来源库存参考日未说明，不改标2025。`verify.py`核原目录和原七名集合，`extract_schools.py`核十三详情地址、候选集合及限制。三个采集脚本拒绝覆盖既有捕获。全部新文件只在本包，0主模型准入、0实际评分区间收窄，V192科学和V193论文保持；下一步须独立验证候选并执行隔离模型准入。
