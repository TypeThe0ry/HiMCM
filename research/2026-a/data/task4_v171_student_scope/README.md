# V171学生原件与范围核查

城市入口及Mittelschulen下载页重新取得，页面明确Stadt Zürich并链接学生工作簿。工作簿53539字节，SHA与V120完全相同；public SekII6582、private1999和总13426是已在V157保存的旧观测，不能称为本轮新增人数。2024为2024/25学年，未推断精确学生统计日。

student_scope.json保存分组、具体源单元格、公共SPF行、KME全校420及衔接课程，未将它们直接转成高中目标学生下界；需要匹配成人／衔接／远程与项目口径。未准入PTR或效用。

retrieval.json保留四次HTTP200记录与原字节，其中dataset_526_original.html只是1042字节Datenkatalog应用外壳，不作为新元数据证据。目录内容存在不等于取得了其中统计数据。extract.py只读工作簿和实际城市下载页，可复现student_scope.json；不修改旧源。整体方法与验证见../../results/task4_v171_envelope_gate。
