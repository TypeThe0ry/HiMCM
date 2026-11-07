# V73：补齐教育和通学仍不足以识别冠军

用当前V72的250格输入重算：即使25城教育和通学两项全部精确测得，在默认α=0.10下仍至少有8城无法排除第一；允许α∈[0.05,0.20]时，可能冠军并集仍至少21城。只补Phoenix这两格，25城均无法排除。真实数据、排名和可能冠军集合保持：Singapore第1、Tokyo第2、Phoenix第24，25城可能第一。

这是对未来观测结果的普遍下界：所选格的精确值无论落在当前区间何处，名单内城市都仍可能第一。不同城市可有不同的权重见证；下界不保证能被同一组观测同时达到。它不是预测、采集成功率或模拟观测。

| 假想精确测得的范围 | 默认权重：冠军数下界 | 连续权重：并集下界 |
| --- | ---: | ---: |
| 所有城市教育 | 25 | 25 |
| 所有城市通学 | 24 | 25 |
| 所有城市教育＋通学 | 8 | 21 |
| 仅Phoenix教育＋通学 | 25 | 25 |
| 全城教育＋通学＋凶杀率 | 1 | 5 |
| 全城教育＋通学＋PM2.5 | 6 | 20 |
| 全城教育＋通学＋研究高校密度 | 1 | 1 |
| 全城教育＋通学＋公共交通密度 | 1 | 1 |
| 全城教育＋通学＋固定宽带 | 7 | 20 |
| 全城教育＋通学＋公共泳池密度 | 1 | 1 |

成本和房价收入比的追加情景仍为8/21，详见[完整摘要](summary.json)。表中1可能仅来自“总有至少一城可能第一”的一般事实，绝不代表补这些数据就能选出唯一冠军。教育在这里指现有师生资源指标，不是新增毕业率指标。所选50个教育/通学格中48格非点值。

## 算法为什么能回答“补数是否足够”

令M为计划测准的单元集合。对候选i，构造对它最不利的测量结果：把它自身M内的值取下端点，把所有竞争城市M内的值取上端点。其余格仍保留原区间。记此时候选的上界效用向量为a_i、竞争城市的下界向量为b_k：

$$a_{ij}=\begin{cases}l_{ij},&(i,j)\in M,\\h_{ij},&\text{其他},\end{cases}\qquad b_{kj}=\begin{cases}h_{kj},&(k,j)\in M,\\l_{kj},&\text{其他}.\end{cases}$$

若

$$S(a_i;\alpha)\ge\max_{k\ne i}S(b_k;\alpha),$$

那么任何所选格的真实精确结果都不能排除i。对于连续偏好，在[0.05,0.20]内寻找满足全部不等式的共同α；TOPSIS比较化为二次多项式，按全部实根分段，而非仅扫网格。每个城市各自最不利的观测赋值可以不同，因此只报告人数下界，不声称联合最小值。

## 当前数学模型与实现

$$S_i(u;\alpha)=100\frac{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}}{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}+\sqrt{\sum_jw_j(\alpha)(1-u_{ij})^2}},$$
$$L_i=S_i(l_i),\quad U_i=S_i(h_i),\quad R_i=\max(0,\max_{k\ne i}U_k-L_i),\quad i^*\in\arg\min_iR_i,$$
$$\mathcal C(\alpha)=\{i:U_i\ge\max_{k\ne i}L_k\}.$$

八项主指标各权重(1−α)/8，两项辅助指标各α/2，默认α=0.10。通学exp(−t/30)，教育岗位资源15T/(N+15T)。来源条件与缺失区间保持，`main_admitted=false`。

新[统一诊断入口](../../scripts/task4_registered_acquisition_limits.py)读取当前模型注册表及权重设置。原证书函数增加显式权重参数，旧默认行为保持。运行前检查输出分析类型、模型版本、权重及输入哈希，拒绝覆盖另一分析或不同基线；结果不写回证据矩阵。此前V68教育/通学下界17/24属于旧输入，现更新为V72下的8/21；这反映输入修订，不能解释为本轮新增数据缩小了真实冠军集。V64最少推荐补数分析仍是历史结果，并未在本轮刷新。

## 数据获取进展

Phoenix新增官方[FY2026 October1表](https://www.azed.gov/sites/default/files/2026/02/Oct1EnrollmentFY2026.xlsx)与[2025届毕业表](https://www.azed.gov/sites/default/files/2025/11/4Y-GradRate-Cohort2025.xlsx)本轮均未取得：requests返回403，浏览器官方目录显示访问被阻止，未取得可用验证或下载入口。未将链接当作已取得记录，未混用年度。

London公开LTDS仍未取得高中身份与时长的联合资料。Toronto的Forest Hill完整报告仍不可下载；新核查[Census at School Secondary通学表](https://censusatschool.ca/data-results/2020-2021/time-to-school/)为加拿大参与课堂汇总，项目[自愿参与](https://censusatschool.ca/about/)，缺少Toronto居住地及城市抽样权重，未准入。以上缺失格保持原样。

## 验证与下一步

统一模型核对250格及冻结排名。4项测试覆盖非默认权重、穷举精确补数结果、固定与连续范围退化一致性、错误分析覆盖拒绝；独立审查另复算300行证书与25组随机三格穷举。所有输入保持不变，数值证书保留浮点容差，非形式化区间算术。

仍优先获取高中教育和真实通学资料；若目标是缩小冠军集，还需按现有定义补其他指标，尤其检查凶杀率和辅助设施指标的城市覆盖。下界较小只是没有被本检验排除的路线，不证明采集成本低、结果有利或指标本身更重要。

```sh
python3 research/2026-a/scripts/task4_registered_acquisition_limits.py --output research/2026-a/results/task4_v73_acquisition_limits
python3 -m unittest discover -s research/2026-a/scripts -p 'test_task4_acquisition_limits.py'
```

[逐城证书](certificates.csv) · [当前排名](baseline/ranks.csv)。本轮没有改动Overleaf论文。
