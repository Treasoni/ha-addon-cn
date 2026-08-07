# ha-addon-cn 领域术语

本仓库是一个 Home Assistant Add-on 中文商店：仓库根目录即商店，各 add-on 目录由上游源镜像而来，README 即中文使用指南。

## Language

**add-on 商店**:
仓库根目录即一个 HA Add-on 商店，`repository.json` 定义商店元数据，各 `{slug}/` 目录是一个 add-on。
_Avoid_: 插件库、仓库商店

**vendored add-on**:
从上游源镜像进本仓库的 add-on，`source: alexbelgium | official | frenck`。同步脚本可更新其除 README 外的文件，但不覆盖本地 README。
_Avoid_: 上游插件、第三方插件

**source: local**:
用户自有的 add-on。同步脚本永不触碰、永不删除。
_Avoid_: 自建插件、本地插件

**中文指南**:
add-on 的 `README.md` 本身即中文使用指南，通过首部标记识别，HA 详情页直接渲染它，因此不另建独立中文文件。
_Avoid_: README_zh、中文说明文件

**审校**:
审校子代理对照 add-on 配置声明核对中文 README、直接修复并留下学习记录的语义核对流程。
_Avoid_: 校对、复核、审核

**结构门禁**:
对中文 README 做的确定性校验，是质量管线的第一道、也是复验用的关卡。
_Avoid_: lint、静态检查

**desync**:
磁盘 README 已含中文指南标记但商店清单仍标注缺失的不同步状态。此时不重写，仅翻转标记。
_Avoid_: 不同步、漂移

**质量维度**:
本工作流强制校验的两个维度：`结构规范`（必含章节/标记/命名）与 `事实准确`（配置项与 add-on 配置声明对应、命令/端口/链接真实）。
_Avoid_: 质量标准、规范
