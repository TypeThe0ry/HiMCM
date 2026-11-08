# V90：Bogotá2023问卷镜像的学段字段核查

新找到[2023家庭问卷的公开镜像](https://es.scribd.com/document/836488287/b-Modulo-Hogar-A-B-C-X)。可见文件内部标明调查年份、编制联合体及委托部门；模块B第8题问最高已达到教育程度，第9题记录上一周是否为学校学生。两题仍不能直接等同于当前高中年级。

这是第三方镜像的人工读取，尚未与[官方问卷ZIP](https://observatorio.movilidadbogota.gov.co/sites/default/files/2025-09/02_Formularios%20EODH.zip)核对字节。官方文件本轮连接被远端关闭；未取得原件，不填哈希，也不宣称全部2023模块都没有当前年级字段。

[访问与字段记录](audit.json)说明下一步需核实官方版本和原始变量字典。新增准入观测为0，Bogotá通学区间保持[0,1]；未修改模型、论文或排名。
