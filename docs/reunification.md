# 恢复单一 HiMCM 仓库 — 2026-11-07

用户撤销此前拆分，要求恢复完整 README，并只保留 HiMCM 一个仓库。研究分支截至 `b0c290e` 的提交历史通过真实 Git 合并保留；论文分支从 `87d646f` 继续，未重写历史。

统一工作目录为 `/Users/hahatt/Documents/ChatGPT/HiMCM 2026/HiMCM`，GitHub 地址保持 `https://github.com/TypeThe0ry/HiMCM`。正文、数据、模型、结果、图库和历史论文均在这个目录中；不再使用独立 HiMCM-research 仓库。

## 内容与完整性

- 恢复拆分前完整 README 的导航、数据说明、目录结构及复现命令，并补充 V16、V17 当前入口；V5/V6 数字明确标为历史快照。
- 研究仓库全部本地文件（含被忽略的生成包和缓存）复制到主仓库。逐文件 SHA256 清单见 [reunification_manifest.json](migration/reunification_manifest.json)，导航文件的有意改写单独列明。
- `main.tex`、`ref.bib`、`mcmthesis.cls` 与合并前主仓库逐字节一致。没有修改在线 Overleaf 文稿。
- 大于 GitHub 单文件限制的可再生 `maps_and_style_guide.zip` 保留本地并继续忽略，其组成资料保留。复制本地文件不代表所有忽略文件已上传。
- 删除独立研究仓库前，须先提交并推送合并历史，核对研究提交已成为主仓库祖先，并完成文件完整性校验。

## Overleaf

HiMCM 仍是原来对应 Overleaf 的 GitHub 仓库。完整研究树超过 Overleaf 的文件数量和推荐同步体积，因此恢复单一仓库不等于修复 Overleaf 在线同步。这里遵从用户的单仓库选择，保留完整数据；不擅自再次拆分，也不声称在线同步已恢复。检查输出保存于 `migration/reunification_overleaf_check.json`。
