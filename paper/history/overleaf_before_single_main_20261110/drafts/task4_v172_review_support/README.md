# V172：同国辅助案例显示全部指标差异

当前自有独立审阅稿启用V172。把第7节原来的四城总分区间表替换为一张图：上部保留四个原区间，下部完整显示两对城市、十指标的20个效用差异。7项方向被保留范围识别，13项跨零；两对城市的整体分数都不识别必要赢家。数据、权重、原有正文和主16城结果保持。

Phoenix相对New York的生活费／住房效用较高；Mumbai相对Delhi的空气效用较高，而Delhi在生活费、住房、学校资源代理及宽带效用较高。逐格差值为[a下界−b上界,a上界−b下界]，不是加权得分贡献、置信区间或实际夺冠概率。完整20项同时显示，不只画7项方向明确的结果。独立agent另核全部端点与原固定权重总分；见[source_scope_review.json](source_scope_review.json)。

## 严格区分辅助案例与主分析

图中四城仍为冻结legacy25 V117辅助材料，不进入主16城榜单。学校代理保留2024–25学校所在地、全年龄XI–XII人数及名义教师人数分配，不写成FTE或教学成效；Delhi NCT与Mumbai教育行政标签的原范围保留，未把镜像与官方原件字节一致性称为已证。生活费／住房是2025 Numbeo具名城市众包，空气是2021 WHO监测均值，宽带为2026年9月索引的7–9月测试窗口。图注明确混合年份、边界和人群范围。

V126 case source index只覆盖8项房价／生活费和2项空气观测，不把学校和宽带假称也已由该索引完整映射。正文原有同国比较说明逐字保留；新图注补充相应指标范围。

## 版面与用户格式

27页=25主文及参考+2暂定AI，49个编译引用。新Figure3在第18页，结论在同页图后；新闻19–20、参考21–25、AI26–27。原矩阵Figure1仍第9页，主16城分数Figure2仍第12页。增加FloatBarrier将同国图留在结论之前，不改正文措辞、字号、边距或共享模板。

新图宽6.5英寸、高4.1英寸，PDF实际Tf最小9.5pt；矢量无栅格图像。图、图注及结论已按最终整页实看；27页均渲染检查，24个原页面正文区域与V168逐像素相同，只有目录及第17–18页正文结构变化。页眉保留原生Team # PENDING／Page x of27，页脚空白；真实控制号仍未核实。

当前保留的25页主文预算已用满，余量0页。45项交付清单保持原44项状态和14个待完成事项；新增同国图范围审阅，纠正现有同国核对标记以匹配实际legacy25文字。页码、大小、余量和当前PDF身份绑定V172，不能沿用V168的26页／1页余量。submission_ready仍为false，未声称最终合规或正式提交。

## 验证与同步

[verification.json](verification.json)核187科学文件及551个旧Overleaf文件保持；唯一已有稿件文件修改是自有current_review指针。core相对V168恰为一个表输入换图输入及结尾FloatBarrier，所有原段落、结论、新闻、引用、AI记录、队友main/ref/class保持。

20差值、7明确方向、4原分数及各来源哈希逐项核对。直接稿与根代理归一化全文一致；零overfull、两个原underfull段落实看可读。[reproduction.json](reproduction.json)核五个builder输出逐字节复现；[body_pixel_comparison.json](body_pixel_comparison.json)绑定当前PDF及24个不变正文页；[visual_review.json](visual_review.json)保存实际版面核对。

复现研究scripts/task4_v172_country_figure.py、Overleaf drafts/build_task4_v172.py；在drafts运行tectonic -Z search-path=..，根代理task4_v172_review_entry.tex可在根目录运行tectonic。审核scripts/task4_v172_review_audit.py绑定当前PDF、图、原件、模板和45项清单。

主科学及扩展仍V154，0新准入0评分收窄，Zurich保守、16可能／0必要冠军。本轮改善是让同国任务的已有证据更容易核对；不增加评价模型。未改默认在线Main设置或验证服务器编译；私有Overleaf按授权同步，公开研究push仍待既有选择，长期goal active。
