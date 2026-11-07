# Singapore：修正 Pre-U 与 ISCED 3 的学段错配

官方 UIS 新加坡映射把 Secondary 3–4 Express 与 Secondary 3–5 Normal 编为 ISCED-P 343；Junior Colleges 编为 444。因此，旧版本用 Pre-U 学生与教师解释 `upper_secondary_ptr` 的学段不匹配。这里修订教育资源的统计对象，不把学生教师比称为教育质量。

新原件为 [UIS 官方 XLSX](https://download.uis.unesco.org/ISCED%20mapping/ISCED_2011_Mapping_Singapore.xlsx)，从 [UIS 映射目录](https://www.uis.unesco.org/en/methods-and-tools/isced/mapping-and-diagrams) 的 Singapore / 2011 链接发现，首表 A3 标注参考学年 **2023**。本地原件、字节数、SHA256 与下载记录见 [manifest.json](manifest.json)。目录经网页工具读取成功，直接 HTTP 请求目录失败；原始 XLSX 下载成功，不把目录工具转录冒充原始网页文件。学生与教师使用已归档的 [MOE ESD 2025 原件](../task4_v38_singapore/manifest.json)，统计年为 **2024**。

| 观测 | 原表位置 | 数值 |
| --- | --- | ---: |
| Secondary 3、4、5 学生 | ESD `4!C14:C16`；复核 `6!L16,L24,L32` | 39977、39611、1981 |
| 上述年级 N(T) 学生 | `6!L22,L30` | 9721 |
| Specialised 学校全部 Secondary 学生池 | `21!S23` | 2838 |
| 分类为 Secondary 的 Teacher 人数 | `3!C8` | 12353 |
| 所有报告学段 Teacher 总池 | `3!C4 = C5+C8+C14` | 29605 |

MOE 印刷第 vii 页把普通 N(T) 说明为通往 GCE N(T) 的四年课程，与 UIS 的 Normal / GCE N 或 O 级课程相符。但是表 6 脚注 1 明确 N(T) 还包括 Specialised 学校的 ISC 课程及完成 ISC 后的两年 work-study；不能将这部分都直接判为 ISCED 343。设混入上述目标年级的未核实课程学生为 $q$，整个 Specialised Secondary 学生池给出 $0\le q\le2838$，因而条件学生界为

$$N=81569-q\in[78731,81569].$$

该池包括全部 Secondary 年级，故只是混入人数的上界，不是已识别的目标年级人数；不直接扣除 2838 作为一个点估计。另保留把全部 N(T) 都视为未识别的更宽分母界 $[71848,81569]$，用于检验上述课程匹配判断的影响。

教师表未按 Secondary 1–2 与 3–5 分配，且表 3 脚注允许混合学校按所教学段或受训学段分类。因此只用分类为 Secondary 的 12353 人无法包住跨分类实际授课。主条件界改用全部报告学段的 **Teacher** 总池 29605，排除校长、副校长和非教师职员。令 $T$ 为该总池分配给目标课程的教师等价人数，只约束 $T\in[0,29605]$。零下界表示没有数量下界证据，不表示实际没有教师。模型沿用资源转换：

$$u_E=\frac{15T}{N+15T}\in[0,0.849406854550].$$

更宽 N(T) 判断和 Secondary 分类池分别作为敏感性，数值由 observation.json 给出。Secondary 分类池 $T\in[0,12353]$ 对应 $u_E\in[0,0.701805882754]$，该结果不能当作实际目标学段全部教师的界。分母减少使效用增大，教师增加使效用增大；上端点使用最小学生数和整个教师池。将所有教师分给目标课程只是保守外包极值，不是实际分配，也未声称极值可实现。

**适用条件。** 这是 MOE 表内五类学校、普通 Secondary 课程与所有报告学段 Teacher 总池的条件资源界。表 3 脚注允许混合学校按所教学段或受训学段分类，教师还包含兼职；29605 不能称为实际目标学段 FTE。表 4 脚注 2 按学生所在学段分类，表 7 脚注把 IP 第 5–6 年计入 Pre-U，这支持按报告年级匹配 Secondary 3–5；UIS 2023 映射没有单列 IP/SIS 各课程映射，因此仍是年级与课程映射条件，不能声称每一课程已逐一认证。MOE 表的五类学校不构成国际学校和其他私校完整覆盖证据；本计算也没有实施 14–18 岁筛选。若目标是无上述条件的全城高中阶段实际师资，现有来源只支持保留 $[0,1]$，不得把本条件界外推成完整城市界。2024 从 Secondary 1 开始取消分流，对本次 Secondary 3–5 的课程表不构成同届标签替换。

复现：`python3 research/2026-a/data/task4_v68_singapore/extract.py`。程序验证本轮与 V38 原件哈希、映射代码、年级加总、学校池和教师池，输出 [observation.json](observation.json)。原件保持不变，旧 Pre-U 输入留在 V38 供前后比较。
