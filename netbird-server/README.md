<!-- zh-guide -->
# NetBird Server

## 简介

NetBird Server 在单个容器内运行 NetBird 自托管服务端全套组件（Management 管理端 + Signal 信令 + Relay/STUN 中继 + Dashboard 仪表盘），并内置 Caddy 反向代理，与官方 NetBird 自托管快速入门流程保持一致。NetBird 依赖 gRPC 通信，内置 Caddy 配置已预先接线好 HTTP 与 gRPC 端点的反向代理，与官方快速入门文档的推荐方式一致。本加载项不使用 Home Assistant 的 Ingress。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 netbird-server 并安装。

## 配置

首次启动时，加载项会在 `/config/netbird` 下生成标准的快速入门配置文件，并在后续启动时复用：

- `management.json`（位于 `/config/netbird/management/`）
- `relay.env`（位于 `/config/netbird/relay/`）
- `dashboard.env`（位于 `/config/netbird/dashboard/`）
- `Caddyfile`（位于 `/config/netbird/`）

加载项的配置选项如下：

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ------------- | ---- |
| `domain` | 字符串，默认 `netbird.example.com` | 解析到 Home Assistant 主机的公网域名（如 `netbird.example.com`）。若保留默认值不变，加载项会尝试改用 Home Assistant 的 `external_url` 或 `internal_url` 中的主机名 |

如需高级设置，可停止加载项后直接编辑上述生成文件，重启后修改会被保留。仪表盘的界面配置可通过编辑 `/config/netbird/dashboard/env` 覆盖，例如 `NETBIRD_MGMT_API_ENDPOINT`（管理 API 公网地址）、`NETBIRD_MGMT_GRPC_API_ENDPOINT`（gRPC API 公网地址）以及预填好的 `AUTH_*` OIDC 设置。

## 使用 / 访问入口

启动并设置好 `domain` 后，通过你的公网域名访问仪表盘（例如 `https://netbird.example.com`）并完成引导流程。加载项映射的默认端口如下：

- `80/tcp` → 宿主端口 `80`：Caddy HTTP（ACME HTTP-01 证书校验）
- `443/tcp` → 宿主端口 `443`：Caddy HTTPS（仪表盘与 API）
- `443/udp` → 宿主端口 `443`：Caddy HTTP/3（可选）
- `3478/udp` → 宿主端口 `3478`：Relay STUN

请确保宿主机与路由器已开放上述端口，并将你的公网域名解析到 Home Assistant 主机。

## 常见问题

- **这个加载项用 Ingress 吗？** 不用。它通过公网域名 + 443 端口提供服务，不使用 Home Assistant 侧边栏 Ingress。
- **已经有了自己的反向代理怎么办？** 可以编辑生成的 `Caddyfile` 来禁用 Caddy，或者在别处终结 TLS 后把请求转发到 `80` 端口。
- **身份认证怎么处理？** 加载项使用 NetBird 自带的嵌入式 IdP（基于 Dex），与官方快速入门布局一致。
- **修改生成文件后会不会被覆盖？** 不会。加载项只在首次启动时生成这些文件，之后的编辑在重启后会保留。
- **启动报端口冲突？** 管理端、信令与中继使用各自独立的指标端口以避免启动冲突，若遇到冲突请检查是否有其他服务占用相关端口。

---
- 英文原版：NetBird Server (quickstart)；链接 https://github.com/netbirdio/netbird/blob/main/docs/selfhosted/selfhosted-quickstart.md
- 来源仓库：alexbelgium
