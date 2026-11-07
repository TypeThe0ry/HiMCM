# V72：把墨西哥城通学人群校正为14—18岁

使用原始2020普查记录，修正此前3—17岁的年龄筛选。符合既有高中进阶假设的记录从7655增至9217，新增1562名18岁记录；可选成员从330降至86，保留未知年龄、学段与在读状态。原始数据与提取验证见[证据包](../../data/task4_v72_mexico/README.md)。本轮没有新增调查或下载。

| 结果 | V70 | V72 |
| --- | --- | --- |
| Mexico City通学效用 | [0.284942,0.557210] | [0.283284,0.543641] |
| Mexico City综合分区间 | [29.360768,72.664935] | [29.347410,72.502705] |
| Mexico City决策排名 | 19 | 19 |
| Singapore / Tokyo / Phoenix | 1 / 2 / 24 | 1 / 2 / 24 |
| 固定及连续权重范围内可能冠军数 | 25 | 25 |

只改变1格，其他249格逐格相同；全部决策排名保持，Kendall τ=1。连续α∈[0.05,0.20]仍推荐Singapore，认证未决0。年龄口径更贴近目标高中生；两个区间不嵌套，不能把人口更换称为同一总体精度提升。当前学段仍由已完成年级推断，并非直接观测，抽样误差尚未包含。

## 不确定成员如何进入模型

对条件性已分类样本加权总人数N及效用和端点A_L、A_U，未知资格记录权重w_r、效用[a_r,b_r]：

$$l=\min_{z_r\in\{0,1\}}\frac{A_L+\sum_rz_rw_ra_r}{N+\sum_rz_rw_r},\qquad h=\max_{z_r\in\{0,1\}}\frac{A_U+\sum_rz_rw_rb_r}{N+\sum_rz_rw_r}.$$

按端点排序枚举前缀求极值，并用独立线性分式规划核验。没有给未知记录指定在读概率。通学效用exp(−t/30)，教育资源效用15T/(N+15T)；核心区间TOPSIS与最小最大遗憾公式保持，完整公式见[当前压力检验](../task4_v72_joint_stress/README.md)。

## 本轮额外发现

[当前输入的压力重跑](../task4_v72_joint_stress/README.md)显示：仅扩张Singapore的不确定性时，ε=0.05、α=0.05已改推Tokyo；默认α=0.10下ε=0.075改推Tokyo。这比V69历史输入更早。与[本轮修订前V70冻结结果](../task4_v72_pre_revision_stress/README.md)一致，因此该脆弱性变化来自此前V70人口/岗位修订，不能归因于本轮Mexico City年龄修订。

Phoenix本轮未取得新可准入记录。ADE出现[FY2026 October1人数表](https://www.azed.gov/sites/default/files/2026/02/Oct1EnrollmentFY2026.xlsx)与[2025届毕业表](https://www.azed.gov/sites/default/files/2025/11/4Y-GradRate-Cohort2025.xlsx)入口；前者本机下载403，后者未取得原件。两者均未进入模型，缺失界保持。后续仍需同年、同城市、同高中学段及兼容教师口径。

## 复核与复现

原件哈希、276007条记录、旧V23分箱与端点完全复现；年龄边界、未知成员及独立LP两组四个端点检查通过。模型脚本断言其余249格不变；统一入口再核对250格、来源登记及冻结排名。压力检验另核验连续矩形与失效反例。

```sh
python3 research/2026-a/data/task4_v72_mexico/test_extract.py
python3 research/2026-a/scripts/task4_mexico_age_revision.py
python3 research/2026-a/scripts/task4_current_model.py
```

[排名对照](ranks.csv) · [全部输入](utility_bounds.csv) · [摘要](summary.json)。本轮未修改论文。
