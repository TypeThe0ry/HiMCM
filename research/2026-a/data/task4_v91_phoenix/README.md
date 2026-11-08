# V91：Phoenix官方年份元数据与高中评价规则原件

取得官方报告卡公开年份接口的原始JSON：列出FY2018—FY2025，`activeFiscalYear=true`对应FY2025。接口由此前保存的官方前端`getFiscalYearsList()`明确调用。目录返回FY2026记录不代表所有报告组件已发布FY2026；同样，毕业接口为空也不能否定已存在的2025届工作簿链接。该元数据只证明接口当时的公开返回，不证明每个端点的完整数据覆盖。

另通过Google Drive连接器，取得[ADE官方资源页](https://www.azed.gov/accountability-research/resources)链接的[2024–25 A–F Business Rules Omnibus](https://docs.google.com/document/d/1ynYRBE9l9Kddb2TImig3Vwl9pGItsFfCNl9ign35PnU/edit)全文纯文本导出，保留字节和哈希。文本说明FY2025毕业改善部分比较2024届与2023届四年毕业率，纳入FAY与非FAY学生。并行入学按发文凭学校归属的文字位于CCRI章节，不能移作毕业队列去重规则。因此原学校合计6287与学区6285的差异仍未解决。

导出不是PDF原件，图片或图像公式可能缺失；本轮仅使用可见文字规则。新的2026年9月毕业技术手册网页读取403，未取得原件。University of Arizona下载页只显示未解析图表占位，未获得学校队列数据。

[原件与导出清单](manifest.json) · [核查记录](audit.json)。新增城市数值观测0，模型和缺失区间保持。

```sh
python3 research/2026-a/data/task4_v91_phoenix/verify.py
```
