# Singapore：补齐748名Pre-U学生的条件师资分配界

MOE Education Statistics Digest 2025记录2024年Pre-U学生25130人，其中748人在Specialised Independent Schools（SIS）。旧输入仅覆盖其余24382人。本轮保存完整官方PDF和Excel，以Excel单元格提取观测事实，并保留SIS教师学段分配未知量。

| 事实 | 官方Excel位置 | 数值 |
| --- | --- | ---: |
| Pre-U学生总数 | `21!S25` | 25130 |
| SIS Pre-U学生数 | `21!S33` | 748 |
| 分类为Pre-U的Teacher Total | `3!C14` | 1979 |
| SIS的Teacher Total | `3!C12` | 404 |

PDF印刷第3页（文件第20页）Table3的表头和脚注已经目视核验。404列在Secondary学段，另有副校长10、校长4；1979和404均采用Teacher列，排除校长及副校长。表内各学段和学校类型加总吻合，SIS没有其他学段教师行，故404是该表报告的SIS教师总池。Excel表21与PDF印刷第29页的学生数一致。

令H为该报告教师总池中分配给Pre-U的教师等价数量，只约束0≤H≤404；保留原来1979名教师的统计分类作为基准：

$$PTR(H)=\frac{25130}{1979+H},\qquad E(H)=\frac{15(1979+H)}{15(1979+H)+25130}.$$

由此PTR∈[10.54553084,12.69833249]，教育效用E∈[0.54154885,0.58718686]。端点来自完整池界，无需给H指定概率分布或人为最小分配量。

**条件与含义：** Pre-U涵盖JC、CI和Pre-U centres，不代表所有高中阶段课程。脚注允许混合学校教师按实际教学或受训学段分类，因此1979也不能解释为精确的实际Pre-U教学人数；新界只修正SIS学生覆盖与其教师分配，未包含全部分类误差。教师含兼职，H不是实测工时或FTE。报告排除总部、休假、外派及NIE在读教育人员，详见`observation.json`原文脚注。统计师资是教育资源指标，不能直接称为教育质量。

为显示这一条件的重要性，结果中另将Singapore教育项整体撤回[0,1]。新覆盖总体与旧子总体不同，旧点值和新界的比较属于覆盖定义修订，不是同总体信息单调收紧。

`manifest.json`记录官方URL、下载日期、字节数及SHA256；原件保持不变。`extract.py`直接读取XLSX XML，校验标签、加总和哈希，输出`observation.json`。复现：

```sh
python3 research/2026-a/data/task4_v38_singapore/extract.py
python3 research/2026-a/scripts/task4_singapore_coverage_revision.py
```

[比较结果](../../results/task4_v38_singapore/README.md)。
