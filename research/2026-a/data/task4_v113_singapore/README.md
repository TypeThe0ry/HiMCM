# Singapore：补入已实际开学的艺术大学，保留通学和师资缺口

新增原件确认 University of the Arts Singapore（UAS）是独立的学位授予大学，2024 年已招收首届本科与研究生。此前经核验名录仅列六所自治大学，没有 UAS。本次按现有“经核验独立高教机构”规则新增一所；不另计其成员 LASALLE 和 NAFA，不把新增大学数量解释为高中教育质量或高中生实际可达性。

## 原始证据

- [MOE 2022-08-30 公告](https://www.moe.gov.sg/news/press-releases/20220830-new-private-university-of-the-arts-singapore-formed-by-alliance-between-nafa-and-lasalle-to-open-in-2024)：确认政府支持的私立大学、中央实体 UAS Ltd 及独立学位授予职能。原件 `moe_announcement.html`。
- [大学官方介绍](https://uas.edu.sg/about-us)：确认首届学生于 2024 年 8 月入学，学位由 UAS 授予。原件 `uas_about.html`。与既有 MOE ESD2025 原件（`../task4_v38_singapore/esd2025.pdf`）对大学身份与实际入学年度的说明一致。
- [大学官方联系页](https://uas.edu.sg/contact-us)：中央地址为 111 Middle Road, National Design Centre, Singapore 188969。原件 `uas_contact.html`。这是机构中央地址，不将三个地址或两个成员学院重复计数。

四份新下载原件的 URL、2026-11-08 访问日期、字节数和 SHA256 见 `manifest.json`。HTTP200 后另校验正文关键事实，未把状态码本身当作成功证据。

## 同口径计算

沿用旧名录的全新加坡城市国家范围及 2026 年人口 6,208,500，不修改人口年、转换尺度或权重。现有总体本来就是高校部分名录，下界补充不意味着完整覆盖。

| 量 | 补前 | 补后 |
|---|---:|---:|
| 经核验机构数下界 | 6 | 7 |
| 每十万人机构数下界 | 0.0966417009 | 0.1127486510 |
| 高教资源效用下界 | 0.0881251377 | 0.1013244554 |
| 高教资源效用上界 | 1 | 1 |

沿用 $x=n/P\times100000$，$u=x/(1+x)$。November 2026 网站快照和 June 2026 分母均保留真实年份，不写成 2025 观测。此包只提出一个单元下界更新，城市排名由主模型重跑决定；不预设冠军范围缩小。

## 仍未得到的证据

[SingStat 官方 SDG4.c.1 元数据](https://www.singstat.gov.sg/find-data/sustainable-development-goals/goal-4/indicator-4-c-1) 明确说明中学教师因跨学段任教，不分列 lower/upper secondary。原件 `singstat_teacher_scope.html` 中说明位于页面序列化内容，可由提取器直接核验。此证据支持保留原师资分配区间，没有提供可用于缩界的新数字。

另查阅 [MOT 2025-11-06 对 2024 Household Travel Survey 的答复](https://www.mot.gov.sg/news-resources/newsroom/weekday-commute-times-based-on-lta-s-latest-household-travel-survey-separated-by-household-types-and-income/)，其通学时长按住房／收入分组，没有高中年龄×当前年级子群。这个网页只用于发现范围缺口，未下载为本包输入，也不据其全年龄学生统计缩小高中生通学区间。既有 V70/V71 的通学缺口仍然成立。

## 复核

从仓库根目录运行 `python3 research/2026-a/data/task4_v113_singapore/extract.py`。程序验证四个原件哈希、正文、六所原名录身份、新机构不重复、原人口分母，并导出 `verified_inventory.csv` 和 `observation.json`。没有更改主模型注册表、其他数据或论文。
