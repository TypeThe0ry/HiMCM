# V122扩展与论文交接｜2026-11-08

主数据仍为V121的16城×10指标，保守推荐Zurich、可能冠军仍16城。V122没有补新主样本数据，而是完成用户要求的数据搜集写作、基线5.1--5.3、未来/偏好/扰动、同国独立案例，以及公平性/成长阶段证据分析。不要把扩展版本当新数据版本，也不要切回旧25城入口。

## 最新入口

- [任务完成矩阵与关键结果](../../research/2026-a/results/task4_v122_revision/README.md)。
- `research/2026-a/design/task4_user_current_model.json`仍V121，区间工厂`task4_user_v121_revision.revised_bounds()`。
- 新扩展索引`design/task4_user_v122_extensions.json`。三个`task4_v122_preferences.py`、`task4_v122_future.py`、`task4_v122_method_country.py`脚本及同名结果目录均显式读V121；方法对照另有标识清晰的V118控制臂、同国案例为历史25城V117。
- [公平性/年龄证据说明](../research/task4_v122_equity_age_evidence.md)。
- `results/task4_v122_revision/audit.py/.json`为独立综合审计，全部通过；未改变主数据及原134格、五格V121补数和所有主榜结果。

## 结论不可写错

基准和独立生活优先仍推荐Zurich，教育优先改为Oslo；三组均16城可能冠军。AHP只是按分析者声明权重比构造，CR=0不证明真实学生偏好。9组MC仅扰动权重、未填缺失；平均名次和确定权重minimax可能推荐不同，不事后换主榜规则。

未来是无日期的条件压力情景，没有真实3--5年同口径面板。统一10%资源/生活压力/均衡改善均仍推荐Zurich，均衡改善交换Oslo与Singapore的2/3名。未来冲击MC seed20261108122；权重MC seed序列[20261108,100]与V121原样对齐。频率不是实际夺冠概率。Singapore的平均效用界不能直接两端幂变换：r<1用[L,U^r]，r>1用[L^r,U]；有原均值的城市单独用Jensen，未知仍未知。

V121固定权重同中点TOPSIS/VIKOR tau-b=0.483333，首位分别Zurich/Dublin；等权VIKOR最低Q的Oslo不满足接受条件。不能写高度一致或以最低Q直接宣布单一折衷推荐。

16城分别属16国，主样本无法做同国配对。美国/印度案例独立使用V117历史25城数据，两对均无总体必要优胜者。上海16区2025师资案例可以比较学生加权分区及底部20%资源效用，但按学校所在地、排除中职、教师人数非FTE、区内同质，不是个体或居民可达性。Istanbul2012年龄组为14--15/16--18，不是当前精确14/18；Singapore2020精确年初18岁165人仅secondary在读者。两者不支持年龄权重或16城年龄榜。

## Overleaf与环境

Git认证已成功，最初fetch远端为6e0aa39。仅新增`drafts/task4_v122_*`及构建脚本，旧`main.tex`、`ref.bib`、其他成员正文与V119草稿不改。新稿为独立章节，不是完整比赛提交稿。共享主稿仍有旧Super Bowl模板与四指标AHP示例，而且缺原有`framework.png`；尝试编译主稿在该图处失败，未修补/替换他人素材。

新增稿覆盖章节4、5、6、7，包含M=16/N=10、真实采集案例、来源、公式、排名与两幅科学图。独立编译用Tectonic0.17.0；构建图表另装requirements-research.txt中已有的matplotlib3.9.2，核心numpy/pandas/scipy版本不变。论文用选定CSV、矢量PDF/SVG和源脚本仅在Overleaf；未把整棵研究资料复制过去。

## 后续优先项

先确认最新Overleaf远端和队友编辑，再按具体授权整合新章节；用户持续要求保护队友正文，不能借“整合”自动重写旧摘要、假设或其他章节。完整比赛稿仍需统一旧模板内容、配齐原图、摘要/新闻稿/参考文献与AI使用报告并做整篇版面检查。真实14/18与居民公平性仍需匹配人口/学校/设施/时间数据；现有框架不当作已完成实证。

普通研究commit/push和本轮独立章节commit/push均已授权。两个仓库各自fetch、审diff、正常push，不force。不要提交venv、缓存、LaTeX日志、凭据或旧机器绝对路径。
