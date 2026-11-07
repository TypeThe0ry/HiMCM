# Copenhagen：取得校级原件，保留时点与城市范围条件

取得DST当前高中校级入学原始响应及Rysensteen Gymnasium官方资源报告。尚未建立同一时点、完整城市覆盖的高中教师/学生配对，本轮模型单元变化0。

[资源报告](rysensteen_resources2024_25.pdf)虽题为2024–25，PDF第15页年龄表给出教师97人（46男、51女），第16页图注明确对应2024年第二季度，来源为Isola人员统计；两页已目视核验。PDF第14页109是2024–25全员工FTE，不能当教师人数。DST INST11原始响应中该校2025年10月1日学生1177，不用不同日期的1177/97充作同日师生比。

DST旧INST02止于2014年，当前表应使用INST11（普通高中）和INST12（商科技术高中）。本目录保存两张现行表2025年、机构代码以101开头的全部响应，分别17行/10255人和4行/3952人。这是明确查询集合，不是已经核验的Copenhagen市总数：机构历史编码、迁移、分部及合并仍须逐一映射到现行市界，跨校机构也可能涉及市外校区；零行不解释为学校不存在。课程范围也未包含全部职业教育路径。没有把代码前缀直接用作城市边界。

[官方教师—学生登记说明](https://www.dst.dk/da/presse/Pressemeddelelser/2024/2024-03-15-nyt-banebrydende-register-giver-nye-forskningsmuligheder-paa-uddannelsesomraadet)说明扩展高中数据可供授权研究者通过Danmarks Datavindue访问。本轮未申请权限。LABY48元数据仅提供市镇组和至2021年的平均教育距离，不是Copenhagen高中实际通学时长。

## 复现

`python3 research/2026-a/data/task4_v62_copenhagen_education/audit.py`

脚本验证所有下载哈希、表版本、查询行、Rysensteen人数与原PDF时间说明。原始数据请求保存在`inst11_query.json`、`inst12_query.json`，POST至[官方DST API](https://api.statbank.dk/v1/data)；[清单](manifest.json)记录URL、SHA256和字节数。[提取审计](audit.json)明确不准入条件。未修改模型、论文或既有来源。
