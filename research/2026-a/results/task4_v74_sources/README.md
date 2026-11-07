# V74：补齐学校级证据，保留尚未识别的城市统计

本轮取得新的学校级官方资料，缩小了后续核查的具体问题。科学模型保持V72；当前250格输入和全部排名与冻结基线一致，Singapore第1、Tokyo第2、Phoenix第24，固定及连续α范围内仍有25个可能冠军。连续推荐仍Singapore，未决0。此次资料获取没有被包装成城市分数改善。

## 新资料实际解决了什么

- [Phoenix三份官方原件](../../data/task4_v74_phoenix/README.md)：解释了21个NCES行政记录与23校介绍的数量差异。2023可见地图含24个学校名称，其中3个为额外项目名称；历史页记载Educator Preparatory于2024关闭。地图有重叠旧文字层，已按渲染页面核对，避免误数学校或把支持设施当学校。目录名称解释并未证明毕业队列归属及师生去重。
- [Toronto两份官方原件](../../data/task4_v74_toronto/README.md)：找到Toronto Ouest的28条教师目录记录和四校合计57.49的计划Secondary教学配置。同校另有7–8年级，目录缺少实际FTE和高中岗位分配；预算不等于实际岗位。后续可以向这些具体表格对应的实际年终统计核对，不能用计划比例分摊全学区教师。

- [Athens官方目录与下载审计](../../data/task4_v74_athens/README.md)：定位到学校级学生与学校目录资源，但CSV传输在3,456,385字节处中断，两个ZIP下载超时，没有取得完整数据。新教师目录只覆盖私立学校，不能作为全市教师上界。保留目录和失败状态，不使用部分传输推算人数。

Phoenix、Toronto和Athens的教育、通学未知区间保持；其余已有条件性数据仍按原定义使用。没有把少数学校当成全市、没有将缺失教师数填成0。

## 当前公式

通学效用为exp(−t/30)，t为单程分钟；教育岗位资源效用为15T/(N+15T)，N、T须具有相容的学校范围和时期。八项主指标权重(1−α)/8，两项辅助指标α/2，默认α=0.10，检验范围[0.05,0.20]。

$$S_i(u;\alpha)=100\frac{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}}{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}+\sqrt{\sum_jw_j(\alpha)(1-u_{ij})^2}},$$
$$L_i=S_i(l_i),\quad U_i=S_i(h_i),\quad R_i=\max(0,\max_{k\ne i}U_k-L_i),\quad i^*\in\arg\min_iR_i,$$
$$\mathcal C(\alpha)=\{i:U_i\ge\max_{k\ne i}L_k\}.$$

矩形区间及人口、学段、地理、年份条件保留，`main_admitted=false`。决策排名不代表已识别真实优劣顺序；可能冠军不是胜率。

## 复核

Phoenix原件哈希、21个行政标识集合、课程目录说明与特殊码检查通过；可见地图另由两名agent独立检查。Toronto提取核对哈希、教师栏条目唯一性、四校预算列及合计，另检查实际PDF页。统一入口核对250格、来源登记、冻结排名及连续偏好推荐。

[本轮排名](baseline/ranks.csv) · [完整复算摘要](baseline/summary.json) · [当前补数能力下界](../task4_v73_acquisition_limits/README.md)。没有修改Overleaf论文。

```sh
python3 research/2026-a/data/task4_v74_phoenix/audit.py
python3 research/2026-a/data/task4_v74_toronto/extract.py
python3 research/2026-a/scripts/task4_current_model.py --output research/2026-a/results/task4_v74_sources/baseline
```
