<!-- zh-guide -->
# Portainer Business Edition

## 简介

Portainer 是一款开源的轻量级 Docker 管理界面，可以轻松管理一个或多个 Docker 主机或 Swarm 集群，提供容器、镜像、网络和卷的详细概览与便捷管理。本加载项是 Portainer 的 **Business Edition（商业版）** 变体，内置 `portainer/portainer-ee` 构建。商业版在注册获得授权密钥后，最多可免费用于 3 个节点（在 <https://www.portainer.io/take-3> 注册）；首次启动时在 Web 界面中输入密钥即可解锁，未输入密钥则按限期试用版运行。其余行为与社区版加载项一致。

> 警告：Portainer 功能非常强大，几乎可以访问你的整个系统。虽然本加载项在安全方面经过了仔细设计与维护，但若被不当使用或交给缺乏经验的人操作，可能会损坏系统，请谨慎使用。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 portainer_be 并安装。

## 配置

可配置选项如下：

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ------------- | ---- |
| `ssl` | 布尔，默认 `false` | 是否为 Web 界面启用 HTTPS |
| `certfile` | 字符串，默认 `fullchain.pem` | SSL 证书文件（位于 `/ssl/` 目录） |
| `keyfile` | 字符串，默认 `privkey.pem` | SSL 私钥文件（位于 `/ssl/` 目录） |
| `password` | 字符串（可选），默认 `homeassistant` | 管理员密码（至少 12 个字符；留空可恢复备份） |
| `env_vars` | 列表（可选） | 附加环境变量列表，每项包含 `name`（变量名）与 `value`（变量值） |

默认登录用户名是 `admin`，密码是你在此 `password` 选项中设置的值（默认 `homeassistant`），首次登录后请尽快修改。

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 Portainer Business Edition 图标，点击进入。若需要直接访问，Web 界面端口 `9099/tcp` 映射到宿主端口 `9000`；端口 `8000/tcp` 为 Edge Agent API（管理远程 Edge Agent 时启用，未发布到宿主机）。

首次使用建议：在加载项配置面板中设置密码，关闭保护模式（Protection mode）后启动加载项，打开 Web 界面登录（默认 `admin` / `homeassistant`），首次启动时输入商业版授权密钥。

## 常见问题

- **如何恢复备份？** 打开加载项选项，将 `password` 设置为空并重启加载项，即可进入从备份恢复的流程。请将备份放在 `/share` 等可访问目录中以便挂载。
- **如何重置数据库？** 只需修改加载项选项中的 `password`，数据库即会被重置。
- **通过反向代理访问超时？** 加载项自身包含很长的超时时间，但如果你使用 Nginx Proxy Manager 等额外代理层，其默认超时为 60 秒，需要相应调大代理层的超时设置。
- **安装了自定义容器会影响 Home Assistant 吗？** 手动安装自定义容器会把 Home Assistant 状态标记为不受支持/异常，期间会被阻止升级 Home Assistant 及加载项；停止该自定义容器即可恢复正常状态。
- **如何远程管理 Edge Agent？** 启用并开放 Edge Agent API 端口 `8000/tcp`，在 Portainer 中添加 Edge Agent 环境。

---
- 英文原版：Home assistant add-on: Portainer Business Edition；链接 https://github.com/alexbelgium/hassio-addons/blob/master/portainer_be/README.md
- 来源仓库：alexbelgium
