# 当前模型统一复算入口（V102）

当前模型V102，最新审查V105。Copenhagen四所已核验高校形成部分下界，上界未知；分数区间宽度缩小5.52%，仍第3。默认排名Singapore第1、Warsaw第8、Phoenix第16；固定及连续偏好下可能冠军均25城。

复算：`python3 scripts/task4_current_model.py`。入口核验250格与5城通学来源。

[本轮数据、对照与公式](../task4_v102_intake/README.md)。连续补数与共享补数已更新为V102输入，并新增集合枚举证明；压力等历史诊断仍分别标注原版本。[V103结果](../task4_v103_intake/README.md)。

[V104精度诊断](../task4_v104_survivor_precision/README.md)：规定残余效用宽度0.01时，理想补数最优候选数为5，实际仍25。

[V105真实学校核查](../task4_v105_intake/README.md)：Phoenix新版报告覆盖改善，关键人数和私校覆盖仍未知，实际排名保持。
