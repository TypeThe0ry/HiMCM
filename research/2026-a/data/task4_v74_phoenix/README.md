# V74 Phoenix：学校目录数量差异有了可核验解释

取得三份PXU官方原件：2023-09-07学区地图、2023–24课程目录、当前历史页。原始URL、哈希和字节数见[manifest.json](manifest.json)。它们改善目录覆盖核查，尚不能识别毕业队列的成员归属或全市高中教师分母。

可见地图列24个学校名称，以及25、26号两个支持设施。V42完整Phoenix市界名单列21个PXU NCES行政记录，其中包括Digital和Educator Preparatory；排除Digital后的高中名单为20条。地图额外列出ARCH、Camelback Montessori、Maryvale Gifted & Talented三个项目名称。课程目录PDF第85页明确将Camelback Montessori描述为校内学校；三项目与对应大校同址，但同址本身不能证明全部学生、教师或毕业队列已经并入行政记录。

官方历史页序列化内容记载Educator Preparatory于2023开办、2024关闭。因而21＋3−1＝23，为此前“21个NCES记录与23校宣传介绍”的差异提供了跨年份、不同名称单位的解释。这不是同年度完整队列覆盖证明，也不表示可以从毕业分母任意减去一校。

Educator Preparatory的2023地图地址为3839 W Camelback，CCD2024–25地址为4525 N Central，不能声称全部历史地址一致。CCD的学生数0、FTE为缺失码−1；历史页未给准确闭校日期，不能把缺失教师填为0或据此替换旧年度记录。历史页闭校信息来自HTML中的序列化页面内容，不是静态body正文。

## 必须保留的PDF提取问题

地图PDF存在重叠的旧文字层：文本提取可先读到23个学校与旧支持设施编号，但实际显示的是24校和25/26号支持设施。已由两名agent独立查看渲染页面，采用可见名单人工转录到[catalogue_crosswalk.csv](catalogue_crosswalk.csv)。程序核对转录的21个行政标识与完整NCES集合相等，不将3个额外项目重复计为新行政学校。

`python3 research/2026-a/data/task4_v74_phoenix/audit.py`核验原件哈希、NCES集合、课程目录的校内学校表述、闭校年份和CCD特殊码，输出[summary.json](summary.json)。这部分人工转录可对照原PDF复核；脚本本身不能证明隐藏文字与可见文字的视觉关系。

本轮不修改Phoenix教育[0,1]或通学[0,1]。下一步缺口具体为同届行政队列与项目归属、转学处理、教师岗位分配和全市覆盖；目录数差异本身不再作为唯一障碍。未修改论文。
