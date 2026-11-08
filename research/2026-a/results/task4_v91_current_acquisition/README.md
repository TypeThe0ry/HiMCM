# V91：新Phoenix空气观测后的连续补数分析

当前输入为V91，历史对照为V90分析使用的V79。Phoenix连续最少有利精确补数项从3降至2；固定权重仍2项。六个可认证二项组合包括教育＋通学，最小认证裕量约0.163259。这里只检查最有利端点能否改变稳健推荐，不预测实际观测或保证唯一冠军。

550个组合包括335个负裕量反例、215个认证组合；426个连续区间证书覆盖α∈[0.05,0.20]。独立long-double复算、25城最小性枚举与输入250格核对通过，未决0。当前真实排名、可能冠军和公式见[主修订](../task4_v91_phoenix_monitor/README.md)。

```sh
python3 research/2026-a/scripts/task4_registered_continuous_acquisition.py --output research/2026-a/results/task4_v91_current_acquisition --prior-results research/2026-a/results/task4_v90_current_acquisition --prior-model V79
```

[最少项数](minimum_bundles.csv) · [与V90分析对照](comparison_prior.csv) · [组合反例/认证](bundle_evaluations.csv) · [区间证书](bundle_certificates.csv) · [摘要](summary.json)。
