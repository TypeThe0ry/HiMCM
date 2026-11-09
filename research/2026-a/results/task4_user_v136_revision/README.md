# V136：London受控单格补数，待成套启用

从已核TfL站级库存纳入59个operator站／hub实体，ONS全分辨率London边界逐点核对。只提高London transport全未知格下界至0.012769306569299622，上界1；159格不变、144个已有信息格保持。原CSV、9122909／2025人口、权重、锚点、矩形区间规则不变。新受控矩阵112点／33部分／15全缺失，累计21原全缺失格补充；当前注册表仍V130，待V137全稿迁移后启用。

fixed平均宽度16.092069666942→16.089333559066（收窄0.017003%），equal18.919371949112→18.914257170686（0.027035%）。全部静态主决策名次不变，London仍14、Zurich保守、16可能／0必要保持。不要把条件库存更新称城市改善或冠军确定。

独立审计通过16静态设置、24组各10000次同流权重MC和完整撤回；before匹配V130，撤回精确恢复全部160格界。历史Singapore代理在before/after两臂独立撤回。before/after推荐频率最大变化0；k100 London平均rank固定13.7863→13.7607、等权13.5768→13.5395。只是声明权重分布下的条件平均名次。

科学快照design/task4_user_v136_snapshot.json固定原审计及所有主输出；已有回执时再跑audit_task4_v136_revision.py另写recheck_audit.json，不覆盖原审计。live注册表仅前后保护、不作为数组来源，允许后续切换版本后重放固定V136结果。重放历史不表示当时结果仍为当前。

复现：依次用.venv-v120/bin/python执行scripts/task4_user_v136_revision.py及scripts/audit_task4_v136_revision.py。源V135包已由准入表固定所有所需字节；不要覆盖旧extract/README/capture来记录新解释。完整API原件lossless gzip已入研究仓库，外置原始JSON缺失时仍可复算；upper1保留其他模式／票区未知，静态库存不等于实时开放或学生可达性。
