# Stockholm：13处现行市营游泳设施下界

市政府[现行总览](https://motionera.stockholm/trana-gymma-simma/)称有13处simhallar。[逐名清单](https://motionera.stockholm/trana-gymma-simma/simhallarna/)列14处，其中Vällingby明确装修关闭；其余13处名称唯一，分布在Innerstaden、Söderort和Västerort。Nälstabadet为装修期间全年开放的替代设施，计一次；每处设施含多少水池不重复累加。

2026年1月市政府发布的新闻稿仍称14处，与当前开放设施清单不同，因此不采用旧新闻稿的14。原网页HTML以下载字节归档，访问日2026-11-08；网页页脚更新时间2025-06-18不等于库存观测年，不据此重建2025状态。

用户CSV人口999200（2025）不变，只补原本缺失的泳池密度。13处/固定人口给每10万人1.3010408处，原锚点1下效用为[0.5654141,1]。这是市营公开设施子集，未证明全运营者覆盖；其余供给保留未知，上界仍1。设施供给不能直接解释青少年使用或街区公平性。

在仓库根运行 `python research/2026-a/data/task4_v121_pools/extract.py`，会独立核对当前总览、逐名清单、关闭项、原CSV缺失状态和固定人口，生成候选观测、逐名列表、提取文本和SHA256清单。
