# V183：两项新旅时来源保持独立，主模型不准入

新查得Vienna与Tokyo官方原件，各有明确数值，但均未识别当前高中实际单程旅时。该包0准入，不改V181模型／V182稿件或原始CSV。

- **Vienna：** ÖROK《Erreichbarkeitsanalyse 2024》表30（印刷74页／PDF物理76页）给出ISCED3的ÖV2023加权旅时8.2分钟，学校日到达窗口7:00—8:15；目标学校库存为2021/22。它衡量模型中的最近教育设施可达性，不能当作学生实际就读学校的通学均值或2025观测。表格已渲染实看核数。
- **Tokyo：** 2024年鉴17-19原CSV中，15—19岁、男女合计的工作／上学合并时间为62分钟。对象和整周时间用途口径不同于高中单程；不能直接除二变31分钟。原CSV尾部表题明确观测年2021（令和3年）；2024是年鉴版次，不把版次冒充观测年。

原始PDF45.2MiB与CSV原字节保存，URL／HTTP200／访问UTC／SHA见`retrievals.json`；字段提取、年份／地理／人群和拒收原因见`findings.json`。六个搜索查询限定两个城市路线，未重做Warsaw2022混合年龄小样本。保持三项缺失学校旅时的原有区间。

原件：[ÖROK官方报告](https://www.oerok.gv.at/fileadmin/user_upload/publikationen/Schriftenreihe/216/OEROK_SR216_Erreichbarkeitsanalyse_2024.pdf)；[Tokyo官方CSV](https://www.toukei.metro.tokyo.lg.jp/tnenkan/2024/tn24qv171900.csv)。完整研究原件只在研究仓库，未复制到Overleaf。
