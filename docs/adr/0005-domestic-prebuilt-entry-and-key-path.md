# 国内预构建入口与关键路径边界

Status: accepted

## 背景

国内用户首次安装自有 add-on 时，Supervisor 既可能需要拉取 Docker Hub 的构建器镜像，也可能需要直连 GHCR。要求用户先手工配置两条通道，会把“换源工具”本身卡在换源之前。HACS 安装器还不应把 `get.hacs.vip`、GitHub 或境外 PyPI 作为安装前提。

## 决策

- `haos-mirror-switcher` 和 `hacs-cn-install` 采用国内入口预构建镜像：
  - `ghcr.nju.edu.cn/treasoni/haos-mirror-switcher-{arch}`
  - `ghcr.nju.edu.cn/treasoni/hacs-cn-install-{arch}`
- CI 仍构建 `amd64` / `aarch64` 两个架构，并推送到 GHCR；用户安装时只访问国内 pull-through 入口。
- `haos-mirror-switcher` 的镜像源换源仍独立管理 Supervisor 的 `registries_mirror`，不把“安装镜像入口”误当成“运行时镜像源”。
- HACS 安装器固定 Gitee commit、TUNA 前端和 `aiogithubapi` wheel，并在 `/config/deps` 预置依赖。
- “国内关键路径可用”只覆盖首次安装、换源和 HACS 安装；OTA 与 HACS 安装后的仓库访问仍可能依赖无 SLA 的公益代理。

## 后果

- 普通用户不需要先手工配置 Docker Hub/GHCR 双通道，也不需要进入容器执行 pip。
- 国内入口失效时安装仍会失败，因此 README 必须明确无 SLA，并保留重试和恢复说明。
- CI 必须为两个 add-on、两个架构发布与 `config.yaml` 版本一致的镜像 tag；发布前按真实 manifest 端点验证，不使用 `latest` 或 `tags/list` 作为可用性证明。
