# Cape Town：2025 DBE NSC考试结果的学校ID匹配

按官方2025学校名录的NatEmis与市界字段匹配，Cape Town的299个DBE NSC考试学校报告44071名考生、39056名取得NSC，通过比例为 **88.6206%**。分母是参加该考试的考生，不是入学队列、全体高中在校生或城市居民；这一结果也不等于控制生源后的教育质量。

## 原件与匹配

[DBE 2025 School Performance Report](https://www.education.gov.za/Portals/0/Documents/Reports/2025%20SCHOOL%20PERFORMANCE%20REPORT.pdf?ver=2026-01-12-191404-360)记录2023—2025的学校考生和取得证书人数。本目录保存2025原PDF及SHA256；复用[2025 Q3 Western Cape名录](../task4_v62_cape_school_roster/README.md)原件。

Western Cape部分469个EMIS编号全部与名录一对一匹配，均为2025、OPEN且市字段非空；其中299个属于CITY OF CAPE TOWN，170个明确位于城外。没有按学校名模糊匹配，也没有按“METRO”教育区代替市界。全部469个考试中心编号亦唯一。城市样本中22个名录ExamNo与报告CentreNo不同（含99等占位/不同编码），已列出；地理匹配依据为共同的NatEmis，而非这些考试编号。

原报告说明其覆盖参加该NSC考试的公立、特殊与独立学校。匹配结果含233所公立secondary、15所独立secondary、42所combined、8所special及1所intermediate。只选名录SECONDARY SCHOOL会漏掉其他实际有NSC考生的学校。该名录另有27所secondary没有本报告结果，不能视为零通过或零考生；可能的其他评核体系、未参加考试等情况未逐校核实。

## 指标解释与限制

$$q_{DBE,city}=\frac{\sum_{s\in city}A_s}{\sum_{s\in city}W_s}=\frac{39056}{44071}=0.88620635.$$

A是取得NSC人数，W是实际写考人数。应按考生加权，不取学校通过比例的简单平均（后者为88.6647%）。5015名报告考生未取得NSC不等于退学人数。学校所在地不等于居住地；名录第三季度与年底考试并非同日，学校边界稳定性没有额外推断。市名录以外的非DBE考试、人群或私人评核未证实覆盖。学生个人跨中心重复未独立核验，当前使用官方公布的中心计数。

本证据可用于明确限定的DBE考试考生结果分析。它不能直接替换主模型的高中师资资源格，也不能与Phoenix/NYC入学队列毕业率混用。`main_admitted=false`，未修改现有模型、未知区间或论文。

## 验证与文件

执行 `python3 research/2026-a/data/task4_v63_cape_nsc/extract.py`。脚本校验两原件哈希，提取2025最右侧三个字段，检查所有469行取得人数≤考生数及四舍五入百分比（0.051个百分点容差），核对唯一学校/中心编号及全部地理匹配。原PDF第144页（印刷142）已渲染目视核查标题和换行记录；保留进步生人数等不稳定提取列不参与计算。

[审计结果](audit.json) · [299个城市学校](cape_town_exam_matches.csv) · [469个全省匹配](western_cape_all_exam_matches.csv) · [按类型结果](cape_town_phase_outcomes.csv) · [考试编号差异](exam_number_mismatches.csv) · [未匹配结果的secondary学校](roster_secondary_without_dbe_result.csv) · [原件清单](manifest.json)。
