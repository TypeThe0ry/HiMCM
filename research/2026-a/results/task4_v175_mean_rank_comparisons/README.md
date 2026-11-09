# V175：用已有数值误差界区分蒙特卡洛平均名次的先后

37个既有模拟设定的4440项城市间平均名次比较中，4254项的方向可由原有同时误差界认证，186项尚未区分；22个设定可认证唯一最小期望平均名次。这里比较的是各自声明模拟分布中的期望平均决策名次，数值越小越好。它为用户提出的“按平均名次排序”增加可核验的比较精度，不替换固定权重的最小最大遗憾决策。

一个直接影响解读的例子是基线偏好κ=100：Oslo−Zurich的样本平均名次差为−0.1528，差值界为[−0.866563,0.560963]。样本表中Oslo在前，但该数值证书不能认证其模拟期望严格更小。原始均值、排名、抽样和当前论文保持。

## 同一事件上的差值界

[V169](../task4_v169_mc_precision/README.md)已对2064个基础均值建立共同至少95%的数值误差事件，条件是每个设定内draw按声明机制IID。跨城市、证据臂和设定可以共享draw，事件不要求这些均值互相独立。

在该共同事件中，若μ_A∈[L_A,U_A]、μ_B∈[L_B,U_B]，直接有：

    μ_A−μ_B ∈ [L_A−U_B, U_A−L_B]。

当上端小于0时认证A的期望平均名次更小；下端大于0时认证B更小。否则保留未区分。4440项都是原事件的逻辑推论，不为每项再分配显著性，也不把共同95%写成4440个独立95%检验。本程序用1e−12符号保护；序列化端点是近似展示，最接近零的已认证端点仍相距0.002736996，分类不依赖末位舍入。

## 偏好敏感性中的具体含义

每组16城产生120个无序城市对。下表“未被排在后面的集合”指没有另一城市被本证书认证具有更小期望平均名次的城市；它不是均值相等、真实夺冠或主模型可能冠军集合。该集合若只有一城，其均值上界严格低于其余15城的下界，便能在原事件上认证严格最小。

| 分析者偏好 | κ | 方向已区分 | 尚未区分 | 未被排在后面的集合 |
| --- | ---: | ---: | ---: | --- |
| baseline | 100 | 112 | 8 | Oslo, Singapore, Zurich |
| education_priority | 100 | 114 | 6 | Oslo, Singapore |
| independent_living_priority | 100 | 111 | 9 | Singapore, Zurich |
| baseline | 20 | 110 | 10 | Oslo, Zurich |
| education_priority | 20 | 115 | 5 | Oslo |
| independent_living_priority | 20 | 112 | 8 | Oslo, Zurich |
| baseline | 500 | 113 | 7 | Oslo, Singapore, Zurich |
| education_priority | 500 | 115 | 5 | Oslo, Singapore |
| independent_living_priority | 500 | 113 | 7 | Zurich |

九个偏好设定中，教育优先κ=20认证Oslo的条件期望平均名次最小，独立生活优先κ=500认证Zurich最小；其他七组有多城未被区分。κ控制围绕分析者指定中心的权重扰动集中程度，不代表年龄或调查样本量。不同偏好使用的中心权重仍是原来的构造值，没有新增AHP调查。

全部37组分别属于9个偏好设定、12个未来假设冲击设定和16个固定情景随机权重设定。只在同一设定内比较；未来表与偏好表的并列名次定义不同，不跨族合并均秩。全部比较见[pairs.csv](pairs.csv)，逐组摘要见[settings.csv](settings.csv)，每城已有均值界和已认证前后关系见[cities.csv](cities.csv)。这是均值差的界，不是逐draw两城胜负频率；不生成胜率网络、PageRank或新综合排名。

## 验证、来源与本轮改善

运行：

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-v120/bin/python research/2026-a/scripts/task4_v175_mean_rank_comparisons.py
PYTHONDONTWRITEBYTECODE=1 .venv-v120/bin/python research/2026-a/scripts/audit_task4_v175.py
```

生成器默认只写新的本目录，已存在非空目录时拒绝覆盖；复跑生成器须用`--output-dir`指定新空目录。审计器核验已存的本目录，用50位Decimal重新计算原始Hoeffding半宽，并从三个冻结MC导出核对592个均值及所有4440项差值、592个城市记录、37组摘要；还检查关系无环、传递及每个单城集合均直接优于其余15城。独立agent另用Decimal逐项复核，计数相同。输入和输出哈希见[summary.json](summary.json)与[verification.json](verification.json)，187项科学及590项已有论文文件保持。

本轮另取得[Zurich官方年度工作量原件与口径记录](../../data/task4_v175_zurich_payroll/README.md)。全年教学VZE尚不能给秋季普查时点上界，保持0准入、0评分收窄。新的实际改善是明确既有均秩榜单中4254项有数值方向保证、186项须保留未区分；没有重放draw、改变随机分布或补全缺失指标。

保证范围沿用V169：声明模拟分布下的MC积分误差，不是现实胜率、未来预测校准、来源误差或识别区间统计覆盖率。更精细的配对draw信息可能进一步缩界，本轮没有取得或假造该信息。主16城V154仍Zurich保守推荐、16可能／0必要冠军；论文V173及页眉页脚、队友main/ref/class、主文件设置保持。研究公开push继续待既有选择，私有Overleaf只新增支持材料，长期goal active。
