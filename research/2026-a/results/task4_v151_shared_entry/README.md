# V151：根目录审阅入口与共享稿依赖核查

新增Overleaf根目录文件task4_review_entry.tex，导入现有自有V148完整稿并解决根目录下的相对路径解析。原队友main.tex、ref.bib、mcmthesis.cls、旧章节、7个自有章节、原PDF和数据保持。没有切换项目默认主文件；当前在线选择与服务器编译器未核实。

## 本轮确认的入口差异

当前Git镜像中的根main.tex保留赛事选址模板，另输入冻结的25城阶段章节；并不代表当前16城V136分析。原模板还包含彼此不同的控制号文字，均不是已核实注册号，不能据此更新PENDING。移除TeX行注释及comment环境后，扫描19处字面项目依赖，其中17处图片引用缺失。两仓库现有文件及可用本地Git图片路径历史没有同名原件匹配；不声称其他机器或外部档案没有原图，也不将新16城流程图冒充旧模板原图。

| 本地构建检查 | 实际结果 |
| --- | --- |
| 根布局中直接input真实V148源码 | 在task4_v137_generated.tex处失败，无输出页；临时副本中真实源码和生成文件均存在于drafts |
| 根目录import代理 | 解析相同源码及资源，24页，零警告 |
| 代理与同源新直接编译 | 95dpi全部24页像素相同 |
| 代理与存档V148 PDF | 22页像素相同；8／14页有同源直接重编也出现的细微字距变化，逐页归一化文字一致 |

这组检查证明当前本地路径适配及同源新编译等价性，不定位存档与新编译字距变化的更深原因，也不冒充Overleaf服务器实测。全部24页已渲染查看，8／14页单独实看，无裁切／重叠或新警告。存档原PDF SHA仍f4e50119defd735828ca34d4427ff54f9bc8b58750ae9f3a87a3c3dca76eb6a8。新代理PDF、字号与内容属于同一V148审阅稿，仍有真实控制号和完整AI史等未完成项，不是最终提交件。

## 文件与复现

- shared_dependencies.csv记录源文件／行号／目标／存在状态；inventory.json记录字面扫描范围与两仓库可用历史搜索，不是完整TeX解释器或在线主文件检查。
- task4_v151_entry_inventory.py只读扫描。audit_task4_v151_entry.py核源哈希、24页和页头、编译日志、负例、两种逐页对比，保护139科学文件和82稿件文件。结果verification.json及原样stdout保存在本目录。
- 新入口与生成PDF仅在Overleaf；GitHub研究仓库不复制稿件或LaTeX正文。主仍V13616×10／112点33部分15未知，扩展V137，0准入／0主得分收窄；Zurich保守／16可能／0必要保持。
- 以下重放需当前V148源和现有环境。先在/data/scratch/himcm_v151_probe/project创建隔离副本，仅复制drafts/task4_v137_*.tex和task4_v137_assets；根probe只有input到drafts/task4_v137_paper.tex。原项目不作负例改写。对隔离根probe运行Tectonic，记录预期未找到生成文件的失败；再直接编译隔离drafts/task4_v137_paper.tex。最后从真实Overleaf根目录执行`tectonic --keep-logs --keep-intermediates --outdir drafts/task4_v151_entry_review task4_review_entry.tex`，stdout保存在/data/scratch/himcm_v151_entry_compile.txt。
- 准备好上述负例日志和新直接编译PDF后，用研究仓库现有.venv-v120/bin/python运行research/2026-a/scripts/audit_task4_v151_entry.py；实际看完全部新渲染后才加--render-review-confirmed。脚本对本次源版本与已观察差异页作严格断言，不是跨引擎位级复现保证；不同版本需新报告，勿覆盖历史回执或存档原PDF来强求通过。

根目录入口方案依据[Overleaf官方主文件文档](https://docs.overleaf.com/getting-started/recompiling-your-project/the-main-document)。若团队决定在在线界面预览，拟选根task4_review_entry.tex；正式选择／服务器编译仍需具体授权与验证。本轮不改主文件设置，不覆盖队友正文或补造缺图，不进行上传。V149清单继续对应原PDF，本轮对新根构建另作记录。长期goal active。
