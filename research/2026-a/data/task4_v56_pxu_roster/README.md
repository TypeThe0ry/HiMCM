# V56：PXU 学校名册对账

**23 与 21 的差异已找到具体学校对应关系。** 官方 2023–24 课程目录列出 24 个学校／项目；V42 的 2024–25 NCES 名册列出 21 个独立实体；2025 fact sheet 的 2024–25 profile 列出 23 个学校／项目。差异来自三个共址项目和一所于 2024 年关闭的学校。

| 项目 | 官方历史地址 | 对应 NCES 校园 | 差异性质 |
|---|---|---|---|
| Advanced Readiness at Chavez High（ARCH） | 3921 W Baseline Rd | Cesar Chavez，040633001882 | 项目与宿主同址，无单独 NCES 行 |
| Camelback Montessori College Preparatory | 4612 N 28th St | Camelback，040633000540 | 同址，2024 官方招生表要求注册至 Camelback High School |
| Maryvale Gifted & Talented Academy | 3415 N 59th Ave | Maryvale，040633000549 | 项目与宿主同址，无单独 NCES 行 |
| Phoenix Educator Preparatory | 3839 W Camelback Rd | 历史地址与 Alhambra，040633000538，同址 | 2023 开办、2024 关闭；现 NCES 自身实体 040633003806 的 MEMBER 为 0，地址为 Central 校园 |

因此，`2023–24 catalog 24 = NCES 21 + 3 个共址项目`；`2024–25 profile 23 = catalog 24 − Educator Preparatory`。名册中支持设施另外编号 25、26，不计入学校。数字学校为单独 NCES 实体 040633003578，继续排除。现网页已将 Cesar Chavez 更名为 Cactus Canyon（2026）；本对账采用队列时期名称。

24 个历史地址均可对应至 V42 已核验位于**当前 Phoenix 市界内**的校园。Laveen 邮政地址的 Cesar Chavez、Betty Fairfax 也在该边界内。这里保留时间区别：用历史校园地址对接当前边界，不声称重建了 2023–24 市界。20 个非虚拟 NCES 实体也不意味着 20 份独立毕业队列。

## 对毕业下界的实际作用

这轮证据解决了“23 所学校为何只有 21 个 NCES 实体”和历史校园位置的问题。主模型的 Phoenix 区间保持原样。学区 All 行为毕业 4813／未毕业 1472；Digital Academy 为毕业 286／未毕业 199。机械相减得到 4527／1273，现仅记录为**有条件的算术结果**。

要把它们作为目标城市实体学校的毕业／未毕业下界，仍须证明：

- 学区与 Digital Academy 队列的唯一学生归属及毕业状态兼容，状态分别相减不会遗漏或重复。
- 所有目标外责任学生均已覆盖，包括历史关闭实体、特殊安置和无实体校园的学区层级责任。招生名册无法单独证明毕业责任全集；未毕业者可能归于最后就读学校，而非毕业年份仍入学学校。
- 三个共址项目的毕业问责归属有正式对应。Montessori 招生表证明其注册宿主；另外两个项目的地址证据仅证明共址。

这几个条件决定计数能否进入模型。不能用 NCES 的 MEMBER=0 推断毕业队列为零，也不能把学区结果直接解释为 Phoenix 居民学生结果。

## 原件和复核

- [官方 2023–24 课程目录](https://core-docs.s3.us-east-1.amazonaws.com/documents/asset/uploaded_file/4844/BFHS/4405654/2023-2024_Course_Catalog.pdf)：`course_catalog2023_24.pdf`，PDF 第 139 页／印刷 C-131，图面注明 2023-07-21 更新。24 项名单和地址为嵌入图片，CSV **人工逐行视觉转录**。
- [官方历史页](https://www.pxu.org/page/history)：`pxu_history.html`，含 Educator Preparatory 2023 开办／2024 关闭，以及 Cyber High 2010 关闭。网页未构成历年问责实体的穷尽清单。
- [官方 Montessori 2024 申请表](https://core-docs.s3.us-east-1.amazonaws.com/documents/asset/uploaded_file/4844/pxu/4398864/Camelback_Montessori_College_Preparatory_Application.pdf)：`montessori_application2024.pdf`，注册至 Camelback High School 的要求。
- V55 fact sheet、学区原始毕业 API JSON、V9 Digital API JSON、V42 NCES 空间对账 CSV 原件复用，不重复下载；路径和 SHA256 均记于 `manifest.json`。

从项目根目录运行：

```sh
python3 research/2026-a/data/task4_v56_pxu_roster/audit.py
pdftoppm -f 139 -singlefile -scale-to 2200 -png research/2026-a/data/task4_v56_pxu_roster/course_catalog2023_24.pdf /tmp/pxu-roster
```

`roster_join.csv` 保留每一项的历史名称、地址、NCES ID、宿主校园、profile 编号、排除标志。`audit.py` 验证原件哈希、24→21→23 数量恒等式、地址匹配、当前边界、Digital 排除、关闭时间和 Montessori 注册文字，并从原始 JSON 的唯一 All 行重算有条件差值。图片名册需要对照渲染页人工复核，脚本不会把人工转录伪装成自动提取。`audit.json` 明记 `main_admitted=false`、`city_bound_changed=false`。
