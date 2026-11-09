# V178：扩展实际根会话AI记录，并保留工具内生成文本

当前根会话的完整行取证窗口从V140的2026-11-09 03:17 UTC延长至14:31:18.850 UTC，即新加坡时间11月9日22:31。固定前缀266948392字节、17669完整行；旧125条选集和其私存字节前缀保持。新选集为326条：6条按规则选定的真实请求、259条可见进度、61条完整可见答复，比旧选集增加201条。统计不是全部用户输入，也不是模型独立实验次数。

新增私存1865条根会话工具调用输入：1749条custom_tool_call的input和116条function_call的arguments。在这一根日志和截止范围内，调用字符串中出现的生成代码、LaTeX及提取指令有了原文保留；旧记录只保留可见消息，没有覆盖这一部分。它们是当时记录的助手输入，不证明每个调用成功，也不证明exec包装中的每个嵌套工具都实际执行。工具输出、子agent回答及其他会话不属于本次导出。

74条根会话turn_context均记录模型标签gpt-6.1-sol。会话起始元数据记录Codex Desktop／CLI0.166.0-alpha.5.1；这些标签不证明不可变服务构建、每个工具内部的模型或所有并行agent使用同一模型。摘要见[capture_summary.json](capture_summary.json)，完整公开元数据和逐记录哈希见[session_manifest.json](session_manifest.json)。公开清单不包含导出的消息正文或工具输入正文。

## 私存与复核

实际选定文字与工具输入分别私存在仓库外`/data/scratch/himcm-ai-v178/visible_records.jsonl`和`assistant_tool_arguments.jsonl`，163285／3300240字节。目录0700、文件0600；不入GitHub或Overleaf，不作为已经审核的提交记录。原始根日志也未复制进仓库。来源哈希、行号和导出记录哈希将公开清单与本机私存原件绑定，团队可据此审查实际查询和输出。

生成器只投影选定可见text_parts与明确的明文arguments/input字段；排除推理／analysis、system/developer消息、加密字段和内部元数据、工具返回结果、附件、注入goal／环境、未选中的回复封装、其他会话和队友资料。工具输入字符串自身可含粘贴文件或指令，所以仍按私有内容保管；这里没有声称私存字符串在语义上从不出现system等词。

生成采用固定完整行截止，重放不自动扩到新日志尾；既有冻结源哈希改变则拒绝，私存路径不能在两仓库内或祖先处，也不能覆盖另一捕获。先写0600临时文件，完成源身份／旧前缀／选集核验后再替换正式私存文件；校验失败会清理临时件并保留既有私存和公开清单。

实际复现需要对应本机根日志：

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-v120/bin/python research/2026-a/scripts/task4_v178_ai_provenance.py \
  --session /absolute/path/to/this-root-session.jsonl --private-output /data/scratch/himcm-ai-v178
PYTHONDONTWRITEBYTECODE=1 .venv-v120/bin/python research/2026-a/scripts/audit_task4_v178_ai_provenance.py \
  --session /absolute/path/to/this-root-session.jsonl --private-output /data/scratch/himcm-ai-v178
```

[独立核验](verification.json)重新流式读取固定前缀，逐条比较326可见记录、1865调用输入、74模型上下文及全部公开索引／哈希。29个合成过滤案例与2个实际入口失败重放案例通过：错误根会话与写出后触发的旧前缀错误均不覆盖正式记录；合成测试不是论文数据。187科学／621已有论文文件、3个旧V140元数据文件和三个当前注册表／PDF保持；未重放MC或编译未改稿件。

## 对当前论文的作用

这补充了本根会话的新证据窗口和工具内文本，不等于完整全队AI使用报告。仍缺工具返回内容、其他会话／队友记录及后续截止之外的工作，不能重建缺失提示或凭标签猜模型。当前V176自有AI页仍描述旧03:17窗口，本轮没有改论文；下一轮应只更新自有AI记录段，并验证主文／参考内容保持。实际注册控制号、全队确认及正式提交仍未完成。

科学／扩展V154、论文V176、50引用和原生页眉空页脚保持；0新数据、0评分变化，Zurich保守／16可能／0必要。按既有授权分别同步研究与选定私有论文支持，长期goal active。
