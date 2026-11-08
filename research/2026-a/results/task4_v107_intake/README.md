# V107：实际更新Mexico City通学输入

本轮主模型更新至V107。INEGI新发布的EIC2025 CDMX原始居民资料通过独立核验，用于替换2020通学来源；同时放松跨学段进阶假设，保留已完成初中者是否属于当前高中群体的不确定性。仅改1格，其余249格不变，撤回可精确恢复V102。论文未修改。

| 结果 |V102|V107|
|---|---|---|
|Mexico City通学效用|[0.283284,0.543641]|[0.213824,0.584100]|
|Mexico City决策排名|20|23|
|固定／连续可能冠军|25／25|25／25|
|连续保守推荐|Singapore|Singapore|

只更新年份的控制为第21；仅放松旧年分类为第23。修订改善了数据时效和分类透明度，尚未缩小冠军范围。区间变宽体现新增保留的不确定性，不能称为估计精度提高。[五情景对照、人数和证明](../task4_v107_mexico_revision/README.md)。

## 其他数据路线

Phoenix取得官方Report Card页面和前端脚本，确认All Enrolled表示在该校就读且参加测试者，并非所有在册学生。该定义与既有Assessment DetailsFAY接口相连；仍缺legacy AzMerit/type1与当前考试品牌、有效成绩分母的完整对应，未重释319条结果或填入师生比。[原始定义](../../data/task4_v107_phoenix/README.md)。

Jakarta的[BPS2023官方目录](https://silastik.bps.go.id/v3/index.php/mikrodata/view/aUR5VUVFTXM1Vnd2RFdiTHZ3MTRLQT09)列出居住地、年龄、当前学段／年级、去返旅时和权重，但实际记录未取得。调查只直接覆盖跨市县commuter，不能把其均值当全市高中生均值；仍需与全体目标居民匹配的覆盖份额，将未覆盖人群保留未知。没有用字段目录冒充观测，也未重复归档失败响应。

## 当前数学公式

通学$u_t=e^{-t/30}$；师资$u_E=15T/(N+15T)$；八项主指标权重$(1-\alpha)/8$，两项辅助指标$\alpha/2$，默认α=.10，连续范围[.05,.20]。

$$S_i=100\frac{\sqrt{\sum_jw_ju_{ij}^2}}{\sqrt{\sum_jw_ju_{ij}^2}+\sqrt{\sum_jw_j(1-u_{ij})^2}},\quad L_i=S_i(l_i),\quad U_i=S_i(h_i).$$
$$R_i=\max(0,\max_{k\ne i}U_k-L_i),\quad i^*\in\arg\min_iR_i,\quad\mathcal C(\alpha)=\{i:U_i\ge\max_{k\ne i}L_k\}.$$

Mexico成员资格用加权分式极值求界，不作可选成员概率插补。新输入仍为条件性样本识别界，未包含复杂抽样置信包络。此前补数、压力和精度诊断保持原版本标签，不能冒称已按V107重算。

数据处理：新原始个人ZIP只在本地忽略目录，GitHub发布无个体记录的充分聚合数据与复现入口。此前EPJA旧提交清理仍等待已请求的历史重写授权。

[当前排名](ranks.csv) · [250格](utility_bounds.csv) · [摘要](summary.json)。

验证：2020与2025原始记录分别经独立聚合核查；5情景1250格、125排名和10段连续推荐证书通过独立算法；分类边界4项、当前入口5项、通学索引4项及公开离线复算／单格撤回2项测试通过。
