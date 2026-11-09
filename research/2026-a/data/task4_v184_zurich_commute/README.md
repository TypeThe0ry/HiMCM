# V184：Zurich39.9对应官方工作通勤估计，不缩窄旅时界

Eurostat当前原始API提供与原表数值／年份相同的记录：`urb_ctran`、`TT1019V`（Average time of journey to work - minutes）、`CH002C` Zurich (greater city)、2024期，39.9分钟，标记`e`（estimated）。同一响应的公共交通工作通勤份额60.41也与原表一致。它确认存在匹配的提供方观测；原CSV未给出处或提取回执，不能据此证明该CSV的完整历史传递链。

这条原件补齐了重要范围：工作通勤而非高中通学，当前标签greater city与人口字段所标city proper需分别保留，提供方估计标记而非无误差的已知均值。2024为API观察期标签，精确调查窗口尚未另行识别，2026-11-04是数据更新时间。CSV没有另行标明通勤地理，不能把人口边界字段自动当作所有指标边界，也不据此宣布原通勤值地理错误。当前标签尚未核到精确2024边界多边形或国家调查实施。原用户39.9／2024／ok保持，提供方标记另存，0准入、0评分变化；未取得同人群同口径的时长分箱，不能以不相干学校分布缩窄现有条件界。

初次按参考线索请求CH001C时，当前官方字典返回Bern (greater city)、37.69分钟，不能当作Zurich。随后全城市2024同指标响应和CH002C完整城市响应共同确认当前代码和值，避免把代码相似或旧参考当作地理证明。

四份HTTP200原件保留原字节；`retrievals.json`记录URL、访问UTC、长度和SHA。`findings.json`区分原表标签、匹配提供方字段、地理／估计状态与未证明的传递链。六次定向查询限定两条路线，第三方页面只作导航，不作数值权威。历史工作通勤定义可查同轮Dublin包的2004官方手册，不能直接代表2024瑞士调查实施。

[匹配官方响应](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/urb_ctran?lang=EN&cities=CH002C&time=2024)；[全城市2024工作旅时](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/urb_ctran?lang=EN&time=2024&indic_ur=TT1019V)；[官方城市统计元数据](https://ec.europa.eu/eurostat/cache/metadata/en/urb_esms.htm)。科学V181、自有稿V182与三个注册表均未修改。
