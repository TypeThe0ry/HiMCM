# V6 新增学生通学证据与拒绝入模审计

获取日期2026-11-07，仅本目录文件由本子任务创建。

## 可条件接入：Mexico City 高中阶段通学保守界

来源为CDMX评估机构Evalúa的官方《Infancias en la Ciudad de México 2020》，2020-04-30发布，**图49，印刷页71，实际调查2015 Encuesta Intercensal**：

https://www.evalua.cdmx.gob.mx/storage/app/media/invyest/INFANCIAS%20EN%20LA%20CIUDAD%20DE%20MEXICO%202020.pdf

必须明确：官方源站直接HTTP(S)下载超时，web打开和截图也失败；本目录**没有原PDF，没有视觉核验图表颜色**。`mexico_official_index_extract.json`是对官方PDF搜索索引完整图49文本及注释的结构化转录，保留原URL、查询、页码、全部条形数值及三个群体总数。不是二手新闻数字，也不冒称原始PDF归档。它只适合明确的索引取数条件情景；`strict_archived`撤回为[0,1]。

图表对象为居住CDMX、3–17岁且正在接受义务教育的儿童。EMS是media superior，即高中阶段；并非把所有儿童代为高中生。图中EMS报告时长人数228,967。图49给三个分组（基础教育、EMS、两者合计）、每组5根条形、共15个标注计数；抽取顺序与颜色无法核实，因此做两个独立保守处理：

1. 枚举全部C(15,5)=3003个子集，只有一组计数合计恰为EMS228,967：39,240、79,954、77,881、29,661、2,231。这确认了学段归属，而不依赖颜色识别。
2. 对这5个计数和5个时长箱的全部5!=120种映射取最坏效用，不采用看起来最自然的图表顺序。

同一图表注释给义务教育总人数1,625,498，其中报告时间1,548,151，所以未报告时间77,347。因为EMS属于这个同城市、同年龄母体，可把**所有77,347人都最坏分配给EMS**；不假设各学段缺失率相同，不把没填时间的人删除。最大目标人数为306,314。

图表时间是 casa-escuela-casa 往返时间R。单程入校时间t≤R，对任意方向不对称都成立；故exp(-t/30)≥exp(-R/30)。我们不把R除以2，也不把往返时间直接当单程点估计。

令计数集合为n，五箱往返上端点b=(30,60,120,240,∞)，q=(exp(-1),exp(-2),exp(-4),exp(-8),0)，M=77,347，N=228,967。允许任何计数到箱的排列π：

\[
L=\min_{\pi\in S_5}\frac{\sum_{k=1}^5 n_{\pi(k)}q_k}{N+M}=0.0182157874085163,\qquad U=1.
\]

尾部开放箱和全部缺失时长者都允许零效用。缺失者人数m∈[0,M]，分子非负，故最坏取m=M。上界仍1，因为没有入校/返家方向分配的资料，不能从总往返时间推出入校时间正下界。

`bounds.csv`只输出这一行mapping-robust界。最坏排列对应(2231,29661,39240,77881,79954)。未经图像确认的自然排列给下界0.0871412，**只写诊断文件，禁止主模型采用**。

这不是95%置信区间。它以官方公布的调查估计人数及整数呈现为条件，没有设计方差信息，也没有将2015证据冒充2026观测；仅涵盖未满18岁EMS，不覆盖18岁及以上高中生。故它只能扩大真实学段证据覆盖，不能宣称已完成全体高中生现状评估。低下界是保守推导的结果，不能为了获得更显著排名变化而换成自然映射或假设单程对称。

## Tokyo：真实高中群体，但拒绝主入模

官方e-Stat原始Excel已完整下载并记录SHA256：

https://www.e-stat.go.jp/stat-search/file-download?statInfId=000032223730&fileKind=0

2021社会生活基本调查，表66-2，工作表a066_2，行23498：平日、Tokyo、男女合计、高校、智能手机使用合计，J23498=87分钟，AD23498=67（该行样本大小，并非保证所有67人都进行了通学活动）。

该87分钟是**一天累计“通勤・通学”活动者平均**，混合可能的工作通勤，且活动者分母不一定等于实际上学学生。无法直接转为居住地到就读地点的单程时间；不÷2、不套Jensen当主界。`tokyo_diagnostic_row.json`记录准确单元及标签，主模型Tokyo仍[0,1]。

## 其他检索线索及为何拒绝

- London市政府2020/2160答复，https://www.london.gov.uk/who-we-are/what-london-assembly-does/questions-mayor/find-an-answer/detailed-data-childrens-journeys-school ：LTDS分学段公开的是交通方式份额，样本不足以按年×区×方式×学段分解。模式份额不是时间，未产生通学效用界。
- 英国NTS2024学校出行，https://www.gov.uk/government/statistics/national-travel-survey-2024/nts-2024-travel-to-and-from-school ：公开结果England全国，不能填London。
- Toronto Eglinton项目高中调查，https://ontarioactiveschooltravel.ca/wp-content/uploads/2017/10/Eglinton-Crosstown-STP-Project-Supplementary-Report-High-Schools.pdf ：真实高中问卷有时间箱，但属于项目学校，未核全市目标群体的概率抽样/完整覆盖权重，不能直接当Toronto全市分布。
- Shanghai学生交通研究，https://pmc.ncbi.nlm.nih.gov/articles/PMC8124258/ ：作者明确说未收集学校距离或通学时间。交通方式与时间不可互换。
- Dubai官方学生交通方式资料和学生幸福感调查线索没有核到同高中阶段城市时长分布，拒绝用“平均30–60分钟”的媒体概括替代。

这些为检索审计，不暗示相应数据不存在。全国、成人、最近学校可达性、学校巴士规定上限等均未入主模型。

## 离线复算

`python3 research/2026-a/data/task4_v6_commute/extract_commute.py`

仅使用Python标准库。先校验归档SHA256，再检查3003子集唯一阶段归属、120映射最坏界、开放尾部与缺失人数处理，最后核对Tokyo原始Excel精确单元。保留每项原始口径的撤回选择。
