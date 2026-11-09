# V161：Dublin工资册FTE与岗位分配的真实范围

新取得官方2025/26教师工资册报告及City of Dublin ETB年报，确认“岗位分配额可直接充当实际任职FTE上界”在该来源中不成立：同一行工资册FTE为411.8、分配FTE为376.1，相差35.7。这个实际反例使后续师资区间构造有明确的准入检查，避免用计划岗位压低真实教师分母。

## 新来源与可核数值

Department of Education and Youth的The Teaching Workforce in Ireland，2025/26 School Year，发布标记April2026，采用2025年11月末工资册。PDF第14页表10的City Of Dublin ETB post-primary vocational行是376.1分配／411.8工资册FTE，Difference35.7，Cover显示100%。直接相除约109.49%，与显示值分开保存；不据此反推未报告的统一截断算法。Dublin & Dun Laoghaire是另一ETB行，不能当作Dublin市同义词。

PDF第12页表9的Dublin为郡级secondary、community和comprehensive部分，工资册FTE6075.7；vocational另在表10。这个郡级行不能直接作全市全部提供者的教学分母。第18页定义明确排除完全由私校自行雇用的人员；对post-primary教师还要求雇主是认可学校，FET中心任职者排除。因此不能把该工资册分项与ETB全部成人教育员工混为一谈。

City of Dublin ETB Annual Report2024的PDF第18页、印刷第16页，列11个Community Colleges、3862名full-time students，参考学年2024/2025。此为ETB子集，不是全市高中学生总数；工资册为下一学年2025/26的11月时点，不能因都含日历年2025而直接相除。年报还覆盖小学、特殊学校、成人FET及其他服务，近似全机构员工数不替代教学FTE。

## 本轮准入决定

本轮未建立高中阶段教学FTE拆分、全部提供者的城市覆盖及同学年学生分母。即便某些表名含City Of Dublin，也不能自动通过这些条件。工资册私人雇用人员覆盖限制还阻止把郡／全国政府工资册直接认作全体目标教师的上界。Dublin师资效用保持[0,1]；不生成错配师生比，不以分配额、注册人数或全机构人员填缺。

新增入模0、评分区间收窄0。主分析／扩展仍V154，当前独立稿仍V160，Zurich保守、16可能／0必要冠军。未重跑MC，也未改正文、参考文献、图或PDF。

## 采集真实性与复核

搜索索引中的旧年报地址含-English，实际HTTP404；官方出版目录的现行链接去掉该后缀，已成功取得61页原PDF。报告为20页，出版目录HTML一并保存，共3个成功原响应；失败尝试与正确地址、UTC时间、字节数和SHA均记retrieval.json。年报经可及性处理，提取文本含重复表示；3862只读取一次，不对重复文本求和。

extract.py以Poppler layout提取工资册行；scripts/audit_task4_v161_dublin.py独立使用raw页解析和Decimal核对差额，校验三个原件、20／61页及现有187科学快照、463既有论文文件。工资册PDF12、14、18页与年报PDF18页均渲染实看。scope_audit.json，包含结构化范围与空observations；verification.json为核验回执。没有新建或编辑PDF。

当前V160的41项交付状态不改变，真实控制号、完整全队AI记录及最终提交仍待实际证据。本轮将精简范围说明／回执存入私有Overleaf独立目录，原件留研究；公开研究push继续待既有用户选择。长期goal active，后续跳过已查岗位分配和这组错期ETB配对，转向新的同口径来源或其他结论相关数据。
