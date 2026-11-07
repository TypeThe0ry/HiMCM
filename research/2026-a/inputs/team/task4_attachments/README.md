# 本轮附件接收记录

用户于2026-11-07补充四份文件，用于正在进行的真实城市模型修订。原始文件逐字节复制，SHA256见provenance.json。

- cities(1).csv：25城候选名单，与既有city_candidates_original.csv完全相同；不是指标实测矩阵。
- 评价指标_王树轩_11071410.md：与既有11指标原稿完全相同；其中来源、样例与主张仍需独立核验。
- 简易评价指标_王树轩_11071427.md：与既有5指标原稿完全相同。
- cities_pilot.numbers：新增10城试点名单；11行（含表头）、9列，含名称、国家、分组、取数锚点与角色描述，没有教育或可达性数值。派生CSV为pilot_sheet0_table0.csv，使用隔离环境的numbers-parser读取。

原件中的strong/weak及城市角色属于团队预设描述，未作为训练标签、筛选目标或验证真值。原25城主比较保留；10城试点另输出学习设施可达性表，不把两种样本悄悄混合。

隔离读取方式：Python环境安装numbers-parser后，Document('cities_pilot.numbers').sheets[0].tables[0].rows(values_only=True)。原Numbers文件未修改。
