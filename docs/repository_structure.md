# 研究与论文工作区结构

用户于2026-11-07确认按用途拆分：GitHub `TypeThe0ry/HiMCM` 保存研究，旁边的 `HiMCM-Overleaf` 对应[权威论文项目](https://www.overleaf.com/project/6aeec16f3ea7a24e3d91e894)。

## GitHub 研究仓库：HiMCM

- `research/2026-a/data/`：原始数据、来源记录和提取脚本。
- `research/2026-a/scripts/`：模型与验证代码。
- `research/2026-a/results/`：历次结果；保存各版证据对照、补数策略和条件模型；最新版本与复现入口以根README为准。
- `research/2026-a/design/`：指标定义、研究设计及实验记录；论文正文草稿在Overleaf。
- `research/2026-a/visuals/`：研究图表、地图、来源和制图代码；论文LaTeX插入文件在Overleaf。
- `library/`：历史获奖论文和索引，属于参考资料，保留在GitHub。
- `docs/`：规范、历史迁移记录与核验。

## 论文工作区：HiMCM-Overleaf

- 根目录 `main.tex`、`ref.bib`、`mcmthesis.cls`：当前论文、参考文献及模板。
- `drafts/task4_paper_core.md`：任务4正文主线。
- `research/2026-a/visuals/`：迁入的LaTeX插图片段、图集源码和选用的论文资产。
- `archive/github_before_split/`：拆分前GitHub版本的论文材料；保留原始内容与路径，供追溯。

两边分别获取和推送各自远端更新；选用研究结果时将需要的论文资产放入Overleaf，不同步整个数据与参考库。在线Overleaf与本地检出状态须区分。

完整研究导航、数据口径及复现命令见根目录[README](../README.md)。本轮路径与哈希见[拆分记录](migration/overleaf_split_2026-11-07.json)。早期[合并记录](reunification.md)与[迁移表](file_moves.csv)保留历史状态，不代表当前布局。
