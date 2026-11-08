# V127：两格真实公共地铁下界

Vienna99个市内既有地铁站区、Prague57个市内地铁复合体替换两个全未知模型utility；其余158格及141格原有非全缺失信息原样保留。矩阵现在为112point、31partial、17fullmissing。原CSV SHA、人口、固定/等权参照、锚点与区间规则不变；16城主入口已登记V127。

| 权重 | V124平均分数宽度 | V127平均分数宽度 | 相对收窄 |
|---|---:|---:|---:|
| fixed | 16.15002092 | 16.10728557 | 0.264615% |
| equal | 19.02662147 | 18.94657608 | 0.420702% |

固定权重Vienna决策名次12→11、Warsaw11→12；Prague仍第5。等权完整决策顺序不变。Zurich仍为保守推荐，16城仍可能冠军、没有必要冠军；其固定最大遗憾17.3680463550不变。本轮改善是减少未知范围与更新信息下的排序，不是城市随时间改善或已确定冠军。

## 真实源与拒收门槛

- [Vienna99站区](../../data/task4_v127_vienna_transport/README.md)：2026导出DIVA与官方既有站层/市界逐项匹配，110线路出现次数不作110复合体。含车库/未证乘客资格对象的1695大清单明确拒收；2024静态镜像也不冒充2026。
- [Prague57复合体](../../data/task4_v127_prague/README.md)：当前市内PID线路名单、交换站去重及Flora闭站；原2025年报61线路出现→58复合体作交叉核对。2025与2026闭站不是同一排除对象。完整56.6MB年报在/data/datasets/HiMCM/source_archives，Git保留必要提取/页图及原件hash/重取命令。
- [教育新路线](../../data/task4_v127_education/README.md)0准入：Dublin提问未恢复回答，Amsterdam BRIN多campus/全VO口径不匹配；没有区域/机构分母替换城市高中数据。
- [Vienna2001通学](../../data/task4_v127_vienna_travel/README.md)只历史案例：居民所选stage全分母42774，2170未知质量；官方编辑/估补且向2025/26迁移无依据，未填当前travel。原PDF受限不再分发。

新准入均为2026供给子集配原2025人口；其他设施上界仍1，不推断个人可达性、全年连续开放、调查偏好或未来趋势。候选包保持其原提议标记，正式选择与accepted状态在[准入表](../../design/task4_user_v127_admissions.json)。

## 验证与重现

独立[revision_audit.json](revision_audit.json)通过20静态比较与24组同种子10000次权重扰动，复算加权范数、自排除竞品、并列分摊、排名与冠军集合。before精确复现V124，撤回全部新项精确还原160格，70来源文件hash通过。没有随机填补数据。

```bash
.venv-v120/bin/python research/2026-a/scripts/task4_user_v127_revision.py
.venv-v120/bin/python research/2026-a/scripts/audit_task4_v127_revision.py
```

[固定快照](../../design/task4_user_v127_snapshot.json)约束后续V128扩展；旧V124及V125各自冻结不覆盖。当前完整迁稿使用V127证据与V128扩展，独立审阅稿位于Overleaf的drafts/task4_v128_paper.tex/.pdf。旧25城入口仅历史案例，不是此处的主分析。

注册表推进后的复核会另写[post_activation_audit.json](post_activation_audit.json)，保留原启用前revision_audit.json与V127固定快照不变。
