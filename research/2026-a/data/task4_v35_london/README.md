# London真实在校年级数据：尚不能形成教师分母识别界

取得DfE官方2024/25两套完整CSV并作字节无损gzip归档。解压后的原始CSV哈希及压缩文件哈希均在manifest；本地未压缩CSV忽略，不上传超过50MB的文件。

London state-funded secondary学校January2025 Year12学生56499、Year13学生49547，合计106046。November2024 workforce表InnerLondon同phase教师人数估计13215.63636、OuterLondon24963，合计38178.63636（另有FTE36359.32545）。年级不是年龄，学校地点不是学生居住地；仅涵盖学校sixth form，非London所有高中/FE学生。

直接把两个量相除得2.777626707，不是高中师生比。若额外假设上述教师估计为同一目标群体所有任课教师的上限，才得到条件效用上界0.8437571700；这一额外假设尚未建立，因此`main_admitted=false`，主模型仍应保留[0,1]。

## 已发现的阻碍

[官方方法](https://explore-education-statistics.service.gov.uk/methodology/school-workforce-in-england)已归档：

- “Size of the schools’ workforce”说明未提供可用数据的学校通过分层缩放估计，故发布人数不是确定完整计数；没有取得该估计的上界。
- “Data sources”明确排除一些原先属FE、现转为academy的sixth-form colleges，名义上的state-funded secondary标签不自动保证学生与教师学校全集一致。
- 多合同教师合并为一个记录，以主合同优先；不能由当前区域/phase标签断言包含所有在目标学校授课者。
- 教师November2024与学生January2025是不同快照，即使属于同一学年，仍需教师总量稳定或变动界。

因此任何模型中的0.843757情景只能称“假定发布教师数为上限”的规划敏感性，不能称新增已识别城市指标。要真正准入，需要校级同ID匹配并界定缺失学校教师总数，或获得直接高中教师统计。

## 复核

extract.py验证原件哈希，筛两London分区与两年级行，核对每年级男女合计等于Total。observation.json保存原始筛选行、精确计数、条件计算和未满足前提。

来源：

- [教师数据集](https://explore-education-statistics.service.gov.uk/data-catalogue/data-set/f3ccc6bf-cc26-46ef-9df0-45bae4cc94ea)
- [当前年级学生数据集](https://explore-education-statistics.service.gov.uk/data-catalogue/data-set/dd0a61a1-6db7-4014-a302-1233b7f32910)

复现：`python3 research/2026-a/data/task4_v35_london/extract.py`。
