# 三城官方通学来源核验：保留原有缺失区间

本轮定位到 Cape Town 可直接识别当前高中年级的调查字段，但未取得原始微数据。三个来源包均不新增城市观测。重新运行现有模型，Singapore仍为推荐城市，Phoenix第24，可能冠军25城，分数和排名与V27一致。

| 城市 | 新核验内容 | 本轮准入 |
| --- | --- | --- |
| Cape Town | GHS2023同一人员文件有地区代码、当前10—12年级、单程到校时间分箱、个人权重 | 微数据下载受阻，保留[0,1] |
| Istanbul | 2005问卷有高中学生编码；2012学校旅时均值对应另一套调查 | 年份及学段未对齐，保留[0,1] |
| Jakarta | 2023官方表分别提供当前学段和旅时边际分布 | 缺少学段与旅时联合记录，保留[0,1] |

本轮改善的是数据入口的可执行性，没有改善排名精度或缩小冠军范围。Cape Town下一步应取得GHS2023人员微数据，核验当前年级、地区、无旅程和未知成员记录，并检查个人权重及抽样设计；NHTS的Grade R—12混合类别不能替代当前高中年级。Istanbul的2005学生代码不能直接拼接到2012学校平均旅时。Jakarta两张边际表不能按比例配出高中时长。

## 模型公式保持

学生时长效用为 $u(t)=e^{-t/30}$。时间箱 $[a,b]$ 对应 $[e^{-b/30},e^{-a/30}]$；未知旅时为[0,1]。加入新数据前，还需处理未知在读身份、总体覆盖和抽样不确定性。

$$S_i=100\frac{\sqrt{\sum_jw_ju_{ij}^2}}{\sqrt{\sum_jw_ju_{ij}^2}+\sqrt{\sum_jw_j(1-u_{ij})^2}},\quad L_i=S(l_i),\quad U_i=S(h_i).$$

$$\mathcal C=\{i:U_i\ge\max_{k\ne i}L_k\},\qquad i^*=\arg\min_i\max(0,\max_{k\ne i}U_k-L_i).$$

[完整当前模型](../../design/task4_current_model.md)包含权重、实际人群范围和条件限制；本轮未改变算法。

- [Cape Town来源与字段](../../data/task4_v28_cape_town/README.md)
- [Istanbul来源与问卷](../../data/task4_v28_istanbul/README.md)
- [Jakarta表号审计](../../data/task4_v28_jakarta/README.md)
- [重跑脚本](../../scripts/task4_source_round_check.py) · [排名](ranks.csv) · [摘要及来源哈希](summary.json)

脚本逐城验证V27与本轮分数、决策名次一致（绝对容差1e-12），并断言三城通学界保持[0,1]。研究材料保存在GitHub，Overleaf论文未改动。
