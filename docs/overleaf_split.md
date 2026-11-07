> 历史记录：此拆分方案已按用户要求撤销。当前只使用 HiMCM，见[合并记录](reunification.md)。下文描述当时操作，不是当前目录要求。

# Overleaf 仓库精简 — 2026-11-07

HiMCM 保持论文主仓库与原 GitHub 地址。研究材料迁入 [HiMCM-research](https://github.com/TypeThe0ry/HiMCM-research)，保留完整 Git 历史和工作区未提交的研究资料；后者按迁移快照提交，并不表示 V8 研究已经完成验证。

迁移前完整本地快照逐文件 SHA-256 校验：2,194 文件，1,346,494,332 字节。完整清单在研究仓库 `docs/migration/overleaf_split_manifest.json`。源文件另外移入相邻 `_local_archive/overleaf_split_20261107/`，可以恢复。

主稿 `main.tex`、文献 `ref.bib` 与模板 `mcmthesis.cls` 不变。原稿有 21 个原始配图引用，其中 17 个在去除注释后有效，均在迁移前已缺失。缺图影响本地完整编译；本次没有用研究图替换正文图。在线项目可能另有图文件，应保留并核对后同步。

研究库的生成包 `maps_and_style_guide.zip`（109,741,560 字节）保留于本地，因超过 GitHub 单文件限制而不入库；组成文件保留。主仓库历史不重写，因此 `.git` 和历史下载仍大，本次精简的是供 Overleaf 使用的当前文件树。

[Overleaf 官方限制](https://docs.overleaf.com/getting-started/free-and-premium-plans/plan-limits)：项目最多 2,000 文件；Git/GitHub 同步建议低于 100 MB；100 MB 不是项目硬性总容量限制。使用 `scripts/check_overleaf_size.py` 检查已暂存文件。

在线检查：当前浏览器两个打开的 Overleaf 项目均显示仅项目所有者可以建立 GitHub 关联，因此本次不声称已完成在线拉取。GitHub 主仓库地址保持不变；项目所有者应核对正确项目及在线未同步内容后重试。
