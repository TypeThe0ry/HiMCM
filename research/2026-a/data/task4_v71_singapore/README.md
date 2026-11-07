# Singapore V71：取得2020年级×年龄实数，通学子群仍未识别

本轮新取得MOE官方[Secondary Enrolment by Level and Age](https://data.gov.sg/datasets/d_cc84fc751ef5106d9e26cfdbf61776c8/view)完整541行API，以及[2021年5月11日国际学生比例答复](https://www.moe.gov.sg/news/parliamentary-replies/20210511-number-of-overseas-singaporean-students-and-international-students-in-singapore)。下载原件、字节数和SHA256见`manifest.json`。没有修改主模型或论文。

## 新证据给出了什么

2020年MF（男女合计）人数如下；只取MF，未将F重复相加。

| 当前年级 | 全年龄人数 |
|---|---:|
| Secondary 1 | 40,154 |
| Secondary 2 | 39,719 |
| Secondary 3 | 39,909 |
| Secondary 4 | 38,809 |
| Secondary 5 | 3,480 |
| 全Secondary | 162,071 |

Secondary 3–5合计82,198人；其中**年初**14–17岁82,000人，年初14–18岁82,165人。年初14–17岁者若仍在同一目标课程就读，到年中年龄处于14–18岁范围；这只处理年龄边界，不证明年中就读、居住和通学状态。

官方答复表示2019和2020年小学、中学及初级学院的国际生比例低于5%。它没有给出14–18岁×年级×国籍交叉人数，也未说明与Census通学参考日的衔接。因此不能把82,000乘95%当作已观测居民高中生人数，更不能把这个乘积塞进Census通学分箱。

## 具体缺口

1. 新表明确年龄按年初计算，未找到其2020 enrolment的精确时点。Census为2020年中居民统计。相同年份不能替代相同日期的成员关系。
2. 表中无公民/永久居民字段。国际生比例答复不能单独证明MOE年级子群与Census居民子群的覆盖对应；在同总体前提核实前，不能进行集合相减。
3. 新表备注覆盖Specialised schools，其N(T)包括ISC及完成ISC后的两年work-study。年级×年龄表没有课程字段，不能把所有Sec3–5直接认定为V68所需普通高中课程。
4. V70已核验Census通学表排除居家学习及海外至少六个月者。新表没有这些排除项对目标年级年龄子群的数量上界。

因此，这批新证据尚不能给出**同一Census通学总体**内目标高中生人数的正下界。`summary.json`保留`admitted_to_model=false`及`revised_travel_interval=[0,1]`。这里的[0,1]表示目标平均效用未识别，不表示实测学生没有通学数据。V70原分箱继续保留。

本轮也复核了V70已归档GHS2025报告的粗学段定义；它没有提供当前Sec3–5与单岁年龄的通学联合分布，不重复归档同一原件。尝试旧MOE Education Statistics Digest 2021路径返回404，未把错误页保存成PDF或作为证据。

## 如何真正缩界

需要同参考日、同居民及通学覆盖的年龄×当前课程人数下界，或直接取得目标人口的通学分箱。国际生、课程差异和未通学排除项如有可靠上界，可用集合计数得到保守人数下界，再由V70子群分配优化求效用界；本轮不把这些缺失上界设为零。

复现：`python3 research/2026-a/data/task4_v71_singapore/extract.py`。脚本校验3个原件哈希、541行完整性、2020 MF年级年龄行及总数，输出`summary.json`。这一步新增了可核验人数，但没有通过更换总体或人为缩区间改变排名。
