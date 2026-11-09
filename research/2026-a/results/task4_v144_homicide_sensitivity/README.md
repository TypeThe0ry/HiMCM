# V144：定位到一个未核实点率的推荐依赖

只撤回Zurich的homicide点utility为[0,1]时，基准推荐变为Singapore、等权为Oslo；只撤回Amsterdam对应点时均仍Zurich。两点一起撤回时仍Singapore／Oslo。该检验由真实原记录的单位／期间核查触发，原用户数值和现行推荐没有改写。

| 信息撤回情景 | 变化格数 | 基准推荐 | 等权推荐 | 基准均宽 |
| --- | ---: | --- | --- | ---: |
| 无（现行V136） | 0 | Zurich | Zurich | 16.089334 |
| Amsterdam凶杀点 | 1 | Zurich | Zurich | 16.720516 |
| Zurich凶杀点 | 1 | Singapore | Oslo | 16.602168 |
| 两点 | 2 | Singapore | Oslo | 17.233350 |

每个单点试验保持其他159格，两点试验保持158格；原48非点边界和21补充均保持。全部8个“情景×权重”仍16可能／0必要冠军。撤回是信息政策压力测试，不是测得城市改变、rate校正、概率误差模型或确定冠军。官方CBS受害人数与PKS行为数没有被塞入率值。

运行scripts/task4_v144_homicide_sensitivity.py，再audit_task4_v144_homicide.py。独立审计从冻结V136 after_conditional边界出发，直接csv读取并用math.fsum标量TOPSIS重算128城市情景、256得分界、遗憾、所有表现／决策／中点排名和冠军标记；同时重抽原PDF三页、核CBS原HTML单年行和XLSX期间／单元格。source_sha256绑定旧科学集合、V143结果、新原件及提取器。原verification保留，复核另写recheck_verification。
