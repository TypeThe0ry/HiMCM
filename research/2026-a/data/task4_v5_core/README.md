# V5 生活成本、住房、凶杀与公交设施

获取日期2026-11-07。本目录原始manifest保留，不改写已有原文件。`extract_core.py`离线校验manifest中每个成功文件SHA256，并从原始文件重建52条 `observations.csv`。

## 生活成本与房价收入比：25城各一条

直接读取此前归档 `../task4_real/numbeo_quality_of_life_2025.html` 的原表，按此前 `city_indicators_2025.csv` 内完整 `source_city` 精确匹配，不猜城市别名。新提取25城2025版 Cost of Living Index，并核对25城PIR与旧矩阵一致。

原始页面URL：https://www.numbeo.com/quality-of-life/rankings.jsp?title=2025

原HTML SHA256：`b5b9bc3bae7488bfe05be50420df86e74ccaf29be22447f273c1ae4d685280bf`。

生活成本指数纽约=100，不含房租；不是绝对支出，不再自行重复作PPP换算。PIR保持Numbeo定义，不能当Demographia税前家庭中位数倍数，更不能解释成租金收入比。二者是众包城市聚合，不称已统一所有行政边界或全体家庭普查。方法页面另存 `numbeo_method.html`，不把作者未公开的消费篮子权重虚构出来。

## Singapore 凶杀率

World Bank WDI `VC.IHR.PSRC.P5`归档API中最新非空年份为2023：**0.0690954942050905 /10万人**。2024与2025为null，不向后填充成年份较新观测。城市国家地理边界使该国家级值可用于Singapore，其他城市不照搬国家均值。指标是intentional homicides，不使用安全感指数替代，也不把未遂案件率和死亡率混合。

来源：https://api.worldbank.org/v2/country/SGP/indicator/VC.IHR.PSRC.P5?format=json

这是国际数据库汇编，不冒称本轮取得警方原始逐案记录；元数据来源口径须由主报告说明。

## Singapore 公交名录资源下界

LTA官方GeoJSON共5205条Point，`BUS_STOP_NUM`为5205个唯一、非空代码，全部更新时间字段位于2026年。分母是Singapore2026年总人口6,208,500（同地理范围；官方SingStat核验见相邻 `task4_v5_resources/sg_population_verified_web_extract.json`）。

5205/6,208,500×100,000 = **83.8366755255个公交站代码/10万人**。

来源：https://data.gov.sg/datasets/d_3f172c6feb3f4f92a2f47d93eed2908a/view

计数单位明确为**有独立代码的公交上车/停靠点**，不是50米合并后的换乘站或物理站址。对向站点可能是不同代码；不能宣称执行了附件中的50米聚类。本轮只有公交模式，轨道及其他模式未纳入，故在“公开公共交通停靠点代码”维度上作为单侧名录下界；`lower_bound_only=True`要求模型仍保留未知上界。

该下界以名录所列站点可作为设施记录为条件；未独立验证每站是否临时停用或班次足够，不能称实际服务可达人口下界。若主模型要求“当前运营且统一聚类”的站点指标，该记录必须降为补充情景，主值未知。

## 泳池与失败抓取

泳池目录页面可列出25处设施，但临时关闭页面表明“目录存在”不保证当前全年开放；未逐设施核对季节性、关闭、运营主体和去重。因此**本轮泳池维度仍未知**，不将25直接当可用公共泳池数。

NYPD凶杀页面返回403，manifest保留失败记录；纽约人口页本身不能补出凶杀率，故纽约该维度仍缺。Ookla重复归档仅保留来源，实际宽带提取在 `task4_v5_resources/` 完成，避免两套互相覆盖的观测。
