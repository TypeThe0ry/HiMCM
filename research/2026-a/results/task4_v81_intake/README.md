# V81：核对新数据的学段、地理与问卷版本

本轮新增原始资料，但没有足够证据改变主模型的任何一个区间。复算250格与V79基准一致，25城排名不变；固定权重及连续偏好下可能冠军仍为25城，Singapore仍是最小最大遗憾推荐，连续证书无未决区间。Phoenix第24、Cape Town第5。这是来源审计轮，数学模型仍为V79。

## 本轮实际发现

- [Phoenix](../../data/task4_v81_phoenix/README.md)：仪表板2025年Phoenix Union独立教师总数1330，高中分类1311、多年级25，其他两个分类各1。分类合计1338，不能直接相加。另有学校在州表标为Phoenix、实际校址为San Tan Valley，说明城市字段需要物理校址核对。
- [Barcelona教育](../../data/task4_v81_barcelona/README.md)：2025/26市内Batxillerat学生23149，广义中学教师11219；2024/25为23699和11238。两套教师分类表在区×公私立×性别层面一致，但教师与学生学段覆盖未匹配，不能直接组成高中师生比。
- [Barcelona通学](../../data/task4_v81_travel/README.md)：2025问卷只保留方式题，删除2021的分钟变量。后续采集应获取2021实际时长记录或另一调查；2025绿地五分钟题不能替代通学。
- [Cape Town既有数据](../../data/task4_v63_cape_travel/README.md)：GHS2025原件已取得，182名14—18岁、当前10—12年级学生已经进入模型，无需重复完成旧验证码请求。

本轮改善是避免三种具体的错误补数：把邮寄城市当实际校址、把跨学段教师当高中专任教师、把旧问卷变量移植到新版调查。没有新增可准入格，也没有实测缩小冠军集合，不能把来源核查报告成排名改善。

## 当前公式

收益型效用为 $u=x/(a+x)$，成本型为 $u=a/(a+x)$；通学为 $u_t=\exp(-t/30)$，教学资源为 $u_E=15T/(N+15T)$。Delhi与Mumbai的名义高中资源分配为 $T\in[D-Z,D+M]$，保留共享教师与零高中学生学校的不确定性。

$$S_i(u,w)=100\frac{\sqrt{\sum_jw_ju_{ij}^2}}{\sqrt{\sum_jw_ju_{ij}^2}+\sqrt{\sum_jw_j(1-u_{ij})^2}}.$$

八个主要指标各取 $(1-\alpha)/8$，两个辅助指标各取 $\alpha/2$；默认 $\alpha=0.1$，连续检查 $[0.05,0.20]$。令 $L_i=S_i(\underline u_i,w)$、$U_i=S_i(\overline u_i,w)$，最小化 $R_i=\max(0,\max_{k\ne i}U_k-L_i)$ 给出决策排名。可能冠军满足 $U_i\ge\max_{k\ne i}L_k$；连续偏好集合取该条件在允许权重下的并集。推荐与已识别的实际第一名是不同结论。

## 复现与输出

运行三个来源目录的 `extract.py` / `verify.py`，随后执行：

```sh
python3 research/2026-a/scripts/task4_current_model.py --output research/2026-a/results/task4_v81_intake
```

[排名](ranks.csv)、[250格区间](utility_bounds.csv)、[摘要](summary.json)、[连续推荐证书](recommendation_certificate.csv)保留本轮输出。原始文件哈希、Barcelona两套教师表对账与问卷年份对照均由来源脚本检查。没有修改论文。
