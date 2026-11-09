# V160：当前独立审阅稿与逐稿交付核对

当前独立稿启用V160，主模型和受控扩展保持V154。第6.4节补齐公平性最紧界的权重分母和缺失集合定义：观测权重499950、最大权重681503，未知效用[0,1]且可选成员身份不确定。最紧历史差距0.226686及45分钟达界见证保持，读者可将公式中的符号对应到实际汇总。

## 实际修改

四段修改都在自有第6.4节：补充联合界定义，精简供给／可及性引入、区级聚合解释和精确年龄测量要求。Shanghai案例宏、历史年龄组边际界、共享成员联合界及两种顺序见证保持。用matched resident utilities和separately elicited weights继续区分年龄的可达性与偏好机制；分析者偏好仍无年龄标签。正文前后其他章节字节保持，图表、参考文献、新闻与AI选集均复用冻结V154。

V159作为历史候选保留；V154独立稿冻结。新增research/2026-a/design/task4_user_current_review.json，与Overleaf drafts/task4_current_review.json逐字同内容，分别指明主科学V154、当前自有稿V160、PDF哈希和根入口。AGENTS仅更新自有审阅稿指针，不改权限条款。队友main.tex／ref.bib／class和默认项目设置保持。

## 核验结果

PDF24页、163810字节，SHA b09ebe38d0e9a70b39a9e11125ab5e5791b05f78f86b20211ea8d3bc3a6e682c。主文参考22页，新闻16—17页、参考18—22页、暂定AI记录23—24页；47编译引用。直接构建及根代理task4_v160_review_entry.tex均成功、零警告、归一化文本相同；未核服务器编译。24页长边1050像素渲染实看，第14页全图检查。相对V159，23页像素／文本完全相同，第14页变化；187科学快照与450个旧稿文件保持，另一个旧文件AGENTS的自有稿指针按精确diff核验。

交付映射共41项：原V156的40项全部逐标记重查、状态保留，另增联合界定义核对1项。8技术通过、18范围审阅、1技术限定、4部分、5未核、3待团队、1未就绪、1未执行。14项待完成状态完整保留。四份官方要求原响应复用V156存档并重新核哈希，本轮没有声称重新联网取件或规则变更。

实际新PDF字体清单列182个8pt数学脚标片段，普通文字经Poppler整数取整至少12pt；不把该清单当作全部字形字号认证或官方例外。真实控制号仍PENDING、完整全队AI记录尚未协调、最终队友稿整合／注册／上传／收件未验证，submission_ready=false。实际重试root main仍因framework.png缺失失败，日志保留。

## 复现与后续

Overleaf drafts/build_task4_v160.py生成三个自有tex入口与manifest，以Tectonic编译；研究scripts/task4_v160_review_audit.py核验来源、段落范围、187科学文件、保护稿件、24页／47引用、根入口和交付标记。requirements.csv、font_inventory.csv、math_script_spans.csv、protected_files.json、verification.json保留逐项证据；原V156清单仍对应旧PDF，当前使用本轮映射。

0主数据准入、0主评分区间变化：Zurich保守推荐、16可能／0必要冠军。Istanbul结果保持2012条件经验集合与官方门户投影范围，不迁移为当前城市公平性水平。后续优先新的同口径师资数据或会改变论文结论的证据核查；私有Overleaf正常同步，研究公开push继续待既有用户选择。长期goal active。
