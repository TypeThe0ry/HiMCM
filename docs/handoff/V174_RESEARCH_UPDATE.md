# V174：当前自有稿与16城的独立复现入口

当前论文仍V173、科学／扩展V154。新增研究scripts/task4_v174_reproduce.py，当前注册表／PDF身份绑定、585论文tracked路径及Git blob/工作文件完全匹配后，归档到两个独立临时源码副本。删除对应旧PDF和TeX辅助文件，各用全新outdir和--only-cached构建direct/root代理，不依赖旧scratch产物、不下载或回退。

最终实际运行通过：两入口26页逐页文本及全部72dpi灰度PGM与注册PDF相同，Letter／原生页眉空页脚、main-end24/news18–19／49引用核验；160格和32固定／等权城市案例独立复算一致，Zurich保守、16可能／0必要。187科学／585已有论文文件及两Git状态保持。八异常guard临时fixture测试通过，非真实论文数据；第一轮配置失败明确保留，未与成功混记。

[完整说明和命令](../../research/2026-a/results/task4_v174_reproducibility/README.md)、[复现回执](../../research/2026-a/results/task4_v174_reproducibility/rebuild.json)、[核验](../../research/2026-a/results/task4_v174_reproducibility/verification.json)。需当前科研Python环境、Git／Poppler／Tectonic及已有TeX缓存；输出必须仓库外新建／空目录。可信哈希源码的常规编译不是系统沙箱；只证明本地所列条件下文本／版式及确定性结果可复现，不证明冷缓存运行、在线编译、原始来源全面重审、MC重放或最终提交就绪。

论文／当前稿注册指针、队友main/ref/class、默认主文件设置保持。0新数据0评分收窄；本轮改善是可执行、无旧辅助文件依赖的复现流程。私有Overleaf只新增独立回执与说明，公开研究push仍待既有选择，长期goal active。

私有Overleaf常规push已确认：`5547de0295fc786141320f50f0132805f2a287d0`，仅五个新增复现支持文件、原585文件保持，工作区干净且HEAD=origin/main；实际重建所测试源码HEAD仍为`0adb8478baddb2894f98943820f23a6b801de0ed`。见[同步](../../research/2026-a/results/task4_v174_reproducibility/sync.json)。
