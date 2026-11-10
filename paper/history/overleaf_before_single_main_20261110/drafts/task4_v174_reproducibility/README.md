# V174：在独立临时副本中复现当前稿与16城确定性结果

新增一个可运行入口，验证当前注册的V173自有稿不依赖旧TeX辅助文件或本机特定scratch路径。在指定本地工具和已有TeX缓存下，两个独立副本均完成只用缓存的重建，26页逐页规范化文本及全部72dpi灰度PGM与注册PDF一致；160效用格和32个城市／权重案例经独立公式复算一致。论文、原始数据、权重和科学版本保持。

## 运行

从当前研究工作区运行，选择仓库之外、尚不存在或为空的输出目录：

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-v120/bin/python research/2026-a/scripts/task4_v174_reproduce.py \
  --output-dir /data/scratch/himcm-current-review-rebuild
```

如论文仓库不在相邻HiMCM-Overleaf，可用`--paper-root /absolute/path`指定；研究仓库位置可用`--research-root`指定。不能把输出放在两个仓库内部／祖先目录、已有非空目录或指向仓库的链接处，也不会自动删除旧输出；再次运行请使用新的空目录。

依赖当前研究Python环境中的NumPy、pandas、SciPy、Matplotlib，以及Git、Tectonic和Poppler。实际验证使用Python3.11.18、NumPy1.26.4、pandas2.3.1、SciPy1.13.1、Matplotlib3.9.2、Tectonic0.17.0；Poppler版本及完整命令见[rebuild.json](rebuild.json)。Tectonic必须已有所需资源缓存：`--only-cached`缺资源就失败，无下载或旧PDF回退。环境名称v120只是既有环境名，模型入口严格取当前16城V154注册表，不运行旧25城主程序。

## 检查范围

- 先绑定两个仓库的当前审阅注册表、注册PDF SHA及当前核验身份；验证187项科学快照。
- 用Git HEAD归档论文；逐路径、Git blob及当前工作文件字节核对，拒绝export-ignore／export-subst导致的差异、links／gitlinks和LFS指针。
- direct与root代理各用独立源码副本和全新outdir，删除副本中的当前旧PDF及TeX辅助产物，保留图形PDF作为输入。原始仓库不修改。
- 两入口必须实际产生新PDF，逐页对照规范化文本、26页Letter尺寸、主文／新闻／引用标签、原生页眉空页脚及72dpi灰度页面。PDF元数据可使二进制SHA不同；不要求两份PDF字节一致。
- 科学侧读取已注册factory重建160格，用平方加权距离及显式自排除竞争者独立复算固定／等权的32城市案例，核分数、遗憾、排名、可能／必要冠军。两种权重仍Zurich保守、16可能／0必要。
- 正常异常路径也执行输入保护检查；报告保留明确失败，不把失败当作通过。最后核187科学文件、585个既有论文文件及两仓库Git状态保持。

验证采用可信、完整且哈希匹配的论文源码常规编译，不是系统安全沙箱。每个作业的log、bbox、标签和渲染均在本次生成。`dependencies.mk`保留引擎输出的逻辑路径，仅作诊断，不把它当成可直接重放的Makefile或额外的实际文件访问证明。

## 已执行的证据

[verification.json](verification.json)汇总当前代码哈希；[rebuild.json](rebuild.json)绑定测试时的paper HEAD `0adb847`、当前V173 PDF身份和工具版本。[guard_checks.json](guard_checks.json)的8个异常测试覆盖PDF身份不符、输出在仓库内／祖先／非空目录／符号链接，以及三种异常Git归档；另有当前PDF身份的正例。所有异常都在临时合成fixture中测试，不是论文数据。

异常测试可单独运行：

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-v120/bin/python research/2026-a/scripts/audit_task4_v174_guards.py \
  --output-dir /data/scratch/himcm-current-guard-check
```

[initial_failed_attempt.json](initial_failed_attempt.json)保留最初配置失败：额外启用untrusted模式会屏蔽原构建的父目录搜索，导致找不到实际存在的mcmthesis.cls。随后恢复可信源码的标准编译方式，同时继续强制only-cached，最终运行通过。失败与通过记录分开，不汇总重复运行数充作独立实验。

当前代码另经独立agent只读审查。成功构建的log、aux和依赖规则保留在direct／root目录；生成的验证PDF及bbox在外部输出目录。当前V173原稿未重新发布为新版本。

## 结论边界与同步

这证明在已记录本地工具与已有缓存条件下，当前注册自有稿可从干净副本重建其文本和已检查的版式结构，并复核确定性结果。不证明无工具／无缓存的新系统能直接运行、Overleaf服务器已编译、全部原始观测已重新核实、MC已重放或最终比赛提交就绪。

科学及扩展V154、论文V173保持：0新准入、0评分收窄，24主文参考+2暂定AI，现有14个最终交付待办不变。私有Overleaf只同步选定复现回执与说明，公开研究push继续待既有选择，长期goal active。
