# Phoenix 高中成果数据接口：取得首份真实结果

2026-11-07 从 Arizona 官方 https://azreportcards.azed.gov/ 页面及其公开客户端脚本发现 Graduation Rate 接口，成功取得实体5439（Central High School）的 fiscalYear=2025 数据。具体请求在 request.json，原始响应和脚本已归档，manifest.json 保存哈希。

All组：numInCohort=395，numGraduated=301，公布gradRate=76（百分比）。301/395约76.20%，公布百分数有舍入，聚合应使用人数。分组行是重叠分类，不可与All组重复相加。负数-11为特殊码，不得作为负人数或零人数计算。进一步需要核实抑制规则及该fiscalYear对应的毕业届别。

当前只是一所学校的成果证据，不代表Phoenix市、城市居民或全部高中。尚未加入主模型，新增城市指标为0，原缺失区间保持不变。下一步：将官方实体ID与既有市界学校清单建立可核验连接，取得各校同届All组分母，记录缺校与抑制，构造覆盖清楚的学校所在地公校结果情景。毕业率是成果指标，不能直接填入教师人数比率。

浏览器访问cms.azed.gov数据目录亦被Cloudflare阻断；School Report Cards公开站点与接口HTTP200，已改变后续数据获取路径。

并行发现Bogotá 2023调查新官方镜像：https://observatorio.movilidadbogota.gov.co/publicaciones/resultados/encuesta-de-movilidad-2023 ，含个人、行程及字典下载，但尚未成功取得ZIP，须验证高中在读、时间与权重字段后才准入。

当前模型仍为 S=100 sqrt(B)/(sqrt(A)+sqrt(B))，B=sum(w*u²)，A=sum(w*(1-u)²)，u属于证据区间；主指标权重(1-alpha)/8，辅助alpha/2，alpha属于[0.05,0.20]。本次未修改评分输入，沿用上轮25城可能冠军结果，不声称重新估计排名。
