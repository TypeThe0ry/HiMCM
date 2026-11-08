# V128：V127证据下的完整扩展与独立审计

偏好、未来、方法及受控修订已全部迁移到主16城V127，原权重、锚点、区间和随机流保持。当前基准保守推荐Zurich，教育优先Oslo；三个偏好均保留16可能冠军，无必要冠军。旧V125(V124输入)保持冻结，没有只改版本号或把旧值冒充新结果。

## 实际变化（V125→V128）

| 对比量 | 原V124证据 | 新V127证据 |
|---|---:|---:|
| 教育优先与基准排序tau | .700000 | .716667 |
| 教育优先k100 Prague条件推荐频率 | 5.34% | 8.71% |
| 基准k100 Zurich推荐频率 | 43.34% | 43.33% |
| 基准k100 Oslo平均名次 | 2.1071 | 2.1092 |
| equal中点TOPSIS/VIKOR tau | .750000 | .666667 |
| fixed中点/区间修订tau | .600000 | .583333 |
| fixed Prague联合成本缩减情景切换阈值 | 31.849118% | 28.473803% |

固定方法tau同为.500000，但4个VIKOR名次变化；equal有6个。fixed主决策Vienna12→11、Warsaw11→12，等权主序不变。未来两臂shock MC推荐频率逐项不变，单独权重MC42行变化（最大0.19个百分点）。以上均为指定模型/分布下的受控比较，不是实证学生偏好、年度预测或真实胜率。

## 可核入口

- [偏好](../task4_v128_preferences/README.md)：三profile、分析者AHP一致比率、18组独立逐draw检查及配对48rank/144MC行。
- [未来](../task4_v128_future/README.md)：V121/V122与V124/V125两套精确控制、六表完整键对比、正确旅行矩界及两SG代理臂。
- [方法/历史案例](../task4_v128_method_country/README.md)：同中点、同权重及VIKOR接受条件；六历史CSV原字节和数值不变。
- [修订诊断](../task4_v128_revision_diagnostic/README.md)：同160矩阵的中点与矩形区间，112point/48uncertain、合法端点和严格内部反例、16possible/0necessary。
- [总审计](audit.json)：使用另行核验的范数、原始量/odds转换与自排除竞品公式，独立复算9组偏好MC、16确定性情景、3232扫描点/32阈值、12未来冲击组、16权重组、4方法组、两个权重的completion与历史撤回。

当前[V127固定快照](../../design/task4_user_v127_snapshot.json)的9项哈希全程守恒，源CSV原字节未改；旧V124原件/结果另与Git8565a65逐字节核对。总审计绑定55份当前扩展CSV/JSON，均与最终文件一致。所有MonteCarlo每设置10000次，数据未知/部分格没有随机填值。

```bash
.venv-v120/bin/python research/2026-a/scripts/audit_task4_v128_extensions.py
```

当前论文为Overleaf `drafts/task4_v128_paper.tex/.pdf`：V127主证据、V128扩展统一摘要、表图、结论与新闻。控制号、完整团队AI史和队友稿整合授权仍待真实资料；不把审计通过等同最终提交完成，长期goal active。
