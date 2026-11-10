# V122独立章节：基于16城V121证据

`task4_v122_sections.tex/.pdf`覆盖数据搜集第4节、基线第5节、未来/偏好/扰动/内部差异第6节和同国独立案例第7节。它是可供队伍整合的独立章节，不是完整比赛提交稿。原`main.tex`、`ref.bib`、队友正文及旧V119稿没有修改。

基准仍为M=16、N=10的V121；8项主指标各0.1125，交通和泳池各0.05，保留缺失区间和最小最大遗憾规则。教育优先情景改推荐Oslo，基准/独立生活优先仍推荐Zurich；均未识别确定冠军。未来是无年份的条件压力模拟，不是3--5年真实趋势或未来概率预测。14／18岁、居民公平性与学校所在地/宽年龄组之间的范围差异在正文中明示。

## 构建

从研究仓库根运行，`--research-root`显式指向其`research/2026-a`目录；不要依赖旧机器路径：

```sh
python ../HiMCM-Overleaf/drafts/build_task4_v122.py --research-root research/2026-a
cd ../HiMCM-Overleaf/drafts
tectonic --keep-logs task4_v122_sections.tex
```

图表生成需要numpy/pandas及matplotlib3.9.2；模型核心锁定仍为numpy1.26.4、pandas2.3.1、scipy1.13.1。此机使用Python3.11.18和Tectonic0.17.0。

`task4_v122_generated.tex`数值段落及`task4_v122_tables/`四表来自研究CSV/JSON；修改科研数字时应改对应分析、复核并重新生成，不手改已排版数字。`task4_v122_assets/`包含两幅PDF/SVG、预览PNG及两份选定源CSV，manifest保存研究输入哈希。字体最小9pt，按正文全宽插入后不缩至该下限以下。没有复制完整研究树、模型原始数据或个人记录。

## 验证与整合边界

研究综合独立审计位于研究仓库`results/task4_v122_revision/audit.py/.json`，通过全部既定检查。新增稿编译后逐页渲染检查，确认引文/公式/表格/图中文字可读；共享主稿另按仓库指令尝试编译，因原有`framework.png`缺失而失败。主稿还含旧Super Bowl正文、旧摘要与四指标AHP示例；这些不是本轮新增章节，未代替队友修写。

整合时需要具体确定替换的章节和来源归属，并统一摘要、假设、符号、新闻稿与AI使用报告。不得把旧V119的V118排名/阈值当作当前结果，也不得把本稿独立案例混入16城总榜。论文全稿的25页限制需整合后重新检查。
