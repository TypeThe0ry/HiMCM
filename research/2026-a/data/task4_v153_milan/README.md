# Milan官方地铁站库存原件

市府第0层Stazioni_Metro原响应130条，原ID集合核对完整；市码／comune／municipio筛后109条，按ATM原图5组换乘别名合为104实体。数据日期为元数据注明的2024-10-16，获取时间和原响应哈希见retrieval.json。第3层入口不计，21地理未匹配项省略；WGS84为服务器按outSR=4326返回，未独立叠置市界。地图用于换乘核查，不冒充独立现时站数普查。

extract.py校验全部原件、写retained_line_station_records／retained_hubs／omitted_records／near_pairs四CSV及extraction.json。原件保持，未保存个人信息。完整计算解释与试算在../../results/task4_v153_milan_proposal/README.md；当前主入口仍V136，不能把候选试算写成已启用。指定反防御性写作技能已用于本轮说明。
