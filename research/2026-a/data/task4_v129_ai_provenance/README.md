# V129：延长已核验的本任务AI记录

本次把同一任务的可核验选集从52条扩至66条，新增12条可见进度消息和2条完整可见答复。原V126前缀及其52条记录逐字节保留；新前缀截止 **2026-11-08 19:10:12 UTC**（新加坡11月9日03:10:12）。这提高了已保存局部记录的覆盖范围，没有补造全队历史。

[session_manifest.json](session_manifest.json)记录新前缀的51,288,059字节、4,343个完整行及SHA-256。13个已记录根任务turn context均标为`gpt-6.1-sol`，客户端标为`0.166.0-alpha.5.1`；这些是实际日志标签，不是固定服务构建或所有子agent模型的证明。66条选集包括4条真实用户请求、53条进度消息、9条完整可见答复。

[verification.json](verification.json)独立核对源行身份、模型标签、消息角色、可见阶段、原文文本及导出记录哈希；同时核对旧52条清单完全一致，V126原回执、V127注册表、准入和冻结主输出均未改动。可见文本只写入仓库外的`/data/scratch/himcm_v129_ai_provenance/visible_records.jsonl`，目录权限700、文件600；两个Git仓库均只保存元数据及验证回执。

复现使用原提取器和新增的连续性验证器：

```sh
.venv-v120/bin/python research/2026-a/scripts/task4_v129_ai_provenance.py \
  --session /root/.codex/sessions/2026/11/08/rollout-2026-11-08T22-50-21-01a1bba3-8ac1-7963-90bf-08d8c2fec116.jsonl \
  --private-output /data/scratch/himcm_v129_ai_provenance
```

已有回执时默认重放同一字节截止点；不会因会话增长静默扩大本版本。该选集仍排除推理、内部指令、工具载荷、附件和其他会话，因而不覆盖工具调用中的生成代码／论文文字、subagent会话及其他队员使用。它不能替代比赛要求的最终完整AI使用报告；V128完整稿继续准确声明其原V126截止范围，新证据另附支持材料。
