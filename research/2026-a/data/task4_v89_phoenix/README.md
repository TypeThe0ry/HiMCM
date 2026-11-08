# V89：Phoenix财政与教师口径核查

新增Career Success Schools的官方财政表读取转录：FY2025报告印刷页II-116的Teacher Salary栏，Prior FY2024与Current FY2025年末FTE均为32.00。同表2023/24高中ADM为1068.0014、全学段ADM1219.0697。原PDF直接请求403，未取得原件，哈希保留为空。[官方来源](https://www.azed.gov/sites/default/files/2026/01/2025%20SAFR%20V2%20FINAL.pdf)。

该LEA同时包含K—8及高中；工资口径的财政年度末FTE尚未与2023/24学校课堂教师、秋季学生数对齐。官方[NCES当前学区记录](https://nces.ed.gov/ccd/districtsearch/district_detail.asp?ID2=0400219)另报2024/25课堂教师36.50 FTE、学生1145人，属于下一学年，不能回填2023/24。未按32.00或36.50人为设置高中教师上界。

本轮还检查了学校自身的[预算与会议目录](https://careersuccessschools.org/board-documents/)和独立的[ADE旧审计文件入口](https://www.ade.az.gov/sfsinbound/GeneralUpload/193485.pdf)。后者返回403，审计年份未核实。学校FY2024预算链接返回HTTP200，但内容实际为HTML，不是PDF；没有把成功状态码误记为取得原件。网页读取的预算摘要只有拟定经费和平均工资，不提供可用的实际教师FTE。

North Star的[官方会议目录](https://www.arizonapreparatoryacademy.com/board-meetings)有2023/24议程与会议记录条目，本轮未取得同年完整实际教师计数。另排除Eagle, Idaho的同名North Star学校，未混用其审计报告。

[访问记录与字段转录](audit.json)区分官方网页读取、原件失败和口径限制。新增可准入单元为0；保留Phoenix缺失区间，未联系机构、提交申请或修改模型、论文。
