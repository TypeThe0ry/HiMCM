# Copenhagen：实际查询界面确认市级筛选需合作方权限

2026-11-07在官方Transportvaner工具进入`Ture`页面，页面已加载TU0625v1数据及人员、行程筛选。`Bopæl`公开下拉框标为`Region`，其说明明确写有：`LOG PÅ PARTNER-VERSION FOR FILTRERING PÅ KOMMUNE`，即按市镇筛选需登录合作方版本。

这补足V38仅有变量字典、尚未核验网页功能的缺口。完整字典包含当前高中生`RespPrimOcc=116`和居住市镇代码，但不能据此断言这些字段在公开查询层均可使用。没有登录、申请权限或以首都大区值替代Copenhagen市。

公开界面默认统计六岁以上人群2016年以来的全部行程，不是已筛选的高中通学结果。本轮未复制该默认数值进模型；Copenhagen通学仍[0,1]。

来源：[Transportvaner](https://transportvaner.dk/)，实际已加载的PowerBI页名`Ture`，`Bopæl`筛选说明。核验方式：浏览器可访问树与屏幕检查；本目录为界面审计记录，不是原始微数据。
