# V122：在V121的16城证据上完成偏好、未来与独立案例扩展

本轮没有新增或替换主样本观测。证据入口仍为16城、10指标的V121，基准保守推荐Zurich、可能冠军仍16城。V122是以同一输入完成的扩展分析，不是新的数据版本。用户CSV、权重基准、效用锚点、160格区间、主排名和主注册表与提交`deae2f3`逐字节一致。

## 各任务交付

| 用户任务 | 本轮成果及入口 |
|---|---|
| 数据搜集章节 | Overleaf独立章节4：原附件与官方补充的来源区别；2025名义基线和真实混合年份；Oslo平台去重、Zurich市域/区域区分、Stockholm关闭泳池、教育分母匹配、Singapore404镜像及未覆盖调查质量保留。没有编造纽约2024公园替代2025的实例。 |
| 基线5.1/5.2/5.3 | 同一V121的权重、效用、TOPSIS、排除自身的最大遗憾、16城表与得分区间图。原始附件至V121累计补15格，平均宽度18.81077→16.18302，缩小13.97%；当前112点、27部分、21全缺失。 |
| AHP偏好与扰动 | [preferences](../task4_v122_preferences/README.md)：教育优先推荐Oslo，基准/独立生活优先推荐Zurich；三者仍16可能冠军。三组矩阵仅重构分析者权重，CR=0是代数性质，非学生调查。9组Dirichlet扰动保留原数据界。 |
| 未来6.1 | [future](../task4_v122_future/README.md)：三组统一±10%压力情景两权重下均推荐Zurich；修正Singapore期望效用的幂变换，保留正确矩界。分开未来冲击随机与权重随机；没有造3--5年历史面板或真实未来预测。 |
| 多模型对照 | [method/country](../task4_v122_method_country/README.md)：同中点TOPSIS首Zurich、VIKOR首Dublin，Kendall tau-b=0.483333；等权下VIKOR虽最低Q为Oslo，但单一折衷接受条件不成立。主TOPSIS区间规则不被事后替换。 |
| 同国城市比较 | 16城分别属于16国，主样本无同国配对。仅单列既有历史25城V117的美国Phoenix/New York、印度Mumbai/Delhi；两个总分区间均重叠，没有总体必要优胜者，未混入16城主榜。 |
| 城市内部公平性 | 上海既有16区普通高中师资小案例：汇总效用0.60448141、学生加权分区0.60326691；按效用排序的底部20%学生人数权重均值0.58095358。明确学校所在地、教师人数和区内同质条件，未冒充居民设施可达性。 |
| 14与18成长阶段 | [证据与缺口](../../../../docs/research/task4_v122_equity_age_evidence.md)：Istanbul2012宽年龄组效用界重叠；Singapore2020精确年初年龄人数仅中学在读口径。未拼接成精确14/18居民通学或捏造年龄AHP权重。 |

## 最有决策意义的结果

固定基准、教育优先、独立生活优先浓度100的Zurich推荐频率依次为43.34%、6.83%、58.99%；Oslo为28.00%、45.62%、15.46%；Singapore为28.23%、42.11%、25.12%。教育优先会改变保守推荐，不能从基准首选推论所有偏好均首选Zurich。

同一基准权重分布下Oslo平均决策名次2.1062优于Zurich2.2305，虽然确定权重最小遗憾仍推荐Zurich。这反映平均名次与最小最大遗憾回答不同问题。主榜预先保留后者，频率不解释为真实夺冠概率。

仅让一座城市的PTR、PM2.5和时长同比降低，Oslo与最佳竞争者形成保守推荐平局约需5.6850%，Singapore10.3086%，Stockholm28.8745%。这些是指定联合变化的模型阈值，不是现实因果政策需求，更不是成为确定冠军的阈值。旧V119的Zurich24.55%已不适用。

## 验证与复现

三个模块各有边界、输入及结果核验；[audit.py](audit.py)独立写出范数、排除自身的遗憾、原始量变换及VIKOR组件，不调用被审计脚本的数值函数来证明自身。[audit.json](audit.json)通过：9组偏好MC全部draw、16个未来确定情景/权重/证据臂、3232个阈值网格点及根两侧、6组未来冲击MC、8组权重MC、四组方法对照及独立历史案例。

```sh
python research/2026-a/scripts/task4_v122_preferences.py
python research/2026-a/scripts/task4_v122_future.py
python research/2026-a/scripts/task4_v122_method_country.py
python research/2026-a/results/task4_v122_revision/audit.py
```

核心环境仍为Python3.11、numpy1.26.4、pandas2.3.1、scipy1.13.1。扩展索引为[task4_user_v122_extensions.json](../../design/task4_user_v122_extensions.json)，主数据注册表仍V121；V119/V118历史脚本与结果未覆盖。

## 论文交付及边界

已在独立[Overleaf项目](https://www.overleaf.com/project/6aeec16f3ea7a24e3d91e894)新增`drafts/task4_v122_sections.tex/.pdf`、数值生成脚本、四表、两幅矢量图及其选定源数据。论文、LaTeX和论文配图均只放Overleaf仓库，没有同步整棵研究树。源文件中原团队内容和`main.tex`未改动。

Overleaf Git读取认证成功。共享主稿仍包含旧Super Bowl内容及四指标AHP示例，其原有`framework.png`缺失使主稿编译在该图片处失败；这项既有问题没有被伪装为新章节编译成功。本轮新增章节独立编译与逐页渲染检验另行完成；它是供整合的章节贡献，不是完整比赛提交稿。主稿其他成员内容继续保留。
