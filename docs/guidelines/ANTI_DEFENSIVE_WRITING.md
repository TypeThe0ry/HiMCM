# 必须使用的反防御性写作技能

用户于2026-11-08明确要求安装并在后续HiMCM论文和材料迭代中必须使用此技能。

- 上游：[Adkid-Zephyr/anti-defensive-writing-Skill](https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill)。
- 已核对并安装的提交：`82d31402caa0db1790026824399044538483171b`。
- 中文安装名：`anti-defensive-writing`；英文安装名：`anti-defensive-writing-en`。
- Codex安装位置：`$CODEX_HOME/skills/<安装名>/SKILL.md`，默认Codex home为`~/.codex`。首次自动发现从下一次对话消息起生效；当前工作已直接读取安装文件并应用。
- 研究仓库可移植副本：[中文](../../research/2026-a/visuals/guidelines/anti-defensive-writing/zh/SKILL.md)、[英文](../../research/2026-a/visuals/guidelines/anti-defensive-writing/en/SKILL.md)。安装文件与仓库快照逐字节一致；MIT许可证随快照保留。

## 执行方式

1. 开始一轮写作或编辑时读取相应语言技能，并明确本轮要支持的中心判断及其证据。
2. 按判断、证据、含义组织段落，突出可验证的贡献；采集日志及复现细节留在支持材料。用户要求的数据搜集章节保留具有解释作用的真实采集案例。
3. 保留会改变结论的条件及反例：16城仍可能夺冠、保守推荐与确定冠军的区别、偏好改变推荐、VIKOR对照分歧、混合年份与人群、设施供给和实际可达性的区别。
4. 文字编辑不改变城市、指标、权重、锚点或缺失界；模型或证据修订须单独记录、重算和验证。AHP情景及未来模拟保留真实的来源与假设标签。
5. 仅在获授权的稿件范围内编辑，保留队友正文；涉及PDF时重新编译并检查最终版面。完成后分别审查两个仓库的diff，再正常commit/push。

原始上游技能保持不改写。本项目的证据要求、用户明确约束及稿件权限在执行中一并适用。

## 安装复现

使用Codex自带`skill-installer/scripts/install-skill-from-github.py`，参数：

```text
--repo Adkid-Zephyr/anti-defensive-writing-Skill
--ref 82d31402caa0db1790026824399044538483171b
--path skills/anti-defensive-writing skills/anti-defensive-writing-en
```

已安装目录存在时先比较版本和内容，保留本地改动；不要直接覆盖或删除。新环境没有全局技能时，可先按仓库内快照执行，再补全安装。
