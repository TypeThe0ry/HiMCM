# 新下载London原始数据，拒绝不成立的教师上界

本轮获得两份DfE官方CSV：London学校Year12及Year13学生106046人，以及同学年secondary教师发布人数估计38178.63636。原件已无损归档并完成筛选、男女加总和两区域核对。

但教师方法说明确认统计经过缺失学校扩张估计，并排除部分由FE转为academy的sixth-form colleges；教师November2024与学生January2025也不是同一快照。尚不能证明发布教师人数是同一学生群体教师数的确定上限。因此本轮新增准入城市指标为0，主模型保持V34，London教育仍[0,1]。

## 防止来源错误造成虚假改善

若错误地把发布教师估计当作高中教师上限，就会得到效用上界15/(15+106046/38178.63636)=0.8437571700，使London得分上界从71.679683降为70.917914，表面缩窄0.761769分。

此结果保存在`inadmissible_naive_cap`情景以供审计，**不是有效证据更新，也不用于当前排名**。当前证据与该试算的London决策名次均17；Singapore仍推荐，可能冠军均25城。没有把试算的缩窄幅度称作模型改善。

这次采集改变下一步行动：需要按学校ID匹配学生与教师覆盖、核实缺失学校及教师估计误差，不能继续依赖相同的secondary标签拼接汇总表。

## 当前模型和检查

$$u_{education}=\frac{15}{15+PTR},\quad u_{travel}=e^{-t/30},\quad S_i=100\frac{\sqrt{\sum_jw_ju_{ij}^2}}{\sqrt{\sum_jw_ju_{ij}^2}+\sqrt{\sum_jw_j(1-u_{ij})^2}}.$$

$$L_i=S(l_i),\quad U_i=S(h_i),\quad R_i=\max(0,\max_{k\ne i}U_k-L_i),\quad\mathcal C=\{i:U_i\ge\max_{k\ne i}L_k\}.$$

八主指标各0.1125、两辅助各0.05，按R_i递增推荐。主模型入口仍为[delhi_bounds()](../../scripts/task4_delhi_school_revision.py)，本轮没有新的准入函数。

程序核验压缩和解压原件哈希；逐项复现V34主情景的25城得分、排名和最大遗憾；试算仅改London教育上界，其余249格不动。当前证据的Phoenix第24、Delhi第14和25个可能冠军保持。

[原始数据与方法审计](../../data/task4_v35_london/README.md) · [排名](ranks.csv) · [摘要](summary.json)。复现：`python3 research/2026-a/scripts/task4_london_admission_audit.py`。

另核查[Lagos](../../data/task4_v35_lagos/README.md)、[Nairobi](../../data/task4_v35_nairobi/README.md)官方高中来源，原件访问失败或表头未核实，均未入模；失败页面未冒充数据。论文未改动。
