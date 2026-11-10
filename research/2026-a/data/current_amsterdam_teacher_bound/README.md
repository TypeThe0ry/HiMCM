# Amsterdam 教师 FTE 全国上界核查

**结论：本次没有可准入的部分区间。** 建立城市高中生师比下界需要同一参考时期内的正值城市高中学生子集，以及覆盖所有目标提供者的实际全国教师 FTE 上界。本包考察的全国数列不能证明后者；V203 的 Amsterdam `upper_secondary_ptr` 效用仍为 `[0,1]`。没有改动模型、论文或输入。

## 可复核的全国数值

[Eurostat API 原件](eurostat_nl_2021_fte.json)为 `educ_uoe_perp02`、Netherlands、2021、男女合计、机构类型合计、`TOT_FTE`。`id` 的维度顺序与 `size` 表明只有 `isced11` 维度多于一个元素；其 `category.index` 中 `ED2=4`、`ED3=5`，对应 `value` 的键 `4=45309`、`5=46539`。两个位置均不在 `status` 对象中；这只表示响应未给这两个位置标志，**不是完整实测或单侧上界证明**。机械相加 91,848 是候选诊断值，不能当全国实际总量硬上界，也未用于评分。文件提取、哈希、原始 URL 见 [retrieval.json](retrieval.json)，机器可读范围见 [scope.json](scope.json)。

[OECD 2023 技术说明](oecd_eag2023_notes.pdf) PDF 第 422 页、Netherlands 段写到私立机构教师人数按其学生数及公立机构师生比估计（原文短摘：“teachers in private institutions is estimated”）。估计量没有已验证的单侧误差上界，不能假定高于真实值。该技术说明提供方法风险证据；本次没有证明其参考学年与上述 Eurostat 2021 单元完全对应，也没有将其视为所有年份均按同样方法处理的证明。

## DUO 来源范围

[DUO 全国 FTE 页面](duo_fte_page.html) 的“质量”部分写明并非所有机构已报送，全国第 1–3 个表页使用权重补充缺报；因此其全国表不是已证实覆盖全部目标教师的实际总 FTE。[DUO IPTO 方法文件](duo_ipto_method.pdf) PDF 第 2 页区分实际授课人数与 `Onderwijs in cijfers` 中的教育人员，并指出后者不包括非雇员授课人员；该 IPTO 数据是人数而不是可直接替代的 FTE。

[DUO 学生页面](duo_pupil_page.html)列有 2021 按校区和学校类型的学生数据；该下载入口本次未进一步核对单校位置、学段、保密处理或与教师数据的参考年匹配。即使存在正值学生子集，也不能弥补缺失的教师硬上界。

若未来证实同年且覆盖所有目标提供者的教师 FTE 上界 `T_max` 和城市高中学生数下界 `N_min > 0`，则师生比下界为 `N_min/T_max`，对应效用上界为 `15/(15+N_min/T_max)`。该计算依赖覆盖与计量的集合包含关系，而不是将全国点估计或工资名册小计视为硬上界。
