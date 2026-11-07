# V74 Toronto：取得校级师资目录与分校预算，实际高中FTE仍待核实

本轮新取得两份Viamonde官方原件，解决了“是否有分校资料”的检索问题。它们没有补齐实际October教师FTE，因此Toronto主模型教育界仍为[0,1]。

- **Toronto Ouest 2024–25人员目录**：`Personnel enseignant`栏有28个互不重复的人员条目，另列校领导、行政、助教和其他岗位。该目录没有每人FTE、任教学段、统计日或缺勤替补关系，不能直接当28个高中教学FTE。
- **Viamonde 2024–25预算**：PDF第25页／印刷3-3页列出学校级Secondary教学人员配置：Collège français 13.83、Étienne-Brûlé 18.83、Toronto Ouest17.00、Michelle-O'Bonsawin7.83，合计57.49。它们是预算配置，不是已取得的实际October岗位统计；不能替换V38实际财报总量，也不能假设实际分校比例与预算比例相同。
- 同一预算PDF第17页单列Toronto Ouest7–8年级人数，说明学校人员目录与9–12年级统计的人员范围不能仅靠学校名称匹配。28个目录条目与17.00个预算配置的差异不能解释为多聘11人：两者单位、学段和统计时点不匹配。

[manifest.json](manifest.json)保存官方URL、原件字节数与SHA256；原件未修改。已目视检查PDF第25页表头及四校行，确认第三个数值列是`Personnel enseignant`，没有混入方向、助教、图书馆或秘书列。

`python3 research/2026-a/data/task4_v74_toronto/extract.py`核对原件哈希、目录角色边界、条目唯一性、四校7列结构和预算合计，生成[summary.json](summary.json)。提取输出只含汇总，不复制目录中的人名或工作邮箱。

接下来需要同年学校级实际教学FTE与9–12学生匹配、MonAvenir三校的相同资料，以及成人/特殊项目、私立覆盖的处理。V39已给出的条件性公校诊断仍不能升级为全城市观察；本轮没有发现可纠正主模型数值的结构性错误，未改模型或论文。
