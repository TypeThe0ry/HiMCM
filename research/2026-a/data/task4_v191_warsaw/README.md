# Warsaw：38个具名地铁复合体候选下界

新取得Metro Warszawskie官方两条线路原HTML：M1有21个站名，M2有18个；唯一共同名称为Świętokrzyska。按换乘复合体合并后保留38处，而不是把39次线路站点出现当作39处设施。配保留人口1,863,800（2024）和交通密度锚点50，得到密度至少2.03884537／十万人、效用候选`[0.03917929683472522,1]`。尚未主准入，未改CSV、模型或论文。

## 来源、范围和时间

- [M1线路具名站点](https://metro.waw.pl/metro-warszawskie/linia-m1/przebieg/)与[M2线路具名站点](https://metro.waw.pl/metro-warszawskie/linia-m2/przebieg/)保存为完整原响应HTML。只提取正文accordion中的`Stacja`标题，不把导航、图片alt文字、站台长度或入口数加入计数。`station_appearances.csv`保留每个原名、线路顺序和原DOM元素定位；DOM ID不是稳定站点ID。
- [官方网络图PDF](https://metro.waw.pl/wp-content/uploads/2026/02/PLAN-METRA_2.pdf)第一页给出21／18站，第二页把现有线网与规划线网分开。已实际渲染查看第二页：Świętokrzyska为两线交点，Karolin、Chrzanów、Lazurowa为虚线建设段，技术车辆基地STP不计入。图内标注2024年4月，PDF元数据创建于2024年5月；URL中的2026/02不是其内容观测年份。
- [马佐夫舍省国家消防局2025年通报](https://www.gov.pl/attachment/2b7775c0-aa52-487e-809a-66df1b991b59)封面为2025年通报、2026年2月发布。物理第4页明确将M1的21站和M2的18站定位在华沙市域（m.st.Warszawy），支持地理范围，未借用全省人口。第5页关于Bródno–Bemowo建成于2023的叙述不用于断定具体历史开通日期。

候选采用2026-11-09 UTC取回的线路目录快照，配保留2024人口；图和消防资料分别提供较早拓扑及市域佐证。这不是2025设施普查，也没有把静态目录当作逐站实时运营核验。其他交通模式未计入，上界保留1；站名列表不识别高中生的使用资格、开放时段、频率或可达性。

`retrievals.json`保存实际URL、最终URL、UTC访问时间、HTTP状态、原字节长度、SHA与响应头。四份原件均为HTTP200完整响应；不使用搜索摘录作数值来源。`fire_service_scope_extracted.txt`仅为物理4—5页派生文字。

## 离线核验

```sh
.venv-v120/bin/python research/2026-a/data/task4_v191_warsaw/extract.py
```

仅使用Python标准库与Poppler，核原响应哈希、21／18站标题、唯一交集、38个复合体、建设站排除、官方市域句、原CSV哈希与人口，重建命名清单和`findings.json`。图面判断在`visual_check.json`中明确列为视觉核读，脚本不冒称自动证明图形拓扑。收集脚本仅供来源路线复核，已冻结原件不被再次下载覆盖。
