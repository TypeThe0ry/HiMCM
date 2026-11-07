# Athens：校级学生数据入口已定位，完整数据下载未成功

本轮新增模型观测0。希腊教育部在data.gov.gr公开的学生校级表和学校目录，提供了进一步核对Athens市范围的具体入口；目前未取得完整原件，不能计算市级学生数或师生比。没有用Attiki区域比率代替Athens。

## 已获得的资料

- [学生表元数据投影](minedu_students_school_metadata.json)：`minedu_students_school`，包含官方CSV及ZIP稳定下载URL。CSV预期8722830字节，`datastore_active=false`。
- [学校目录元数据投影](minedu_schools_metadata.json)：`minedu_schools`，包含官方CSV及ZIP稳定下载URL，`datastore_active=false`。
- [教师资料原始元数据响应](teacher_metadata.json)：官方说明明确为**私立**小学及中学学校教职人员、按学校类型统计。不能把它当作公私立合计的完整教师上限；XLS资源仍指向旧页面，ZIP资源URL为`dummy-value`。

前两项是明确标记的元数据字段投影，省略操作缓存和临时签名重定向；第三项保留官方响应原始字节。[来源与哈希](manifest.json)记录各自性质。2026年的目录更新时间不证明学生观测发生在2026年，未读取完整数据前不指定观察年份。

## 下载结果与剩余缺口

学生CSV曾实际接收数据并持续运行，最后明确退出为`IncompleteRead`：收到3456385字节，仍缺5266445字节。学生ZIP和学校目录ZIP分别以读取超时退出。本轮没有保留不完整内容作为CSV/ZIP原件，也没有将工具等待超时误判成下载失败；结论依据下载进程的终止错误。

尚需取得完整学生记录、同年学校地域目录，完成城市范围和高中类别识别，再匹配同年兼容范围的教师资料或完整教师池上限。本轮没有实际完成市级连接、年龄筛选、高中师生统计或通学数据提取。[结构化审计](source_audit.json)保留这些边界。

复核：`python3 research/2026-a/data/task4_v74_athens/audit.py`。脚本检查三件已取得元数据的哈希及私立教师范围，同时确认不存在被误当完整原件的下载文件。
