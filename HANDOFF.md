# HiMCM 论文整理接力说明

交接日期：2026-11-06（Asia/Singapore）。

## 当前已完成

- 收录 68 篇独立论文：62 Outstanding、4 Finalist、1 Meritorious、1 Honorable Mention。
- 68 篇全部与 COMAP 官方名单中的赛季、队号、题号、奖项核对。
- 2018—2023 六个赛季全部 Outstanding，共 50 篇，已收齐。
- 附有 84 份参考 PDF、来源快照、CSV、可离线筛选的 HTML 索引。
- 记录 SHA-256、PDF 页数、来源、官方名单原文依据和文件路径。
- 官方名单 CSV 仅涵盖可解析行；不可将行数解读为历年完整队伍总数。

## 优先补齐的 Outstanding

以下队伍已有官方获奖依据，但目前没有收到其论文全文。

| 赛季 | 题号 | 队号 | 官方依据 |
| --- | --- | --- | --- |
| 2017 | A | 8028、8040、8206、8393 | [2017 Results](https://www.contest.comap.com/highschool/contests/himcm/2017results.html) |
| 2024 | A | 16159 | [2024 Results](https://www.contest.comap.com/highschool/contests/himcm/2024results.html) |
| 2024 | B | 15022、15502、16226 | 同上 |
| 2025 | A | 16390、16486、16603、16843、17401 | [2025 Results](https://www.contest.comap.com/highschool/contests/himcm/2025results.html) |

更早年份与其他奖项仍有大量缺口。`获奖论文缺口清单.csv` 中的「未找到公开全文」仅表示本次尚未取得，不代表论文一定公开，也不表示已穷尽所有网络来源。

## 已定位的来源

- [COMAP 历年比赛索引](https://www.contest.comap.com/highschool/contests/himcm/previous%20problems.html)：官方获奖核对的入口。
- [公开论文合集](https://beldore.club/competitions/papers)：已取得其中 55 篇 HiMCM。
- [adithyabsk/himcm](https://github.com/adithyabsk/himcm)：2016 A题 7059，Finalist。
- [UhanWu/Math-Modeling-Papers](https://github.com/UhanWu/Math-Modeling-Papers)：2021 A题 11727 Meritorious；2022 A题 13057 Honorable Mention；2023 B题 13849 Finalist。
- [IMSA 2016 Outstanding 元数据页](https://digitalcommons.imsa.edu/math_sw/5/)：公开下载端点本次返回403，未收录全文。可从机构或作者其他公开入口继续找，勿把元数据页当成已下载论文。
- [Consortium86](https://lebailly.github.io/pdfs/Cons86.pdf)：2004年出版，包含2003赛季获奖论文节选；已归入参考资料，不计入68篇独立论文。
- [COMAP 会员资源](https://www.comap.org/membership/member-resources/)：部分历史论文和评委点评需要 Mathmodels 会员。没有现成授权时仅记录入口，不绕过访问限制。

## 已纠正的标签

1. 用户原文件 `2026O奖1/2/3.pdf` 分别对应 **2025 B题** 16738、16739、16442，均为Outstanding。原文件名保留，分类采用论文摘要页与官方名单年份。
2. 用户原文件 `f奖1.pdf` 为 **2025 B题 17372 Finalist**，首页是扫描图，已使用OCR识别队号并核对官方名单；`f奖2.pdf` 为 **2025 B题 16742 Finalist**。
3. 公开合集将2017年已下载的五篇论文题号标反：8121、8124、8201应为B；7359、7879应为A。仓库已经纠正，来源URL中的原始A/B路径保持不变。
4. `15041.pdf`、`15504.pdf`、`15926.pdf`、`14995.pdf` 都是2024 A题Outstanding。
5. 用户2023 O奖ZIP中的九份论文，与合集中的九个队号相同，未重复计数。不同字节版本见重复文件对照，原件仍保留。
6. `2025_HiMCM_Article.pdf` 是总结与评委文章，不是独立参赛论文。

## 新增资料的流程

1. 先查看 `论文总目录.csv` / `论文清单.json`，按「赛季 + 队号」判断是否已有。
2. 下载到临时位置，确认内容是可打开的PDF，而非HTML错误页；从首页或OCR识别赛季、题号、队号。
3. 在官方获奖名单中逐队核对，保存名单URL及证据原文。只有文件名或作者自述时，先放入待核实目录，不能标记为已核实。
4. 核实后保存为 `论文/年份/奖项/题号/HiMCM_年份_题号_奖项_队号.pdf`；更新CSV、JSON、HTML索引、年份覆盖、缺口清单、README统计。HTML索引内嵌了JSON数据，新增时也需同步。
5. 同队不同文件版本保留原件及对照，独立论文数量只增加一次。期刊节选不能冒充完整论文。
6. 核对SHA-256、页数、所有本地链接，再更新Release压缩包。未来的压缩包也应包含最新JSON与接力说明。

## 未成功下载的资料

具体URL及错误在 `下载来源及失败记录.csv`。

- 官方页面链接的2000、2007、2008、2009结果PDF本次返回404；对应官方HTML结果页快照保留。
- 2017 B题的两份赛题附件经 Mathmodels 重定向后连接超时，未计入已下载资料。
- IMSA 2016论文下载端点返回403。

## 本次检查

68份归档论文均成功解析，页数及SHA-256与清单一致；84份参考PDF可解析；论文目录指向的PDF及官方名单文件均存在；首版ZIP通过完整性检查。

下一步建议先查找上表13份Outstanding的学校或作者公开版本，再扩展较早年份。取得会员访问授权或新的用户文件后，可据此继续补齐。
