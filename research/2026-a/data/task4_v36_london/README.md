# London学校ID实际匹配：覆盖105274名高中在读者，尚不能给出全城教师上界

本轮取得两份新的官方校级原件并按URN一对一合并：January2025学校学生CSV（23.6MB），November2024学校教师汇总XLSX（8.7MB）。两份均为原始发布字节，来源URL、大小和SHA256见manifest。

London state-funded secondary共514所学校，其中411所报告Year12或Year13学生。8个年级×性别×全/兼职学生字段之和为106046，与V35区域汇总完全相符；没有学生计数缺失。407所有正高中人数学校匹配到数值教师人数，覆盖105274名高中学生；剩余4校772人未匹配到教师记录。

| 未匹配URN | 学校 | Year12+13学生 |
| --- | --- | ---: |
| 150889 | London Nautical, City of London Academy | 181 |
| 135584 | Ark Globe Academy | 156 |
| 134369 | Alec Reed Academy | 223 |
| 137928 | Gumley House RC Convent School, FCJ | 212 |

匹配407校的全学段教师headcount之和32339，均为正整数；不能解释成高中专属教师数。未匹配原因尚未确定，不能自动按同名、旧URN或学校转换记录补齐，也不能将缺失教师当零。school_match.csv保留全部514所目标学校、匹配状态和学生/教师字段，不包含个人学生信息。

## 改善与仍未解决的问题

与上一轮只能比较地区汇总不同，现在已有真实学校名单和精确缺失覆盖，后续可以针对4所学校寻找同快照教师记录。但学校teacher总数仍混合年级，4校教师上界未知，教师与学生快照相隔两个月；不能据此宣称完整London高中PTR被识别。

此目标仅为state-funded secondary中的Year12/13，排除独立学校和FE等其他路线。学校所在地不是学生居住地；年级不是实际年龄14–18。多校任职教师可能在学校间重复，headcount加总不能未经说明当唯一人数。主模型教育未知界应保持[0,1]，`main_admitted=false`。

## 复核

extract.py用标准库解析XLSX（无新依赖），验证原件SHA256和长度、校级URN唯一、当前学生学年、8个年级字段、106046区域一致性及匹配/未匹配学生总和。抑制与未知标记转为未知，不转零。原始教师工作簿第5–7行定义x不可用、c保密、z不适用。

复现：`python3 research/2026-a/data/task4_v36_london/extract.py`。
