# V60 — Phoenix公开TRP材料的人群核验

本轮取得两份PXU官方2024–25原始PDF，均明确发给区内员工，支持员工通勤减排与激励安排。两份文件均没有高中生通学时长、学生回应分母或学生Summary Analysis。新增可准入高中生通学观测为0，Phoenix缺失区间保持原样。

- `pxu_amu_letter_2024_25.pdf`：AMU激励及校园协调员表，对象为Phoenix Union Employees，登记的是上班采用替代方式的员工。
- `pxu_welcome_letter_2024_25.pdf`：员工乘车保障、公交卡等安排，对象同样为员工。
- `manifest.json`保存原始URL、获取时间、字节数与SHA256；同名txt是pdftotext派生文本。运行`python3 audit.py`核验原件及对象。

公开搜索覆盖Phoenix Union、Brophy、Saint Mary的TRP/Travel Reduction/Trip Reduction、Summary Analysis及通学分钟。未取得学生实际时长汇总。搜索命中的2025-06-10 Maricopa议程只列Brophy为Employer Plans条目，没有学生统计表。未进入账号、联系协调员或申请非公开数据。

另外发现州图书馆收录的2004–05县TRP年报搜索索引提及学生平均15分钟。原页读取403，故仅列作未核验线索，未保存为原件或填入模型；县级历史调查也不能自动代表当前Phoenix高中生。检索记录见`search_audit.json`。不能从本轮检索失败推断该数据不存在。
