# V126：仓库可证明的AI辅助工具使用

仓库回执明确证明 **Exa `web_fetch_exa` 被实际用于官方网页、PDF和开放数据接口的读取／文字提取**。多份记录保存服务名、访问日、来源URL和返回文字；这些记录没有保存Exa内部模型名称或模型版本。因此可据实披露Exa工具使用，不能由此补写某个GPT、Claude、Gemini版本，或断言每一次文字提取都调用了生成式模型。

本次检查截至2026-11-09，范围为研究仓库的provider捕获、提取收据、对应脚本及范围审查。没有读取本地Codex会话史，也没有据已安装软件或可用插件认定实际使用。本文不是完整AI使用史，不能据此声称所有团队成员、全部轮次或所有提示词已完整披露。Codex生成活动及其他成员的服务／模型使用另由会话记录和用户确认补足。

## 可据实填写的条目

| 项目 | 实际记录支持的内容 |
| --- | --- |
| 服务／工具 | Exa；回执通常标为`Exa web_fetch_exa`。IBB记录明确保存完整工具名`mcp__codex_apps__exa_web_fetch_exa`。 |
| 已记录日期 | 下列V116–V120示例为2026-11-08；V124 Tokyo清洁文本捕获的伴随manifest记录2026-11-09。访问日与原统计观测年分开。 |
| 用途 | 读取官方来源，提取可供后续分析的文本；包括市政／运营方设施清单、交通统计PDF、学校旅行调查问卷与CKAN字段投影。 |
| 服务版本 | 未在所核回执中记录；不能以插件安装版本冒充实际服务版本。 |
| 内部模型及版本 | 未在所核回执中记录。服务名和工具名不能充当模型版本。 |
| 输入记录 | 记录包含原URL；部分收据保留完整带参数的请求URL，另有复核说明保留`maxCharacters=20000`。通常没有完整外层工具请求JSON，也没有伴随调用的完整自然语言提示词。 |
| 输出记录 | provider JSON／文本保存返回内容，部分包含`content`、`structuredContent`、`isError`和耗时元数据。这些是工具输出，不能标为原始PDF／HTML响应体。 |
| 核验方式 | 对来源地理、学段、单位与日期作范围审查；用确定性脚本检查设施身份、去重、分母、字段或计数关系；可取得原件时另外保留并核对原件。提取文本与原件的验证强度分别标注。 |
| 记录完整性 | 下面是可核验的使用实例，不是全部调用清单。没有找到的提示词、版本或输出不重建为“精确历史记录”。 |

这些条目支持“使用Exa读取并提取官方资料”的陈述，不支持“Exa生成了论文正文”或“某特定底层模型参与了这些调用”的陈述。仓库普通`web_tool_response.json`记录还能证明网页读取工具输出确实保存过，但不能凭通用文件名识别其模型或额外服务供应商。

## 代表性使用与事实核验

所有下列路径均以本研究仓库根目录为基准。

| 使用实例 | 直接证据 | 实际核验及边界 |
| --- | --- | --- |
| Zurich、Milan公共泳池资料 | `research/2026-a/data/task4_v118_pools/zurich_provider_capture.json`；同目录`milan_provider_capture.json`。两者顶层`provider`为`Exa web_fetch_exa`，`retrieved`为2026-11-08。 | `extract.py`检查7／17个设施名字在捕获文字中、名称去重、原CSV格为空且人口未变，再按固定锚点算下界。这里是清单文字与脚本检查，不是全部设施的独立现场验证；上界保留1。 |
| Zurich、Helsinki交通范围和单位 | `research/2026-a/data/task4_v120_transport/zurich_provider_sources.json`、`helsinki_provider_source.json`、`zurich_stop_unit_definition.json`。 | 同目录`extract.py`从**另行取得的原件**`vbz_facts2025.pdf`第6页读取Zurich市内446、广域235；provider文字用于站点／站台单位定义及Helsinki19／Espoo11分区。原PDF存在不等于所有provider文字均有原件复核。 |
| Istanbul历史调查资料读取 | `research/2026-a/data/task4_v116_ibb/source_audit.json`明确保存工具名、表示类型、资源和逐页投影URL；同目录`provider_*.txt`和`provider_text_sha256.json`。 | 收据和README记录当前在读高中字段与已完成教育字段的区别、分母／权重、重复检查和缺失处理；`verify_aggregates.py`以汇总分布复算界，独立审查位于`task4_v116_ibb_review/`。个体投影仅在内存处理，未保存逐人原始行，不能宣称原始CSV字节可由仓库完整复现。它是历史独立案例，不是主16城新实测资料。 |
| 土耳其议会答复的反向范围检查 | `research/2026-a/data/task4_v116_tbmm/provider_extraction.json`保存provider、访问日、`requested_url`和结果；`task4_v116_tbmm_review/audit.json`记录同工具重复提取及长度参数。 | 范围审查发现政策讨论没有高中年龄／实际旅时分布，未准入；复核记录还明确字符乱码及未完成原PDF视觉核验。重复同一提取服务不等于独立视觉或OCR验证。 |
| Tokyo提取错误被识别后换证据 | `research/2026-a/data/task4_v124_transport/provider_capture.json`；同目录`manifest.json`和`nonadmission_audit.json`。 | 2025体育设施PDF工具文本存在跨行错序，原件403且未恢复可检查页图，计数不准入。最终五场馆下界来自另外下载的9份练马区官网**原HTML**，逐地址去重并核对当前与未来闭馆；见`extract.py`和`pool_venues.csv`。这组原HTML不应反过来描述为该Exa捕获的原件。 |

上述核验是现有脚本／收据记载及本次只读检查所确认的处理规则。本次未运行会改写旧数据的提取脚本，也没有新增独立原件回收或视觉核对的声明。

## 已核对的文件SHA-256

SHA-256核验文件身份和当前保存字节，不能单独证明提取内容与远端原件完全一致，也不能恢复未保存的提示词。下面由本次直接读取文件计算；路径中的`research/2026-a/data/`前缀统一省略。

| 文件 | SHA-256 |
| --- | --- |
| `task4_v118_pools/zurich_provider_capture.json` | `fa7ffcca7f94ad211b78ac3851d8471c1bc6d60fd90c9c8c143a51be6b173100` |
| `task4_v118_pools/milan_provider_capture.json` | `e23c110f00a0c4c88b5114e7d1c0ac23c851915b504d5395c815d24dcbe98279` |
| `task4_v120_transport/zurich_provider_sources.json` | `43ee8ba161a4ca9ff17351d419cfb69d0c907471948aeb5e74bf7c4d753c49e2` |
| `task4_v120_transport/helsinki_provider_source.json` | `3bd2aacb9c259da0c4243a3dc3dda971224e8a9b675bbc1770789abc46e6d6b1` |
| `task4_v116_ibb/source_audit.json` | `f8fa18e2f07b0585115ca02c2e3bcf0154fa2cfbd7bf6e04adfacd5fe329e176` |
| `task4_v116_ibb/provider_text_sha256.json` | `ca8f92344747177ff5f4b9a70c9f36cd589d2bea0f7e1e032e79f5f94d33d624` |
| `task4_v116_tbmm/provider_extraction.json` | `42298306c1ecd1ff6d8ab4c6bb04b4ae068b4e7db751b71a6918102137b4d253` |
| `task4_v116_tbmm_review/audit.json` | `8e38a37873693ae514375b2bbf7fd7204348a6ccb1642ae204e22b630cd6c394` |
| `task4_v124_transport/provider_capture.json` | `864f05c1aa010d9dc334fe2135cee15309b2b2583d4c39e2f5ffad54f0607a28` |
| `task4_v124_transport/manifest.json` | `093e70944c6a1101415ceb3b5323a93fee2335884d3de7d6dceaeb8206fcc31d` |

例如可在仓库根目录运行只读核验：

```bash
sha256sum research/2026-a/data/task4_v118_pools/zurich_provider_capture.json
sha256sum research/2026-a/data/task4_v124_transport/provider_capture.json
```

## 提示词／输出的可交接范围

- 上表provider文件中的返回文本可以按实际保存内容引用；必须仍标明是工具返回，而非模型自由生成答案或原始下载文件。
- `task4_v116_ibb/source_audit.json`的`queries[*].url`和TBMM的`requested_url`是确实保存的输入片段。保留原字段和值即可；不把这些URL改写成据称当时发送的自然语言提示词。
- `task4_v116_tbmm_review/audit.json`保存了长度参数的文字记录，但它不是完整外层调用JSON。其余调用是否存在未归档参数、检索请求或中间结果，当前仓库不能完整确定。
- 查到的证据没有为Exa标出内部模型版本，也没有证明另外使用了ChatGPT网页、Gemini、Claude或图像生成服务。这里的“没有证明”不等同于团队从未使用；完整性仍需用户和会话史确认。

本研究说明按中英文anti-defensive-writing技能及仓库证据规范整理，只新增此说明文件；没有更改provider记录、历史数据、论文或AI报告正文。
