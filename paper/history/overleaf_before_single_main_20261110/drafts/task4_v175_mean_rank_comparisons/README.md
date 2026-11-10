# V175：已有MC平均名次的比较精度

37个既有模拟设定共4440项同设定城市比较，4254项可认证期望平均名次的严格方向、186项尚未区分。22个设定可认证严格最小期望平均名次。沿用V169对2064基础均值的共同至少95%事件及每设定内IID抽样假设：若均值界为[L_A,U_A]和[L_B,U_B]，差值界为[L_A−U_B,U_A−L_B]；派生比较不需额外多重校正，跨城市和设定共享draw允许。

基线偏好κ=100，Oslo−Zurich样本均秩差−0.1528，差值界[−0.866563,0.560963]，未认证严格先后。九个偏好设定中，教育优先κ=20认证Oslo最小、独立生活优先κ=500认证Zurich最小，其余七组保留多城未区分。均秩比较不等于逐draw胜负频率或真实冠军概率；κ不是年龄或调查人数。

[全部差值](pairs.csv)、[各设定摘要](settings.csv)、[城市均值界及前后关系](cities.csv)、[输入身份与条件](summary.json)、[Decimal审计](verification.json)。未被认证排在后面的城市组成待区分集合，不表示均值相等，也不等于主模型的可能冠军集合。不同族并列名次定义保持，不跨设定合并排名。592原始均值、4440差值、592城市与37摘要经50位Decimal及独立agent逐项核验；187科学／590已有论文文件保持。未重放draw、未改模型。

本轮取得[Zurich州官方2024薪资统计](https://www.zh.ch/content/dam/zhweb/bilder-dokumente/organisation/finanzdirektion/personalamt/personal--und-lohnstatistik/personal_und_lohnstatistik_2024.pdf)，[口径记录](new_source_scope.json)说明全年教学工作量不是秋季时点教师上界，未准入。原始PDF／HTML及获取哈希保存在研究仓库`research/2026-a/data/task4_v175_zurich_payroll/`；生成器与审计器在`research/2026-a/scripts/task4_v175_mean_rank_comparisons.py`和`audit_task4_v175.py`。此处仅选定支持副本，不包含完整研究树。

科学V154、论文V173保持；Zurich为固定权重保守推荐，16可能／0必要冠军。队友正文、原生页眉空页脚、模板及默认编译设置保持，无新PDF或在线编译声明。研究公开push仍待既有选择，长期goal active。
