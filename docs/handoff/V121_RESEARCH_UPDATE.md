# V121研究交接｜2026-11-08 Asia/Singapore

当前主分析为16城V121；V120已在新环境完整恢复后，才开展本轮补数。沿用原用户CSV、权重、锚点和缺失区间规则。当前保守推荐仍为Zurich，两权重下可能冠军仍全部16城，必要冠军为空。

## 当前权威入口

- 注册表：`research/2026-a/design/task4_user_current_model.json`，V121。
- 工厂：`scripts/task4_user_v121_revision.py`的`revised_bounds()`，返回`(frame,lower,upper)`；路径相对`research/2026-a/`。
- 准入：`design/task4_user_v121_admissions.json`；基线仍显式调用V120，禁止改用25城入口。
- 结果：[V121 README](../../research/2026-a/results/task4_user_v121_revision/README.md)、同目录`current_ranks.csv`、`all_ranks.csv`、`utility_bounds.csv`、`mc_city_summary.csv`、`summary.json`。
- 独立审计：同目录`audit.py`及`audit.json`，全部通过。
- 本轮采集诊断：`results/task4_v121_priority/`，输入是V120的26个完全缺失格。**它是采集前诊断，不是V121补数后最新优先级**；下一轮如需优先级须基于V121重新计算。

## 本轮实际变化

五格：Stockholm教育（Kolada2025/26市内高中、全部提供者、教师FTE比率）、Stockholm交通（2025市内两区13地铁站）、Stockholm泳池（当前网页13处开放设施）、Paris交通（244市内地铁站，RATP2021/Apur2022）、Dublin交通（2023规划现有站点图中19个市中心具名电车站）。局部设施只给下界，上界1；固定人口不变。教育主动降精度包络[16.35,16.45]明确为表示约定，不是调查误差界。

固定权重平均得分宽度16.9344056021→16.1830247163，缩小4.4370%；等权19.9382223723→19.0864688811，缩小4.2720%。Stockholm决策名次fixed13→4，equal14→5。5格更新、155格不变；V120原134个非完全缺失格原样保留；现112点、27部分区间、21全缺失。用户CSV哈希仍为`430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c`。

两组权重仍推荐Zurich、仍16可能冠军。Paris/Dublin历史库存联合撤回、Singapore历史学段代理撤回及全部新证据撤回均已保存；全部撤回精确恢复V120。16个情景、32组权重结果及24组MC独立复核。MC仅权重扰动频率，不是实际冠军概率。

## 来源及失败记录

`data/task4_v121_education/`、`task4_v121_transport/`、`task4_v121_pools/`保存原件、提取脚本、URL、日期、口径与哈希；`task4_v121_travel/`只记录未准入路线。Paris教育学生与全部第二级教师含collège不匹配；Dublin原始站点下载403；Paris旧地理数据404；Warsaw通学原件下载超时，删除部分文件后跳过。没有从失败下载或检索摘要计算效用。Stockholm无关年鉴只留本地scratch，不是可复现依赖。

## 环境与远端

本机`uv`安装Python3.11.18，独立`.venv-v120`包含numpy1.26.4、pandas2.3.1、scipy1.13.1，可继续运行V121。该环境未提交。Poppler已可用。V120完整复跑未产生已跟踪差异，独立复算4changed/156unchanged、fixed宽度16.9344056021、Zurich推荐/16possible均通过。

本地旧main与远端重写后的历史分叉，旧分支已保留为`archive/local-main-before-v120-20261108`，新main从e122d68跟踪origin/main；没有force push。GitHub读取及后续推送按用户授权进行。Overleaf只读`ls-remote`返回`fatal: unable to get password from user`，新环境无可用Git认证；没有修改或推送论文。认证问题不阻碍本轮研究。旧Overleaf V119草稿依然不是V121结果。

## 下一轮

先读AGENTS、GUIDELINES及本更新，再恢复V121，重新计算基于V121的采集优先级。保留全部用户已有值、134格旧证据和本轮已准入界；继续优先匹配教育分母、真实高中通学及同城联合缺项。失败快速跳过，不为缩小冠军集合改权重／区间、不编造AHP问卷或未来趋势。普通补数不授权改Overleaf队友正文。正常commit/push已获授权；使用现有Git身份，不提交凭据、venv、缓存或机器专属文件。
