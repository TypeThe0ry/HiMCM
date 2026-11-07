# HiMCM — 论文主仓库 / Overleaf

本仓库保留论文正文、文献、模板、实际使用的成稿配图和团队规范，继续作为 Overleaf 对应的 GitHub 主仓库。

- `main.tex`：主稿；`ref.bib`：参考文献；`mcmthesis.cls`：模板。
- [团队规范](GUIDELINES.md)：写作、证据、制图和交付要求。
- [研究仓库](https://github.com/TypeThe0ry/HiMCM-research)：原始数据、模型代码、迭代结果、历史论文与参考图库。新研究工作在相邻的 `HiMCM-research` 目录进行。
- [迁移记录](docs/overleaf_split.md)：校验、保留范围与同步状态。

运行 `python3 scripts/check_overleaf_size.py` 检查当前 Git 索引准备提交的文件数及大小。研究文件夹已从主仓库迁出；仅对新文件设置 `.gitignore` 无法精简已跟踪文件。最终采用的图表按正文引用路径复制进本仓库，勿复制整套图库。

Overleaf 仍是主稿权威工作区。拉取或推送前核对在线更改；保持正常快进历史，不强推。此次仅精简仓库，正文、文献和模板字节未变。
