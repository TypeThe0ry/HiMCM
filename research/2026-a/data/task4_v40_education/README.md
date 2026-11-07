# Nairobi真实高中阶段学生数据：教师分母仍缺失

已取得KNBS《Statistical Abstract 2025》官方教育原始Excel。Nairobi City的2024年Secondary学生为**129988人（暂定值）**，位于`TAB 15.6!H51`；Junior学生158570人位于另一张表`TAB 15.4b!C51`，未混入Secondary。数据来源栏为Ministry of Education。

该文件Table15.3仅提供全国教师数，不能与Nairobi学生数相除。本轮新增可核验的城市学段学生分子，尚未取得匹配教师人数，因此PTR为空、教育效用仍保留[0,1]，模型排名未因本数据包改变。学生数本身不能推导有实质信息的教师数量界。

## 来源核查

- [KNBS2025官方发布页](https://www.knbs.or.ke/reports/2025-statistical-abstract/)提供本次下载的教育分章Excel。原件63364字节，已检查ZIP签名和工作表标签，哈希见`manifest.json`。
- 同时下载[Nairobi County Assembly发布的CIDP2023–27](https://www.nairobiassembly.go.ke/ncca/wp-content/uploads/2023/04/NAIROBI-CITY-COUNTY-INTEGRATED-DEVELOPMENT-PLAN-FOR-2023-2027.pdf)。其印刷610–612页统计附录列有Primary、Special Needs和Vocational数据，未找到可匹配Secondary教师分母。其他政府环境评估材料将48669学生／2028教师转引为该CIDP数据，但本次实际CIDP文本中未检出这些数值，不能当成2024年观测或与129988配对。
- [Nairobi2024县统计摘要编制公告](https://nairobi.go.ke/nairobi-county-commences-development-of-county-statistical-abstract-2024)只说明编制启动；尚未定位完整发布的2024/2025县级师资表。
- 已阅读V35来源审计。对旧教育部2020原PDF换用系统curl进行一次35秒请求仍连接超时；AfricaCheck镜像网页读取仍403，未保存伪PDF。没有重试HTML挑战DOCX，也没有把索引数字拼成PTR。

## 文件和复现

`knbs2025_education.xlsx`及`nairobi_cidp2023.pdf`为原件；`manifest.json`记录URL、获取日期、字节数及SHA256。`extract.py`校验原件，提取Nairobi分学段学生数及来源脚注；`teacher_table_extract.json`保留全国教师表的单元格结构，以便复核不准入原因。

```sh
python3 research/2026-a/data/task4_v40_education/extract.py
```

检查已经通过。下一项需要的是同年Nairobi City Secondary教师表，包含公私范围、教师类型及是否计入校长；不能使用Junior招聘名额、全国教师总量或全学段教师量直接替代。
