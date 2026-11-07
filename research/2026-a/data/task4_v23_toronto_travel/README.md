# Toronto 2022 TTS：实际公开表与高中通学字段核验

已下载官方 Toronto 两份 CSV 和完整数据字典；新增可纳入高中生通学效用的观测为 **0**。公开表包含 406 个汇总指标，但没有高中阶段 × 实际通学时长的联合记录，因此保留现有缺失区间。

来源是 University of Toronto Data Management Group 的 [TTS 下载页](https://dmg.utoronto.ca/download-tts-data/)。两份 2022 周期表分别含 16 个 Planning District 和 25 个 Ward，市级合计列的 406 项完全一致。CSV 首行说明旅次覆盖 5 岁及以上人员；少于 4 条样本记录的类别以 `*` 抑制，不能当作零。数据周期名为 2022，调查跨 2022 年秋季和 2023 年春季。

## 实际字段限制

[官方数据字典](https://dmg.utoronto.ca/wp-content/uploads/2024/12/2022TTS_Data_Guide-1.pdf)的页码：

- 第 55 页：`n_stu_k12` 是家庭 K–12 在读人数，学校阶段未知时使用年龄 5–17 岁补分类。该字段既未单列高中，也不全是直接报告的学校阶段。
- 第 63 页：`stu_stat` 区分全日制、非全日制、非学生和未知，未区分高中。
- 第 65 页：`sch_code` 是学校代码；详细学校代码表需联系 DMG 取得。本轮没有申请、发信或创建账户。已下载 CSV 不含逐人学校代码。
- 第 71–75 页：旅次字典列出出发时刻 `start_time`、目的、地理和直线／曼哈顿距离，没有到达时刻或时长变量。相邻活动的出发时刻差会包含活动停留，不能当作通学时长。

CSV 中的全日制学生合计 510,001、非全日制 57,580、学生状态未知 38,354，以及居民全天 home-based school trips 712,300 都是全学段背景量，没有进入高中模型。旅次数不是学生人数，home-based school 也包含返家方向。

## 复现

`python3 research/2026-a/data/task4_v23_toronto_travel/audit.py`

脚本校验下载文件 SHA-256、406 项市级合计的一致性、公开指标标签及字典关键字段。PDF 文本提取使用 `pdftotext`。结果保存于 [coverage_audit.json](coverage_audit.json)，下载 URL、字节数与哈希见 [download_manifest.json](download_manifest.json)。原始文件保持下载字节。

后续需要直接高中身份或可审计学校代码对照、实际旅时、市内居民筛选、权重与缺失记录。年龄分组、校车数量或路网估计时间不能补成已观测高中通学时间。
