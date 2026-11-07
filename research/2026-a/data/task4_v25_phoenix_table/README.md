# Phoenix：公开县级毕业表取得数值，语义仍需核实

通过正常浏览器表格筛选，已读到 [KIDS COUNT 4616](https://datacenter.aecf.org/data/tables/4616-four-year-graduation-rates) 的 Maricopa 数据。显示年份 2024 对应 **Number 50,023、Percent 78.8%**；2025 对应 52,234、80.3%。这是县级公开表的实际显示值，不是 Phoenix 市值。

本轮没有重试此前被拦截的下载。浏览器切换 By County → Uncheck All → Maricopa 后读取可见表；[CSV](visible_table_transcription.csv) 是人工转录的 2016—2025 两地域显示值，未冒称下载的原始工作簿。精确筛选 URL、标签、哈希和核验限制见 [来源审计](source_access_audit.json)。

**暂不收窄 Phoenix 区间。** 同表 Arizona 2024 显示 Number 94,651、Percent 78.4%。既有 ADE FY2025 API 的 All 行为队列 94,501、毕业 74,261（比值约 78.5822%）。这些数字未能直接对应；Number 标签也未单独定义为毕业人数或队列人数。不能因它接近某个已知数字就替换字段名或推算确定分母。还需要核实显示年份与队列年度的对应、数据版本以及学校所属县覆盖。

结果：新取得公开显示值，新增可准入 Phoenix 教育观测 **0**。模型和缺失区间保持。

同一公开 ADE API 的相邻版本也已归档核查：FY2024 的 All 行为队列 92,895、毕业 72,324、77.86%，未与 AECF 显示 2023 的 72,415／77.5% 完全对应；FY2026 返回空数组。请求及原件哈希见 [版本核查](state_vintage_requests.json)。现有证据不支持通过简单年份平移消除差异。
