# Bogotá EM2021当前高中与通学规则核验

2026-11-07核查官方变量字典；本轮未取得原始微数据，没有新增观测。

- [NPCHP2](https://microdatos.dane.gov.co/index.php/catalog/743/variable/F51/V5003?name=NPCHP2)：1为当前在读，但包括假期待续读、灵活课程、暂时缺席者，不能等同线下到校。
- [NPCHP6](https://microdatos.dane.gov.co/index.php/catalog/743/variable/F51/V5008?name=NPCHP6)：4为Media（10–13），NPCHP6A为当前年级；需结合人口模块实际年龄筛14–18岁。
- [NPCHP18AO](https://microdatos.dane.gov.co/index.php/catalog/743/variable/F51/V5043?name=NPCHP18AO)：1为不出行、2为否。没有证据表明所有不出行都来自疫情或远程学习，不能直接记零分钟或统一排除。
- [NPCHP19](https://microdatos.dane.gov.co/index.php/catalog/743/variable/F51/V5044?name=NPCHP19)：单程分钟，含等待和所有交通方式。元数据范围5–999未说明999是否特殊码，当前不能当作确定长旅程或确定缺失码。
- [调查方法](https://microdatos.dane.gov.co/index.php/catalog/743)：2021-04-15至11-30采集，一阶段分层整群，平均约10户的住宅段为PSU；Bogotá城镇95层。覆盖非机构化人口，包含Bogotá城镇和农村及部分Cundinamarca，需筛地域。权重经框架、覆盖与段扩张调整及2018人口普查投影校准。

后续必须取得问卷/变量结构确认资格与特殊码，再建立未知时长和不出行规则；在此之前通学格保持[0,1]。官方SDP替代ZIP浏览器访问也连接超时，未确认任何成功下载。
