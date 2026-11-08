# V89：学习成果比例的条件区间与缺失资料追查

[SIMCE整数重建](../../data/task4_v89_simce_counts/README.md)将一位小数等级比例、列示考生数及质量标记共同纳入计算。62校可唯一还原人数，两校保留未知等级分配：阅读55人、数学80人。条件下至少elemental比例分别56.25%—57.12%、53.09%—54.33%。[官方方法原件](../../data/task4_v89_simce_method/README.md)未确认公开人数字段与百分比分母完全相同、亦未确认舍入细节，故保持条件诊断，未准入主模型或与PISA混用。

[Phoenix教师追查](../../data/task4_v89_phoenix/README.md)取得Career Success FY2024年末教师FTE32.00的官方读者信息，仍为全学段财政口径，不能填同年高中课堂教师缺失。[Santiago通学追查](../../data/task4_v89_santiago_travel/README.md)定位到EOD2012问卷另置数字附件的证据，当前学段题措辞仍未取得；不把已完成教育程度当当前在读阶段。

## 重跑结果

当前主模型仍V79，250格与基准逐一相同，全部名次保持；Singapore第1、Phoenix第24。默认权重及连续α∈[0.05,0.20]下可能冠军仍为25城，连续推荐Singapore，未决区间0。5城真实通学区间保持，新增准入格为0。论文及Overleaf未改动。

## 当前数学公式

资源效用 $u_E=15T/(N+15T)$，通学效用 $u_t=e^{-t/30}$；8项主指标各权重$(1-\alpha)/8$、2项辅助指标各$\alpha/2$，默认α=0.1。

$$S_i=100\frac{\sqrt{\sum_jw_ju_{ij}^2}}{\sqrt{\sum_jw_ju_{ij}^2}+\sqrt{\sum_jw_j(1-u_{ij})^2}},$$
$$L_i=S_i(l_i),\quad U_i=S_i(h_i),\quad R_i=\max(0,\max_{k\ne i}U_k-L_i).$$

最小R决定稳健推荐；$U_i\ge\max_{k\ne i}L_k$保留冠军可能。本轮新增的条件整数区间公式见[数据说明](../../data/task4_v89_simce_counts/README.md)，没有替代上述主评分。

```sh
python3 research/2026-a/scripts/task4_current_model.py --output research/2026-a/results/task4_v89_intake
```

[排名](ranks.csv) · [区间](utility_bounds.csv) · [运行摘要](summary.json)。
