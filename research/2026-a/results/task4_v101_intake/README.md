# V101：当前输入下的补数条件与新的下载线索

真实主模型仍V96。逐格重算后，250个区间、完整排名及可能冠军保持：Singapore第1、Tokyo第2、Warsaw第8、Phoenix第16；固定与连续偏好下可能冠军均25城。本轮新增准入观测为0，没有缩小原缺失区间。

## 补数分析实际更新

[连续偏好补数分析](../task4_v101_current_acquisition/README.md)由V91输入更新至V96，独立核对550个组合、420个连续证书叶及25城最少项数。全部组合身份、判定及最少项数保持。Phoenix仍有6个连续认证的二项组合，包括教育＋通学；前提是这些指标取到现有上端这一最有利精确结果，不能承诺实际补数后推荐Phoenix。

Warsaw22个组合在共同权重点的裕量改变：不选择教育的16个组合受益于实测修订后的较高下界；选择教育的6个组合受新的略低上界约束。信息既减少悲观空间，也减少不受证据支持的乐观空间，所有判定仍未越界。

通用运行器新增历史结果保护及旧结果版本标签校验，两项回归测试证明错误调用会在搜索、写入前拒绝。GitHub首页原“Phoenix两项补数为何不足”仍指向V27，已改为当前分析入口，历史报告保留原位。

## 数据获取结果与待办

Phoenix的CRDC2023/24公开镜像检索中，大学目录仅有调查表；GitHub `jknowles/crdc-arrests` 固定提交 `f40c455820f29ad0895605c786719172b109ac2b` 提供身份对应与入学／逮捕处理，未提供工作人员表。已实际下载的Hugging Face `civilytics/crdc-school-arrest-rates` 文件虽名为 `full_crdc_data_y2324.parquet`，字段仍是入学、逮捕及转介记录，没有教师FTE。未把不相关的15.5MB镜像加入仓库，也未凭只列变更ID的表推断其余学校身份不变。

Barcelona发现新的[Idescat公共微观数据入口](https://www.idescat.cat/dades/micro/)，EUT2024原ZIP链接为 `https://www.idescat.cat/dades/micro/eut2024.zip`。[官方方法](https://www.idescat.cat/pub/?id=eut&m=m)描述10岁以上人口活动日记及Barcelona市调查范围；公开文件是否保留城市标识、当前高中阶段及可恢复单向通学的信息仍待核实。直接连接与普通Chrome均超时，浏览器检查停在about:blank，没有启动下载或留下待运行的下载任务。没有据此断言公开ZIP已下架，也没有用日记方法说明冒充实际观测。

接下来应取得真正的CRDC工作人员文件，或EUT2024 ZIP及字典，逐项验证参考期、学校／居民地域、当前学段和实际旅时。既有高中通学区间和Phoenix缺失师资保持。

## 当前数学公式

通学$u_t=e^{-t/30}$，师资$u_E=15T/(N+15T)$；八项主指标权重$(1-\alpha)/8$，两项辅助指标$\alpha/2$。默认α=.10，连续范围[.05,.20]。

$$S_i=100\frac{\sqrt{\sum_jw_ju_{ij}^2}}{\sqrt{\sum_jw_ju_{ij}^2}+\sqrt{\sum_jw_j(1-u_{ij})^2}},\quad L_i=S_i(l_i),\quad U_i=S_i(h_i),$$
$$R_i=\max(0,\max_{k\ne i}U_k-L_i),\quad i^*\in\arg\min_iR_i,\quad\mathcal C(\alpha)=\{i:U_i\ge\max_{k\ne i}L_k\}.$$

补数假设仅令目标城市待测集合B中的$l'_{ij}=h_{ij}$，其他格保持；检查$g_i(B,\alpha)=\min_{k\ne i}R_k-R_i$在整个偏好范围严格为正。该假设用于计算模型内最有利补数条件，不写入真实输入。论文未修改。

[真实排名](ranks.csv) · [250格](utility_bounds.csv) · [复算摘要](summary.json)。
