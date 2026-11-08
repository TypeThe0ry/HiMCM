# V127 Prague：57个具名市内地铁站复合体候选

官方PID市内站点清单在2026-11-09访问时，提供**57个不同名称／节点的地铁站复合体**，每个实体均有A、B或C线路时刻表链接，且链接标明`inprague=1`。作为交通设施供给子集，沿用附件Prague人口1,407,084（2025）与锚点50，得到密度下界`57×100000/1407084=4.050930861270542`，效用候选 **`[0.07494655127527473,1]`**。本包只提议候选，须经parent独立审计后决定准入。

该计数是2026官方网页快照与2025附件人口的混合年份资料，不是2025年末运营计数。其他交通模式及运营方未计，上界保留1；没有推导学生通学时间、班次、居民公平性或个人可达性。

## 市界、实体与运营状态

直接来源是[PID官方“Prague市内站点”清单](https://pid.cz/zastavky-pid/zastavky-v-praze/)。其HTML对字母分组设置`data-inprague="1"`，所链接原始`pid_script.js`的`requestStopTab`将该值传入`getStopTab`的`in_prague`参数。`retrieval_requests.json`完整记录21个字母组POST的URL、方法、form和值及本地响应文件；对应JSON均保存HTTP响应原始字节，不经过Exa或生成式提取。

市界依据是官方市内／市外**站点清单**，没有将票价P、0或B区当行政市界。[市外站点清单](https://pid.cz/zastavky-pid/zastavky-mimo-prahu/)的同一分组使用空`in_prague`值；原HTML及一个相同B字母的市外对照响应也已归档，见`geography_control_requests.json`。市内B组列Bořislavka、Budějovická的地铁线路，市外对照没有这两个名称。57个计入实体各自的原JSON定位、PID node和地铁线路URL见`station_complexes.csv`；每个地铁URL亦检查`inprague=1`。这使用发布方地理分类，没有另做边界多边形叠置。

按名称合并跨字母组的重复返回，并检查同名实体只有一个PID node。Můstek、Muzeum、Florenc各服务两条地铁线，每个只计一个站复合体。未累加月台、出入口、时刻表链接或线路出现次数。

[DPP官方Flora限制详情](https://www.dpp.cz/omezeni-a-mimoradne-udalosti/detail/15)说明该站自2026-02-02起关闭至另行通知，列车通过不停站；2026-11-09取得的PID市内清单中也没有Flora的A线路条目，因此不计。[Florenc C限制详情](https://www.dpp.cz/omezeni-a-mimoradne-udalosti/detail/39)为部分出口和无障碍通行受限，保留出口可用，不能解释成整个站复合体关闭；PID清单仍提供B、C两条线路，故计一次。这是常规运营站点快照，不保证访问当日每一时段无临时中断或每个出入口开放。

## 2025年报提供独立名单交叉核对

[DPP官方年报目录](https://www.dpp.cz/spolecnost/o-spolecnosti/vyrocni-zpravy)链接的2025英文原PDF已完整取得，**56,581,286bytes，192页**，保存在研究仓库外：

`/data/datasets/HiMCM/source_archives/task4_v127_prague/dpp_annual_report_2025.pdf`

完整原件SHA-256为`4e84c413e0d6e51702202f0bf7e04a1569e79ad63b01c71eab3cb60b03a1a7b9`。Git内保存必要的第17、103页提取文字／页图，以及第103页Poppler bbox词坐标。第103页实际图像已查看，三个分栏分别列A17、B24、C20；标明2025-12-31范围。61是线路停站出现次数，三处换乘名称各重复一次，按复合体去重为58。当前57名精确等于该58名中去掉Flora，线路归属也逐名吻合。

第17页记录2025的闭站：Pankrác为2025-01-06至12-19；Českomoravská从2025-01-06关闭，报告预计持续至约2026年3月。因此年报的58个登记复合体不表示2025全年同时开放。即便另外计算2025年末运营子集，排除项应是当时尚关闭的Českomoravská，**不是2026关闭的Flora**。本候选不使用该历史运营推算，Pankrác和Českomoravská由当前PID实际线路清单支撑。D线建设中的未来站点不纳入A/B/C既有设施计数。

原PDF下载命令（写到仓库外）：

```bash
curl -fL --max-time 180 'https://www.dpp.cz/cs/data/V%C3%BDro%C4%8Dn%C3%AD%20zpr%C3%A1vy/Annual%20report/DPP_ANNUAL_REPORT_2025.pdf' -o /data/datasets/HiMCM/source_archives/task4_v127_prague/dpp_annual_report_2025.pdf
sha256sum /data/datasets/HiMCM/source_archives/task4_v127_prague/dpp_annual_report_2025.pdf
```

本轮初次90秒请求在55,456,230bytes中断，随后用`curl -C -`补齐；只有补齐并可解析后的完整文件获得上面的原件hash。网页读取工具因文件体积拒绝直接读取，不作为另一份原件。PDF元数据显示创建于2026-09-01；没有将该创建时间当成已证实的精确发布日期。

## 复现与文件

```bash
.venv-v120/bin/python research/2026-a/data/task4_v127_prague/extract.py
```

脚本使用Python标准库。存在外部原PDF时，另调用Poppler `pdftotext`核对完整hash，并从第103页重新抽取词坐标来复核17／24／20和去重名单。外部原件不在时，仍可用Git内保存的bbox、JSON及HTML重现候选，但manifest会将该次原PDF检查标为false；不会声称完整原件随Git分发。

检查覆盖：原附件SHA、人口与V124该格仍为`[0,1]`；两套官方市内／市外列表及请求参数；每个命名实体的市内地铁URL；跨响应／换乘去重；全部57名及线路与2025登记名单匹配；当前Flora闭站与Florenc部分出入口受限的区别。`manifest.json`记录各来源表示、原URL和原件hash；`station_complexes.csv`保留完整具名提取结果；`observations.json`为待审候选。

无新人口、无线路总数冒充设施总数、无全区域交通合计准入。本目录没有改原CSV、权重、锚点、主准入表、旧结果或论文。
