# V90：Phoenix毕业数据发布入口与API覆盖核查

本轮新增可准入观测0，2024届学校队列6287与学区6285的差异仍未解决。未把净差2解释为重复人数上界。

[官方数据入口](https://www.azed.gov/accountability-research/data)现在明确列出[2025届四年毕业工作簿](https://www.azed.gov/sites/default/files/2025/11/4Y-GradRate-Cohort2025.xlsx)及[2024届四年工作簿](https://www.azed.gov/sites/default/files/2025/04/4Y-GradRate-Cohort2024.xlsx)。网页阅读器对两个链接返回不支持的Excel内容类型，未取得工作簿数值或原件字节；本地下载均403。正常Chrome访问官方入口显示Cloudflare“Sorry, you have been blocked”，本轮没有绕过访问控制。

与此同时，Phoenix Union实体4286的FY2026毕业API请求返回HTTP200及空数组。官方工作簿链接已存在，因此不能将此空数组解释为“2025届尚未发布”、零毕业生或新数据不存在。下一步应取得准确届别工作簿，而不是依赖旧API空响应推断发布状态。

本包保存[访问记录](retrieval.json)和[核查说明](audit.json)，没有伪造工作簿哈希或抑制数值。既有2024届整数、原有毕业条件界、城市教育与通学缺失界均保持；未修改模型、论文或提交。
