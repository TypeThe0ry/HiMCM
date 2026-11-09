# V169：现有蒙特卡洛均值的同时数值误差保证

科学与受控扩展V154、当前自有稿V168保持。新增研究证书对三表37设定、每组10000draw、2064基础均值给出同时至少95%保证：频率半宽2.37921个百分点、平均名次半宽0.3568815。Hoeffding有界均值界+union bound允许分数并列credit；只要求每组跨draw的IID设计，不要求城市／情景之间独立，固定PRNG未经验认证。原始论文第16页定理2式2.6实看并存原件来源哈希。

全部2064估计和裁切端点逐项核原CSV；50位Decimal独立核公式，AST核抽样常量，独立agent复核。187科学／538已有Overleaf文件逐字节保持。五个已发表值示例定位当前原输出；100.00%是经验频率，非模拟期望精确到.01pp。Oslo／Zurich均秩的通用界重叠，不推断期望严格先后；最终固定权重minimax规则不变。

详见[研究说明](../../research/2026-a/results/task4_v169_mc_precision/README.md)、[验证](../../research/2026-a/results/task4_v169_mc_precision/verification.json)。只读冻结导出，没有重跑MC或新数据准入、0评分收窄；Zurich保守、16可能／0必要冠军。差值与分位数未作为基础均值加入保证族，现实胜率、未来预测校准、来源误差不在此保证内。

Overleaf仅新增drafts/task4_v169_mc_precision四个选定支持文件；当前注册仍V168，正文及用户页眉页尾、队友main/ref/class不改，不重复编译未变化稿件。公开研究push继续待既有选择；私有稿件仓库按既有授权独立fetch并正常同步，长期goal active。下一轮可优先新同口径教师FTE／通学证据；如需认证很近的模拟期望名次差，先设计限定比较与paired差变量证书，不能凭打印小数或重叠通用界作严格排序。

同步实证：私有Overleaf正常push至`6a69706`，HEAD=origin/main且干净；只新增四个支持文件。选定文件哈希及研究公开push保持状态见`results/task4_v169_mc_precision/sync.json`。未核服务器编译。
