# V195 Vienna：工作旅时分箱的模型定义核查

本轮两条新路线没有产生可准入的实测通勤数据，当前Vienna旅时仍保留未知区间。市府平等监测页展示工作旅时分箱，但原始HTML的`Anm. 2`说明其时间来自道路速度模型计算的住址—工作／学习地点最快路线，涉及汽车可通行路段。它不是受访者实际方式下的单程旅时，不能因页面标题写“工作旅时”而作为实际分布接入。

- [Stadt Wien Frauenservice，J5工作旅时](https://www.gleichstellungsmonitor.at/kapitel/Kapitel-J-Umwelt-und-Mobilitaet/indikator/Dauer-des-Arbeitsweges)：原HTML HTTP200，25694字节。定义定位在`dfn`的`title`属性，网页可见正文或搜索摘录可能不展示该脚注。页面提及2015／2019／2021比较；这些年份不改标2025。图形组件`J5.1`不是本轮获取的完整数值原表，不从近似正文重建分布。
- [Stadt Wien步行及居民出行索引](https://www.wien.gv.at/verkehr/zahlen-fakten-zu-fuss-gehen)：本轮直接请求HTTP403后跳过，无原件、不用搜索摘录构造观测。

`retrievals.json`记录实际UTC、成功响应哈希及失败路由。`verify.py`离线检查原件大小／SHA及脚注关键定义。本轮不计算效用界，不把最快汽车路线、最近学校模型或日总出行时间替代实际单程旅时。0新增准入、0实际评分区间收窄；不修改用户CSV、V192模型或论文。
