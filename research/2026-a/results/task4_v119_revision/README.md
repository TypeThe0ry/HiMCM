# V119：把模型扩展落实为可计算的决策变化

主分析仍为16城V118的十指标与原数据区间。核心为区间TOPSIS＋最小最大遗憾；VIKOR只作同中点对照，AHP比率矩阵和蒙特卡洛用于偏好敏感性。没有新增Borda/PageRank，也没有把无面板的情景称为预测。

- [未来与改善阈值](../task4_v119_future/README.md)：三种10%情景均保留Oslo首选和16城可能冠军。其他城市固定时，Zurich三项成本同时下降24.55%与Oslo打平，Singapore需39.54%。这是条件决策边界，不是实证政策效果。
- [偏好与蒙特卡洛](../task4_v119_preferences/README.md)：教育/独立生活两组分析者偏好；没有真实问卷。Vienna教育优先10→5。三个场景共30,000次，Oslo推荐频率69.31%、79.72%、76.94%。缺失区间未被抽样替代或收窄。
- [方法与同国案例](../task4_v119_method_country/README.md)：中点TOPSIS首选Zurich、VIKOR首选Dublin，Kendall 0.5167。16城恰为16国；美国、印度比较单独使用已有25城资料，不混入主榜。

本轮新增分析，没有新增观测数据，因此没有宣称可能冠军范围缩小。上一轮6格真实补数缩小平均区间4.62%，冠军集合仍16城。

## 公式

效用成本 a/(a+x)、收益 x/(a+x)，通学均值只给Jensen下界。D−=sqrt(sum w*u²)，D+=sqrt(sum w*(1-u)²)，S=100D−/(D−+D+)；L=S(lo)，U=S(hi)。R_i=max(0,max_other U−L_i)，推荐argmin R；可能冠军满足U_i≥max_other L。

## 交付与验证

三份脚本分别生成全部数值输出；独立agent复核了AHP特征向量、30,000次MC、VIKOR/Kendall、未来逆变换和阈值两侧符号。基线与V118逐项一致，CSV及admission哈希不变。各子目录保留复现命令与范围说明。

论文草稿仅放相邻Overleaf仓库 `drafts/task4_v119_sections.tex`，包含数据搜集、第5—6节及独立同国案例；现有main.tex及队友内容未修改。未来多年度实测、真实学生偏好、年龄分组和城市内部公平性仍需对应数据。
