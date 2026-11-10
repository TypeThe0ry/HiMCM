# V196 Milan：用原PDF复核17个泳池及文内日期

本次直接取得被引Milanosport泳池价目表的原PDF，HTTP200、95997字节，SHA256见`retrieval.json`。V118冻结包保留的是provider提取文本；新增原件不覆盖旧表示，也不更改科学输入。

从原PDF独立提取两个重复的设施清单，A组13处、B组4处，合计17个不同名称，与V118已采用名称集合完全一致。保留原人口1399079／2025及效用界[0.5485500692302455,1]；0新增准入、0实际评分区间收窄。这是设施价目表子集，不证明城市完整清单、持续营业或学生实际可达性。

原文有效日为2025年6月1日；页面右下角明确写“aggiornato al 9 settembre 2025”，即2025年9月9日。URL文件名含`agg-9-10-2025`，与文内月份不一致，不能从文件名推定本文更新日或上传日。当前自有参考文献写9October2025，应以此次原件的文内日期为依据处理；旧文档及原捕获保持冻结。本任务未编辑论文。

来源：[Milanosport原PDF](https://www.milanosport.it/workspace/uploads/nuovi-tariffari-1-giugno-2025-agg-9-10-2025.pdf)。`collect.py`拒绝覆盖已有原件／回执；`extract.py`离线核哈希、17名称、A/B重复清单和两个文内日期；`verification.json`保留比较结果及旧表示哈希。物理第1页已按1800像素渲染实看，名称和右下日期均可辨。`tariff_extracted.txt`是派生提取，不是原件。
