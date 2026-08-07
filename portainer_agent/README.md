<!-- zh-guide -->
# Portainer Agent

## 简介

Portainer Agent 是用于管理 Swarm 集群中所有 Docker 资源的代理端，它弥补了 Docker API 的一个限制：通过 Docker API 管理 Docker 环境时，用户只能操作请求所指向节点上的资源（容器、网络、卷、镜像等）。安装本代理后，你可以从另一个 Portainer 实例连接并管理 Home Assistant 上的 Docker 资源。本加载项基于官方 Portainer Agent 镜像，并针对 Home Assistant 基础镜像做了适配。

> 警告：Portainer Agent 功能非常强大，几乎可以访问你的整个系统。虽然本加载项在安全方面经过了仔细设计与维护，但若被不当使用或交给缺乏经验的人操作，可能会损坏系统，请谨慎使用。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 portainer_agent 并安装。

## 配置

可配置选项如下，均可在加载项配置页中填写：

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ------------- | ---- |
| `PORTAINER_AGENT_ARGS` | 字符串（可选） | 传给 portainer-agent 可执行文件的命令行参数 |
| `AGENT_CLUSTER_ADDR` | 字符串（可选） | 集群中其他 Agent 的地址，用于 Swarm 集群互联 |
| `AGENT_CLUSTER_PROBE_INTERVAL` | 字符串（可选） | 集群节点探测的间隔 |
| `AGENT_CLUSTER_PROBE_TIMEOUT` | 字符串（可选） | 集群节点探测的超时时间 |
| `AGENT_SECRET` | 字符串（可选） | Agent 加入集群使用的共享密钥 |
| `AGENT_SECRET_TIMEOUT` | 字符串（可选） | Agent 密钥的有效超时时间 |
| `EDGE` | 枚举 `list(0\|1)`（可选） | 是否启用 Edge 模式，`0` 关闭、`1` 启用 |
| `EDGE_ID` | 字符串（可选） | Edge 模式下 Agent 的唯一标识 |
| `EDGE_INACTIVITY_TIMEOUT` | 字符串（可选） | Edge 模式下的非活动超时时间 |
| `EDGE_INSECURE_POLL` | 枚举 `list(0\|1)`（可选） | 是否允许非安全的 Edge 轮询，`0` 关闭、`1` 启用 |
| `EDGE_KEY` | 字符串（可选） | Edge 模式下的注册密钥 |
| `LOG_LEVEL` | 字符串（可选） | 日志详细级别 |
| `env_vars` | 列表（可选） | 附加环境变量列表，每项包含 `name`（变量名）与 `value`（变量值） |

## 使用 / 访问入口

Portainer Agent 没有独立的 Web 界面，它是供外部 Portainer 实例连接管理的代理：

1. 在加载项配置中关闭保护模式（Protection mode）。
2. 从你的其他 Portainer 集群中，添加一个类型为 Agent 的新环境。
3. 地址填写 Home Assistant 的 IP，端口填写 `9001`（端口 `9001/tcp` 映射到宿主端口 `9001`，即 Portainer agent 端口）。
4. 端口 `80/tcp` 为 Portainer Edge agent 端口（未发布到宿主机）。

## 常见问题

- **如何让 Portainer 管理 Home Assistant 的 Docker？** 关闭本加载项的保护模式，然后在外部 Portainer 中添加类型为 Agent 的环境，地址填 Home Assistant 的 IP，端口填 `9001`。
- **这个加载项安全吗？** 它几乎拥有系统的全部访问权限，功能强大，请务必只在自己的受信任环境中使用，并避免交给没有经验的人操作。
- **如何传递自定义环境变量？** 使用 `env_vars` 选项，每项填写 `name` 与 `value`。
- **Edge 模式是什么？** 通过 Portainer 边缘计算（Edge）功能远程管理 Agent，需要在 Portainer 中配置 Edge 相关参数并使用 `EDGE_*` 选项。

---
- 英文原版：Home assistant add-on: Portainer_agent；链接 https://github.com/alexbelgium/hassio-addons/blob/master/portainer_agent/README.md
- 来源仓库：alexbelgium
