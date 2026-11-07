# Phoenix新增官方入口核查（2026-11-07）

本轮只读检查MAG官方字段说明，没有新增可准入观测，Phoenix通学仍保持未知区间。

| 官方入口 | 实际内容 | 准入判断 |
| --- | --- | --- |
| [2025就业/TRP服务](https://geo.azmag.gov/arcgis/rest/services/maps/StateEmployment_2025_v2/MapServer) | 2025数据，页面注明截至2026-08-01 | 就业资料入口 |
| [EmployerDatabase层0](https://geo.azmag.gov/arcgis/rest/services/maps/StateEmployment_2025_v2/MapServer/0) | Employees、trpid、JURISDICTION与坐标；未提供学生年龄、当前年级、通学时长或学生权重 | 不可作为高中生通学；雇员人数也不可替代教师人数 |
| [CommuteSheds层8](https://geo.azmag.gov/arcgis/rest/services/maps/StateEmployment_2025_v2/MapServer/8) | 就业通勤圈多边形，含MAX_TIME字段 | 并非实际学生旅程，不能准入 |

官方网页字段说明已读取；直接JSON请求超时，未保存原始响应，也未声称下载了微数据。此表是访问与排除记录，不是数据观测。由独立检索agent核查。
