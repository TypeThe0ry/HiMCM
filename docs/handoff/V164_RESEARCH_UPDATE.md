# V164：按用户mcmthesis格式整理自有稿

当前自有独立审阅稿启用V164，调用既有mcmthesis类，按用户附件统一页眉、页脚、摘要及目录版式。正文页左上Team # PENDING，右上Page x of25，页脚为空；摘要页使用模板专用Problem／HiMCM Summary Sheet／Team Control Number栏，无运行页眉页码。共享main.tex、ref.bib、mcmthesis.cls及队友正文均未修改。

## 所有权与格式范围

附件是格式参照，未把其中旧赛事正文、Olympic Game标题、2025日期或旧25城内容复制进自有稿。附件tcn18213与author18214冲突，实际登记号仍未核实，独立稿继续PENDING；不替队友选定号码。格式来源只保存SHA和相关设置，未复制队友全文。design/task4_user_format_reference.json与Overleaf自有format_reference记录原件SHA及共享类SHA；生成器不依赖私有附件路径。

自有新文件使用Letter纸、1英寸边距、Palatino正文、12pt主体和模板原生11pt运行页眉。长URL允许断行；现有图的插入尺寸保持可读，没有缩小字号来压页。摘要删去一条正文已提供的矩阵数量说明，使摘要和关键词同处第一页；精简自有结论并移除一处强制换页，消除短尾页。模型、数据、权重、区间规则及结论含义保持。已有自有V160稿冻结，没有改写旧文件。

## 继续完善的数据搜集章节

第4.2节在自有巴黎案例段后加入两项有原件支撑的计量区别：Dublin2025年11月City Of Dublin ETB分项411.8工资册FTE超过376.1分配额；Finland的FTE采用工资／私立提供者资料估算，未经一侧误差包络验证不作Helsinki教师保证上界。与巴黎学段不匹配案例共同说明为何这三城PTR仍未知。新增两条直接参考文献，原47条条目保持；不因此将两条来源当成新入模观测。

## 最终核验

最终PDF25页、148244字节，SHA e3d6fe2793b14c322b4705361d68305dd0c5608184a90894572f939f6ce5f4ab。主文及参考23页，新闻17—18页、参考19—23页、暂定AI记录24—25页，49编译引用。直接构建使用tectonic -Z search-path=..，根代理task4_v164_review_entry.tex可从根目录构建，二者归一化全文相同。自有graphicspath适配两入口，共享类保持原样，未切换在线默认Main document，也未核服务器编译。

25页全部按长边1100像素渲染实看，目录、结论和末页另全图检查；所有正常页眉左右坐标、各页页脚空白均由PDF bbox复核。无overfull框，保留两个轻微underfull段落警告，相关历史年龄段与AI说明已实看可读。42项映射保留原41状态及14个待完成门槛，新增用户模板格式核对。字体清单单列48个11pt模板页眉片段和182个8pt数学脚标，不声明所有字形均12pt或推定官方例外。

187科学文件、474个已有稿件文件字节保持；另两个已有自有任务说明／入口指针文件只作版本导航更新。队友main实际构建仍因原有framework.png缺失失败，日志保存，不补造图片、不改队友正文。实际控制号、完整全队AI记录、最终整合／注册／上传／收件等仍待真实证据，submission_ready=false。

## 交付与复现

build_task4_v164.py生成自有front／core／conclusion／references及paper／根入口。格式代码采用共享类的原生页眉页脚；自有源和参考文献按实际diff审阅。脚本仅为排版和来源说明，不执行新评分或MC。研究scripts/task4_v164_review_audit.py核模板／原件／文件保护、来源链、49引用、页眉页脚、页数、字体和交付映射；requirements.csv、font_inventory.csv、small_spans.csv、protected_files.json及verification.json保存证据。生成器的可移植路径清理后，六个最终生成TeX源逐字复现通过。

主模型／受控扩展仍V154，112点／34部分／14全未知，22累计补充；原CSV字节保持。0主数据准入、0主评分收窄，Zurich保守、16可能／0必要冠军。后续自有稿继续按该用户格式，仍不改队友共享入口／正文。私有Overleaf正常同步，公开研究push仍待既有用户选择；长期goal active。
