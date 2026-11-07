# V7 Phoenix：核验公开数据的识别边界

2026-11-07。本轮不重复V6失败的学生问卷PDF/MAG下载地址，不改V6数据或模型。新增可核验材料支持**继续保留Phoenix真实高中生通学[0,1]**，没有新增合格数值。空`observations.csv`明确表示没有新主观测，而不是抓取失败就填0。

## NHTS2022：不能从全国文件筛出Phoenix

已归档官方技术说明PDF及pdftotext派生文本。文档末页“被省略变量”部分明确：由于2022样本缩小，无法支持低于Census division的可靠估计，因此删除HHSTATE和HH_CBSA。不能以新年份全国旅行记录假装Phoenix本地高中样本，也不能基于城市人口份额随机分配记录。

来源：<https://nhts.ornl.gov/media/2022/doc/2022%20NextGen%20NHTS%20Compatibility%20with%20Prior%20Data%20V2.1.pdf>

## NHTS2017：有实际旅行，但都会区不等于行政市

已归档官方完整codebook XLSX和用户手册。直接解析XLSX XML，无需安装新的Excel依赖。`nhts2017_variable_inventory.csv`保留全部文件变量名与标签，`nhts2017_selected_fields.csv`保存相关字段的代码与频数。

- HH_CBSA=38060对应Phoenix–Mesa–Scottsdale **都会区**。codebook显示735个家庭、1465个人，是全年龄样本，不是735/1465个Phoenix高中生。
- 年龄R_AGE、实际行程分钟TRVLCMIN、WHYFROM/WHYTO确实存在，因而调查本身是真实行程来源；但公开代码本没有Phoenix行政市居住身份。
- SCHTYP区分公私学校、在家教育、不在校，并不直接给高中年级。年龄筛选也不能自动等同upper-secondary，18岁尤其可能进入大学。
- 家庭tract/blockgroup变量是人口/密度**分类**，不是可地理连接到Phoenix市界的tract ID。不能用密度猜测市界。
- 用户手册说明加购样本支持相应地方分析；Arizona加样不等于公开文件可任意细分城市高中生，也不豁免抽样误差核算。

因此本轮没有下载80MB全国微观数据后制造一个不具备可识别地理范围的“Phoenix”均值；先以元数据排除不可成立的筛选。若获得受控细地理标识和对应权重，应重新审计，而不是认为NHTS永远无法提供地方信息。

来源：<https://nhts.ornl.gov/media/2017/doc/codebook_v1.2.xlsx>；<https://nhts.ornl.gov/media/2017/doc/NHTS2017_UsersGuide_04232019_1.pdf>。

## TRP公开议程：确认真实高中参与，但不是测量结果

新归档2026-07-14官方审批议程，明确列Phoenix Union High School District、Brophy College Preparatory、Phoenix Country Day School及Saint Mary's Catholic High School等。它缩小了下一步可询问的数据拥有者范围，但所检查议程没有学生单程分钟分布、回应人数、权重或居住城市筛选。

学校/学区的plan审批名录不能当成学生调查结果；高校和员工也不能混入。另查Phoenix College官方交通页面，其调查对象为学院学生和员工，故不作为高中生证据。该页直接HTTP403已记录，网页索引可读不冒称原始页面成功归档。

本轮没有发送邮件、联系机构或提交信息请求。

## 下轮可接入的数据要求

`evidence_gaps.csv`逐来源记录已有内容、拒绝原因和精确缺口。若用户补数据，至少需要：调查年份、学校/年级或年龄定义、Phoenix居住范围、家庭到学校单程分钟（或分箱及各箱人数）、有效回复分母、覆盖学校/学生总数与未回复人数。若是多段行程，还需要可把步行/等候/换乘合成单程的链标识；仅车内时间不能称门到门时间。

有部分样本而没有总体权重时，可保留样本条件结果，或在**已知覆盖质量**的前提下推部分识别界；不能自行规定覆盖率来缩区间。教师headcount仍未取得新的合格城市记录，V6的FTE子群只保留诊断身份。

## 验证

```sh
python3 research/2026-a/data/task4_v7_phoenix/audit_sources.py
```

核验成功下载SHA256、2017都会区字段/频数、公开家庭字段无city标识、2022删除地理字段说明、官方议程中的真实高中条目。只检查本次可见公开材料，不宣称全网不存在任何可用记录。原始PDF/XLSX/HTML保持字节不变；未改变模型任何城市的观测值或区间。
