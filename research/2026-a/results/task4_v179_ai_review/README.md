# V179：已核AI取证范围进入自有附录

当前自有稿启用V179。仅替换原AI页的Recovered records and coverage段，并将模型上下文计数28改为74个根会话上下文；其他AI文字、主文、参考文献、图表、科学输入和格式源保持。正文前24页的完整72dpi渲染（含页眉页脚）与V176逐像素相同，仅AI25／26页变化。

新附录明确V178固定窗口截止2026-11-09 14:31:18.850UTC（新加坡22:31），选定可见消息326=6请求+259进度+61答复；工具输入1865=1749custom input+116function arguments，旧125及私存前缀保持。仍排除工具返回、子agent回答、附件、其他会话／队友和窗口后工作，不将工具输入写成成功执行证明，不公开任何私存消息或调用载荷。完整全队AI史仍未成立。

[核验](verification.json)通过：26页=24主文参考+2暂定AI，50引用，主文余量1；新闻18–19、参考20–24、AI25–26不变，Letter／Palatino／12pt正文、11pt原生页眉及空页脚保持。直接与根代理逐页规范化文本相同，改动AI页均130dpi渲染实看；0overfull、2原underfull仍可读。四生成文件字节复现，47项交付清单原状态全部保持，13项实质待办仍在。

187科学文件、623个原论文文件以及全部V178 JSON证据保持；唯一原稿件变动是自有current_review指针。冻结取证验证属于其捕获时点，不能将旧V178依赖V176指针的审计直接当成新稿验收；本轮通过冻结取证哈希与独立审阅绑定新的自有稿。当前复核入口：

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-v120/bin/python research/2026-a/scripts/task4_v179_review_audit.py
```

源稿及build_task4_v179.py在独立Overleaf仓库，主模型／扩展V154保持。未重放无变化MC，未改队友main/ref/class、默认主文件、字体或边距。实际控制号PENDING、全队AI披露、最终共享稿整合、服务器编译和正式提交收件仍待真实证据；submission_ready=false。按既有授权分别普通push，长期goal active。
