# 下一位 AI 的恢复 prompt（2026-11-09，Asia/Singapore）

> **长期goal保持active：** 用户要求持续迭代论文与论文材料，所有新增／修改文字必须使用已安装的中英文anti-defensive-writing技能。先读[长期工作计划](LONGTERM_GOAL.md)和[强制技能规则](../guidelines/ANTI_DEFENSIVE_WRITING.md)，再按当前数据与稿件权限推进；不要把单轮任务完成误记为长期goal完成。

> **V125最新：** 主数据仍16城V124，偏好／未来／方法／受控修订已统一重跑并独立审计；Overleaf当前完整独立审阅稿为`drafts/task4_v125_paper.tex/.pdf`（17页主文+1页暂定AI记录）。先读[V125交接](V125_RESEARCH_UPDATE.md)和[总审计](../../research/2026-a/results/task4_v125_revision/README.md)。新tau为独立生活0.883333、fixed方法0.500000、equal修订0.650000；勿沿用旧值。Zurich仍保守推荐、教育优先Oslo、16可能冠军。控制号／完整AI史／主稿整合／公开推送选择未解决，goal保持active；以下为历史状态。

> **V124最新：** 主注册表已指向16城V124，新增Madrid交通／Tokyo泳池两格真实下界；平均fixed宽度16.18302472→16.15002092（约0.204%），Zurich仍保守推荐、可能冠军仍16城。先读[V124交接](V124_RESEARCH_UPDATE.md)和[主结果](../../research/2026-a/results/task4_user_v124_revision/README.md)。Overleaf V124为三页配套材料；V123完整稿及V122扩展仍固定V121，下一轮须重跑扩展并统一全文。下方V123/V122/V121为历史记录。公开GitHub推送仍待用户选择，不擅改可见性。

> **V123最新：** 主数据仍16城V121；新增[受控修订诊断与完整审阅稿交接](V123_RESEARCH_UPDATE.md)。Overleaf独立稿`drafts/task4_v123_paper.tex/.pdf`为17页主解答+1页暂定AI报告，已编译渲染；控制号/完整AI史未核实，不可直接提交。GitHub现为PUBLIC，赛期公开推送问题已询问用户，答复前暂缓本轮研究公开push、不擅改可见性。下方V122及V120/V121为历史恢复记录。

> **最新进度：数据仍为16城V121，模型扩展与独立论文章节已到V122。先读[V122交接](V122_RESEARCH_UPDATE.md)及[V122结果](../../research/2026-a/results/task4_v122_revision/README.md)。** Overleaf Git已认证；新增稿在`drafts/task4_v122_sections.tex/.pdf`，主稿及队友内容未改。教育优先情景推荐Oslo，基准/独立生活优先推荐Zurich；可能冠军仍16城。V121主数据注册表不改，下方V120/V121文字为恢复基线和历史上下文。

> **当前已推进至16城V121。先读[V121研究交接](V121_RESEARCH_UPDATE.md)及[V121结果](../../research/2026-a/results/task4_user_v121_revision/README.md)。** 本页以下保留V120恢复基线及历史上下文，V120入口／计数不是最新主模型。当前注册表指向`task4_user_v121_revision.revised_bounds()`；五格新证据使fixed平均宽度16.93440560→16.18302472（缩小4.44%），Zurich仍保守推荐、可能冠军仍16城。V121采集诊断输入仍是补数前V120，下一轮须重新按V121计算优先级。Overleaf只读Git认证未就绪，本轮论文无修改。

你接手 HiMCM 城市评价研究。先恢复现状，再继续做有证据支持的补数和模型分析。不要从零重建、重验用户已有值或把旧模型当当前模型。以下是用户已授权的工作范围及交接事实。

## 1. 工作区与必须遵守的约束

研究仓库：https://github.com/TypeThe0ry/HiMCM 。clone 后以仓库根目录为工作目录。先读 AGENTS.md、GUIDELINES.md 及对应的证据/写作规范。

- GitHub保存代码、原始资料、结果、参考文献库与研究说明；本队论文正文、LaTeX、论文配图及论文草稿只放独立Overleaf Git。
- Overleaf项目：https://www.overleaf.com/project/6aeec16f3ea7a24e3d91e894 。Git入口：https://git.overleaf.com/6aeec16f3ea7a24e3d91e894 。新环境需自行使用安全认证；凭据不在交接文件内。
- 旧机器的相邻目录名为HiMCM和HiMCM-Overleaf，但不要硬编码旧机器绝对路径。
- 保留队友正文；仅在用户授权的具体范围内作最小修改。研究补数不自动授权更新论文。写论文前fetch并检查远端，禁止force push。
- 用户偏好多agent并发、失败的数据入口迅速跳过、完成后commit。正常研究提交与push已获授权。旧pre-push日期hook可能阻止立即上传；必要时仅本次使用 `git -c core.hooksPath=/dev/null push origin main`，不要删除hook或声称它已自动同步。
- 用户提供的16城CSV已有值直接采用，不再核验/替换；只补真实缺失项。固定权重、效用锚点和缺失区间规则，不为缩小冠军范围人为改动。
- 不编造AHP学生判断、年度趋势、年龄偏好、因果效果。没有真实问卷；现有AHP矩阵是明确标注的分析者偏好情景。

## 2. 当前权威入口（最重要）

所有以下路径相对仓库根。

- 当前16城注册表：`research/2026-a/design/task4_user_current_model.json`，版本V120。
- 当前模型：`research/2026-a/scripts/task4_user_v120_revision.py`，函数 `revised_bounds()` 返回 `(frame, lower, upper)`。
- 准入清单及源文件哈希：`research/2026-a/design/task4_user_v120_admissions.json`。
- 当前报告：`research/2026-a/results/task4_user_v120_revision/README.md`。
- 当前结果：同目录 `current_ranks.csv`、`all_ranks.csv`、`utility_bounds.csv`、`mc_city_summary.csv`、`summary.json`。
- 补数优先级：`research/2026-a/results/task4_v120_priority/README.md`，及 `priority.csv`、`exclusion_thresholds.csv`、`revision_audit.json`。
- 用户CSV归档：`research/2026-a/data/task4_v117_team_intake/city_indicators.csv`，SHA256 `430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c`。

**陷阱：** `design/task4_current_model.json` / `scripts/task4_current_model.py` 属于原25城研究；不要把它当16城主模型。V119偏好/未来脚本固定研究V118证据，是历史扩展，不会自动随V120更新。要迁移它们须另建版本并做受控对比。

## 3. 当前数学模型

16城、10指标：homicide、PM2.5、生活成本、房价收入比、学校学生/教师资源、高教密度、交通站点密度、通学/通勤时长效用、宽带、泳池密度。原附件部分指标是代理，不冒充全部为高中居民实测。

基准权重：8个主要指标各0.1125，交通站点和泳池各0.05；另报告十项等权0.1。原主观权重不冒充真实AHP问卷。

收益效用 `u=x/(a+x)`；成本效用 `u=a/(a+x)`；原锚点见 `task4_v5_model.SPEC`。通学效用为 `exp(-t/30)`，只有均值时Jensen给 `[exp(-mean/30),1]`，不以均值效用当效用均值。分箱数据用端点积分，无中点填补、无有限尾部上限。全缺失 `[0,1]`；局部设施清单只给下界、上界1。

`Dminus=sqrt(sum(w*u²))`，`Dplus=sqrt(sum(w*(1-u)²))`，`S=100Dminus/(Dminus+Dplus)`。权重只在平方距离中乘一次。

`L=S(lower)`，`U=S(upper)`；`R_i=max(0,max_{k!=i} U_k-L_i)`，推荐最小R；可能冠军满足 `U_i>=max_{k!=i}L_k`。矩形不确定集合，端点为条件数据界，不是抽样置信区间。决策名次不等于已识别真实质量名次。

## 4. 已完成与当前结果

研究最新计算提交 `c0c2f7f`（V120，已push）；此前V119 `4f86d28`、V118 `2412555`。本交接会另加一个docs提交，故以git log为准。

V118补6格：Oslo交通、Zurich泳池、Milan泳池、Singapore公交及泳池、Warsaw教育FTE范围。V120再补4个原先完全未知的格子：

1. Zurich：官方VBZ2025市域446站，不计区域235站。效用下界0.6691999235，上界1；运营方库存不是全市全运营商普查。
2. Helsinki：官方19个市内地铁站，排除Espoo11站；2026快照，固定附件人口不变，效用[0.0518847830,1]。
3. Prague：ČSÚ2024/25学校表，学生80073减lower-gymnasium8748=71325；教师FTE6877.1减737.8，保留舍入[6139.2,6139.4]。学生/教师扣除学段已独立核对。全所有制、全学习形式含成人、学校所在地资源口径；不是精确14–18岁居民教师指标。
4. Singapore：官方2020按Secondary/Post-secondary非高等/Polytechnic三个在读学段通学分箱。Table93全学段居民分母；Table124未覆盖人数效用保留[0,1]；未知阶段比例取凸包。效用[0.2104836424,0.6188393016]。**历史学段代理条件准入，不是2025或精确14–18岁识别界。** `withdraw_historical_stage_proxy`单列撤回该格。

原件/提取脚本位于 `data/task4_v120_education`、`data/task4_v120_transport`、`data/task4_v120_singapore`。

V120仅4格更新、156格不变；原130格非完全缺失全部保留。现112点值、22部分区间、26完全缺失。

固定权重平均得分区间宽度17.942190→16.934406（缩小5.62%）。Zurich3→1，Singapore2→2，Oslo1→3，Prague11→4。**两权重下可能冠军都仍16城，未排除任何城市。** 撤回Singapore历史代理后Zurich仍第1，可能冠军仍16城。

Zurich虽下界低于Oslo仍获最小遗憾推荐，是因为自身最高U不计入自身竞争者，非实现错误。已独立复算。

MC使用两中心×浓度20/100/500，每组10000，seed20261108；不随机填补缺失。fixed中心浓度100：Zurich推荐频率15.06%→43.16%，Oslo69.31%→28.39%，Singapore15.30%→28.23%。这不是实际夺冠概率。

独立审计通过全部评分、self-excluded regret、排名、源哈希、18组MC推荐频率；before与V118精确一致；全部撤销恢复160格。审计详见revision_audit.json。

## 5. 已写论文与历史扩展

Overleaf提交 `6e0aa39` 已push，独立草稿 `drafts/task4_v119_sections.tex` / `.pdf`（5页）含数据搜集、第5基线、第6未来/偏好/扰动及同国案例。未改main.tex或队友正文。此草稿基于V118/V119，尚未更新V120新排名，不能直接当最新结果引用。

V119有三份独立可复现分析：`task4_v119_preferences.py`、`task4_v119_future.py`、`task4_v119_method_country.py`，结果同名目录。
- 分析者教育/独立生活偏好；非真实学生调查或年龄14/18的实测偏好。
- 未来10%条件压力情景，非多年度预测；Zurich24.55%等改善阈值是V118条件模型结果，不能直接移植到V120（V120推荐已改变）。
- TOPSIS/VIKOR同中点对照；16城各属不同国家，不能主样本内做同国比较。美国/印度案例单独用历史25城，不混入16城榜单。

## 6. 下一轮建议

用户持续目标：真实缺失数据优先、失败跳过，保留权重与区间规则，重跑前后对比、说明实际改善、commit。

先用V120重新计算补数优先级；现有V120_priority其实诊断的是补数前V118，名字不是输入版本保证。重点评估同一城市联合缺失项，尤其教育与真实高中通学；单格乐观端点不代表可实现证据。

已有优先级说明：V118下Singapore通学单格理论最多排除3城，但排除首城需效用下界>0.871331；真实新资料远低于它。Amsterdam教育单格要靠低表现排除自身也需极端PTR证据。不要按希望的结论挑数据，或长期卡住一个来源。

已失败线索可快速跳过：Zurich学生统计有但教师只有性别百分比；Helsinki人员总数非教师且非市内全部学校；Dublin教师注册/岗位配置非同市实际教师；Dublin区域交通总数不等于市内。失败记录已存，不要重复下载相同文件。

后续可研究城市内部资源公平性、14/18不同成长阶段，但目前没有足够街区/年龄分组证据；不能仅换权重宣称实现公平性或成长阶段实证修订。模型主线保持精简，不堆Borda/PageRank。

## 7. 新环境复现

建议Python3.11独立venv。现有research依赖锁在requirements-research.txt；仅当前排名链所需核心包为numpy/pandas/scipy。源PDF提取另需Poppler的pdftotext；论文编译可用tectonic。不要为跑模型强装全部论文库工具。

```sh
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install numpy==1.26.4 pandas==2.3.1 scipy==1.13.1
python research/2026-a/scripts/task4_user_v120_revision.py
```

结果应满足：4changed/156unchanged；fixed平均宽度16.9344056021；Zurich首选；16possible。离线模型复现不需要旧Downloads目录或登录网站，源文件都已归档。运行前后检查git diff，随机库版本差异不可误当实证变化。若新环境无Python3.11，先建立兼容环境，不擅自修改科学依赖或模型输出。

不要提交venv、凭据、缓存。下一轮启动时先确认git工作区/远端、阅读当前注册表与报告，报告恢复成功后再分配独立agent任务。

## 8. Goal状态说明

旧线程goal仍是受阻的伊斯坦布尔任务，系统拒绝创建新goal；没有为腾位置虚报完成。此限制不是数据或代码阻碍。新会话如果没有未完成goal，可按用户已明确要求建立16城证据迭代goal；不要继承旧目标为当前数据范围。
