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

**镜像地址重写（image rewrite）**:
把 add-on `config.yaml` 里 `image:` 行的 registry 主机（`ghcr.io` 或已知镜像源）改写为国内镜像源的脚本化幂等变换。保留路径与 `{arch}` 占位符形状，支持换源迁移。
_Avoid_: 换源、改镜像、本地化镜像

**镜像源 / registry proxy**:
pull-through 代理 `ghcr.io` 的国内镜像站（当前为 `ghcr.nju.edu.cn`）。与「镜像仓库」（上游代码仓库全量镜像）是两码事。
_Avoid_: 加速器、Docker 镜像加速（那是 docker.io 的 daemon.json 配置，对 ghcr.io 无效）

**镜像入口**:
预构建 `source: local` add-on 面向国内用户的安装入口，例如
`ghcr.nju.edu.cn/treasoni/haos-mirror-switcher-{arch}` 和
`ghcr.nju.edu.cn/treasoni/hacs-cn-install-{arch}`。它解决的是“首次安装 add-on 镜像从哪里拉”的问题，
不等同于 Supervisor 的 `registries_mirror` 配置；国内 pull-through 入口是公益服务，不承诺 SLA。

**下载代理**:
仅用于 OTA 或 HACS 安装后的运行时下载中转。下载代理不参与 Supervisor 拉取容器镜像，也不代表上游服务本身可达。

**国内关键路径可用**:
首次安装、镜像换源和 HACS 安装不要求用户直连 GitHub、GHCR 或 `get.hacs.vip`；不承诺所有公益代理永久稳定。

**同步后变换（post-sync transform）**:
同步管道里对 config.yaml 的重写步骤：拷贝上游文件后立即套镜像地址重写，先变换再与本地对比，保证改写不被下次同步冲掉、幂等且不误报 updated。当前镜像源记录在 `addons-manifest.json` 的 `image_mirror` 字段。
_Avoid_: 同步钩子、改写步骤

**上游资料卡**:
自有 add-on 的 config.yaml 头部注释块，记录上游软件端口、默认账号、数据目录、环境变量与版本，是「先收集资料再写」的强制落地物，未收集完成不得编写 Dockerfile 与 options。
_Avoid_: 需求文档、开发笔记

> 「镜像」三义：**镜像仓库**（vendored add-on，代码全量拷贝）/ **镜像源**（registry proxy，代理 ghcr.io 的镜像站）/ **镜像地址重写**（image rewrite，改 `image:` 字段）。语境不同含义不同。
