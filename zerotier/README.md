<!-- zh-guide -->
# ZeroTier One

## 简介

ZeroTier 用一套系统提供了 VPN、SDN 与 SD-WAN 的能力，让本地网络和广域网上的所有资源都能像身处同一数据中心一样被管理。它可以无缝连接笔记本电脑、台式机、手机、嵌入式设备、云资源与应用。安装本应用后，你的 Home Assistant 实例也可以加入 ZeroTier 虚拟网络，实现从任何地方安全访问。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 zerotier 并安装。
3. 在 [zerotier.com](https://www.zerotier.com/) 注册免费账户并创建网络，获得网络 ID 后填入 `networks` 选项，再启动应用。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `networks` | 列表，默认 空 | 要加入的 ZeroTier 网络（VLAN）ID 列表，网络 ID 可在你的 ZeroTier 账户中获取；支持 `!secret`。 |
| `api_auth_token` | 字符串，默认 空 | ZeroTier 本地 HTTP JSON API 的访问令牌，相当于该 API 的密码；不打算使用此功能可留空，支持 `!secret`。 |
| `log_level` | 枚举，默认 `info` | 日志级别：`trace`、`debug`、`info`、`warning`、`error`、`fatal`。 |

> 注意：修改配置后需要重启应用才能生效。

## 使用 / 访问入口

ZeroTier 运行在宿主网络（`host_network`）上，使用端口 9993（`9993/tcp` 映射到宿主端口 9993）与其他节点进行 P2P 通信。加入网络后，你的 Home Assistant 实例会出现在 ZeroTier 账户的设备列表中；ZeroTier 本地 HTTP JSON API 也监听在端口 9993。

## 常见问题

1. **加入的网络不生效**：先在 ZeroTier 账户中创建网络并获取网络 ID，填入 `networks` 选项后重启应用，实例才会出现在你的 ZeroTier 账户中。
2. **`api_auth_token` 的作用**：它是访问本机 ZeroTier HTTP JSON API 的令牌，供工具或程序查询、控制本实例；如无此需求可留空。
3. **修改配置后需要重启**：ZeroTier 的配置变更不会自动生效，保存配置后请重启应用。
4. **配置中是否支持密钥引用**：`networks` 与 `api_auth_token` 均支持 `!secret` 引用 Home Assistant 的 secrets 文件。

---
- 英文原版：[Home Assistant Community App: ZeroTier One](https://github.com/hassio-addons/repository/blob/main/zerotier/README.md)
- 来源仓库：frenck
