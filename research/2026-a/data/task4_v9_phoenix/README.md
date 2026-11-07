# Phoenix 高中成果数据接口：取得首份真实结果

2026-11-07 从 Arizona 官方 https://azreportcards.azed.gov/ 页面及其公开客户端脚本发现 Graduation Rate 接口，成功取得实体5439（Central High School）的 fiscalYear=2025 数据。具体请求在 request.json，原始响应和脚本已归档，manifest.json 保存哈希。

All组：numInCohort=395，numGraduated=301，公布gradRate=76（百分比）。301/395约76.20%，公布百分数有舍入，聚合应使用人数。分组行是重叠分类，不可与All组重复相加。负数-11为特殊码，不得作为负人数或零人数计算。进一步需要核实抑制规则及该fiscalYear对应的毕业届别。

当前只是一所学校的成果证据，不代表Phoenix市、城市居民或全部高中。尚未加入主模型，新增城市指标为0，原缺失区间保持不变。下一步：将官方实体ID与既有市界学校清单建立可核验连接，取得各校同届All组分母，记录缺校与抑制，构造覆盖清楚的学校所在地公校结果情景。毕业率是成果指标，不能直接填入教师人数比率。

浏览器访问cms.azed.gov数据目录亦被Cloudflare阻断；School Report Cards公开站点与接口HTTP200，已改变后续数据获取路径。

并行发现Bogotá 2023调查新官方镜像：https://observatorio.movilidadbogota.gov.co/publicaciones/resultados/encuesta-de-movilidad-2023 ，含个人、行程及字典下载，但尚未成功取得ZIP，须验证高中在读、时间与权重字段后才准入。

当前模型仍为 S=100 sqrt(B)/(sqrt(A)+sqrt(B))，B=sum(w*u²)，A=sum(w*(1-u)²)，u属于证据区间；主指标权重(1-alpha)/8，辅助alpha/2，alpha属于[0.05,0.20]。本次未修改评分输入，沿用上轮25城可能冠军结果，不声称重新估计排名。

## 批量获取与抑制区间更新

collect_city.py 在143所市界内、非全虚拟、运营中且NCES最高年级12的学校中，按规范化名称完全一致及坐标距离小于0.5 km匹配64个官方实体（ID无重复）。这是一组保守候选匹配，不是全市完整学校连接；尚需对历史学校变化和同名校核验。64份响应全部归档，57份有唯一All组。

24所人数完整的子集合计队列10,081人、毕业8,647人（85.78%）。扩大到所有队列人数已知的53所学校，分母12,805人；按毕业人数抑制保留[0,n]，并依据官方客户端的>98%率代码保留整数约束，毕业人数为[9,245,11,371]，对应[72.20%,88.80%]。这是该53校的区间，不是城市区间。其他4所队列被抑制、7所无All组及未匹配学校不能静默删除后宣称全市代表性。

客户端常规毕业率标题显示 Cohort=fiscalYear-1，因此FY2025对应2024届。率字段-98映射>98、-2映射<2、-11映射抑制星号；人数负码不套用率字段解释。[官方技术手册](https://www.azed.gov/sites/default/files/2024/02/FY24%20Grad%20Drop%20and%20Persistence%20Rate%20Tech%20Manual.pdf)说明统计为公立高中学生的最后记录学校归属，不是居民所在地统计。

bound_outcomes.py 的可复算公式：对已知队列n_s，完整人数取g_s；抑制人数取[0,n_s]；率>98%时取[floor(0.98n_s)+1,n_s]。子集率区间为[sum g_s^L/sum n_s, sum g_s^U/sum n_s]。检查所有人数边界0≤gL≤gU≤n、整数组队列及实体ID唯一。没有改写评分输入，因此主模型缺失区间、排名和可能冠军结果保持原版本；尚未做城市教育成果模型替换。

## 官方实体市界扩展（第二次覆盖核查）

collect_spatial.py 直接使用官方名录坐标和既有市界多边形（含孔洞），不依赖NCES名称匹配。全名录2,759学校行/2,460唯一ID；市内577行/515唯一ID。别名按ID去重，保留别名表。515个请求成功，106个有唯一All组。学校类型按全名录同ID全部标签合并，排除任一标签为Online School或Private School的95个实体，防止线上学校通过Charter别名重新进入。

剩余学校中90所队列人数已知，共15,581人。保留毕业人数抑制及率区间，毕业人数界为[9,991,12,706]，子集率为[64.12%,81.55%]。与前次53校结果不同，原因是观测学校集合改变，不是相同总体的区间收缩。完整响应及请求地址、按实体排除记录均保存。

全州缺坐标198行/146个ID，其中包括名称带Phoenix的学校；不能默认为市外。名录缺少运营状态、学段和历史学年，当前坐标与2024届最后记录学校口径未完全对齐。因此扩大名录改善了覆盖审计，尚不证明全市毕业率，也不改写城市模型输入或宣布冠军变化。主模型公式及25城可能冠军结果仍保持上一版本。

复现：collect_spatial.py（缓存成功响应，失败留状态）、audit_spatial.py（按ID合并类型与抑制区间）。验证：515实体ID唯一、响应成功、所有计数界0≤下界≤上界≤队列人数；官方别名坐标在市内同ID一致。尚未完成当前市界与历史位置的一致性验证。

## 缺坐标实体的官方ID恢复

recover_locations.py 从缺坐标学校中找到10个唯一NCES同名候选，逐校获取ADE FY2025 GetEntity记录，用官方leances+nces组成完整NCES学校ID，10个均与NCES2024–25记录一致。以该NCES记录中的坐标补充空间核查，而非只凭名称或邮寄城市认定。保留实体原始响应、坐标来源和ID匹配表。

3所Online学校仍排除。其余7所中Roadrunner School队列被抑制；6所队列已知，新增1,199人（Trevor Browne632、Career and College Prep24、International Commerce145、Anthem Prep40、BASIS Phoenix66、Hope College and Career Readiness292）。与原空间候选按实体ID排重后，已知队列子集增至96校、16,780人；毕业人数界[10,620,13,465]，比例[63.29%,80.24%]。recover_locations.py与audit_spatial.py --include-recovered可复现，原90校输出保留供比较。

学校ID验证解决了这10个实体的连接问题，未解决其他缺坐标学校、被抑制分母、私校和历史位置覆盖，因此未将子集率填为全市指标。本轮主评分输入不变，保留上一模型结果。

Bogotá并行下载核查：官方镜像的问卷ZIP经requests连接关闭、网页访问超时、Chrome ERR_SOCKET_NOT_CONNECTED，未获得ZIP。SIMUR目录确认调查覆盖Bogotá及20个邻近市镇、5岁及以上人口；尚未核实高中在读字段、时长和家庭调查权重。没有拿拦截调查EODI权重说明替代家庭调查EODH方法，也没有新增通学观测。

## Correction: returned year and cohort overlap

All ten recovered entity detail responses actually return fiscalYear=2026 despite requesting 2025. Identifiers match, but historical attributes are not verified. Graduation responses themselves return 2025. See entity_year_audit.json.

The 2015 official technical manual permits some dual-enrolled graduates to be recorded as G at both schools. Accordingly, all preceding aggregate counts mean SCHOOL COHORT RECORDS, not demonstrated unique students. The 16,780 records and associated rate bounds describe the school-record-weighted subset only. Current-year duplication rules remain unverified.

State All cohort=94,501 and graduates=74,261 are archived; comparability with cross-school summed records is unverified. The outcome-margin model is a conditional scenario, not admitted evidence.
