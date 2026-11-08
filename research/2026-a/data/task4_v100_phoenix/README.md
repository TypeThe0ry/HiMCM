# Phoenix：2023/24 CRDC 是新的同年师资数据路线，尚未取得观测文件

本轮定位美国教育部已公布的[2023–24 CRDC 公共数据发布页](https://www.ed.gov/laws-and-policy/civil-rights-laws/civil-rights-data-collection-crdc/civil-rights-data/civil-rights-data-collection-crdc-2023-24-school-year)，并取得官方资源社区的学校调查表和数据项目清单原件。它提供学校教师FTE这一实际采集项目，值得用于追查[V85同年CCD](../task4_v85_phoenix_public/README.md)中的104条缺失学校师资记录，其中60条为已有名册定义下的纯高中学校。**本轮取得的是原始调查工具，新增教师观测仍为0。**

## 已核验的定义

学校调查表PDF第61–63页的STAF-1要求报告整个2023–24正常学年的教师，排除暑期及学期间短期课程；范围为学前、K–12及相当的无年级教育。单位为岗位分配FTE，保留两位小数，不能用STAF-5a按种族／性别记录的教师人数替换。即使学年相同，也须核对其整学年口径与CCD参考时点的差异。

该表没有直接给出高中阶段专属FTE。混合学段学校仍需保留分配区间；不能因老师任职于含高中学段的学校就全部归入高中。第61页明确未知或未收集应留空，只有已收集且数值确为零才报零。公开使用文件的保留代码、学校ID交叉表和实际披露内容仍需另行核验，调查表本身不能证明公开数据没有抑制。

## 当前下载结果与下一步

官方数据门户在普通Chrome和直接请求下均返回403。公开研究下载器给出的ZIP入口为 `https://civilrightsdata.ed.gov/assets/ocr/docs/2023-24-crdc-data.zip`，本轮请求返回403及919字节HTML，没有ZIP原件。另一个官方主页 `ocrdata.ed.gov` 同样返回403。没有绕过访问限制；[访问记录](access_checks.json)将这些失败与成功取得的PDF区分。

[Urban Institute公开文档](https://educationdata.urban.org/documentation/schools.html)的教师／工作人员端点当前只列2011、2013、2015、2017、2020、2021年，因此未用2021年替代2023/24缺失值。下一步应取得真正的2023/24公共使用学校工作人员、学校特征文件及代码手册，再以稳定NCES ID对104校逐一核对。先处理60所纯高中候选，可以减少学段分配缺口；还须解决参考期、岗位、学校覆盖与私校非响应后才可建立全市指标。

[PDF原件与哈希](manifest.json) · [审计结果](audit.json)。运行 `python3 research/2026-a/data/task4_v100_phoenix/audit.py` 核验原件、STAF定义及既有缺失名册哈希。主模型、区间和论文未修改。
