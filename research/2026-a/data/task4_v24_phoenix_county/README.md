# Phoenix 县级毕业数据：新增公开入口核验

本轮新增可纳入观测为 **0**，Phoenix 教育区间不变。

找到 [KIDS COUNT 4616](https://datacenter.aecf.org/data/tables/4616-four-year-graduation-rates) 的县级四年毕业数据入口：页面提供 Maricopa、年份以及 Number／Percent 选项，注明原始来源为 ADE。普通浏览器可以打开页面，但公开原始工作簿下载被 Chrome 报为 `ERR_BLOCKED_BY_CLIENT`；直接请求返回 403。未修改安全设置，也未取得可归档的工作簿或 2024 数值。

[AZMAG GitHub 仓库](https://github.com/AZMAG/gis-az-schools-data-docs) 提供学校数据结构文档，检查到的目录未包含所需毕业队列原始数据。2024 年出版的县级报告分别使用 2022 或 2023 队列，不能替代 2024 队列。

详细 URL、访问结果与排除原因见 [source_access_audit.json](source_access_audit.json)。本目录是访问审计，不是已取得的数据集；无虚构人数、模型新假设或数据准入。
