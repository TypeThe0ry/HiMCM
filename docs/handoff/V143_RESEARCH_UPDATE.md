# V143：推荐对年份和来源信息的依赖

新增五组（含现行）×两权重的受控信息撤回诊断：112个提交点值中64标2026、2标2025、46更早；28带非ok标记（MODELLED16、STALE8、SUSPECT3、NATIONAL1）。只将所选点utility扩成[0,1]，原CSV数值、21补数、48个非点边界及主权重／锚点完全不动。标签与截止年是诊断分类，不是错误概率或自动排除政策。

| 撤回点值组 | 格数 | 基准推荐 | 等权推荐 | 基准平均区间宽度 |
| --- | ---: | --- | --- | ---: |
| 无（现行V136） | 0 | Zurich | Zurich | 16.08933 |
| 早于2020 | 13 | Singapore | Zurich | 21.16464 |
| 晚于2025（均2026） | 64 | Zurich | Zurich | 48.43148 |
| 非ok标记 | 28 | Berlin | Paris | 29.13846 |
| 上述并集 | 95 | Singapore | Singapore | 68.80419 |

全部情景16可能／0必要冠军。结果明确推荐依赖接受的源信息，不能声称对所有来源处理均稳健。撤回信息使界变宽，不是城市实际恶化；替代保守推荐也不是确定冠军。现行主数据V136／扩展V137未改，平均宽度本轮收窄0，真实新数据准入0。Dublin／Zurich本轮有界检索未取得新的匹配城市高中教学FTE原表，旧地区统计／岗位分配仍不代填。

## 核验与论文

- scripts/task4_v143_vintage.py生成112点标签表、200个情景×撤回格记录和160城市结果；audit_task4_v143_vintage.py直接用csv读原件、冻结V136 after_conditional边界及math.fsum标量TOPSIS重算320个得分界／160城市情景、最大遗憾及推荐，全部通过。各组重叠显式去重，原48非点保持。首次verification.json保留；重放另写recheck_verification.json。
- 自有稿第5.5节及五行表展示来源依赖，摘要、结论、新闻同步重要条件；摘要同时更新为V142全部16城严格内点证据。稿仍命名drafts/task4_v137_paper.tex/.pdf，文档修订V143。只改四个自有章节及builder/checker/选定资产；队友main/ref/class和项目主文件设置保持。
- PDF152187字节，SHA f1385f15ea5648fa9ada1d24d54ccab94ad25fe7ba0e3b6c9b324510f2d247b9。23页=21主文参考+2暂定AI；新闻16–17、参考18–21、AI22–23；零warning。23页95dpi、六张总览及新表第11页单独实际查看通过；摘要仍单页，新闻仍两页。
- 当前交付审计scripts/audit_task4_v143_documentation.py及results/task4_v143_documentation/核139科学文件、39原资产／章节和74历史稿保护，五行表逐值对照并核新PDF／编译／QA。旧V142回执冻结，不能以旧22页／旧PDF哈希检查新稿。总页数已变，未声称像素保持。
- 指定anti-defensive-writing中英文技能用于本轮，按证据贡献组织，保留改变结论的源政策条件。原CSV SHA仍430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c。

## 持续任务与权限

长期goal active。下一轮应优先核实能改变源依赖的具体原记录或新匹配高中教师／实际通学源；来源表中的ok不是独立认证。保留原表，任何再估测或新准入另做受控对照。当前无connected文档session，只使用已fetch镜像，Overleaf独立稿按既有授权正常推送，sync.json记录结果；GitHub公开发布选择仍待答，只本地研究commit，不擅改可见性或force。实际控制号PENDING、全队AI史、最终稿具体整合授权、正式提交回执仍待真实资料，稿件非最终交付。AI125条局部选集及截止保持，不把本轮消息混进旧capture。
