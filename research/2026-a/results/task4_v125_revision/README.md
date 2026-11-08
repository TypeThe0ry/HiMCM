# V125：以V124统一偏好、未来、方法与完整审阅稿

本轮将全部主分析扩展统一到16城×10指标V124证据。基准仍保守推荐Zurich，教育优先仍推荐Oslo，可能冠军均16城；同一随机流下，部分城市的条件名次与方法相关性确有变化。论文不再混用V121的偏好／方法数字与V124主表。

| 对照 | 冻结V121证据 | 当前V124证据 |
| --- | ---: | ---: |
| fixed中点TOPSIS与VIKOR的Kendall tau-b | 0.483333 | 0.500000 |
| equal方法tau-b | 0.766667 | 0.750000 |
| 独立生活优先相对各自基准的tau-b | 0.916667 | 0.883333 |
| 独立生活优先Madrid决策名次 | 10 | 8 |
| baseline权重MC浓度100的Oslo平均决策名次 | 2.1062 | 2.1071 |
| equal中点完成与区间决策的tau-b | 0.666667 | 0.650000 |

主数据未再变动：112点值、29部分区间、19完全缺失；原始表至V124累计17格补数，fixed平均得分区间18.81077309→16.15002092，收窄14.14483159%（正文14.14%）。V124最近两格对应的增量收窄为0.20394086%，不能将两者相加或互相替代。

## 数学范围与结果

- [偏好分析](../task4_v125_preferences/README.md)复用原3组分析者权重、AHP精确比率矩阵、浓度20/100/500及SeedSequence([20261108,k])。每组10,000draw不补填未知数据。首选不变不意味着排序全部不变：独立生活情景3城改名次；部分推荐频率、平均名次和top3频率也改变。不存在学生问卷或年龄偏好的新调查。
- [未来条件情景](../task4_v125_future/README.md)保留原倍率和seed20261108122，并为Singapore历史学段代理撤回增加相同draw的配对MC臂。保留代理时，fixed Zurich三情景频率100/96.85/97.72%；撤回时100/99.19/97.72%。这些是预设压力分布下的敏感性，不是有日期的预测、真实胜率或连续冲击空间内的证明。
- [方法及独立案例](../task4_v125_method_country/README.md)仍用同一中点输入比较TOPSIS和VIKOR。fixed VIKOR推荐Dublin且接受条件满足；equal最低Q为Oslo但不满足接受条件。主排名仍预先确定为区间TOPSIS最大遗憾，不根据结果更换方法。6份同国／上海／历史年龄支持案例CSV与V122逐字节相同并单独标口径。
- [受控修订](../task4_v125_revision_diagnostic/README.md)在V124的相同160格界上比较中点完成和保留区间的决策。fixed有13城名次不同、tau0.600；equal有15城、tau0.650。合法矩形内端点／严格内部反例仍能使Dublin超过Zurich，支持“保守推荐不等于确定冠军”。这不虚构团队历史初始模型，也不构成额外观测。

## 验证

各迁移脚本都先运行V121控制，精确复现冻结旧输出，保护原CSV、V124主数据和旧脚本／结果。父agent的独立审计使用此前独立audit的norm／odds反解／显式自排除公式，未调用本轮生产评分函数：

- 三profile×三浓度的当前MC全draw重新计算，含平均rank、first及top3并列份额；矩阵／权重／确定决策核对。
- 16个确定未来设置、32个城市×参考阈值、3232扫描点与交点两侧；两证据臂12个未来冲击及16个权重MC设置，每设置10,000draw，全未知界保持。
- 四组V121/V124×fixed/equal中点TOPSIS/VIKOR分数、排名、tau及接受条件独立复算；6份独立历史案例字节保护。
- 两参考下全部诊断完成逐格核区间、112点值保持、严格内部合法性、分数／排名和端点兑现的最大遗憾；CSV使用round-trip解析保持原浮点端点，不以普通解析微差伪造越界或放宽原界。
- 当前注册表、原CSV及V124结果逐字节与提交8565a65对齐。94项迁移源哈希回执核实；偏好控制CSV全部共同列与V122精确对齐。当前160格均未改。

`audit.json`为独立总审计；各子目录保留详细控制和审计。总入口`design/task4_user_v125_extensions.json`不替换V124主数据注册表。

## 复现与论文

```sh
.venv-v120/bin/python research/2026-a/scripts/task4_v125_preferences.py
.venv-v120/bin/python research/2026-a/scripts/task4_v125_future.py
.venv-v120/bin/python research/2026-a/scripts/task4_v125_method_country.py
.venv-v120/bin/python research/2026-a/scripts/task4_v125_revision_diagnostic.py
.venv-v120/bin/python research/2026-a/scripts/audit_task4_v125_extensions.py
```

Overleaf独立新稿`drafts/task4_v125_paper.tex/.pdf`统一摘要、数据实例、基准表／图、修订、偏好／未来／方法数字、结论与新闻；旧完整V123稿、V124补数材料及队友共享正文保留。仍需真实Team Control Number、完整AI记录及具体授权的主稿整合，不能把编译通过称为已可提交。公开GitHub推送仍待用户对可见性的选择，本地commit与已授权Overleaf同步分别记录。
