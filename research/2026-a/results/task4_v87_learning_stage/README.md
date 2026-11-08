# V87：高中学段统一后，真实学习成果如何影响评价

本轮使用同一PISA2022国际微观数据库，识别5个学校地域内的高中阶段学生。把“年级至少10”改为国际教育阶段编码ISCEDP的3xx，补回Singapore340名、Dubai96名被旧规则遗漏的学生；实际降低两地数学基础达标率。当前资源模型保持V79，新增学习成果作为独立替代检验。

## 真实学习成果与目标人群修正

[原件来源、城市筛选和复算](../../data/task4_v87_pisa_cities/README.md)保留19012条城市子集记录、10个合理值及80个复制权重。全库原始ZIP/SAV在仓库外，城市派生压缩数据约4.1MB。

数学达标定义为达到PISA Level2，即合理值至少420.07分，按[官方阈值](https://nces.ed.gov/surveys/pisa/pisa2022/technical-notes/index.asp)逐个合理值分类后加权。它直接测量基础数学学习成果，避免给PISA均值任意设置效用锚点。

| 学校地域 | 当前高中样本 | 年级≥10规则达标率 | ISCED3规则达标率 | 阶段修正 |
| --- | ---: | ---: | ---: | --- |
| Bogotá | 1399 | 58.05% | 58.05% | 两规则一致 |
| Dubai emirate | 6030 | 70.98% | 69.91% | 补回96人 |
| Greater London | 777 | 78.30% | 78.30% | 两规则一致 |
| DKI Jakarta | 1145 | 46.45% | 46.45% | 两规则一致 |
| Singapore | 6534 | 92.66% | 92.06% | 补回340人 |

这次修正降低Dubai达标率1.064个百分点、Singapore0.593个百分点；不是城市教育质量在时间上下降。原始样本实际年龄约15.25—16.42岁，范围因地区而异。估计针对被调查学校内相应年龄、阶段学生；升留级选择、非响应、学校地域与居民地域差异不由抽样标准误覆盖。Dubai emirate、Greater London和DKI Jakarta到候选城市的对应仅用于明确标注的条件检验。

## 模型对照：区分指标替换与学段修正

保持其他9项指标及权重不变，运行三种设定：

1. 当前V79教师资源模型。
2. 教育列替换为数学达标比例，使用年级≥10筛选。
3. 同一学习成果列，修正为ISCED3筛选。

后两者中，未取得可识别学习成果的20城均为[0,1]，不沿用教师资源值填补。这是指标构念替换；它也改变了证据覆盖，排名变化不能全部归因于新增5地的真实表现。

| 城市 | 资源基准名次 | 年级筛选学习模型 | 学段修正学习模型 |
| --- | ---: | ---: | ---: |
| Singapore | 1 | 1 | 1 |
| Dubai | 11 | 2 | 2 |
| Bogotá | 10 | 4 | 4 |
| London | 17 | 6 | 6 |
| Jakarta | 18 | 20 | 20 |
| Phoenix | 24 | 24 | 24 |

指标替换改变多座城市的决策名次；学段修正本身名次变动为0，Kendall τ=1，变化体现在得分区间。三种设定在默认权重和连续辅助权重α∈[0.05,0.20]下均保留25个可能冠军，连续最小最大遗憾推荐均为Singapore，未决区间0。没有据此宣称唯一冠军或正式替换主模型。

本轮实际改善有两项：直接测量高中群体的学习成果；用国际学段编码纠正跨教育体系的年级错配。冠军范围未缩小。当前通学数据及缺失界完整保留。

## Phoenix补数

[官方财政报告转录](../../data/task4_v87_phoenix/README.md)找到North Star FY2024年末教师FTE6.00的线索；同表高中平均日成员数ADM755.1591与CCD秋季人数1554定义和时点不同，未拼成师生比。官方原件下载403，保留网页读取转录及准确下载入口，尚不能替代全市缺失教师界。

## 当前数学公式与新增估计

主模型仍采用 $u_E=15T/(N+15T)$，通学效用 $u_t=e^{-t/30}$。整体评分、遗憾和可能冠军条件保持：

$$S_i=100\frac{\sqrt{\sum_jw_ju_{ij}^2}}{\sqrt{\sum_jw_ju_{ij}^2}+\sqrt{\sum_jw_j(1-u_{ij})^2}},$$
$$L_i=S_i(l_i),\quad U_i=S_i(h_i),\quad R_i=\max(0,\max_{k\ne i}U_k-L_i),\qquad
U_i\ge\max_{k\ne i}L_k\ \text{表示可能冠军。}$$

8项主指标各权重 $(1-\alpha)/8$，2项辅助指标各 $\alpha/2$，默认α=0.1。

学习成果替代检验中，令 $H_s=1\{300\le ISCEDP_s<400\}$、学生权重为 $a_s$，则每个合理值的达标比例为

$$p_m=\frac{\sum_s a_sH_s1\{PV_{sm}\ge420.07\}}{\sum_s a_sH_s},\qquad \hat p=\frac1{10}\sum_{m=1}^{10}p_m.$$

用80个复制权重得到 $p_{mr}$，总方差为

$$\widehat V=\frac1{10}\sum_m\frac4{80}\sum_r(p_{mr}-p_m)^2+
\frac{1.1}{9}\sum_m(p_m-\hat p)^2.$$

两个筛选规则×5地共10项比例，使用Bonferroni正态近似区间

$$[\max(0,\hat p-z\sqrt{\widehat V}),\min(1,\hat p+z\sqrt{\widehat V})],\quad z=\Phi^{-1}(1-0.05/20)=2.80703.$$

这是抽样及合理值方差的近似同时置信包络，不包含所有覆盖偏差，也不是确定性的缺失识别界；将其送入评分的排名同样受这些条件约束。

## 验证与复现

独立代理按标量循环复现60组均值/标准误，最大误差1.71×10⁻¹³；三个评分情景共75城次得分、遗憾、名次及可能冠军标志独立复算一致。原始合理值先检查缺失再阈值分类，避免NaN被误判为不达标。225个非教育单元保持不变。

```sh
python3 research/2026-a/data/task4_v87_pisa_cities/analyse.py
python3 research/2026-a/scripts/task4_learning_stage_sensitivity.py
python3 research/2026-a/scripts/task4_current_model.py --output research/2026-a/results/task4_v87_intake
```

[完整名次对照](rank_comparison.csv) · [学习成果包络](learning_intervals.csv) · [情景摘要](summary.json) · [当前主模型重跑](../task4_v87_intake/summary.json)。论文及Overleaf未改动。

后续[V88数值分解](../task4_v88_coverage_attribution/README.md)区分撤回旧资源信息、共同城市指标替换及新增学习成果证据对名次变化的贡献。
