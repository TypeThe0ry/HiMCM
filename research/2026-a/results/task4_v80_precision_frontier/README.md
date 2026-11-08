# V80：Phoenix补数阈值在V79输入上复核

128组补数组合已使用当前V79数据重算，阈值与V76完全一致。这里只分析假想的低端测量结果，不将这些情景录入实际城市数据。

对选中指标j，将Phoenix区间假设为[ℓ_j,ℓ_j+ρ(h_j−ℓ_j)]，其他格保持当前值。连续偏好α∈[0.05,0.20]下，若该城市上分数始终低于至少一名对手下分数，则排除其第一可能。

| 选中指标数 | 最佳组合排除阈值ρ（约） |
| --- | ---: |
| 0—4 | 即使ρ=0也不能排除 |
| 5 | 0.06220205459 |
| 6 | 0.25907974666 |
| 7 | 0.38540100894 |

每个临界值保存“仍排除／开始可能”两端，40次二分括区间宽度不超过2^-40。ρ同时约束结果的位置和残余宽度，不能称作纯测量精度或成功概率。上述最少5项仅针对指定低端结果情景，不保证取得任意5项数据就能排除Phoenix。

[全部128组合](bundle_thresholds.csv)、[前沿](frontier.csv)、[同输入粗网格](same_input_coarse_grid.csv)、[摘要](summary.json)。独立复核分类及两端判断，4项相关测试通过。当前实际Phoenix仍第24、可能冠军仍25城；城市输入未因分析改变。

```sh
python3 research/2026-a/scripts/task4_precision_frontier.py --output research/2026-a/results/task4_v80_precision_frontier
```

与[补数能力下界分析](../task4_v80_acquisition_limits/README.md)合看：仅补Phoenix教育与通学，不论其精确结果如何，都仍无法排除任何城市的第一可能。当前核心模型和公式见[V79](../task4_v79_delhi_allocation/README.md)。
