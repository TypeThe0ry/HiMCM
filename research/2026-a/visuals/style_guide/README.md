# 配图风格指南入口

[全部 guideline 与当前字号／证据标准](../GUIDELINES.md)。PDF 手册已同步最终 9 pt 文字标准；统一指南补充多源地图、证据表达与缩放验收。

- [图文指南](index.html)：地图优先，按用途解释具体获奖原图的可借鉴部分。
- [完整中文规范](STYLE_GUIDE.md)：制作参数、数据边界、地图检查与图注模板。
- [PDF手册](style_guide.pdf)：15页，保留原图例与队号、PDF页码，可离线传阅。
- [全库分类检索](catalog.html)：68篇、998候选页，支持队号/关键词/类别过滤。
- [分类CSV](page_style_index.csv) / [分类JSON](page_style_index.json) / [分类方法与数量](classification_summary.json)。
- [精选参考卡](reviewed_reference_cards.json)：具体出处与选择理由。

分类是页级、多标签图题规则，不是对998页全部做了人工图像识别或审美判断。727页暂未匹配到图型，保留为未分类；19个精选参考页有人工视觉核对标记。一页可能包含多图，不把页数称为图片数，也不把Outstanding、Finalist统一说成O奖。

`build_guide.py`从既有参考图库重建全部文档与索引，检查998条唯一页记录、来源、图片和HTML相对链接。仅写本目录，不修改论文正文和原始输入。PDF使用嵌入并子集化的字体。
