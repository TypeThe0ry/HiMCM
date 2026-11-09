# V173：数据搜集章节缩短34%，保留真实问题与处理规则

当前自有独立审阅稿启用V173。仅重写第4.2节，把逐城库存处理与重复说明收束为五类问题：城市设施单位、库存日期／状态、学校学段与教学单位、率的分母冲突、未观察人群与失败获取。按同一空白分词规则，1482降至976，减少506、约34.14%；原引用键集合完全保留。其他正文及图表源文件不变，26页=24主文参考+2暂定AI，比V172少1主文页，为后续整合恢复1页余量。

## 保留的实质证据

Oslo的186站台→89站点、Vienna拒绝1695含车库对象的范围、Prague扣除低年级的学生／FTE减法、Dublin411.8工资册对376.1分配岗位、Singapore覆盖不足及原效用界等真实案例保留。原人口年份还明确列出Paris2023、Dublin2022、Singapore2024；Dublin十九个既有tram stops明确为2023计划、2024发行的历史地图，而非2026普查。

独立agent对照旧段落复核后，补回Stockholm upper-secondary years1–3、2026泳池访问日期、Prague FTE全称和rounding envelope、London混合对象与2025边界、Milan市域名码匹配，以及Singapore加权人数非完整headcount。Berlin句子的排除对象明确为本研究U-Bahn子集，不把票价区A说成排除其他交通方式。

[semantic_coverage.json](semantic_coverage.json)记录重要事实及范围核对。删去的主要是重复的非实时／非个人可达性声明和部分中间筛选小计，完整原数与提取链仍在冻结研究源包中。保留未知项、成人份额、开放尾部、舍入假设、单位不匹配及全部既有引用，不把篇幅压缩写成新数据或模型改善。

## 当前PDF及版式

26页、49编译引用。数据问题段在5–7页，矩阵Figure1第8页，主16城排名表第10页、分数Figure2第11页；同国Figure3第17页、新闻18–19、参考20–24、AI25–26。正文12pt、原生11pt页眉、Letter／Palatino和空页脚保持；没有靠改字号、边距或图形比例省页。旧图源的矩阵10pt、同国图9.5pt仍按6.5英寸插入。

26页均渲染检查，数据5–7页完整实看；14个页面正文区域与V172逐像素相同，其余发生压缩与重新分页。[visual_review.json](visual_review.json)和[body_pixel_comparison.json](body_pixel_comparison.json)均绑定当前PDF。直接入口与根代理归一化全文一致，零overfull、两个原underfull段落实看可读。

46项交付映射保持原45项状态与14待完成事项，更新实际页码、大小、余量及内容定位；新增数据章节压缩审阅。真实控制号PENDING、完整全队AI史、最终团队整合及正式提交仍未完成，submission_ready=false。V172稿与旧报告冻结，不能把其27页／0余量作为当前稿事实。

## 验证、复现及工作区边界

[verification.json](verification.json)核187科学文件与570个旧Overleaf文件保持，唯一已有稿件文件改变是自有current_review指针。core相对V172的前后两段逐字保持，只替换4.2；wrapper只切版本注释和新core路径。队友main.tex、ref.bib、mcmthesis.cls和项目默认入口没有改动。

[reproduction.json](reproduction.json)核四个builder输出字节复现；Overleaf drafts/build_task4_v173.py读取自有task4_v173_collection.tex生成新core／wrapper／root entry／manifest，研究scripts/task4_v173_review_audit.py验证范围、原件保护、当前PDF和46项清单。在drafts运行tectonic -Z search-path=..；根目录可构建task4_v173_review_entry.tex。

科学及扩展仍16×10 V154，0新准入0评分收窄，不重跑未变化模型或MC；Zurich保守、16可能／0必要冠军。本轮实际改善为数据搜集论证更集中、主文减少1页；私有Overleaf按授权同步，公开研究push继续待既有选择，长期goal active。Git同步不证明在线Main选择、服务器编译或正式提交。
