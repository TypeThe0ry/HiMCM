# Phoenix考试接口：特殊码与实际分母核查

官方学校页的成绩数据表将`-1`和`-11`均显示为星号；两者都不能作为负成绩或零通过率。页面“All Enrolled”提示明确指在该校就读且参加测试的学生，不是所有符合考试资格的学生，也不是全市居民高中生。此核查支持保留V52的未知结果及成绩／参与率分母区分。

## 已核实的前端规则

- 当前学校HTML的数据表直接将两种负码转成`*`。
- 已归档官方JavaScript在FY2025及以后，对整行受限结果或人数特殊码使用无数据哨兵；部分单个成绩带的`-11`可能在图表中转为0。这是绘图行为，不能反推真实学生数或真实比例为0。
- FY2022及以后交互图标题采用通用“Statewide Assessment Results”。FY2025页面说明其为春季州级考试成绩。代码不能证明API的旧`AzMerit`字段准确对应ACT或AzSCI，原字段继续保留。

## 仍未解决

未取得能够核对FY2025普通整数百分数舍入规则的说明，也未证明成绩人数与参与率接口人数具有同一分母。不得据整数百分数和人数制造实测通过人数；不得把两个接口拼成已参加／未参加的互补总体。

[历史ADE数据指南](https://www.azed.gov/sites/default/files/2022/04/Accountability%20Data%20Guide%20FY%2023.pdf)的第3页说明，隐私限制也适用于少量结果人数及可互相反推的相关单元。因此测试总人数大于10仍可能有结果受限。该指南是FY2023通用说明，不作为FY2025每个API负码的逐一语义字典。原PDF直接下载403，`guide_audit.json`仅保存明确标记的网页读取摘要；未冒充原件。

## 来源与复现

[Central官方学校页](https://azreportcards.azed.gov/schools/detail/5439)原始HTML保存为`central_detail.html`。JavaScript复用V46原件，manifest记录字节数和SHA256；未修改旧文件。`audit.py`离线核验哈希、实际HTML表达式、测试人群说明及图表特殊码分支，输出`audit.json`。

```sh
python3 research/2026-a/data/task4_v53_phoenix_assessment_rules/audit.py
```

本次不新增城市成绩观测，不改变V52三个学校的原始记录或任何模型单元，不重建受保护结果。
