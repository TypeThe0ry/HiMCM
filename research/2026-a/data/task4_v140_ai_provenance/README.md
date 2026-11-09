# V140：同一任务可核验AI选集66→125

完整行前缀扩至110005812字节、6542行，截止2026-11-09 03:17:15.271 UTC；SHA为6791749513f650f37d86ef79cdadc3fdc88e78f9d1de37066842bef9e3d7a75e。125条选集由4条真实请求、99条可见进度和22条完整可见答复组成，比旧66条增加59条。28个已记录根任务turn context的标签均为gpt-6.1-sol，客户端0.166.0-alpha.5.1；不能据此确定服务构建或所有子agent的模型。

原V129的66条清单是本选集逐字节相同的前缀，V126及V129旧记录保留。独立核对源行身份、角色、可见阶段、原始文本、模型标签与每条导出哈希；原CSV、V136快照、55扩展输出及捕获时11份论文入口前后保持。私有目录在写入前设为0700并采用umask077，文本文件0600，只在/data/scratch/himcm_v140_ai_provenance/visible_records.jsonl。两个仓库只存元数据／回执，不存私有原文。

已有manifest时重放相同截止字节，不因会话继续增长扩大本版本。已有原verification时另写recheck_verification，保留初始回执；已实际重放并确认前缀／125条记录不变。初始论文哈希对应捕获时V139，recheck对应后续V140文档，均为各次前后保护，不冒称所有历史捕获对应同一PDF。

复现：`.venv-v120/bin/python research/2026-a/scripts/task4_v140_ai_provenance.py --session /root/.codex/sessions/2026/11/08/rollout-2026-11-08T22-50-21-01a1bba3-8ac1-7963-90bf-08d8c2fec116.jsonl --private-output /data/scratch/himcm_v140_ai_provenance`。

这仍是一个根会话的选定可见消息，排除推理、内部指令、注入上下文、工具载荷、附件、其他会话和其他队员。不能覆盖工具调用中生成的代码／论文或所有AI输入输出，不能替代最终完整团队AI报告。私有导出未经队伍核对不发布／提交；论文继续明确incomplete review record。
