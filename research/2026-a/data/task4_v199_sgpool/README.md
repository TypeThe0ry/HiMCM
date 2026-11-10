# V199 ActiveSG 游泳场馆目录候选证据

ActiveSG Circle 官方游泳池目录在本次抓取时列出 25 条场馆记录。目录解析得到 25 个不同的名称、设施页 URL slug、街道地址和邮编；其中 18 个邮编未出现在 V117 的 2025 年 4 月精选文章七场馆子集中。Tampines Swimming Complex 与文章中的 Our Tampines Hub 按相同邮编 528523 识别为同一物理场馆。

这批数据是**当前目录候选清单**，不直接改写 2025 年观测：目录显示最后更新为 2026-11-08，本次原始目录响应于 2026-11-10 抓取。它不能证明其他场馆在 2025 年或模型观测年份已开放。V117 已保存同一官方目录的文字提取，但只有首页十条；此处保存三页原始 HTML 并补全分页，不把旧首页或 2025 年文章重复算作新证据。目录来源回执及 URL、UTC 时间、状态、字节数和 SHA-256 在 `retrieval.json`。

另抓取目录所链接的 25 个官方设施详情页，25 页均返回 HTTP 200；详情页所示名称、地址和邮编与目录卡片全部一致。逐页抓取参数、原始响应字节数及哈希在 `detail_retrieval.json`，HTML 原件在 `details/`，逐页比对与告示定位在 `detail_verification.json`。详情页列出 25 条每周维护闭馆安排；这表示定期维护日，不代表永久闭馆。另有四条非每周的临时泳池闭馆告示：Clementi 两条、Jurong East 一条、Katong 一条；告示作用范围是所列泳池，日期不自动等于全场馆关闭。Jurong East 还显示“Partial Facility Access”并说明部分区域因维护或维修不可进入。逐页文本检查未发现明确的成人专用、儿童专用或仅限会员准入措辞；这不证明所有时段或全部人群均可进入。没有一项计数声称 25 个场馆在抓取日全部开放。

`venues.json` 将设施页 URL 的 slug 记录为 `provider_id`，因为目录没有暴露数值 ID；这是可复核的供应方页面标识，不宣称为内部数据库主键。`candidate_count.json` 仅汇总当前目录及详情页核验：保留 25 个目录候选，不与历史文章记录合并，不作年份回推，也不将候选数写入模型。当前人口 6,036,900、CSV、模型和当前导航均未更改。按物理场馆而非池体、泳道计数。

目录入口：<https://www.activesgcircle.gov.sg/facilities/swimming-pools>。目录分页原件为 `active_sg_directory_page_1.html` 至 `active_sg_directory_page_3.html`；可运行 `python extract.py` 复现目录清单。
