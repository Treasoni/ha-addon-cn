<!-- zh-guide -->
# HACS极速版Gitee安装器

## 简介

HACS极速版Gitee安装器（slug：`hacs-cn-install`）是**不依赖 `get.hacs.vip` 的 HACS 极速版安装方式**：直接下载 gitee 上 [hacs-china/integration](https://gitee.com/hacs-china/integration) 的 china 分支源码，再配合清华 tuna 镜像的 `hacs_frontend` 前端轮子，完整组装 HACS 极速版并写入 Home Assistant 的 `custom_components/hacs`。

> 适用场景：`get.hacs.vip` / `github.com` 在当前网络不可达（被重置）。本加载项运行时只访问 **gitee.com** 与 **pypi.tuna.tsinghua.edu.cn**（均已实测可达），安装过程不触碰 get.hacs.vip 与 GitHub。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：`https://gitee.com/zhqznc_10603234_123/ha-addon`
   - GitHub：`https://github.com/Treasoni/ha-addon-cn`
2. 搜索「HACS极速版Gitee安装器」（slug：`hacs-cn-install`）并安装。
3. 本加载项为**本地构建**，安装时 Supervisor 会拉取构建基础镜像（ghcr.io base 与 Docker Hub 构建器 CLI）。若因网络拉取失败，请先为本机 Docker 配好 `ghcr.io` 与 `docker.io` 两个国内镜像映射（例如用同商店的 `haos-mirror-switcher` 一键配置），再安装本加载项。

## 配置

此加载项为**一次性安装器**（`startup: once` + `boot: manual`），启动后自动完成安装并退出：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `integration_version` | `str` / 默认 `2.0.5.3` | 注入到 HACS `manifest.json` 的版本号（china 分支源码默认 `0.0.0`，需注入真实版本供 HACS 显示与自检更新）。**运行时优先从 gitee 取最新 china tag** 注入，仅当查询失败时回退此默认值 |

## 使用与访问入口

1. 在「配置」页确认 `integration_version`（一般保持默认），点击「保存」。
2. 点击「安装」构建此加载项（本地构建）。
3. 点击「启动」运行一次：日志依次显示下载 gitee 源码 → 下载前端轮子 → 注入版本 → 备份旧 HACS → 拷贝完成。
4. 安装完成后**重启 Home Assistant**，到 设置 → 设备与服务 → 添加集成，搜索「HACS」并添加。

> 本加载项为一次性安装器，无端口、无 Web 界面；使用入口即上述 Home Assistant 设置页操作。

**如何更新 HACS 极速版？** 直接重跑本加载项即可：它会重新拉取 gitee china 分支最新源码，**前端版本自动与源码对齐**（从源码 `scripts/install/frontend` 解析 `FRONTEND_VERSION`），注入版本自动取 gitee 最新 tag，并把旧 HACS 备份为 `hacs.bak-<时间戳>` 后覆盖。运行完重启 HA 生效。

## 常见问题

- **与商店里的 `get`（HACS极速版安装器）有何区别？** `get` 从 `get.hacs.vip` 下载安装脚本，国内网络常被重置导致失败；本加载项全程只访问 gitee.com 与清华 tuna 镜像（均已实测可达），绕开 `get.hacs.vip`。但本加载项**只安装 HACS**，不支持 `get` 的其他 13 个组件。
- **下载失败或日志报 TLS 错误？** 本加载项只依赖 gitee.com 与 `pypi.tuna.tsinghua.edu.cn`，请确认这两个域名在当前网络可达；偶发失败可重试启动。
- **安装完添加 HACS 集成时报错 / HACS 加载失败？** HACS 的 `requirements` 依赖 `aiogithubapi`，HA 默认从 pypi.org 安装；若 pypi.org 被墙，用本加载项预下载到 `/homeassistant/hacs-gitee-deps/` 的轮子手动装一次（需可操作 HA 容器的 shell，如 Terminal&SSH / Portainer）：

  ```bash
  docker exec homeassistant python3 -m pip install /homeassistant/hacs-gitee-deps/aiogithubapi-*.whl
  ```

  装完重启 HA。
- **装完 HACS 后商店里下载插件仍失败？** HACS 极速版内置 gitmirror/fastgit 等 GitHub 代理，是否可用取决于当前网络，超出本加载项安装范围。
- **原有 HACS 会被覆盖吗？** 会。启动时若检测到已存在 `custom_components/hacs`，会先备份为 `hacs.bak-<时间戳>` 再安装新版（极速版与官方共用一套配置，覆盖后无需重新配置集成）。

---
- 来源仓库：[hacs-china/integration](https://gitee.com/hacs-china/integration)（china 分支）

## 英文原版

本加载项为自有开发工具（`source: local`），无上游英文 README；代码与安装流程见 [商店仓库](https://github.com/Treasoni/ha-addon-cn)。安装对象为 HACS 极速版，其上游资料见 [hacs-china/integration](https://gitee.com/hacs-china/integration)。
