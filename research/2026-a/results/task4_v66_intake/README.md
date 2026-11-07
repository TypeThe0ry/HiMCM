# V66：取得新原件，保留未匹配的人群与年份

本轮取得上海121页职业教育质量年报、London 37页LTDS报告和Phoenix地区真实学生调查论文。它们没有提供可直接替换的同口径高中阶段数据。**250个效用区间及全部排名与V63保持一致，可能冠军仍为25城**；Singapore在辅助权重α∈[0.05,0.20]下仍为最小最大遗憾推荐。Shanghai第6、Cape Town第5、Phoenix第24。

## 本轮证据改变了什么

| 来源 | 核验发现 | 准入与下一步 |
| --- | --- | --- |
| [Phoenix真实学生调查](../../data/task4_v66_phoenix_students/README.md) | 2751份家长调查、35校，学段仅3—8年级；另有县域FY2005学生时长索引，原表未取得 | 两者均不代填当前Phoenix高中通学。需城市与当前高中学段联合记录 |
| [London LTDS新报告与字典入口](../../data/task4_v66_london/README.md) | 教育出行次数与通学时长不同；公开采购附件列字典线索，浏览器跳转退出登录页面 | 需取得原字典及可公开使用的人员—行程数据 |
| [Bogotá SIMUR替代入口](../../data/task4_v66_bogota/README.md) | 新2023总包链接已定位，403；公开目录API超时 | 未核实当前年级字段，不能断言它不存在 |
| [上海2025职业教育质量年报](../../data/task4_v66_shanghai_quality/README.md) | 正文9.59万学生是2024年；53所为独立设置且招生的普通全日制中职报告集合 | 不能与2025教师总数混配，需同年课程阶段与机构对应表 |

本轮改善了来源判断：区分真正学生调查与目标学段，识别年报标题年份与数字年份，并取得此前无法由网页工具读取的官方PDF。没有新增合格观测，因此不声称提高排名准确性、缩小冠军范围或形成新的算法创新。保留这些区间是当前证据下的结果。

## 复算与公式

```sh
python3 research/2026-a/scripts/task4_current_model.py --output research/2026-a/results/task4_v66_intake
```

[摘要](summary.json)记录当前注册表与基线哈希；[排名](ranks.csv)、[250格效用界](utility_bounds.csv)和[连续推荐证书](recommendation_certificate.csv)由同一次运行输出。原件哈希与关键定义检查分别见三个取得原件的数据目录中的 `audit.py`；上海年份和学段范围另经独立agent复核。

$$S_i(u;\alpha)=100\frac{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}}{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}+\sqrt{\sum_jw_j(\alpha)(1-u_{ij})^2}}.$$

主指标权重(1−α)/8，辅助指标α/2；默认α=0.1。通学效用exp(−t/30)，师资效用15T/(N+15T)。令城市i各项效用下上界为lᵢ、hᵢ：

$$L_i=S_i(l_i),\quad U_i=S_i(h_i),\quad R_i=\max\{0,\max_{k\ne i}U_k-L_i\},\quad i^*\in\arg\min_iR_i.$$

$$\mathcal C(\alpha)=\{i:U_i(\alpha)\ge\max_{k\ne i}L_k(\alpha)\}.$$

25城可能冠军指矩形外包下尚不能排除的城市；Singapore是最小最大遗憾选择，二者并不矛盾。跨城年份、地理和学段覆盖仍有条件，`main_admitted=false`。本轮没有修改Overleaf论文。
