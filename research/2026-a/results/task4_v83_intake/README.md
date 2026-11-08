# V83：补入Phoenix私校原始资料，保留覆盖未知

本轮首次下载NCES PSS2023/24完整公开学校记录及六份官方方法文件。在现有Phoenix市界内，33条有9—12年级学生的学校记录合计6109人；对应全学段估算FTE为888.6。抽样与非响应、教师跨学段分配、私校2023/24与公校2024/25不同年度仍未统一，因此没有修改主模型250格。

## 本轮实际改善

1. [私校原件与提取](../../data/task4_v83_phoenix_private/README.md)填补了此前只审计公校的资料空白。按物理州与坐标提取，发现13条记录的邮寄城市与市界归属不一致。独立代理用不同CSV读取和射线交叉算法复核，76个市界内学校ID、33个高中记录及6109人数全部一致。
2. [官方方法](../../data/task4_v83_pss_docs/README.md)澄清888.6是工作档位中点折算，档位支持全学段FTE范围[867.25,909.50]。保留这一测量不确定性，避免把折算点当精确高中教师量。全国覆盖估计不能替代Phoenix的局部覆盖率。
3. [Hope跨年核对](../../data/task4_v83_phoenix/README.md)：2025/26目录地址变为Tempe，学生统计仍为2024/25且被抑制。不能用新地址删除旧Phoenix记录以消除缺失。
4. [Nairobi同册核对](../../data/task4_v83_education/README.md)：公布PTR排除706名BOM教师，全部报告类别合计5465。原件未取得，仅保留阅读器转录；方法承认插补与私校覆盖缺口，未准入为精确全市资源指标。

Santiago仍缺原问卷对学历字段的定义，DANE官方微观下载页本轮浏览器确认403；新增可准入通学记录为0。以上成果是实际来源及测量口径改善，不声称冠军集合已缩小。

## 重跑结果与当前公式

[本轮排名](ranks.csv)与V79基准全部一致：Singapore第1、Tokyo第2、Cape Town第5、Phoenix第24。默认权重及连续偏好下可能冠军均25城。全部250格逐一核对一致，连续推荐证书无未决区间。

通学效用 $u_t=e^{-t/30}$；教学资源效用 $u_E=15T/(N+15T)$。八个主要指标各取 $(1-\alpha)/8$，两个辅助指标各取 $\alpha/2$；默认 $\alpha=0.1$，连续范围 $[0.05,0.20]$。

$$S_i=100\frac{\sqrt{\sum_jw_ju_{ij}^2}}{\sqrt{\sum_jw_ju_{ij}^2}+\sqrt{\sum_jw_j(1-u_{ij})^2}},\quad L_i=S_i(l_i),\quad U_i=S_i(h_i).$$
$$R_i=\max(0,\max_{k\ne i}U_k-L_i),\qquad \mathcal C(\alpha)=\{i:U_i\ge\max_{k\ne i}L_k\}.$$

推荐最小化最大遗憾R；可能冠军集合保留尚无法排除的城市。本轮新FTE档位公式见私校来源说明，仅作已发布学校记录的测量诊断，不自动替换城市指标。

运行各来源目录的提取／验证脚本后复算：

```sh
python3 research/2026-a/scripts/task4_current_model.py --output research/2026-a/results/task4_v83_intake
```

[运行摘要](summary.json) · [区间](utility_bounds.csv) · [证书](recommendation_certificate.csv)。未修改Overleaf论文。
