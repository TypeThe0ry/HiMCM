# V75：取得Athens完整校级数据并完成高中子集核对

本轮解决了Athens原件下载障碍，取得27703条历史学生记录和14181条学校目录记录。通过城市、唯一校名及学段/类型核对，得到2019标记下48所匹配高中、10406名注册学生的可复核子集。还取得Phoenix两个校内项目的明确官方说明。科学模型仍为V72：250格和全部排名不变，Singapore第1、Tokyo第2、Phoenix第24，固定及连续权重范围内可能冠军仍25城。

## 已完成的实质进展

[Athens原件与提取](../../data/task4_v75_athens/README.md)现在可以离线复算。分段下载核对206响应、连续字节范围和同一ETag；ZIP CRC及官方内嵌CSV MD5全部通过。2019精确校名匹配45校9454人，保守删除标点/空白后补回3校，得到48校10406人。学段变化、非唯一名称及剩余3所未匹配学校未被强行合并；没有填0或把全国记录当雅典记录。

这些是学校子集，不是完整市级或居民高中生人数。年份标签2018/2019没有明确学年解释，目录无年份；年龄也不可筛选。[ELSTAT教师表核查](../../data/task4_v75_athens_teachers/README.md)给出2018/19与2019/20的Attiki普通高中岗位8628/8823，统计范围包含长期缺勤及借调人员，又未涵盖完整职业/特殊高中池。不能任选一期或取最大值当成已证实的同年城市教师上限。保留教育和通学[0,1]。

[Phoenix新原件](../../data/task4_v75_phoenix/README.md)进一步确认ARCH及Maryvale Gifted & Talented为校内项目，补强V74仅凭同址尚不足的目录解释。它们仍不证明队列去重、转学毕业归属或教师人数分配，未据此从Digital队列或全市分母中减数。

## 当前公式与结果

令效用uᵢⱼ∈[lᵢⱼ,hᵢⱼ]，通学效用exp(−t/30)、教育岗位资源效用15T/(N+15T)。八项主指标各权重(1−α)/8，两项辅助指标各α/2，默认α=0.10、检验[0.05,0.20]。

$$S_i(u;\alpha)=100\frac{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}}{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}+\sqrt{\sum_jw_j(\alpha)(1-u_{ij})^2}},$$
$$L_i=S_i(l_i),\quad U_i=S_i(h_i),\quad R_i=\max(0,\max_{k\ne i}U_k-L_i),\quad i^*\in\arg\min_iR_i,$$
$$\mathcal C(\alpha)=\{i:U_i\ge\max_{k\ne i}L_k\}.$$

本轮城市准入单元变化0、排名变化0、可能冠军变化0；连续偏好推荐Singapore，未决0。`main_admitted=false`继续保留。这轮改善的是原件可获得性、学校身份匹配和后续分母核查基础，没有产生新的城市教育质量估计。

## 验证与下一步

另一agent独立复算ZIP/MD5、两年精确与标准化匹配人数、名称冲突和未匹配学校，全部一致；教师及Phoenix资料各有出处、哈希和范围审计。统一入口复核全部250格、冻结排名及连续推荐。后续首先核实学生年份语义和目录时点，再取得兼容范围的教师资料；Phoenix仍需官方队列归属和实际师资分配。

[本轮排名](baseline/ranks.csv) · [模型复算摘要](baseline/summary.json)。未修改论文。

```sh
python3 research/2026-a/data/task4_v75_athens/extract.py
python3 research/2026-a/data/task4_v75_athens_teachers/audit.py
python3 research/2026-a/data/task4_v75_phoenix/audit.py
python3 research/2026-a/scripts/task4_current_model.py --output research/2026-a/results/task4_v75_sources/baseline
```
