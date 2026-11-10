# 苏黎世高教密度：机构范围追查

提交的 23 所与人口 440,935（表中标注 2025、city proper）可以算出每百万人 52.161883，四舍五入为 52.2；指标表标注 2026。算术吻合不证明 23 所的提取来源、认证条件或人口来源。先前的 ROR v2.14 教育标签与 Zurich GeoNames 标签筛选也得到 23，但包含中学、教育行政机关等，不能认证高等教育机构总数或市界覆盖；参见 `../current_all16_ror_rosters/README.md`。

此次新增四个来源原件，检索旧路线登记和数据说明未见这些 URL；这不是对全仓历史的穷尽检索。州教育局的 [高校入学分析](https://www.zh.ch/de/bildung/bildungssystem/zahlen-fakten/studieneintritte-an-hochschulen.html) 按其州级分析范围列出七所：ETH、UZH、ZHAW、ZHdK、PHZH、HfH、HWZ。该选定范围不是市界机构总数，也不是全部在州内提供课程的高校。州职业教育咨询的 [课程概览](https://bizinfo.zh.ch/artikel/fachhochschulangebot-im-kanton-zuerich/) 另列 Kalaidos 和 FFHS，并称 SBS 位于 Kloten；明确声明概览不保证完整，且机构、分校、地点的计数单位不同。它公布于 2026-07-21，更新于 2026-09-15。其“Zürich”地点文字未被用于确认市界地址。

[瑞士认证委员会决定表](https://akkreditierungsrat.ch/entscheide/)记录上述七所及 Kalaidos 的机构认证决定及有效期，八条有效期均覆盖 2026-11-10；认证状态不证明每个教学地点都在市界内。委员会表页面载明 2026-10-27 更新。[swissuniversities 名单](https://www.swissuniversities.ch/en/topics/studying/accredited-swiss-higher-education-institutions)说明其名单仅供信息参考，正式认证决定由认证委员会负责。原件与精确 URL、访问 UTC、状态和 SHA-256 在本目录 `retrievals.json`。

结果：取得新的范围与认证证据，但没有可直接替换主模型的市界、同一机构单位、同一时点的完整名单或有效上下界；新增主模型观测 0，52.2 的原始来源链未确认。要形成可准入的独立重建，需要预先指定机构或校区、认证类别及时间、分校与重复计数规则，获取带实际地址的完整名单并与明确市界匹配，再配对同边界人口；还须对其余城市采用可比较规则。该工作不应被描述为原 52.2 的来源认证。

复核：从仓库根目录运行 `python research/2026-a/data/current_zurich_he_scope_followup/verify.py`（需 BeautifulSoup4）。脚本核对原件哈希、七所名称出现、八条机构认证起止日和输入表算术，输出 `../../results/current_zurich_he_scope_followup/verification.json`，包括源文件直接 SHA 映射。机构认证核验日为 2026-11-10 UTC，不能推断其在 2026 全年有效。以上核验不验证各市界地址、原始提取或名单完整性。源代码和结果只写入本次两个新目录；无论文、主模型或旧数据修改。
